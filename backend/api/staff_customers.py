"""
营销人员 — 我的客户列表接口
GET /api/staff/customers
    ?login_id=oa001          必填，当前登录员工 OA
    &page=1
    &page_size=20
    &keyword=...             模糊匹配姓名/账号/手机
    &contact_status=已认证|未添加或未绑定
    &asset_level=高价值|中等价值|低价值
    &follow_status=未联系|近3日内联系过|近7日内联系过|近15日内联系过|近30日内联系过
    &risk_level=R1 保守型|...
    &sort_field=t1_aum|age|open_date|annual_return|commission_this_year|commission_last_year|commission_rate|trade_exp_months
    &sort_dir=asc|desc

响应字段:
  fund_account          资金账号
  cust_name             客户姓名
  phone                 手机号（脱敏）
  gender                性别（男/女）         CUSTGROUP.T_CLIENT_INFO.SEX  0=男 1=女
  age                   年龄                  CUSTGROUP.T_CLIENT_INFO.AGE
  open_date             开户日期              CUSTGROUP.T_CLIENT_INFO.OPEN_DATE
  trade_exp_months      交易经验月数（开户日期到今天）
  relation_type         关系类型              DDW_PROD.T_DDW_F22_LCSC_CUST_RLN.CUST_RLN_TP
  contact_status        建联状态（已认证|未添加或未绑定）
  follow_status         跟进状态（5档，基于最近外呼距今天数）
  t1_aum                T-1日净资产（万元）   DDW_PROD.T_DDW_F20_D_CUST_AUM_BD 最新 BIZ_DT
  aum_change_pct        AUM月变化%（当月最新日 vs 上月最新日，保留1位小数）
  asset_level           资产等级
  risk_level            风险等级
  hdly                  来源渠道
  annual_return         本年收益（元）        DDW_PROD.T_DDW_F21_C_Y_AST_PRFT.CUST_YR_PRFT_AMT  最新YR_MON
  commission_this_year  本年佣金（元）        DDW_PROD.T_DDW_F11_C_Y_INCM_AGGR.CMSN_INCM_NET_CMSN 当年最新
  commission_last_year  去年佣金（元）        同上，上一年最新
  commission_rate       佣金费率              DDW_PROD.T_DDW_F22_C_Y_KH360.ORD_TRD_CMSN_RTO 最新
  remark                备注                  T_CUSTOMER_ASSIGN_REL.ASSIGN_NOTE（格式："分配备注：XXX"）
"""
import logging
from datetime import datetime

import cx_Oracle
from flask import request, jsonify

from . import bp
from .manager_customers import _days_to_follow_status          # 复用天数→跟进状态映射
from config import Config
from utils.formatters import mask_phone, get_asset_level, get_risk_level
from utils.mock_data import get_mock_customers, _MOCK_EMPLOYEES

logger = logging.getLogger(__name__)


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def _get_connection():
    dsn = cx_Oracle.makedsn(
        Config.ORACLE_HOST, Config.ORACLE_PORT, service_name=Config.ORACLE_SERVICE
    )
    return cx_Oracle.connect(
        user=Config.ORACLE_USER, password=Config.ORACLE_PASSWORD, dsn=dsn
    )


def _calc_trade_exp(open_date) -> int:
    """开户日期（字符串或 datetime）→ 到今天的完整月数"""
    if not open_date:
        return 0
    try:
        if isinstance(open_date, str):
            dt = datetime.strptime(open_date[:10], "%Y-%m-%d")
        else:
            dt = open_date
        now = datetime.now()
        return max(0, (now.year - dt.year) * 12 + (now.month - dt.month))
    except Exception:
        return 0


_SORT_NUMERIC = {
    "t1_aum", "age", "annual_return", "commission_this_year",
    "commission_last_year", "commission_rate", "trade_exp_months", "aum_change_pct",
}


def _sort_records(records: list, sort_field: str, sort_dir: str) -> list:
    reverse = (sort_dir == "desc")
    if sort_field in _SORT_NUMERIC:
        return sorted(
            records,
            key=lambda x: (x.get(sort_field) is None, x.get(sort_field) or 0),
            reverse=reverse,
        )
    return sorted(
        records,
        key=lambda x: (x.get(sort_field) is None, str(x.get(sort_field) or "")),
        reverse=reverse,
    )


# ── Mock 路径 ─────────────────────────────────────────────────────────────────

def _build_mock(login_id: str, page: int, page_size: int, filters: dict) -> dict:
    keyword    = (filters.get("keyword") or "").strip()
    f_contact  = filters.get("contact_status")
    f_asset    = filters.get("asset_level")
    f_follow   = filters.get("follow_status")
    f_risk     = filters.get("risk_level")
    sort_field = filters.get("sort_field") or "t1_aum"
    sort_dir   = filters.get("sort_dir") or "desc"

    # 找到该员工姓名（用于匹配分配记录）
    emp_name = next(
        (e["emp_name"] for e in _MOCK_EMPLOYEES if e["login_id"] == login_id),
        None,
    )

    all_records = get_mock_customers()

    filtered = []
    for r in all_records:
        # 只取该员工名下的客户
        if emp_name and r.get("assignee_nm") != emp_name:
            continue
        if not emp_name and r.get("assignee_nm") is None:
            continue

        # 关键词
        if keyword:
            kw = keyword.lower()
            if not (
                kw in r["cust_name"].lower()
                or kw in r["fund_account"].lower()
            ):
                continue

        if f_contact and r["contact_status"] != f_contact:
            continue
        if f_asset   and r["asset_level"]    != f_asset:
            continue
        if f_follow  and r["follow_status"]  != f_follow:
            continue
        if f_risk    and r["risk_level"]     != f_risk:
            continue

        # 去掉内部字段
        pub = {k: v for k, v in r.items() if not k.startswith("_")}
        filtered.append(pub)

    filtered = _sort_records(filtered, sort_field, sort_dir)
    total = len(filtered)
    start = (page - 1) * page_size
    return {
        "total":     total,
        "page":      page,
        "page_size": page_size,
        "list":      filtered[start: start + page_size],
    }


# ── 真实 DB 路径 ──────────────────────────────────────────────────────────────

def _build_real(login_id: str, page: int, page_size: int, filters: dict) -> dict:
    keyword    = (filters.get("keyword") or "").strip()
    f_contact  = filters.get("contact_status")
    f_asset    = filters.get("asset_level")
    f_follow   = filters.get("follow_status")
    f_risk     = filters.get("risk_level")
    sort_field = filters.get("sort_field") or "t1_aum"
    sort_dir   = filters.get("sort_dir") or "desc"

    conn = _get_connection()
    try:
        cur = conn.cursor()

        # ── 1. 当前员工名下的客户 ID 列表 ───────────────────────
        cur.execute("""
            SELECT CLIENT_ID, ASSIGN_NOTE
            FROM custgroup.T_CUSTOMER_ASSIGN_REL
            WHERE BRANCH_NO = :branch_no
              AND LOGIN_ID  = :login_id
        """, branch_no=Config.BRANCH_NO, login_id=login_id)
        rows = cur.fetchall()
        if not rows:
            return {"total": 0, "page": page, "page_size": page_size, "list": []}

        cid_list      = [str(r[0]).strip() for r in rows]
        note_map      = {str(r[0]).strip(): r[1] for r in rows}
        id_csv        = "','".join(cid_list)   # 用于 IN 子句

        # ── 2. 基础信息 ─────────────────────────────────────────
        cur.execute(f"""
            SELECT CLIENT_ID, USER_NM, MOBILE, SEX, AGE, OPEN_DATE
            FROM CUSTGROUP.T_CLIENT_INFO
            WHERE CLIENT_ID IN ('{id_csv}')
        """)
        base = {}
        for cid, nm, mob, sex, age, od in cur.fetchall():
            k = str(cid).strip()
            base[k] = {
                "cust_name": str(nm).strip() if nm else "",
                "phone":     mask_phone(str(mob) if mob else ""),
                "gender":    "男" if str(sex).strip() == "0" else ("女" if str(sex).strip() == "1" else None),
                "age":       int(age) if age is not None else None,
                "open_date": od.strftime("%Y-%m-%d") if od else None,
            }

        # ── 3. 建联状态（企微绑定） ──────────────────────────────
        cur.execute("SELECT CLIENT_ID FROM S01_PROD.T_S01_EHT_CIM_T_EHT_ACCOU_BIND")
        bind_set = {str(r[0]).strip() for r in cur.fetchall() if r[0]}

        # ── 4. 跟进状态（外呼流水最近一条） ─────────────────────
        cur.execute(f"""
            SELECT CLIENT_ID, ROUND(SYSDATE - CAST(CALL_TIME AS DATE)) AS DAYS_AGO
            FROM (
                SELECT CLIENT_ID, CALL_TIME,
                       ROW_NUMBER() OVER (PARTITION BY CLIENT_ID ORDER BY CALL_TIME DESC) AS rn
                FROM custgroup.T_CALL_LOG
                WHERE BRANCH_NO = :branch_no
                  AND CLIENT_ID IN ('{id_csv}')
            ) WHERE rn = 1
        """, branch_no=Config.BRANCH_NO)
        follow_map = {
            str(r[0]).strip(): _days_to_follow_status(int(r[1]) if r[1] is not None else None)
            for r in cur.fetchall()
        }

        # ── 5. AUM（日表：当月最新日 & 上月最新日） ──────────────
        # 数据源：DDW_PROD.T_DDW_F20_D_CUST_AUM_BD（日表，BIZ_DT 格式 YYYYMMDD）
        # 取每个客户：① 最新 BIZ_DT 的值（当前 AUM）
        #            ② 上月内最新 BIZ_DT 的值（用于计算月变化%）
        cur.execute(f"""
            SELECT CUST_NO, CUST_TOT_NET_AST, BIZ_DT
            FROM (
                SELECT CUST_NO, CUST_TOT_NET_AST, BIZ_DT,
                       DENSE_RANK() OVER (PARTITION BY CUST_NO
                                          ORDER BY SUBSTR(BIZ_DT,1,6) DESC) AS month_rank,
                       ROW_NUMBER() OVER (PARTITION BY CUST_NO, SUBSTR(BIZ_DT,1,6)
                                          ORDER BY BIZ_DT DESC) AS rn_in_month
                FROM DDW_PROD.T_DDW_F20_D_CUST_AUM_BD
                WHERE CUST_NO IN ('{id_csv}')
            )
            WHERE month_rank <= 2 AND rn_in_month = 1
            ORDER BY CUST_NO, BIZ_DT DESC
        """)
        aum_map = {}
        for cno, ast, biz_dt in cur.fetchall():
            k = str(cno).strip()
            aum_map.setdefault(k, []).append(float(ast) if ast is not None else 0.0)

        # ── 6. 风险等级 ──────────────────────────────────────────
        cur.execute(f"""
            SELECT CLIENT_ID, corp_risk_level
            FROM (
                SELECT CLIENT_ID, corp_risk_level,
                       ROW_NUMBER() OVER (PARTITION BY CLIENT_ID ORDER BY corp_end_date DESC) AS rn
                FROM hs_asset.clientprefer
                WHERE CLIENT_ID IN ('{id_csv}')
            ) WHERE rn = 1
        """)
        risk_map = {str(r[0]).strip(): r[1] for r in cur.fetchall()}

        # ── 7. 来源渠道 ──────────────────────────────────────────
        cur.execute(f"""
            SELECT CUST_NO, HDLY
            FROM DDW_PROD.t_ddw_f27_c_bsc_inf
            WHERE CUST_NO IN ('{id_csv}') AND HDLY IS NOT NULL
        """)
        hdly_map = {str(r[0]).strip(): str(r[1]).strip() for r in cur.fetchall() if r[0]}

        # ── 8. 关系类型 ──────────────────────────────────────────
        cur.execute(f"""
            SELECT FUND_ACCOUNT, CUST_RLN_TP
            FROM DDW_PROD.T_DDW_F22_LCSC_CUST_RLN
            WHERE FUND_ACCOUNT IN ('{id_csv}')
              AND BRANCH_NO = :branch_no
        """, branch_no=Config.BRANCH_NO)
        rln_map = {str(r[0]).strip(): str(r[1]).strip() for r in cur.fetchall() if r[0]}

        # ── 9. 本年收益（最新 YR_MON） ──────────────────────────
        cur.execute(f"""
            SELECT FUND_ACCOUNT, CUST_YR_PRFT_AMT
            FROM (
                SELECT FUND_ACCOUNT, CUST_YR_PRFT_AMT,
                       ROW_NUMBER() OVER (PARTITION BY FUND_ACCOUNT ORDER BY YR_MON DESC) AS rn
                FROM DDW_PROD.T_DDW_F21_C_Y_AST_PRFT
                WHERE FUND_ACCOUNT IN ('{id_csv}')
            ) WHERE rn = 1
        """)
        return_map = {
            str(r[0]).strip(): float(r[1]) if r[1] is not None else None
            for r in cur.fetchall()
        }

        # ── 10. 佣金（年表，取最近两个 YR 年份） ────────────────
        # 当年最新YR_MON → commission_this_year；上一年最新YR_MON → commission_last_year
        this_year = datetime.now().year
        cur.execute(f"""
            SELECT FUND_ACCOUNT, CMSN_INCM_NET_CMSN, SUBSTR(YR_MON,1,4) AS YR
            FROM (
                SELECT FUND_ACCOUNT, CMSN_INCM_NET_CMSN, YR_MON,
                       ROW_NUMBER() OVER (PARTITION BY FUND_ACCOUNT, SUBSTR(YR_MON,1,4) ORDER BY YR_MON DESC) AS rn
                FROM DDW_PROD.T_DDW_F11_C_Y_INCM_AGGR
                WHERE FUND_ACCOUNT IN ('{id_csv}')
                  AND SUBSTR(YR_MON,1,4) IN ('{this_year}', '{this_year - 1}')
            ) WHERE rn = 1
        """)
        cmsn_map: dict[str, dict] = {}
        for fa, cmsn, yr in cur.fetchall():
            k = str(fa).strip()
            cmsn_map.setdefault(k, {})[str(yr)] = float(cmsn) if cmsn is not None else None

        # ── 11. 佣金费率 ─────────────────────────────────────────
        cur.execute(f"""
            SELECT FUND_ACCOUNT, ORD_TRD_CMSN_RTO
            FROM (
                SELECT FUND_ACCOUNT, ORD_TRD_CMSN_RTO,
                       ROW_NUMBER() OVER (PARTITION BY FUND_ACCOUNT ORDER BY YR_MON DESC) AS rn
                FROM DDW_PROD.T_DDW_F22_C_Y_KH360
                WHERE FUND_ACCOUNT IN ('{id_csv}')
            ) WHERE rn = 1
        """)
        rate_map = {
            str(r[0]).strip(): float(r[1]) if r[1] is not None else None
            for r in cur.fetchall()
        }

    finally:
        cur.close()
        conn.close()

    # ── 拼装记录 ─────────────────────────────────────────────────
    records = []
    for cid in cid_list:
        b        = base.get(cid, {})
        aum_vals = aum_map.get(cid, [])
        cur_aum  = round(aum_vals[0] / 10000, 2) if aum_vals else 0.0
        prev_aum = aum_vals[1] / 10000 if len(aum_vals) > 1 else None

        aum_change_pct = None
        if prev_aum and prev_aum != 0:
            aum_change_pct = round((cur_aum - prev_aum) / prev_aum * 100, 1)

        asset_level    = get_asset_level(cur_aum)
        risk_level     = get_risk_level(risk_map.get(cid))
        contact_status = "已认证" if cid in bind_set else "未添加或未绑定"
        follow_status  = follow_map.get(cid, "未联系")
        open_date_str  = b.get("open_date")
        trade_exp      = _calc_trade_exp(open_date_str)

        yr_cmsn  = cmsn_map.get(cid, {})
        note     = note_map.get(cid)
        remark   = f'分配备注："{note}"' if note else None

        # 筛选
        if keyword:
            kw = keyword.lower()
            if not (kw in b.get("cust_name", "").lower() or kw in cid.lower()):
                continue
        if f_contact and contact_status != f_contact: continue
        if f_asset   and asset_level    != f_asset:   continue
        if f_follow  and follow_status  != f_follow:  continue
        if f_risk    and risk_level     != f_risk:     continue

        records.append({
            "fund_account":          cid,
            "cust_name":             b.get("cust_name", ""),
            "phone":                 b.get("phone", ""),
            "gender":                b.get("gender"),
            "age":                   b.get("age"),
            "open_date":             open_date_str,
            "trade_exp_months":      trade_exp,
            "relation_type":         rln_map.get(cid),
            "contact_status":        contact_status,
            "follow_status":         follow_status,
            "t1_aum":                cur_aum,
            "aum_change_pct":        aum_change_pct,
            "asset_level":           asset_level,
            "risk_level":            risk_level,
            "hdly":                  hdly_map.get(cid),
            "annual_return":         return_map.get(cid),
            "commission_this_year":  yr_cmsn.get(str(this_year)),
            "commission_last_year":  yr_cmsn.get(str(this_year - 1)),
            "commission_rate":       rate_map.get(cid),
            "remark":                remark,
        })

    records = _sort_records(records, sort_field, sort_dir)
    total   = len(records)
    start   = (page - 1) * page_size
    return {
        "total":     total,
        "page":      page,
        "page_size": page_size,
        "list":      records[start: start + page_size],
    }


# ── 路由 ──────────────────────────────────────────────────────────────────────

@bp.route("/staff/customers", methods=["GET"])
def staff_customer_list():
    """GET /api/staff/customers"""
    login_id = (request.args.get("login_id") or "").strip()
    if not login_id:
        return jsonify({"code": 400, "msg": "缺少必填参数 login_id"}), 400

    try:
        page      = max(1, int(request.args.get("page", 1)))
        page_size = min(200, max(1, int(request.args.get("page_size", 20))))
    except ValueError:
        return jsonify({"code": 400, "msg": "page 和 page_size 必须为整数"}), 400

    filters = {
        "keyword":        request.args.get("keyword"),
        "contact_status": request.args.get("contact_status"),
        "asset_level":    request.args.get("asset_level"),
        "follow_status":  request.args.get("follow_status"),
        "risk_level":     request.args.get("risk_level"),
        "sort_field":     request.args.get("sort_field", "t1_aum"),
        "sort_dir":       request.args.get("sort_dir", "desc"),
    }

    try:
        builder = _build_mock if Config.MOCK_MODE else _build_real
        data    = builder(login_id, page, page_size, filters)
        return jsonify({"code": 200, "msg": "success", "data": data})
    except cx_Oracle.DatabaseError as e:
        logger.error("数据库查询失败: %s", e, exc_info=True)
        return jsonify({"code": 500, "msg": "数据库查询失败，请联系管理员"}), 500
    except Exception as e:
        logger.error("未知错误: %s", e, exc_info=True)
        return jsonify({"code": 500, "msg": "服务器内部错误"}), 500
