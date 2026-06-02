# ---------------------------------------------------------------------------
# 每日资讯接口
#
# GET /api/staff/news/today
#     返回今日资讯列表（用于首页banner，最多返回5条）
#     响应: { news: [{id, title, category, link}] }
#
# GET /api/staff/news
#     资讯列表（弹窗使用），支持筛选和分页
#     参数:
#       title    — 标题模糊搜索（可选）
#       category — 分类精确过滤（可选，如"市场"）
#       month    — 年月过滤，格式 YYYY-MM（可选，不传则查全部）
#       page     — 页码，默认1
#       page_size— 每页条数，默认20
#     响应: { news: [...], total, page, page_size, categories: [...] }
# ---------------------------------------------------------------------------

import os
from flask import request, jsonify
from . import bp

MOCK_MODE = os.environ.get('MOCK_MODE', 'true').lower() == 'true'

# ── mock 数据 ────────────────────────────────────────────────────────────────
_MOCK_NEWS = [
    {'id': 1,  'title': '央行发布二季度货币政策报告，稳息基调不变',          'category': '市场', 'link': None, 'date': '2026-05-29'},
    {'id': 2,  'title': '个人养老金账户缴存规则调整，年度上限升至2.4万',      'category': '政策', 'link': None, 'date': '2026-05-29'},
    {'id': 3,  'title': '沪深300指数成分股季度调整结果公布',                  'category': '市场', 'link': None, 'date': '2026-05-29'},
    {'id': 4,  'title': '公募基金费率改革二期落地，管理费上限下调',           'category': '产品', 'link': None, 'date': '2026-05-29'},
    {'id': 5,  'title': '美联储5月议息会议：维持利率不变，关注通胀路径',      'category': '宏观', 'link': None, 'date': '2026-05-28'},
    {'id': 6,  'title': '证监会：进一步推进注册制改革完善配套机制',           'category': '政策', 'link': None, 'date': '2026-05-28'},
    {'id': 7,  'title': 'A股市场波动加剧，机构建议关注防御型资产配置',        'category': '市场', 'link': None, 'date': '2026-05-27'},
    {'id': 8,  'title': '国家统计局发布4月CPI数据，同比上涨0.3%',            'category': '宏观', 'link': None, 'date': '2026-05-27'},
    {'id': 9,  'title': '新版理财产品销售管理办法征求意见稿发布',             'category': '政策', 'link': None, 'date': '2026-05-26'},
    {'id': 10, 'title': '债券市场流动性改善，十年期国债收益率走低',           'category': '市场', 'link': None, 'date': '2026-05-26'},
    {'id': 11, 'title': '我行推出季度特惠理财产品，预期年化收益4.1%',        'category': '产品', 'link': None, 'date': '2026-05-25'},
    {'id': 12, 'title': '外资加速布局中国债市，4月净买入创年内新高',          'category': '宏观', 'link': None, 'date': '2026-05-25'},
]


def _apply_filters(news_list, title, category, month):
    result = news_list
    if title:
        result = [n for n in result if title in n['title']]
    if category:
        result = [n for n in result if n['category'] == category]
    if month:
        # month 格式 YYYY-MM
        result = [n for n in result if n['date'].startswith(month)]
    return result


# ── 真实DB工具 ────────────────────────────────────────────────────────────────
def _get_conn():
    import cx_Oracle
    dsn = cx_Oracle.makedsn(
        os.environ['DB_HOST'],
        os.environ.get('DB_PORT', 1521),
        service_name=os.environ['DB_SERVICE'],
    )
    return cx_Oracle.connect(os.environ['DB_USER'], os.environ['DB_PASS'], dsn)


# ── 路由：今日资讯（首页banner） ──────────────────────────────────────────────
@bp.route('/staff/news/today', methods=['GET'])
def get_today_news():
    if MOCK_MODE:
        today_news = [n for n in _MOCK_NEWS if n['date'] == _MOCK_NEWS[0]['date']][:5]
        return jsonify({'news': today_news})

    try:
        conn = _get_conn()
        cur  = conn.cursor()
        cur.execute("""
            SELECT NEWS_ID, TITLE, CATEGORY, LINK
            FROM CUSTGROUP.AIPC_DAILY_NEWS
            WHERE NEWS_DATE = TRUNC(SYSDATE)
            ORDER BY NEWS_ID ASC
            FETCH FIRST 5 ROWS ONLY
        """)
        rows = cur.fetchall()
        conn.close()
        news = [
            {'id': r[0], 'title': r[1], 'category': r[2], 'link': r[3]}
            for r in rows
        ]
        return jsonify({'news': news})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── 路由：资讯列表（弹窗筛选用） ──────────────────────────────────────────────
@bp.route('/staff/news', methods=['GET'])
def get_news_list():
    title     = request.args.get('title', '').strip()
    category  = request.args.get('category', '').strip()
    month     = request.args.get('month', '').strip()       # YYYY-MM
    page      = max(1, int(request.args.get('page', 1)))
    page_size = max(1, min(100, int(request.args.get('page_size', 20))))

    if MOCK_MODE:
        filtered = _apply_filters(_MOCK_NEWS, title or None, category or None, month or None)
        total    = len(filtered)
        start    = (page - 1) * page_size
        paged    = filtered[start: start + page_size]
        all_cats = sorted({n['category'] for n in _MOCK_NEWS})
        return jsonify({
            'news':       paged,
            'total':      total,
            'page':       page,
            'page_size':  page_size,
            'categories': all_cats,
        })

    try:
        conn = _get_conn()
        cur  = conn.cursor()

        # 动态拼接 WHERE 条件
        where_clauses = ['1=1']
        params        = {}
        if title:
            where_clauses.append("TITLE LIKE :title")
            params['title'] = f'%{title}%'
        if category:
            where_clauses.append("CATEGORY = :category")
            params['category'] = category
        if month:
            # month 格式 YYYY-MM → 转为月份首日和末日
            where_clauses.append("TO_CHAR(NEWS_DATE, 'YYYY-MM') = :month")
            params['month'] = month

        where_sql = ' AND '.join(where_clauses)

        # 总数
        cur.execute(f"SELECT COUNT(*) FROM CUSTGROUP.AIPC_DAILY_NEWS WHERE {where_sql}", params)
        total = cur.fetchone()[0]

        # 分页数据
        offset = (page - 1) * page_size
        cur.execute(f"""
            SELECT NEWS_ID, TITLE, CATEGORY, LINK, TO_CHAR(NEWS_DATE, 'YYYY-MM-DD')
            FROM CUSTGROUP.AIPC_DAILY_NEWS
            WHERE {where_sql}
            ORDER BY NEWS_DATE DESC, NEWS_ID DESC
            OFFSET :offset ROWS FETCH NEXT :page_size ROWS ONLY
        """, {**params, 'offset': offset, 'page_size': page_size})
        rows = cur.fetchall()

        # 所有分类（用于下拉选项）
        cur.execute("SELECT DISTINCT CATEGORY FROM CUSTGROUP.AIPC_DAILY_NEWS ORDER BY CATEGORY")
        all_cats = [r[0] for r in cur.fetchall()]

        conn.close()
        news = [
            {'id': r[0], 'title': r[1], 'category': r[2], 'link': r[3], 'date': r[4]}
            for r in rows
        ]
        return jsonify({
            'news':       news,
            'total':      total,
            'page':       page,
            'page_size':  page_size,
            'categories': all_cats,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
