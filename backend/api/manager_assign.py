"""
客户分配管理 — 分配相关接口

接口列表：
  GET  /api/manager/employees/workload      员工负载列表（侧边栏/分配弹窗）
  GET  /api/manager/employees/search        员工搜索（含负载信息）
  POST /api/manager/customers/assign        手动分配
  POST /api/manager/customers/revoke        撤回分配
  POST /api/manager/customers/smart-assign  智能分配
"""
import logging
from datetime import datetime
from math import floor

import cx_Oracle
from flask import request, jsonify, g

from . import bp
from config import Config
from utils.formatters import get_asset_level

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
#  数据库连接                                                                   #
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
#  负载等级计算                                                                 #
# --------------------------------------------------------------------------- #

def _load_level(percentile: float) -> str:
    """
    分位值（0=负载最高，1=负载最低）→ 负载等级文字
    分位区间基于营业部内客户数量从高到低排序：
      [0.0, 0.2)  高负载
      [0.2, 0.4)  偏高
      [0.4, 0.6)  适中
      [0.6, 0.8)  偏低
      [0.8, 1.0]  空闲
    """
    if percentile < 0.2:
        return "高负载"
    if percentile < 0.4:
        return "偏高"
    if percentile < 0.6:
        return "适中"
    if percentile < 0.8:
        return "偏低"
    return "空闲"


# --------------------------------------------------------------------------- #
#  负载重算（每次分配/撤回后调用）                                               #
# --------------------------------------------------------------------------- #

def _recalc_workload(cursor, branch_no: str):
    """
    对指定营业部内所有有分配关系的员工重算客户数量和分位排名，
    结果 MERGE 进 T_EMP_WORKLOAD。
    分位值 = (rank-1) / total，rank 按客户数从高到低排序（rank=1 最多）。
    """
    cursor.execute("""
        SELECT
            r.LOGIN_ID,
            MAX(r.EMP_NAME)  AS EMP_NAME,
            COUNT(*)         AS CUST_COUNT
        FROM custgroup.T_CUSTOMER_ASSIGN_REL r
        WHERE r.BRANCH_NO = :branch_no
        GROUP BY r.LOGIN_ID
    """, branch_no=branch_no)
    rows = cursor.fetchall()

    if not rows:
        return

    # 按客户数从高到低排序，计算分位
    rows_sorted = sorted(rows, key=lambda x: x[2], reverse=True)
    total = len(rows_sorted)
    now   = datetime.now()

    for rank, (login_id, emp_name, cust_count) in enumerate(rows_sorted, start=1):
        percentile  = round((rank - 1) / total, 4)
        level       = _load_level(percentile)

        cursor.execute("""
            MERGE INTO custgroup.T_EMP_WORKLOAD t
            USING (SELECT :login_id AS LOGIN_ID, :branch_no AS BRANCH_NO FROM DUAL) s
            ON (t.LOGIN_ID = s.LOGIN_ID AND t.BRANCH_NO = s.BRANCH_NO)
            WHEN MATCHED THEN UPDATE SET
                t.EMP_NAME   = :emp_name,
                t.CUST_COUNT = :cust_count,
                t.PERCENTILE = :percentile,
                t.LOAD_LEVEL = :load_level,
                t.CALC_TIME  = :calc_time
            WHEN NOT MATCHED THEN INSERT
                (BRANCH_NO, LOGIN_ID, EMP_NAME, CUST_COUNT, PERCENTILE, LOAD_LEVEL, CALC_TIME)
            VALUES
                (:branch_no, :login_id, :emp_name, :cust_count, :percentile, :load_level, :calc_time)
        """,
            login_id   = login_id,
            branch_no  = branch_no,
            emp_name   = emp_name,
            cust_count = cust_count,
            percentile = percentile,
            load_level = level,
            calc_time  = now,
        )


# --------------------------------------------------------------------------- #
#  写分配流水                                                                   #
# --------------------------------------------------------------------------- #

def _write_log(cursor, client_ids: list, login_id: str, emp_name: str,
               op_login_id: str, op_emp_name: str, action: str):
    """
    向 T_CUSTOMER_ASSIGN_LOG 批量写入操作流水。
    action: 'ASSIGN' 手动分配 | 'REVOKE' 撤回
    """
    now = datetime.now()
    for client_id in client_ids:
        cursor.execute("""
            INSERT INTO custgroup.T_CUSTOMER_ASSIGN_LOG
                (CLIENT_ID, BRANCH_NO, LOGIN_ID, EMP_NAME,
                 ASSIGN_TIME, LOGIN_ID_OP, EMP_NM_OP, REMARK)
            VALUES
                (:client_id, :branch_no, :login_id, :emp_name,
                 :assign_time, :op_login_id, :op_emp_name, :remark)
        """,
            client_id   = client_id,
            branch_no   = Config.BRANCH_NO,
            login_id    = login_id,
            emp_name    = emp_name,
            assign_time = now,
            op_login_id = op_login_id,
            op_emp_name = op_emp_name,
            remark      = action,
        )


# --------------------------------------------------------------------------- #
#  1. 员工负载列表接口（侧边栏 & 分配弹窗初始化用）                              #
# --------------------------------------------------------------------------- #

@bp.route("/manager/employees/workload", methods=["GET"])
def employees_workload():
    """
    GET /api/manager/employees/workload
    返回当前营业部全量员工负载列表，按客户数从高到低排序。
    前端侧边栏「员工负载分布」和分配弹窗「选择接收员工」均使用此接口。

    返回示例:
    {
        "code": 200,
        "data": [
            {"login_id": "oa001", "emp_name": "张三", "cust_count": 42,
             "load_level": "适中", "percentile": 0.5}
        ]
    }
    """
    if Config.MOCK_MODE:
        from utils.mock_data import get_mock_employees
        return jsonify({"code": 200, "msg": "success", "data": get_mock_employees()})

    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                e.LOGIN_NM,
                e.USER_NM,
                NVL(w.CUST_COUNT, 0) AS CUST_COUNT,
                w.LOAD_LEVEL,
                w.PERCENTILE
            FROM EDW_PROD.t_edw_t01_sim_new_cust_tab e
            LEFT JOIN custgroup.T_EMP_WORKLOAD w
                ON w.LOGIN_ID  = e.LOGIN_NM
               AND w.BRANCH_NO = :branch_no
            WHERE e.BRANCH_NO = :branch_no
            ORDER BY NVL(w.CUST_COUNT, 0) DESC
        """, branch_no=Config.BRANCH_NO)

        results = []
        for login_nm, user_nm, cust_count, load_level, percentile in cursor.fetchall():
            results.append({
                "login_id":   str(login_nm).strip() if login_nm else "",
                "emp_name":   str(user_nm).strip()  if user_nm  else "",
                "cust_count": int(cust_count) if cust_count else 0,
                "load_level": load_level or "空闲",
                "percentile": float(percentile) if percentile is not None else 1.0,
            })

        return jsonify({"code": 200, "msg": "success", "data": results})

    except cx_Oracle.DatabaseError as e:
        logger.error("查询员工负载列表失败: %s", e, exc_info=True)
        return jsonify({"code": 500, "msg": "数据库查询失败"}), 500
    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------------------------------- #
#  2. 员工搜索接口                                                              #
# --------------------------------------------------------------------------- #

@bp.route("/manager/employees/search", methods=["GET"])
def employee_search():
    """
    GET /api/manager/employees/search?q=张三
    q: 员工姓名或OA号，模糊匹配，最少1个字符

    返回示例:
    {
        "code": 200,
        "data": [
            {
                "login_id":   "zhangsan",
                "emp_name":   "张三",
                "cust_count": 42,
                "load_level": "适中",
                "percentile": 0.45
            }
        ]
    }
    """
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify({"code": 400, "msg": "请输入员工姓名或OA号"}), 400

    if Config.MOCK_MODE:
        from utils.mock_data import get_mock_employees
        kw = q.lower()
        results = [
            e for e in get_mock_employees()
            if kw in e["emp_name"].lower() or kw in e["login_id"].lower()
        ]
        return jsonify({"code": 200, "msg": "success", "data": results})

    conn = _get_connection()
    try:
        cursor = conn.cursor()
        # 从员工主表模糊搜索，LEFT JOIN 负载表取实时负载
        cursor.execute("""
            SELECT
                e.LOGIN_NM,
                e.USER_NM,
                NVL(w.CUST_COUNT, 0)  AS CUST_COUNT,
                w.LOAD_LEVEL,
                w.PERCENTILE
            FROM EDW_PROD.t_edw_t01_sim_new_cust_tab e
            LEFT JOIN custgroup.T_EMP_WORKLOAD w
                ON w.LOGIN_ID  = e.LOGIN_NM
               AND w.BRANCH_NO = :branch_no
            WHERE e.BRANCH_NO = :branch_no
              AND (
                  e.USER_NM  LIKE :q
               OR e.LOGIN_NM LIKE :q
              )
            ORDER BY NVL(w.CUST_COUNT, 0) ASC
        """, branch_no=Config.BRANCH_NO, q=f"%{q}%")

        results = []
        for login_nm, user_nm, cust_count, load_level, percentile in cursor.fetchall():
            results.append({
                "login_id":   str(login_nm).strip() if login_nm else "",
                "emp_name":   str(user_nm).strip()  if user_nm  else "",
                "cust_count": int(cust_count) if cust_count else 0,
                "load_level": load_level or "空闲",
                "percentile": float(percentile) if percentile is not None else 1.0,
            })

        return jsonify({"code": 200, "msg": "success", "data": results})
    except cx_Oracle.DatabaseError as e:
        logger.error("员工搜索查询失败: %s", e, exc_info=True)
        return jsonify({"code": 500, "msg": "数据库查询失败"}), 500
    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------------------------------- #
#  2. 手动分配接口                                                              #
# --------------------------------------------------------------------------- #

@bp.route("/manager/customers/assign", methods=["POST"])
def manual_assign():
    """
    POST /api/manager/customers/assign
    Body:
    {
        "client_ids": ["C10024", "C10089"],   // 选中的客户列表
        "login_id":   "zhangsan",             // 目标员工OA
        "emp_name":   "张三"                  // 目标员工姓名
    }

    前置校验：
      - 已在分配关系表中（ASSIGN_SOURCE=1）→ 返回不可分配列表
      - 已在分配关系表中（ASSIGN_SOURCE=0）→ 提示联系数仓撤销
    成功后：写分配关系表、写流水、重算负载
    """
    body = request.get_json(silent=True) or {}
    client_ids = body.get("client_ids", [])
    login_id   = (body.get("login_id") or "").strip()
    emp_name   = (body.get("emp_name") or "").strip()

    if not client_ids or not login_id:
        return jsonify({"code": 400, "msg": "client_ids 和 login_id 不能为空"}), 400

    # ── Mock 模式 ──────────────────────────────────────────────────────
    if Config.MOCK_MODE:
        from utils.mock_data import mock_assign_customers
        result = mock_assign_customers(client_ids, login_id, emp_name)
        if result["blocked_manual"] or result["blocked_rln"]:
            return jsonify({
                "code": 409,
                "msg":  "部分客户存在分配冲突，无法分配",
                "data": result,
            }), 409
        return jsonify({"code": 200, "msg": "分配成功", "data": {"assigned": result["assigned"]}})

    # 从 Token/Session 取操作人身份
    op_login_id = getattr(g, "login_id", "")
    op_emp_name = getattr(g, "emp_name", "")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        # 查询已有分配关系的客户
        bind_vars = ",".join([f":id{i}" for i in range(len(client_ids))])
        params    = {f"id{i}": cid for i, cid in enumerate(client_ids)}
        cursor.execute(
            f"""
            SELECT CLIENT_ID, ASSIGN_SOURCE
            FROM custgroup.T_CUSTOMER_ASSIGN_REL
            WHERE CLIENT_ID IN ({bind_vars})
            """,
            **params
        )
        existing = {str(r[0]).strip(): int(r[1]) for r in cursor.fetchall()}

        # 分类
        blocked_manual = []   # ASSIGN_SOURCE=1，已被手动分配
        blocked_rln    = []   # ASSIGN_SOURCE=0，外部导入不可操作
        assignable     = []

        for cid in client_ids:
            source = existing.get(cid)
            if source == 1:
                blocked_manual.append(cid)
            elif source == 0:
                blocked_rln.append(cid)
            else:
                assignable.append(cid)

        if blocked_manual or blocked_rln:
            return jsonify({
                "code": 409,
                "msg":  "部分客户存在分配冲突，无法分配",
                "data": {
                    "blocked_manual": blocked_manual,
                    "blocked_rln":    blocked_rln,
                    "assignable":     assignable,
                }
            }), 409

        # 写分配关系表
        now = datetime.now()
        for cid in assignable:
            cursor.execute("""
                INSERT INTO custgroup.T_CUSTOMER_ASSIGN_REL
                    (CLIENT_ID, BRANCH_NO, LOGIN_ID, EMP_NAME,
                     ASSIGN_TIME, LOGIN_ID_OP, EMP_NM_OP, ASSIGN_SOURCE)
                VALUES
                    (:client_id, :branch_no, :login_id, :emp_name,
                     :assign_time, :op_login_id, :op_emp_name, 1)
            """,
                client_id   = cid,
                branch_no   = Config.BRANCH_NO,
                login_id    = login_id,
                emp_name    = emp_name,
                assign_time = now,
                op_login_id = op_login_id,
                op_emp_name = op_emp_name,
            )

        # 写流水
        _write_log(cursor, assignable, login_id, emp_name,
                   op_login_id, op_emp_name, "ASSIGN")

        # 负载重算
        _recalc_workload(cursor, Config.BRANCH_NO)

        conn.commit()
        return jsonify({
            "code": 200,
            "msg":  "分配成功",
            "data": {"assigned": assignable}
        })

    except cx_Oracle.DatabaseError as e:
        conn.rollback()
        logger.error("手动分配失败: %s", e, exc_info=True)
        return jsonify({"code": 500, "msg": "数据库操作失败"}), 500
    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------------------------------- #
#  3. 撤回分配接口                                                              #
# --------------------------------------------------------------------------- #

@bp.route("/manager/customers/revoke", methods=["POST"])
def revoke_assign():
    """
    POST /api/manager/customers/revoke
    Body:
    {
        "client_ids": ["C10024", "C10089"]
    }

    校验：只能撤回 ASSIGN_SOURCE=1 的记录
    成功后：删除分配关系表记录、写流水（REVOKE）、重算负载
    """
    body       = request.get_json(silent=True) or {}
    client_ids = body.get("client_ids", [])

    if not client_ids:
        return jsonify({"code": 400, "msg": "client_ids 不能为空"}), 400

    # ── Mock 模式 ──────────────────────────────────────────────────────
    if Config.MOCK_MODE:
        from utils.mock_data import mock_revoke_customers
        result = mock_revoke_customers(client_ids)
        if result["rejected"]:
            return jsonify({
                "code": 409,
                "msg":  "部分客户不支持撤回，仅限手动分配的客户可撤回",
                "data": {"rejected": result["rejected"]},
            }), 409
        return jsonify({"code": 200, "msg": "撤回成功", "data": {"revoked": result["revoked"]}})

    op_login_id = getattr(g, "login_id", "")
    op_emp_name = getattr(g, "emp_name", "")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        # 查现有关系
        bind_vars = ",".join([f":id{i}" for i in range(len(client_ids))])
        params    = {f"id{i}": cid for i, cid in enumerate(client_ids)}
        cursor.execute(
            f"""
            SELECT CLIENT_ID, LOGIN_ID, EMP_NAME, ASSIGN_SOURCE
            FROM custgroup.T_CUSTOMER_ASSIGN_REL
            WHERE CLIENT_ID IN ({bind_vars})
            """,
            **params
        )
        rows     = {str(r[0]).strip(): r for r in cursor.fetchall()}

        rejected = []   # 不存在或 ASSIGN_SOURCE=0
        revokable = []  # ASSIGN_SOURCE=1

        for cid in client_ids:
            row = rows.get(cid)
            if row is None or int(row[3]) != 1:
                rejected.append(cid)
            else:
                revokable.append((cid, str(row[1]), str(row[2])))

        if rejected:
            return jsonify({
                "code": 409,
                "msg":  "部分客户不支持撤回，仅限手动分配的客户可撤回",
                "data": {"rejected": rejected}
            }), 409

        # 删除分配关系
        for cid, login_id, emp_name in revokable:
            cursor.execute(
                "DELETE FROM custgroup.T_CUSTOMER_ASSIGN_REL WHERE CLIENT_ID = :cid",
                cid=cid
            )
            # 按每个员工分别写流水
            _write_log(cursor, [cid], login_id, emp_name,
                       op_login_id, op_emp_name, "REVOKE")

        # 负载重算
        _recalc_workload(cursor, Config.BRANCH_NO)

        conn.commit()
        return jsonify({
            "code": 200,
            "msg":  "撤回成功",
            "data": {"revoked": [r[0] for r in revokable]}
        })

    except cx_Oracle.DatabaseError as e:
        conn.rollback()
        logger.error("撤回分配失败: %s", e, exc_info=True)
        return jsonify({"code": 500, "msg": "数据库操作失败"}), 500
    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------------------------------- #
#  4. 智能分配接口                                                              #
# --------------------------------------------------------------------------- #

def _smart_distribute(customers: list, employees: list) -> dict:
    """
    分层负载均衡分配算法：
      1. 将客户按资产等级分为 高/中/低 三层
      2. 计算每位员工应接收的总客户数（按当前负载反比分配名额）
      3. 在每位员工的名额内，按 高:中:低 = 全局比例 分配各层客户
      4. 剩余客户（因整除取整产生）补给负载最低的员工

    入参:
      customers: [{"client_id": ..., "asset_level": "高价值"|"中等价值"|"低价值"}]
      employees: [{"login_id": ..., "emp_name": ..., "cust_count": int}]
    返回:
      {login_id: [client_id, ...]}
    """
    if not employees:
        return {}

    # 分层
    tiers = {"高价值": [], "中等价值": [], "低价值": []}
    for c in customers:
        tiers.get(c["asset_level"], tiers["低价值"]).append(c["client_id"])

    total_new  = len(customers)
    n_emp      = len(employees)

    # 按当前客户数反比计算权重（客户越少权重越大，权重=1/(cust_count+1)）
    weights    = [1.0 / (e["cust_count"] + 1) for e in employees]
    weight_sum = sum(weights)
    # 每人应分得的客户数（取整，余量后面补）
    quotas     = [floor(total_new * w / weight_sum) for w in weights]
    remainder  = total_new - sum(quotas)
    # 余量按权重从大到小补给
    indices_by_weight = sorted(range(n_emp), key=lambda i: weights[i], reverse=True)
    for i in range(remainder):
        quotas[indices_by_weight[i]] += 1

    # 全局层比例（用于在每人配额内按比例分层）
    tier_counts = {k: len(v) for k, v in tiers.items()}
    tier_order  = ["高价值", "中等价值", "低价值"]
    tier_iters  = {k: iter(v) for k, v in tiers.items()}

    result = {e["login_id"]: [] for e in employees}

    for idx, emp in enumerate(employees):
        quota = quotas[idx]
        if quota == 0:
            continue
        # 按全局比例在该员工配额内分各层
        tier_alloc = {}
        alloc_sum  = 0
        for i, tier in enumerate(tier_order):
            if i < len(tier_order) - 1:
                n = floor(quota * tier_counts[tier] / total_new) if total_new else 0
            else:
                n = quota - alloc_sum   # 最后一层补满
            tier_alloc[tier] = n
            alloc_sum += n

        for tier, n in tier_alloc.items():
            it = tier_iters[tier]
            for _ in range(n):
                cid = next(it, None)
                if cid:
                    result[emp["login_id"]].append(cid)

    # 将迭代器中未分配的客户（因整除取整产生的余量）补给负载最低的员工
    fallback_login = employees[indices_by_weight[0]]["login_id"]
    for tier in tier_order:
        for cid in tier_iters[tier]:
            result[fallback_login].append(cid)

    return result


@bp.route("/manager/customers/smart-assign", methods=["POST"])
def smart_assign():
    """
    POST /api/manager/customers/smart-assign
    Body:
    {
        "client_ids":  ["C10024", "C10089", ...],  // 待分配客户
        "employee_ids": ["zhangsan", "lisi"]        // 候选员工OA池
    }

    算法：分层（高/中/低价值）+ 负载均衡，确保分配后各员工层比例相近
    成功后：写分配关系表、写流水、重算负载
    """
    body        = request.get_json(silent=True) or {}
    client_ids  = body.get("client_ids",  [])
    employee_ids= body.get("employee_ids", [])

    if not client_ids or not employee_ids:
        return jsonify({"code": 400, "msg": "client_ids 和 employee_ids 不能为空"}), 400
    if len(employee_ids) < 2:
        return jsonify({"code": 400, "msg": "至少需要选择 2 位员工"}), 400

    # ── Mock 模式 ──────────────────────────────────────────────────────
    if Config.MOCK_MODE:
        from utils.mock_data import mock_assign_customers, get_mock_employees
        emp_map = {e["login_id"]: e["emp_name"] for e in get_mock_employees()}
        plan_result = []
        # 前端已计算好方案，直接按 employee_ids 轮流写入（简单均分即可）
        n = len(client_ids)
        n_emp = len(employee_ids)
        for i, cid in enumerate(client_ids):
            login_id = employee_ids[i % n_emp]
            emp_name = emp_map.get(login_id, login_id)
            mock_assign_customers([cid], login_id, emp_name)
        plan_result = [
            {"login_id": eid, "emp_name": emp_map.get(eid, eid),
             "client_ids": [client_ids[i] for i in range(len(client_ids)) if i % n_emp == idx],
             "count": len([i for i in range(len(client_ids)) if i % n_emp == idx])}
            for idx, eid in enumerate(employee_ids)
        ]
        return jsonify({"code": 200, "msg": "智能分配成功", "data": {"plan": plan_result}})

    op_login_id = getattr(g, "login_id", "")
    op_emp_name = getattr(g, "emp_name", "")

    conn = _get_connection()
    try:
        cursor = conn.cursor()

        # 1. 前置校验：过滤已有分配关系的客户
        bind_vars = ",".join([f":id{i}" for i in range(len(client_ids))])
        params    = {f"id{i}": cid for i, cid in enumerate(client_ids)}
        cursor.execute(
            f"""
            SELECT CLIENT_ID, ASSIGN_SOURCE
            FROM custgroup.T_CUSTOMER_ASSIGN_REL
            WHERE CLIENT_ID IN ({bind_vars})
            """,
            **params
        )
        existing       = {str(r[0]).strip(): int(r[1]) for r in cursor.fetchall()}
        blocked_manual = [cid for cid in client_ids if existing.get(cid) == 1]
        blocked_rln    = [cid for cid in client_ids if existing.get(cid) == 0]
        assignable_ids = [cid for cid in client_ids if cid not in existing]

        if blocked_manual or blocked_rln:
            return jsonify({
                "code": 409,
                "msg":  "部分客户存在分配冲突，无法参与智能分配",
                "data": {
                    "blocked_manual": blocked_manual,
                    "blocked_rln":    blocked_rln,
                    "assignable":     assignable_ids,
                }
            }), 409

        # 2. 取各客户资产等级（来自资产聚合表）
        bind_vars2 = ",".join([f":cid{i}" for i in range(len(assignable_ids))])
        params2    = {f"cid{i}": cid for i, cid in enumerate(assignable_ids)}
        cursor.execute(
            f"""
            SELECT CUST_NO, CUST_TOT_NET_AST
            FROM (
                SELECT CUST_NO, CUST_TOT_NET_AST,
                       ROW_NUMBER() OVER (PARTITION BY CUST_NO ORDER BY BIZ_DT DESC) AS rn
                FROM DDW_PROD.T_DDW_F20_D_CUST_AUM_BD
                WHERE CUST_NO IN ({bind_vars2})
            )
            WHERE rn = 1
            """,
            **params2
        )
        asset_raw = {str(r[0]).strip(): r[1] for r in cursor.fetchall()}
        customers = []
        for cid in assignable_ids:
            raw   = asset_raw.get(cid, 0) or 0
            aum   = float(raw) / 10000
            customers.append({
                "client_id":   cid,
                "asset_level": get_asset_level(aum),
            })

        # 3. 取候选员工当前负载
        emp_bind = ",".join([f":eid{i}" for i in range(len(employee_ids))])
        emp_params = {f"eid{i}": eid for i, eid in enumerate(employee_ids)}
        cursor.execute(
            f"""
            SELECT e.LOGIN_NM, e.USER_NM, NVL(w.CUST_COUNT, 0)
            FROM EDW_PROD.t_edw_t01_sim_new_cust_tab e
            LEFT JOIN custgroup.T_EMP_WORKLOAD w
                ON w.LOGIN_ID = e.LOGIN_NM AND w.BRANCH_NO = :branch_no
            WHERE e.LOGIN_NM IN ({emp_bind})
            """,
            branch_no=Config.BRANCH_NO,
            **emp_params
        )
        employees = [
            {"login_id": str(r[0]).strip(), "emp_name": str(r[1]).strip(), "cust_count": int(r[2])}
            for r in cursor.fetchall()
        ]

        # 4. 分层负载均衡分配
        plan = _smart_distribute(customers, employees)

        # 5. 写分配关系表 + 流水
        emp_name_map = {e["login_id"]: e["emp_name"] for e in employees}
        now = datetime.now()
        for login_id, cids in plan.items():
            if not cids:
                continue
            emp_name = emp_name_map.get(login_id, "")
            for cid in cids:
                cursor.execute("""
                    INSERT INTO custgroup.T_CUSTOMER_ASSIGN_REL
                        (CLIENT_ID, BRANCH_NO, LOGIN_ID, EMP_NAME,
                         ASSIGN_TIME, LOGIN_ID_OP, EMP_NM_OP, ASSIGN_SOURCE)
                    VALUES
                        (:client_id, :branch_no, :login_id, :emp_name,
                         :assign_time, :op_login_id, :op_emp_name, 1)
                """,
                    client_id   = cid,
                    branch_no   = Config.BRANCH_NO,
                    login_id    = login_id,
                    emp_name    = emp_name,
                    assign_time = now,
                    op_login_id = op_login_id,
                    op_emp_name = op_emp_name,
                )
            _write_log(cursor, cids, login_id, emp_name,
                       op_login_id, op_emp_name, "SMART_ASSIGN")

        # 6. 负载重算
        _recalc_workload(cursor, Config.BRANCH_NO)
        conn.commit()

        return jsonify({
            "code": 200,
            "msg":  "智能分配成功",
            "data": {
                "plan": [
                    {
                        "login_id":  login_id,
                        "emp_name":  emp_name_map.get(login_id, ""),
                        "client_ids": cids,
                        "count":      len(cids),
                    }
                    for login_id, cids in plan.items()
                ]
            }
        })

    except cx_Oracle.DatabaseError as e:
        conn.rollback()
        logger.error("智能分配失败: %s", e, exc_info=True)
        return jsonify({"code": 500, "msg": "数据库操作失败"}), 500
    finally:
        cursor.close()
        conn.close()
