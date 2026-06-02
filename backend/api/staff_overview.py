# ---------------------------------------------------------------------------
# 工作台总览接口
# GET /api/staff/overview?login_id=xxx
#
# 返回三块数据：
#   aum_card     —— 月AUM净增率（当月最新 vs 上月末）
#   call_card    —— 今日外呼情况（T_CALL_LOG，加微/绑定暂用mock）
#   task_card    —— 任务进度（暂用mock，待任务大厅表建好后替换）
# ---------------------------------------------------------------------------

import os
from flask import request, jsonify
from . import bp

MOCK_MODE = os.environ.get('MOCK_MODE', 'true').lower() == 'true'

# ── mock 数据 ────────────────────────────────────────────────────────────────
_MOCK_OVERVIEW = {
    'aum_card': {
        'current_aum':      15_230_000.0,   # 当月最新总AUM（元）
        'last_month_aum':   14_800_000.0,   # 上月末总AUM（元）
        'net_increase':       430_000.0,    # 净增额（元）
        'net_increase_rate':    2.91,       # 净增率（%）
        'display_increase':   '43.0万',     # 前端展示净增额
    },
    'call_card': {
        'connected':    56,   # 今日外呼接通数
        'total':        89,   # 今日外呼总量
        'wechat_add':   24,   # 今日加微（暂mock）
        'bound':        12,   # 今日微信绑定数（暂mock）
        'bound_total': 1248,  # 微信绑定历史累计（暂mock）
        'intention':     8,   # 意向客户（暂mock）
    },
    'task_card': {
        'todo':     25,
        'done':     16,
        'overdue':   3,
        'rate':     64,   # 完成率 %
    },
}


# ── 真实DB路径工具 ────────────────────────────────────────────────────────────
def _get_conn():
    import cx_Oracle
    dsn = cx_Oracle.makedsn(
        os.environ['DB_HOST'],
        os.environ.get('DB_PORT', 1521),
        service_name=os.environ['DB_SERVICE'],
    )
    return cx_Oracle.connect(os.environ['DB_USER'], os.environ['DB_PASS'], dsn)


def _fetch_aum(login_id: str) -> dict:
    """
    从 DDW_PROD.T_DDW_F20_D_CUST_AUM_BD 取当月最新和上月末 AUM 合计。
    逻辑：
      1. 找该员工名下所有客户（T_CUSTOMER_ASSIGN_REL）
      2. 对每位客户，取最近两个自然月各自最后一个交易日的 CUST_TOT_NET_AST
      3. 按月汇总后相减得净增额和净增率
    """
    conn = _get_conn()
    try:
        cur = conn.cursor()
        sql = """
            SELECT
                SUM(CASE WHEN month_rank = 1 THEN CUST_TOT_NET_AST ELSE 0 END) AS current_aum,
                SUM(CASE WHEN month_rank = 2 THEN CUST_TOT_NET_AST ELSE 0 END) AS last_month_aum
            FROM (
                SELECT
                    CUST_NO,
                    CUST_TOT_NET_AST,
                    BIZ_DT,
                    DENSE_RANK() OVER (
                        PARTITION BY CUST_NO
                        ORDER BY SUBSTR(BIZ_DT, 1, 6) DESC
                    ) AS month_rank,
                    ROW_NUMBER() OVER (
                        PARTITION BY CUST_NO, SUBSTR(BIZ_DT, 1, 6)
                        ORDER BY BIZ_DT DESC
                    ) AS rn_in_month
                FROM DDW_PROD.T_DDW_F20_D_CUST_AUM_BD
                WHERE CUST_NO IN (
                    SELECT CUST_NO
                    FROM CUSTGROUP.T_CUSTOMER_ASSIGN_REL
                    WHERE LOGIN_ID = :login_id
                )
            )
            WHERE month_rank <= 2 AND rn_in_month = 1
        """
        cur.execute(sql, {'login_id': login_id})
        row = cur.fetchone()
        current_aum    = float(row[0] or 0)
        last_month_aum = float(row[1] or 0)
        net_increase   = current_aum - last_month_aum
        net_increase_rate = (
            round(net_increase / last_month_aum * 100, 2)
            if last_month_aum != 0 else 0.0
        )
        # 展示用：转万元，保留1位小数
        display_increase = f"{net_increase / 10000:.1f}万"
        return {
            'current_aum':      current_aum,
            'last_month_aum':   last_month_aum,
            'net_increase':     net_increase,
            'net_increase_rate': net_increase_rate,
            'display_increase': display_increase,
        }
    finally:
        conn.close()


def _fetch_call(login_id: str) -> dict:
    """
    从 T_CALL_LOG 取今日外呼接通数和总量。
    加微/绑定/意向等字段暂无表，返回 None 由前端显示 --。
    """
    conn = _get_conn()
    try:
        cur = conn.cursor()
        sql = """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN CALL_RESULT = '接通' THEN 1 ELSE 0 END) AS connected
            FROM CUSTGROUP.T_CALL_LOG
            WHERE LOGIN_ID = :login_id
              AND TRUNC(CALL_TIME) = TRUNC(SYSDATE)
        """
        cur.execute(sql, {'login_id': login_id})
        row = cur.fetchone()
        return {
            'connected':   int(row[1] or 0),
            'total':       int(row[0] or 0),
            'wechat_add':  None,   # 暂无表，前端显示 --
            'bound':       None,
            'intention':   None,
        }
    finally:
        conn.close()


# ── 路由 ──────────────────────────────────────────────────────────────────────
@bp.route('/staff/overview', methods=['GET'])
def get_overview():
    login_id = request.args.get('login_id', '').strip()
    if not login_id:
        return jsonify({'error': 'login_id 必填'}), 400

    if MOCK_MODE:
        return jsonify(_MOCK_OVERVIEW)

    try:
        aum_card  = _fetch_aum(login_id)
        call_card = _fetch_call(login_id)
        # 任务进度暂用mock，待任务大厅表建好后替换
        task_card = {
            'todo': None, 'done': None, 'overdue': None, 'rate': None
        }
        return jsonify({
            'aum_card':  aum_card,
            'call_card': call_card,
            'task_card': task_card,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
