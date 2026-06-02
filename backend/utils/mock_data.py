"""
本地开发 Mock 数据
仅在 MOCK_MODE=true 时使用，数据结构与真实接口返回完全一致
"""
import random
from datetime import datetime, timedelta, date

# ------------------------------------------------------------------ #
#  仿真数据生成
# ------------------------------------------------------------------ #

_SURNAMES = ["张", "王", "李", "赵", "陈", "刘", "杨", "吴", "周", "徐",
             "孙", "马", "朱", "胡", "林", "郭", "何", "高", "罗", "郑"]
_GIVEN    = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军",
             "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞"]

_RISK_LEVELS     = ["R1 保守型", "R2 稳健型", "R3 平衡型", "R4 进取型", "R5 激进型", "未测评"]
_HDLY_OPTIONS    = ["官网自主开户", "渠道合作-A", "渠道合作-B", "线下营业部", "APP推荐码"]
_GENDERS         = ["男", "女"]
_RELATION_TYPES  = ["核心客户", "存量客户", "新开户", "低频客户", "流失预警"]
_ASSIGN_NOTES    = [None, None, None, None,
                    "高净值，优先维护", "近期有入金意愿，及时跟进",
                    "连续30天未回访，需主动触达", "节假日关怀重点客户"]
# 与 _MOCK_EMPLOYEES 名字完全一致，确保 _recalc_mock_employee_counts 可以正确匹配
_OPERATORS     = [
    ("oa001", "赵经理"), ("oa002", "钱主任"), ("oa003", "周明华"),
    ("oa004", "王涛"),   ("oa005", "李明晨"), ("oa006", "陈梅云"),
    ("oa007", "刘至"),   ("oa008", "孙志远"),
]

_FOLLOW_RESULTS = {
    "未跟进": None,
    "已接通": "接通",
    "未接通": "未接",
}


def _rand_phone():
    prefixes = ["138", "139", "155", "186", "177", "150", "181"]
    return random.choice(prefixes) + str(random.randint(10000000, 99999999))


def _rand_name():
    return random.choice(_SURNAMES) + random.choice(_GIVEN)


def _rand_date(days_back=180):
    base = datetime.now() - timedelta(days=days_back)
    return base + timedelta(days=random.randint(0, days_back))


def _months_since(dt: datetime) -> int:
    """计算从 dt 到今天的完整月数"""
    now = datetime.now()
    return max(0, (now.year - dt.year) * 12 + (now.month - dt.month))


def _mask_name(name):
    if len(name) <= 1:
        return name
    return name[0] + "*" * (len(name) - 1)


def _mask_phone(phone):
    return phone[:3] + "****" + phone[-4:]


def _aum_for_level(level):
    if level == "高价值":
        return round(random.uniform(50, 500), 2)
    if level == "中等价值":
        return round(random.uniform(10, 49.99), 2)
    return round(random.uniform(0.1, 9.99), 2)


def build_mock_customers(seed=42) -> list:
    """
    生成 60 条仿真客户记录，各枚举值均匀覆盖。
    seed 固定，每次进程内数据相同（方便前端分页测试）。
    """
    random.seed(seed)
    records = []

    # 分布策略：高/中/低价值各 20 条
    asset_dist = ["高价值"] * 20 + ["中等价值"] * 20 + ["低价值"] * 20
    # 建联状态：40 已认证 + 20 未绑定
    contact_dist = ["已认证"] * 40 + ["未添加或未绑定"] * 20
    # 跟进状态：5档各 12 条
    follow_dist = (["未联系"] * 12 + ["近3日内联系过"] * 12 +
                   ["近7日内联系过"] * 12 + ["近15日内联系过"] * 12 +
                   ["近30日内联系过"] * 12)
    # 归属状态：40 已分配 + 20 未分配
    assign_dist = [True] * 40 + [False] * 20

    random.shuffle(asset_dist)
    random.shuffle(contact_dist)
    random.shuffle(follow_dist)
    random.shuffle(assign_dist)

    for i in range(60):
        fund_account = f"29100{10001 + i}"
        raw_name     = _rand_name()
        raw_phone    = _rand_phone()
        asset_level  = asset_dist[i]
        aum_wan      = _aum_for_level(asset_level)
        risk_level   = random.choice(_RISK_LEVELS)
        contact_st   = contact_dist[i]
        follow_st    = follow_dist[i]
        hdly         = random.choice(_HDLY_OPTIONS)
        is_assigned  = assign_dist[i]

        # ── 基础信息 ──────────────────────────────────────────────
        gender          = random.choice(_GENDERS)
        age             = random.randint(22, 68)
        open_dt         = _rand_date(365 * 9)        # 0-9 年前开户
        open_date_str   = open_dt.strftime("%Y-%m-%d")
        trade_exp_months = _months_since(open_dt)
        relation_type   = random.choice(_RELATION_TYPES)

        # ── 资产变化 ──────────────────────────────────────────────
        aum_change_pct  = round(random.uniform(-12.0, 20.0), 1)

        # ── 收益 & 佣金（与 AUM 档位正相关）─────────────────────
        base_aum_yuan   = aum_wan * 10000
        annual_return   = round(base_aum_yuan * random.uniform(-0.08, 0.22), 2)
        commission_this = round(base_aum_yuan * random.uniform(0.0004, 0.0010), 2)
        commission_last = round(commission_this * random.uniform(0.7, 1.35), 2)
        commission_rate = round(random.uniform(0.00030, 0.00120), 5)

        # ── 分配信息 ──────────────────────────────────────────────
        assign_info  = {}
        assign_note  = None
        if is_assigned:
            op_oa, op_nm   = random.choice(_OPERATORS)
            emp_oa, emp_nm = random.choice(_OPERATORS)
            assign_time    = _rand_date(90).strftime("%Y-%m-%d %H:%M")
            assign_source  = random.choice([0, 1])
            assign_note    = random.choice(_ASSIGN_NOTES)
            assign_info = {
                "assignee_nm":   emp_nm,
                "assign_time":   assign_time,
                "operator_nm":   op_nm,
                "assign_source": assign_source,
            }

        # remark：有分配备注时格式化展示
        remark = f'分配备注："{assign_note}"' if assign_note else None

        records.append({
            # ── 基础标识 ──
            "fund_account":        fund_account,
            "cust_name":           raw_name,
            "phone":               _mask_phone(raw_phone),
            # ── 客户基础信息 ──
            "gender":              gender,
            "age":                 age,
            "open_date":           open_date_str,
            "trade_exp_months":    trade_exp_months,
            "relation_type":       relation_type,
            # ── 资产 ──
            "t1_aum":              aum_wan,
            "aum_change_pct":      aum_change_pct,
            "asset_level":         asset_level,
            # ── 风险 & 建联 & 跟进 ──
            "risk_level":          risk_level,
            "contact_status":      contact_st,
            "follow_status":       follow_st,
            # ── 渠道 ──
            "hdly":                hdly,
            # ── 收益 & 佣金 ──
            "annual_return":       annual_return,
            "commission_this_year": commission_this,
            "commission_last_year": commission_last,
            "commission_rate":     commission_rate,
            # ── 备注 ──
            "remark":              remark,
            # ── 分配信息 ──
            "assignee_nm":         assign_info.get("assignee_nm"),
            "assign_time":         assign_info.get("assign_time"),
            "operator_nm":         assign_info.get("operator_nm"),
            "assign_source":       assign_info.get("assign_source"),
            # 供关键词搜索用的原始字段（不返回给前端）
            "_raw_name":   raw_name,
            "_raw_phone":  raw_phone,
        })

    return records


# 进程内缓存，避免重复生成
_MOCK_CUSTOMERS = None


def get_mock_customers() -> list:
    global _MOCK_CUSTOMERS
    if _MOCK_CUSTOMERS is None:
        _MOCK_CUSTOMERS = build_mock_customers()
        _recalc_mock_employee_counts()   # 用真实分配数据初始化员工客户数
    return _MOCK_CUSTOMERS


# ------------------------------------------------------------------ #
#  Mock 员工数据
# ------------------------------------------------------------------ #

# cust_count 初始为 0，启动后由 _recalc_mock_employee_counts() 根据实际 mock 客户计算
_MOCK_EMPLOYEES = [
    {"login_id": "oa001", "emp_name": "赵经理", "cust_count": 0, "load_level": "空闲", "percentile": 0.0},
    {"login_id": "oa002", "emp_name": "钱主任", "cust_count": 0, "load_level": "空闲", "percentile": 0.0},
    {"login_id": "oa003", "emp_name": "周明华", "cust_count": 0, "load_level": "空闲", "percentile": 0.0},
    {"login_id": "oa004", "emp_name": "王涛",   "cust_count": 0, "load_level": "空闲", "percentile": 0.0},
    {"login_id": "oa005", "emp_name": "李明晨", "cust_count": 0, "load_level": "空闲", "percentile": 0.0},
    {"login_id": "oa006", "emp_name": "陈梅云", "cust_count": 0, "load_level": "空闲", "percentile": 0.0},
    {"login_id": "oa007", "emp_name": "刘至",   "cust_count": 0, "load_level": "空闲", "percentile": 0.0},
    {"login_id": "oa008", "emp_name": "孙志远", "cust_count": 0, "load_level": "空闲", "percentile": 0.0},
]


def _count_to_load_level(count: int, max_count: int) -> str:
    """根据客户数和最大值动态计算负载档位"""
    if max_count == 0 or count == 0:
        return "空闲"
    ratio = count / max_count
    if ratio >= 0.8:
        return "高负载"
    if ratio >= 0.6:
        return "偏高"
    if ratio >= 0.3:
        return "适中"
    if ratio > 0:
        return "偏低"
    return "空闲"


def get_mock_employees() -> list:
    """员工负载列表 Mock，按客户数从高到低排序"""
    return _MOCK_EMPLOYEES


# ------------------------------------------------------------------ #
#  Mock 写操作（分配 / 撤回）
# ------------------------------------------------------------------ #

def mock_assign_customers(client_ids: list, login_id: str, emp_name: str,
                           op_emp_name: str = "陈经理") -> dict:
    """
    Mock 手动分配：在内存中更新客户归属字段。
    返回 {"assigned": [...], "blocked_manual": [], "blocked_rln": []}
    """
    customers = get_mock_customers()
    index = {c["fund_account"]: c for c in customers}

    blocked_manual = []
    blocked_rln    = []
    assigned       = []
    now_str        = datetime.now().strftime("%Y-%m-%d %H:%M")

    for cid in client_ids:
        c = index.get(cid)
        if c is None:
            continue
        # 已有归属关系时拦截（与真实接口行为一致）
        if c["assignee_nm"] is not None:
            if c["assign_source"] == 0:
                blocked_rln.append(cid)
            else:
                blocked_manual.append(cid)
            continue
        # 写入归属信息
        c["assignee_nm"]   = emp_name
        c["assign_time"]   = now_str
        c["operator_nm"]   = op_emp_name
        c["assign_source"] = 1
        assigned.append(cid)

    # 更新员工客户数
    _recalc_mock_employee_counts()

    return {"assigned": assigned, "blocked_manual": blocked_manual, "blocked_rln": blocked_rln}


def mock_revoke_customers(client_ids: list) -> dict:
    """
    Mock 撤回：只允许撤回 assign_source=1 的记录。
    """
    customers = get_mock_customers()
    index = {c["fund_account"]: c for c in customers}

    rejected = []
    revoked  = []

    for cid in client_ids:
        c = index.get(cid)
        if c is None or c.get("assign_source") != 1:
            rejected.append(cid)
            continue
        c["assignee_nm"]   = None
        c["assign_time"]   = None
        c["operator_nm"]   = None
        c["assign_source"] = None
        revoked.append(cid)

    _recalc_mock_employee_counts()
    return {"revoked": revoked, "rejected": rejected}


def _recalc_mock_employee_counts():
    """重算 Mock 员工客户数、负载档位和百分位（分配/撤回后调用）"""
    customers = get_mock_customers()
    counts: dict[str, int] = {}
    for c in customers:
        if c["assignee_nm"]:
            for emp in _MOCK_EMPLOYEES:
                if emp["emp_name"] == c["assignee_nm"]:
                    counts[emp["login_id"]] = counts.get(emp["login_id"], 0) + 1
                    break

    # 更新客户数（无匹配的归零，不保留旧值）
    for emp in _MOCK_EMPLOYEES:
        emp["cust_count"] = counts.get(emp["login_id"], 0)

    # 动态计算负载档位和百分位
    max_count = max((e["cust_count"] for e in _MOCK_EMPLOYEES), default=0)
    sorted_counts = sorted(e["cust_count"] for e in _MOCK_EMPLOYEES)
    for emp in _MOCK_EMPLOYEES:
        emp["load_level"] = _count_to_load_level(emp["cust_count"], max_count)
        rank = sorted_counts.index(emp["cust_count"])
        emp["percentile"] = round(rank / max(len(_MOCK_EMPLOYEES) - 1, 1), 3)
