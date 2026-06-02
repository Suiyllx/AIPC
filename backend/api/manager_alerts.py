"""
每日提醒接口
GET  /api/manager/alerts?login_id=xxx
    返回该员工近30天内所有未完成的提醒（is_done=0）

POST /api/manager/alerts
    Body: { "login_id": "oa001", "alert_content": "..." }
    新增一条提醒，同时清理该员工30天前的旧记录

PATCH /api/manager/alerts/<alert_id>/done
    标记指定提醒为已完成
"""

import os
from datetime import datetime, date, timedelta
from flask import request, jsonify
from . import bp

MOCK_MODE = os.environ.get("MOCK_MODE", "false").lower() == "true"

# ------------------------------------------------------------------ #
#  Mock 数据存储（进程内，仅 MOCK_MODE 使用）
# ------------------------------------------------------------------ #
_MOCK_ALERTS: list[dict] = []
_MOCK_ALERT_SEQ = 1


def _mock_next_id() -> int:
    global _MOCK_ALERT_SEQ
    _id = _MOCK_ALERT_SEQ
    _MOCK_ALERT_SEQ += 1
    return _id


def _mock_seed():
    """首次调用时预置一些示例提醒"""
    global _MOCK_ALERTS
    if _MOCK_ALERTS:
        return
    today = date.today()
    _MOCK_ALERTS = [
        {
            "alert_id":      _mock_next_id(),
            "employee_id":   "oa001",
            "alert_content": "跟进高净值客户 张伟，近7日未回访",
            "alert_date":    today.strftime("%Y-%m-%d"),
            "is_done":       0,
        },
        {
            "alert_id":      _mock_next_id(),
            "employee_id":   "oa001",
            "alert_content": "本月末佣金达标检查，核实低频客户持仓",
            "alert_date":    (today - timedelta(days=2)).strftime("%Y-%m-%d"),
            "is_done":       0,
        },
        {
            "alert_id":      _mock_next_id(),
            "employee_id":   "oa001",
            "alert_content": "新开户客户激活回访（本周内完成）",
            "alert_date":    (today - timedelta(days=5)).strftime("%Y-%m-%d"),
            "is_done":       0,
        },
    ]


# ------------------------------------------------------------------ #
#  GET /api/manager/alerts
# ------------------------------------------------------------------ #
@bp.route("/manager/alerts", methods=["GET"])
def get_alerts():
    login_id = request.args.get("login_id", "").strip()
    if not login_id:
        return jsonify({"code": 400, "msg": "login_id 必填"}), 400

    if MOCK_MODE:
        return _get_mock(login_id)
    return _get_real(login_id)


def _get_mock(login_id: str):
    _mock_seed()
    cutoff = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    result = [
        a for a in _MOCK_ALERTS
        if a["employee_id"] == login_id
        and a["is_done"] == 0
        and a["alert_date"] >= cutoff
    ]
    # 按日期倒序
    result.sort(key=lambda x: x["alert_date"], reverse=True)
    return jsonify({"code": 200, "data": result})


def _get_real(login_id: str):
    from db import get_connection
    cutoff = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    sql = """
        SELECT ALERT_ID, EMPLOYEE_ID, ALERT_CONTENT,
               TO_CHAR(ALERT_DATE, 'YYYY-MM-DD') AS ALERT_DATE, IS_DONE
        FROM   CUSTGROUP.AIPC_MAN_ALERT
        WHERE  EMPLOYEE_ID = :eid
          AND  IS_DONE     = 0
          AND  ALERT_DATE  >= TO_DATE(:cutoff, 'YYYY-MM-DD')
        ORDER BY ALERT_DATE DESC, ALERT_ID DESC
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, eid=login_id, cutoff=cutoff)
        cols = [c[0].lower() for c in cursor.description]
        rows = [dict(zip(cols, r)) for r in cursor.fetchall()]
    return jsonify({"code": 200, "data": rows})


# ------------------------------------------------------------------ #
#  POST /api/manager/alerts
# ------------------------------------------------------------------ #
@bp.route("/manager/alerts", methods=["POST"])
def create_alert():
    body = request.get_json(silent=True) or {}
    login_id = (body.get("login_id") or "").strip()
    content  = (body.get("alert_content") or "").strip()

    if not login_id or not content:
        return jsonify({"code": 400, "msg": "login_id 和 alert_content 必填"}), 400
    if len(content) > 500:
        return jsonify({"code": 400, "msg": "提醒内容不能超过500字"}), 400

    if MOCK_MODE:
        return _create_mock(login_id, content)
    return _create_real(login_id, content)


def _create_mock(login_id: str, content: str):
    _mock_seed()
    today_str = date.today().strftime("%Y-%m-%d")
    # 清理该员工30天前的记录
    cutoff = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    global _MOCK_ALERTS
    _MOCK_ALERTS = [
        a for a in _MOCK_ALERTS
        if not (a["employee_id"] == login_id and a["alert_date"] < cutoff)
    ]
    new_alert = {
        "alert_id":      _mock_next_id(),
        "employee_id":   login_id,
        "alert_content": content,
        "alert_date":    today_str,
        "is_done":       0,
    }
    _MOCK_ALERTS.append(new_alert)
    return jsonify({"code": 200, "data": new_alert})


def _create_real(login_id: str, content: str):
    from db import get_connection
    today = date.today()
    cutoff = today - timedelta(days=30)

    insert_sql = """
        INSERT INTO CUSTGROUP.AIPC_MAN_ALERT
            (EMPLOYEE_ID, ALERT_CONTENT, ALERT_DATE, IS_DONE)
        VALUES (:eid, :content, TRUNC(SYSDATE), 0)
        RETURNING ALERT_ID INTO :alert_id
    """
    delete_sql = """
        DELETE FROM CUSTGROUP.AIPC_MAN_ALERT
        WHERE  EMPLOYEE_ID = :eid
          AND  ALERT_DATE  < TO_DATE(:cutoff, 'YYYY-MM-DD')
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        alert_id_var = cursor.var(int)
        cursor.execute(insert_sql, eid=login_id, content=content, alert_id=alert_id_var)
        # 顺手清理30天前旧记录
        cursor.execute(delete_sql, eid=login_id, cutoff=cutoff.strftime("%Y-%m-%d"))
        conn.commit()
        new_id = alert_id_var.getvalue()[0]

    return jsonify({
        "code": 200,
        "data": {
            "alert_id":      new_id,
            "employee_id":   login_id,
            "alert_content": content,
            "alert_date":    today.strftime("%Y-%m-%d"),
            "is_done":       0,
        }
    })


# ------------------------------------------------------------------ #
#  PATCH /api/manager/alerts/<alert_id>/done
# ------------------------------------------------------------------ #
@bp.route("/manager/alerts/<int:alert_id>/done", methods=["PATCH"])
def mark_done(alert_id: int):
    if MOCK_MODE:
        return _mark_done_mock(alert_id)
    return _mark_done_real(alert_id)


def _mark_done_mock(alert_id: int):
    _mock_seed()
    for a in _MOCK_ALERTS:
        if a["alert_id"] == alert_id:
            a["is_done"] = 1
            return jsonify({"code": 200, "data": {"alert_id": alert_id}})
    return jsonify({"code": 404, "msg": "提醒不存在"}), 404


def _mark_done_real(alert_id: int):
    from db import get_connection
    sql = """
        UPDATE CUSTGROUP.AIPC_MAN_ALERT
        SET IS_DONE = 1, UPDATE_TIME = SYSTIMESTAMP
        WHERE ALERT_ID = :aid
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, aid=alert_id)
        if cursor.rowcount == 0:
            return jsonify({"code": 404, "msg": "提醒不存在"}), 404
        conn.commit()
    return jsonify({"code": 200, "data": {"alert_id": alert_id}})
