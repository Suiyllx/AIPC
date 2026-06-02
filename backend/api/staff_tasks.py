# ---------------------------------------------------------------------------
# 营销人员任务接口
#
# GET /api/staff/tasks/urgent-summary?login_id=xxx
#     今日高优任务按分类聚合，用于工作台总览「高优任务」区块
#     响应:
#       {
#         "total": 3,                  -- 今日高优任务总数
#         "summary": [
#           {
#             "task_type":   "跟进类",
#             "count":       2,        -- 该类高优任务数量
#             "earliest_due": "10:00"  -- 最早截止时间（HH:MM，仅时分）
#                                      -- 若 DUE_DATE 无时分则为 "今日"
#           },
#           ...
#         ]
#       }
#     只返回今日有高优（PRIORITY='高'）且未完成（STATUS IN 待处理/处理中）任务的分类，
#     按 count DESC、earliest_due ASC 排序。
#
# GET /api/staff/tasks?login_id=xxx&task_type=xxx&status=xxx&page=1&page_size=20
#     任务列表查询（任务大厅 Tab 用），支持分类/状态过滤和分页
# ---------------------------------------------------------------------------

import os
from flask import request, jsonify
from . import bp

MOCK_MODE = os.environ.get('MOCK_MODE', 'true').lower() == 'true'

# 任务分类固定顺序（用于排序）
TASK_TYPE_ORDER = ['建联类', '跟进类', '周期类', '营销活动类', '合规类']

# ── mock 数据（日期动态生成，始终相对于今天） ────────────────────────────────
def _build_mock_tasks():
    from datetime import date, timedelta
    t = date.today().isoformat()                        # 今天
    t1 = (date.today() + timedelta(days=1)).isoformat() # 明天
    t3 = (date.today() + timedelta(days=3)).isoformat() # 3天后
    t5 = (date.today() + timedelta(days=5)).isoformat() # 5天后
    t7 = (date.today() + timedelta(days=7)).isoformat() # 7天后

    return [
        # ── 高优·跟进类
        {'id': 1,  'login_id': 'oa001', 'task_type': '跟进类',     'task_sub_type': '意向跟进',    'task_name': '意向客户跟进',       'priority': '高', 'source': '系统自动', 'issue_date': t,  'due_date': t,  'due_time': '10:00', 'status': '待处理', 'finish_date': None, 'cust_no': 'C001001', 'cust_name': '王*明'},
        {'id': 2,  'login_id': 'oa001', 'task_type': '跟进类',     'task_sub_type': '逾期未回复',  'task_name': '逾期未回复跟进',     'priority': '高', 'source': '系统自动', 'issue_date': t,  'due_date': t,  'due_time': '18:00', 'status': '待处理', 'finish_date': None, 'cust_no': 'C001011', 'cust_name': '李*华'},
        # ── 高优·建联类
        {'id': 3,  'login_id': 'oa001', 'task_type': '建联类',     'task_sub_type': 'AI外呼',      'task_name': 'AI外呼',             'priority': '高', 'source': '系统自动', 'issue_date': t,  'due_date': t,  'due_time': '12:00', 'status': '待处理', 'finish_date': None, 'cust_no': 'C001002', 'cust_name': '陈*兰'},
        # ── 高优·周期类
        {'id': 4,  'login_id': 'oa001', 'task_type': '周期类',     'task_sub_type': '流失预警',    'task_name': '流失预警处理',       'priority': '高', 'source': '系统自动', 'issue_date': t,  'due_date': t,  'due_time': None,    'status': '待处理', 'finish_date': None, 'cust_no': 'C001005', 'cust_name': '赵*强'},
        # ── 高优·营销活动类
        {'id': 5,  'login_id': 'oa001', 'task_type': '营销活动类', 'task_sub_type': '六月财富节',  'task_name': '客户邀约',           'priority': '高', 'source': '主管下发', 'issue_date': t,  'due_date': t3, 'due_time': None,    'status': '待处理', 'finish_date': None, 'cust_no': None,       'cust_name': None},
        # ── 高优·合规类
        {'id': 6,  'login_id': 'oa001', 'task_type': '合规类',     'task_sub_type': '风险测评到期','task_name': '客户风险测评到期',   'priority': '高', 'source': '系统自动', 'issue_date': t,  'due_date': t,  'due_time': '17:00', 'status': '待处理', 'finish_date': None, 'cust_no': 'C001012', 'cust_name': '孙*秀'},
        # ── 中优·建联类
        {'id': 7,  'login_id': 'oa001', 'task_type': '建联类',     'task_sub_type': '人工外呼',    'task_name': '人工外呼',           'priority': '中', 'source': '主管下发', 'issue_date': t,  'due_date': t1, 'due_time': None,    'status': '处理中', 'finish_date': None, 'cust_no': 'C001003', 'cust_name': '张*伟'},
        {'id': 8,  'login_id': 'oa001', 'task_type': '建联类',     'task_sub_type': 'AI外呼',      'task_name': 'AI外呼',             'priority': '中', 'source': '系统自动', 'issue_date': t,  'due_date': t3, 'due_time': None,    'status': '待处理', 'finish_date': None, 'cust_no': 'C001008', 'cust_name': '刘*芳'},
        # ── 中优·跟进类
        {'id': 9,  'login_id': 'oa001', 'task_type': '跟进类',     'task_sub_type': '到期提醒',    'task_name': '产品到期提醒',       'priority': '中', 'source': '系统自动', 'issue_date': t,  'due_date': t1, 'due_time': None,    'status': '待处理', 'finish_date': None, 'cust_no': 'C001006', 'cust_name': '吴*霞'},
        {'id': 10, 'login_id': 'oa001', 'task_type': '跟进类',     'task_sub_type': '重点二次触达','task_name': '重点客户二次触达',   'priority': '中', 'source': '系统自动', 'issue_date': t,  'due_date': t1, 'due_time': None,    'status': '待处理', 'finish_date': None, 'cust_no': 'C001009', 'cust_name': '郑*国'},
        # ── 中优·周期类
        {'id': 11, 'login_id': 'oa001', 'task_type': '周期类',     'task_sub_type': '养客',        'task_name': '持仓关怀',           'priority': '中', 'source': '系统自动', 'issue_date': t,  'due_date': t3, 'due_time': None,    'status': '待处理', 'finish_date': None, 'cust_no': 'C001013', 'cust_name': '冯*梅'},
        {'id': 12, 'login_id': 'oa001', 'task_type': '周期类',     'task_sub_type': '复投',        'task_name': '到期产品复投',       'priority': '中', 'source': '系统自动', 'issue_date': t,  'due_date': t5, 'due_time': None,    'status': '待处理', 'finish_date': None, 'cust_no': 'C001014', 'cust_name': '韩*东'},
        {'id': 13, 'login_id': 'oa001', 'task_type': '周期类',     'task_sub_type': '引客',        'task_name': '新客欢迎触达',       'priority': '低', 'source': '系统自动', 'issue_date': t,  'due_date': t7, 'due_time': None,    'status': '待处理', 'finish_date': None, 'cust_no': 'C001015', 'cust_name': '程*雪'},
        # ── 中优·合规类
        {'id': 14, 'login_id': 'oa001', 'task_type': '合规类',     'task_sub_type': '录音复盘',    'task_name': '外呼录音复盘',       'priority': '中', 'source': '系统自动', 'issue_date': t,  'due_date': t,  'due_time': '17:00', 'status': '待处理', 'finish_date': None, 'cust_no': None,       'cust_name': None},
        {'id': 15, 'login_id': 'oa001', 'task_type': '合规类',     'task_sub_type': '培训作业',    'task_name': '培训作业完成',       'priority': '低', 'source': '主管下发', 'issue_date': t,  'due_date': t1, 'due_time': None,    'status': '待处理', 'finish_date': None, 'cust_no': None,       'cust_name': None},
        # ── 营销活动类（中优）
        {'id': 16, 'login_id': 'oa001', 'task_type': '营销活动类', 'task_sub_type': '基金定投推广季','task_name': '客户推介',          'priority': '中', 'source': '主管下发', 'issue_date': t,  'due_date': t3, 'due_time': None,    'status': '处理中', 'finish_date': None, 'cust_no': None,       'cust_name': None},
        # ── 已完成
        {'id': 17, 'login_id': 'oa001', 'task_type': '建联类',     'task_sub_type': '加微信',      'task_name': '微信添加',           'priority': '中', 'source': '系统自动', 'issue_date': t,  'due_date': t,  'due_time': None,    'status': '已完成', 'finish_date': t, 'cust_no': 'C001004', 'cust_name': '周*丽'},
        {'id': 18, 'login_id': 'oa001', 'task_type': '跟进类',     'task_sub_type': '到期提醒',    'task_name': '产品到期提醒',       'priority': '中', 'source': '系统自动', 'issue_date': t,  'due_date': t,  'due_time': None,    'status': '已完成', 'finish_date': t, 'cust_no': 'C001010', 'cust_name': '黄*军'},
        {'id': 19, 'login_id': 'oa001', 'task_type': '周期类',     'task_sub_type': '流失预警',    'task_name': '流失预警处理',       'priority': '高', 'source': '系统自动', 'issue_date': t,  'due_date': t,  'due_time': None,    'status': '已完成', 'finish_date': t, 'cust_no': 'C001007', 'cust_name': '杨*峰'},
        {'id': 20, 'login_id': 'oa001', 'task_type': '合规类',     'task_sub_type': '录音复盘',    'task_name': '外呼录音复盘',       'priority': '中', 'source': '系统自动', 'issue_date': t,  'due_date': t,  'due_time': None,    'status': '已完成', 'finish_date': t, 'cust_no': None,       'cust_name': None},
    ]

_MOCK_TASKS = _build_mock_tasks()


def _mock_urgent_summary(login_id: str) -> dict:
    """今日高优未完成任务，按分类聚合"""
    from datetime import date
    today = date.today().isoformat()
    urgent = [
        t for t in _MOCK_TASKS
        if t['login_id'] == login_id
        and t['priority'] == '高'
        and t['status'] in ('待处理', '处理中')
        and t['issue_date'] <= today <= t['due_date']
    ]
    # 按分类聚合
    groups: dict[str, list] = {}
    for t in urgent:
        groups.setdefault(t['task_type'], []).append(t)

    summary = []
    for task_type in TASK_TYPE_ORDER:
        if task_type not in groups:
            continue
        items = groups[task_type]
        # 最早截止时间：优先取 due_time，若无则看是否今日到期
        due_times = [t['due_time'] for t in items if t['due_time']]
        if due_times:
            earliest = min(due_times)
        elif any(t['due_date'] == today for t in items):
            earliest = '今日'
        else:
            # 取最近的 due_date
            nearest = min(t['due_date'] for t in items)
            earliest = nearest  # YYYY-MM-DD 格式
        summary.append({
            'task_type':    task_type,
            'count':        len(items),
            'earliest_due': earliest,
        })

    # 按截止时间由近到远排序
    # 排序键：HH:MM → 当天时刻最紧；'今日' → 次之；YYYY-MM-DD → 按日期升序
    def _sort_key(item):
        e = item['earliest_due']
        if len(e) == 5 and ':' in e:          # HH:MM
            return (0, e)
        elif e == '今日':
            return (1, '')
        else:                                  # YYYY-MM-DD
            return (2, e)

    summary.sort(key=_sort_key)
    return {'total': len(urgent), 'summary': summary}


# ── 真实DB工具 ────────────────────────────────────────────────────────────────
def _get_conn():
    import cx_Oracle
    dsn = cx_Oracle.makedsn(
        os.environ['DB_HOST'],
        os.environ.get('DB_PORT', 1521),
        service_name=os.environ['DB_SERVICE'],
    )
    return cx_Oracle.connect(os.environ['DB_USER'], os.environ['DB_PASS'], dsn)


def _db_urgent_summary(login_id: str) -> dict:
    """
    今日高优未完成任务，按分类聚合。
    DUE_DATE 是 DATE 类型（精确到日），如需精确到时刻，
    可在 TASK_NAME 或 REMARK 中附记，或后续给表加 DUE_TIME 字段。
    """
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                TASK_TYPE,
                COUNT(*)                              AS CNT,
                MIN(DUE_DATE)                         AS EARLIEST_DUE
            FROM CUSTGROUP.AIPC_STAFF_TASK
            WHERE LOGIN_ID = :login_id
              AND PRIORITY  = '高'
              AND STATUS    IN ('待处理', '处理中')
              AND ISSUE_DATE <= TRUNC(SYSDATE)
              AND DUE_DATE  >= TRUNC(SYSDATE)
            GROUP BY TASK_TYPE
        """, {'login_id': login_id})
        rows = cur.fetchall()

        # 总数
        cur.execute("""
            SELECT COUNT(*)
            FROM CUSTGROUP.AIPC_STAFF_TASK
            WHERE LOGIN_ID = :login_id
              AND PRIORITY  = '高'
              AND STATUS    IN ('待处理', '处理中')
              AND ISSUE_DATE <= TRUNC(SYSDATE)
              AND DUE_DATE  >= TRUNC(SYSDATE)
        """, {'login_id': login_id})
        total = cur.fetchone()[0]
        conn.close()

        # 构建 summary，按预定顺序排
        raw = {r[0]: r for r in rows}
        from datetime import date
        today = date.today()
        summary = []
        for task_type in TASK_TYPE_ORDER:
            if task_type not in raw:
                continue
            _, cnt, earliest_due = raw[task_type]
            # earliest_due 是 datetime.date 对象
            if earliest_due.date() == today:
                earliest_str = '今日'
            else:
                earliest_str = earliest_due.strftime('%Y-%m-%d')
            summary.append({
                'task_type':    task_type,
                'count':        int(cnt),
                'earliest_due': earliest_str,
            })
        return {'total': int(total), 'summary': summary}
    finally:
        conn.close()


# ── 路由：高优任务聚合 ────────────────────────────────────────────────────────
@bp.route('/staff/tasks/urgent-summary', methods=['GET'])
def get_urgent_summary():
    login_id = request.args.get('login_id', '').strip()
    if not login_id:
        return jsonify({'error': 'login_id 必填'}), 400

    if MOCK_MODE:
        return jsonify(_mock_urgent_summary(login_id))
    try:
        return jsonify(_db_urgent_summary(login_id))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── 路由：任务列表（任务大厅 Tab 用） ─────────────────────────────────────────
@bp.route('/staff/tasks', methods=['GET'])
def get_task_list():
    login_id  = request.args.get('login_id', '').strip()
    task_type = request.args.get('task_type', '').strip()   # 一级分类过滤
    status    = request.args.get('status', '').strip()      # 状态过滤
    page      = max(1, int(request.args.get('page', 1)))
    page_size = max(1, min(100, int(request.args.get('page_size', 20))))

    if not login_id:
        return jsonify({'error': 'login_id 必填'}), 400

    if MOCK_MODE:
        tasks = [t for t in _MOCK_TASKS if t['login_id'] == login_id]
        if task_type:
            tasks = [t for t in tasks if t['task_type'] == task_type]
        if status:
            tasks = [t for t in tasks if t['status'] == status]
        total = len(tasks)
        start = (page - 1) * page_size
        return jsonify({
            'tasks':     tasks[start: start + page_size],
            'total':     total,
            'page':      page,
            'page_size': page_size,
        })

    try:
        conn = _get_conn()
        cur  = conn.cursor()
        where = ['LOGIN_ID = :login_id']
        params = {'login_id': login_id}
        if task_type:
            where.append('TASK_TYPE = :task_type')
            params['task_type'] = task_type
        if status:
            where.append('STATUS = :status')
            params['status'] = status
        where_sql = ' AND '.join(where)

        cur.execute(f'SELECT COUNT(*) FROM CUSTGROUP.AIPC_STAFF_TASK WHERE {where_sql}', params)
        total = cur.fetchone()[0]

        offset = (page - 1) * page_size
        cur.execute(f"""
            SELECT
                t.TASK_ID, t.TASK_TYPE, t.TASK_SUB_TYPE, t.TASK_NAME,
                t.PRIORITY, t.SOURCE,
                TO_CHAR(t.ISSUE_DATE,'YYYY-MM-DD'), TO_CHAR(t.DUE_DATE,'YYYY-MM-DD'),
                t.STATUS, TO_CHAR(t.FINISH_DATE,'YYYY-MM-DD'),
                t.CUST_NO, t.REMARK,
                -- 客户姓名：取自客户基础表，脱敏（第2字替换为*）
                CASE WHEN c.CUST_NAME IS NOT NULL
                     THEN SUBSTR(c.CUST_NAME,1,1) || '*' || SUBSTR(c.CUST_NAME,3)
                     ELSE NULL END AS CUST_NAME_MASKED
            FROM CUSTGROUP.AIPC_STAFF_TASK t
            LEFT JOIN CUSTGROUP.T_CUSTOMER_INFO c ON t.CUST_NO = c.CUST_NO
            WHERE {where_sql.replace('LOGIN_ID','t.LOGIN_ID').replace('TASK_TYPE','t.TASK_TYPE').replace('STATUS','t.STATUS')}
            ORDER BY
                CASE t.PRIORITY WHEN '高' THEN 0 WHEN '中' THEN 1 ELSE 2 END,
                t.DUE_DATE ASC
            OFFSET :offset ROWS FETCH NEXT :page_size ROWS ONLY
        """, {**params, 'offset': offset, 'page_size': page_size})
        rows = cur.fetchall()
        conn.close()

        tasks = [
            {
                'id': r[0], 'task_type': r[1], 'task_sub_type': r[2],
                'task_name': r[3], 'priority': r[4], 'source': r[5],
                'issue_date': r[6], 'due_date': r[7], 'status': r[8],
                'finish_date': r[9], 'cust_no': r[10], 'remark': r[11],
                'cust_name': r[12],
            }
            for r in rows
        ]
        return jsonify({'tasks': tasks, 'total': total, 'page': page, 'page_size': page_size})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
