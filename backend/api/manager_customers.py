"""
客户分配管理 — 客户列表接口
GET /api/manager/customers
    ?page=1&page_size=20
    &assign_status=已分配|未分配
    &asset_level=高价值|中等价值|低价值
    &contact_status=已认证|未添加或未绑定
    &follow_status=未跟进|已接通|未接通
    &hdly=<渠道号>
    &risk_level=保守型|稳健型|平衡型|积极型|进取型|未测评
    &keyword=<客户姓名/资金账号/手机号>

GET /api/manager/customers/hdly-options
    返回当前营业部客户的所有开户渠道号去重列表（供前端下拉使用）

字段说明:
  fund_account    资金账号
  cust_name       客户姓名（脱敏）
  phone           手机号（脱敏）
  t1_aum          T-1日净资产（万元）
  asset_level     资产等级: 高价值 | 中等价值 | 低价值
  risk_level      风险等级
  contact_status  建联状态: 已认证 | 未添加或未绑定
  follow_status   跟进状态: 未跟进 | 已接通 | 未接通
  hdly            客户开户渠道号（来自 DDW_PROD.t_ddw_f27_c_bsc_inf）
  assignee_nm     归属人姓名（来自 T_CUSTOMER_ASSIGN_REL）
  assign_time     分配时间（来自 T_CUSTOMER_ASSIGN_REL）
  operator_nm     分配人姓名（来自 T_CUSTOMER_ASSIGN_REL）
  assign_source   分配来源: 0=外部导入 1=手动分配 None=未分配
"""
import logging
import cx_Oracle
from flask import request, jsonify

from . import bp
from config import Config
from utils.formatters import mask_name, mask_phone, get_asset_level, get_risk_level
from utils.mock_data import get_mock_customers

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
#  数据库连接
# --------------------------------------------------------------------------- #

def _get_connection():
    dsn = cx_Oracle.makedsn(
        Config.ORACLE_HOST,
        Config.ORACLE_PORT,
        service_name=Config.ORACLE_SERVICE,
    )
    return cx_Oracle.connect(
        user=Config.ORACLE_USER,
        password=Config.ORACLE_PASSWORD,
        dsn=dsn,
    )


# --------------------------------------------------------------------------- #
#  辅助查询
# --------------------------------------------------------------------------- #

def _fetch_bind_set(cursor) -> set:
    """已绑定企微的 CLIENT_ID 集合"""
    try:
        cursor.execute(
            "SELECT CLIENT_ID FROM S01_PROD.T_S01_EHT_CIM_T_EHT_ACCOU_BIND"
        )
        return {str(row[0]).strip() for row in cursor.fetchall() if row[0]}
    except Exception as e:
        logger.warning("查询绑定表失败，建联状态将全部标记为未绑定: %s", e)
        return set()


def _fetch_asset_map(cursor) -> dict:
    """T-1日净资产 {CUST_NO: CUST_TOT_NET_AST}，单位：元
    数据源：DDW_PROD.T_DDW_F20_D_CUST_AUM_BD（日表），取最新 BIZ_DT"""
    try:
        cursor.execute("""
            SELECT CUST_NO, CUST_TOT_NET_AST
            FROM (
                SELECT CUST_NO, CUST_TOT_NET_AST,
                       ROW_NUMBER() OVER (PARTITION BY CUST_NO ORDER BY BIZ_DT DESC) AS rn
                FROM DDW_PROD.T_DDW_F20_D_CUST_AUM_BD
            )
            WHERE rn = 1
        """)
        return {str(r[0]).strip(): r[1] for r in cursor.fetchall()}
    except Exception as e:
        logger.warning("查询资产表失败，AUM 将全部为 0: %s", e)
        return {}


def _fetch_risk_map(cursor) -> dict:
    """最新风险等级 {CLIENT_ID: corp_risk_level}"""
    try:
        cursor.execute("""
            SELECT CLIENT_ID, corp_risk_level
            FROM (
                SELECT CLIENT_ID, corp_risk_level,
                       ROW_NUMBER() OVER (PARTITION BY CLIENT_ID ORDER BY corp_end_date DESC) AS rn
                FROM hs_asset.clientprefer
            )
            WHERE rn = 1
        """)
        return {str(r[0]).strip(): r[1] for r in cursor.fetchall()}
    except Exception as e:
        logger.warning("查询风险等级表失败，风险等级将全部为未测评: %s", e)
        return {}


def _fetch_assign_map(cursor) -> dict:
    """
    从分配关系表取当前归属信息
    {CLIENT_ID: {assignee_nm, assign_time, operator_nm, assign_source}}

    assign_source=0  外部导入，不可撤回
    assign_source=1  手动分配，可撤回
    """
    try:
        cursor.execute("""
            SELECT CLIENT_ID, EMP_NAME, ASSIGN_TIME, EMP_NM_OP, ASSIGN_SOURCE
            FROM custgroup.T_CUSTOMER_ASSIGN_REL
            WHERE BRANCH_NO = :branch_no
        """, branch_no=Config.BRANCH_NO)

        result = {}
        for client_id, emp_name, assign_time, emp_nm_op, assign_source in cursor.fetchall():
            key = str(client_id).strip()
            if assign_time is not None:
                try:
                    assign_time_str = assign_time.strftime("%Y-%m-%d %H:%M")
                except AttributeError:
                    assign_time_str = str(assign_time)[:16]
            else:
                assign_time_str = None

            result[key] = {
                "assignee_nm":   emp_name or None,
                "assign_time":   assign_time_str,
                "operator_nm":   emp_nm_op or None,
                "assign_source": int(assign_source) if assign_source is not None else None,
            }
        return result
    except Exception as e:
        logger.warning("查询分配关系表失败，归属人相关字段将全部为空: %s", e)
        return {}


def _fetch_follow_map(cursor) -> dict:
    """
    最新外呼记录 {CLIENT_ID: follow_status}
    按最近一次通话距今天数映射到 5 档跟进状态
    """
    try:
        cursor.execute("""
            SELECT CLIENT_ID,
                   ROUND(SYSDATE - CAST(CALL_TIME AS DATE)) AS DAYS_AGO
            FROM (
                SELECT CLIENT_ID, CALL_TIME,
                       ROW_NUMBER() OVER (PARTITION BY CLIENT_ID ORDER BY CALL_TIME DESC) AS rn
                FROM custgroup.T_CALL_LOG
                WHERE BRANCH_NO = :branch_no
            )
            WHERE rn = 1
        """, branch_no=Config.BRANCH_NO)
        result = {}
        for client_id, days_ago in cursor.fetchall():
            if not client_id:
                continue
            result[str(client_id).strip()] = _days_to_follow_status(
                int(days_ago) if days_ago is not None else None
            )
        return result
    except Exception as e:
        logger.warning("查询外呼流水表失败，跟进状态将全部为未联系: %s", e)
        return {}


def _days_to_follow_status(days) -> str:
    """距今天数 → 跟进状态（5档）"""
    if days is None or days > 30:
        return "未联系"
    if days <= 3:
        return "近3日内联系过"
    if days <= 7:
        return "近7日内联系过"
    if days <= 15:
        return "近15日内联系过"
    return "近30日内联系过"


def _fetch_hdly_map(cursor) -> dict:
    """
    客户开户渠道号 {CUST_NO: HDLY}
    来自 DDW_PROD.t_ddw_f27_c_bsc_inf
    """
    try:
        cursor.execute("""
            SELECT h.CUST_NO, h.HDLY
            FROM DDW_PROD.t_ddw_f27_c_bsc_inf h
            INNER JOIN custgroup.t_client_info c
                ON h.CUST_NO = c.CLIENT_ID
            WHERE c.BRANCH_NO = :branch_no
              AND h.HDLY IS NOT NULL
        """, branch_no=Config.BRANCH_NO)
        return {str(r[0]).strip(): str(r[1]).strip() for r in cursor.fetchall() if r[0]}
    except Exception as e:
        logger.warning("查询客户来源表失败，hdly 将全部为 None: %s", e)
        return {}



# --------------------------------------------------------------------------- #
#  核心数据拼装
# --------------------------------------------------------------------------- #

def _build_customer_list_mock(page: int, page_size: int, filters: dict) -> dict:
    """Mock 模式：从内存假数据中筛选 + 分页，逻辑与真实路径完全一致"""
    keyword   = (filters.get("keyword") or "").strip()
    f_assign  = filters.get("assign_status")
    f_asset   = filters.get("asset_level")
    f_contact = filters.get("contact_status")
    f_follow  = filters.get("follow_status")
    f_hdly    = filters.get("hdly")
    f_risk    = filters.get("risk_level")

    all_records = get_mock_customers()
    filtered = []
    for r in all_records:
        # keyword 匹配原始姓名 / 账号 / 手机
        if keyword:
            kw_lower = keyword.lower()
            if not (
                kw_lower in r["cust_name"].lower()
                or kw_lower in r["fund_account"].lower()
                or kw_lower in r["_raw_phone"].lower()
            ):
                continue

        is_assigned = r["assignee_nm"] is not None
        if f_assign == "已分配" and not is_assigned:
            continue
        if f_assign == "未分配" and is_assigned:
            continue
        if f_asset   and r["asset_level"]    != f_asset:
            continue
        if f_contact and r["contact_status"] != f_contact:
            continue
        if f_follow  and r["follow_status"]  != f_follow:
            continue
        if f_risk    and r["risk_level"]     != f_risk:
            continue
        if f_hdly    and r["hdly"]           != f_hdly:
            continue

        # 过滤掉内部搜索字段，不暴露给前端
        pub = {k: v for k, v in r.items() if not k.startswith("_")}
        filtered.append(pub)

    total     = len(filtered)
    start     = (page - 1) * page_size
    page_data = filtered[start: start + page_size]
    return {"total": total, "page": page, "page_size": page_size, "list": page_data}


def _build_customer_list(page: int, page_size: int, filters: dict) -> dict:
    if Config.MOCK_MODE:
        return _build_customer_list_mock(page, page_size, filters)

    keyword      = (filters.get("keyword") or "").strip()
    f_assign     = filters.get("assign_status")   # 已分配 | 未分配
    f_asset      = filters.get("asset_level")     # 高价值 | 中等价值 | 低价值
    f_contact    = filters.get("contact_status")  # 已认证 | 未添加或未绑定
    f_follow     = filters.get("follow_status")   # 未跟进 | 已接通 | 未接通
    f_hdly       = filters.get("hdly")            # 渠道号字符串
    f_risk       = filters.get("risk_level")      # 保守型 | 稳健型 | ... | 未测评

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        bind_set   = _fetch_bind_set(cursor)
        asset_map  = _fetch_asset_map(cursor)
        risk_map   = _fetch_risk_map(cursor)
        assign_map = _fetch_assign_map(cursor)
        follow_map = _fetch_follow_map(cursor)
        hdly_map   = _fetch_hdly_map(cursor)

        # 主表查询，keyword 在 DB 侧过滤（匹配资金账号、原始姓名、原始手机号）
        sql = """
            SELECT CLIENT_ID, USER_NM, MOBILE
            FROM custgroup.t_client_info
            WHERE BRANCH_NO = :branch_no
        """
        params = {"branch_no": Config.BRANCH_NO}

        if keyword:
            sql += " AND (CLIENT_ID LIKE :kw OR USER_NM LIKE :kw OR MOBILE LIKE :kw)"
            params["kw"] = f"%{keyword}%"

        cursor.execute(sql, params)
        all_rows = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    # Python 侧筛选 + 字段拼装
    filtered = []
    for client_id, user_nm, mobile in all_rows:
        key = str(client_id).strip()

        # 计算各派生字段
        raw_ast        = asset_map.get(key, 0) or 0
        aum_wan        = round(float(raw_ast) / 10000, 2)
        asset_level    = get_asset_level(aum_wan)
        risk_level     = get_risk_level(risk_map.get(key))
        contact_status = "已认证" if key in bind_set else "未添加或未绑定"
        follow_status  = follow_map.get(key, "未联系")
        hdly           = hdly_map.get(key)
        assign_info    = assign_map.get(key, {})
        is_assigned    = bool(assign_info)

        # 筛选逻辑
        if f_assign == "已分配" and not is_assigned:
            continue
        if f_assign == "未分配" and is_assigned:
            continue
        if f_asset and asset_level != f_asset:
            continue
        if f_contact and contact_status != f_contact:
            continue
        if f_follow and follow_status != f_follow:
            continue
        if f_risk and risk_level != f_risk:
            continue
        if f_hdly and hdly != f_hdly:
            continue

        filtered.append({
            "fund_account":   key,
            "cust_name":      str(user_nm).strip() if user_nm else "",
            "phone":          mask_phone(str(mobile) if mobile else ""),
            "t1_aum":         aum_wan,
            "asset_level":    asset_level,
            "risk_level":     risk_level,
            "contact_status": contact_status,
            "follow_status":  follow_status,
            "hdly":           hdly,
            "assignee_nm":    assign_info.get("assignee_nm"),
            "assign_time":    assign_info.get("assign_time"),
            "operator_nm":    assign_info.get("operator_nm"),
            "assign_source":  assign_info.get("assign_source"),
        })

    total = len(filtered)

    # 先筛选完再分页，total 反映筛选后总数
    start     = (page - 1) * page_size
    page_data = filtered[start: start + page_size]

    return {
        "total":     total,
        "page":      page,
        "page_size": page_size,
        "list":      page_data,
    }


# --------------------------------------------------------------------------- #
#  路由
# --------------------------------------------------------------------------- #

@bp.route("/manager/customers", methods=["GET"])
def manager_customer_list():
    """
    GET /api/manager/customers?page=1&page_size=20&...

    筛选参数（均可选，不传则不过滤）:
      assign_status   已分配 | 未分配
      asset_level     高价值 | 中等价值 | 低价值
      contact_status  已认证 | 未添加或未绑定
      follow_status   未跟进 | 已接通 | 未接通
      hdly            渠道号（与 hdly-options 接口返回值对齐）
      risk_level      保守型 | 稳健型 | 平衡型 | 积极型 | 进取型 | 未测评
      keyword         关键词，模糊匹配资金账号/姓名/手机号

    返回示例:
    {
        "code": 200,
        "msg": "success",
        "data": {
            "total": 286,
            "page": 1,
            "page_size": 20,
            "list": [...]
        }
    }
    """
    try:
        page      = max(1, int(request.args.get("page", 1)))
        page_size = min(100, max(1, int(request.args.get("page_size", 20))))
    except ValueError:
        return jsonify({"code": 400, "msg": "page 和 page_size 必须为整数"}), 400

    filters = {
        "keyword":        request.args.get("keyword"),
        "assign_status":  request.args.get("assign_status"),
        "asset_level":    request.args.get("asset_level"),
        "contact_status": request.args.get("contact_status"),
        "follow_status":  request.args.get("follow_status"),
        "hdly":           request.args.get("hdly"),
        "risk_level":     request.args.get("risk_level"),
    }

    try:
        data = _build_customer_list(page, page_size, filters)
        return jsonify({"code": 200, "msg": "success", "data": data})
    except cx_Oracle.DatabaseError as e:
        logger.error("数据库查询失败: %s", e, exc_info=True)
        return jsonify({"code": 500, "msg": "数据库查询失败，请联系管理员"}), 500
    except Exception as e:
        logger.error("未知错误: %s", e, exc_info=True)
        return jsonify({"code": 500, "msg": "服务器内部错误"}), 500


@bp.route("/manager/customers/hdly-options", methods=["GET"])
def hdly_options():
    """
    GET /api/manager/customers/hdly-options

    返回当前营业部下所有客户的开户渠道号去重列表，供前端「客户来源」下拉框使用。

    返回示例:
    {
        "code": 200,
        "msg": "success",
        "data": ["渠道A", "渠道B", ...]
    }
    """
    if Config.MOCK_MODE:
        from utils.mock_data import get_mock_customers, _HDLY_OPTIONS
        return jsonify({"code": 200, "msg": "success", "data": sorted(_HDLY_OPTIONS)})

    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT h.HDLY
            FROM DDW_PROD.t_ddw_f27_c_bsc_inf h
            INNER JOIN custgroup.t_client_info c
                ON h.CUST_NO = c.CLIENT_ID
            WHERE c.BRANCH_NO = :branch_no
              AND h.HDLY IS NOT NULL
            ORDER BY h.HDLY
        """, branch_no=Config.BRANCH_NO)
        options = [str(r[0]).strip() for r in cursor.fetchall() if r[0]]
    except cx_Oracle.DatabaseError as e:
        logger.error("查询渠道号选项失败: %s", e, exc_info=True)
        return jsonify({"code": 500, "msg": "数据库查询失败"}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"code": 200, "msg": "success", "data": options})
