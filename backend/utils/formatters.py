"""
数据格式化工具函数
"""


def mask_name(name: str) -> str:
    """
    姓名脱敏：保留姓，其余用 * 代替
      张三   -> 张*
      王大为 -> 王**
    """
    if not name or len(name) <= 1:
        return name or ""
    return name[0] + "*" * (len(name) - 1)


def mask_phone(phone: str) -> str:
    """
    手机号脱敏：保留前3位和后4位
      13812345678 -> 138****5678
    """
    if not phone or len(phone) != 11:
        return phone or ""
    return phone[:3] + "****" + phone[-4:]


def get_asset_level(aum_wan: float) -> str:
    """
    资产等级（入参单位：万元）
      < 10w  -> 低价值
      10-50w -> 中等价值
      >= 50w -> 高价值
    """
    v = float(aum_wan) if aum_wan else 0.0
    if v < 10:
        return "低价值"
    if v < 50:
        return "中等价值"
    return "高价值"


# DB 风险等级数字 → 前端展示文案
# ⚠️  当前映射基于原始代码中 4-8 的值，请与数据库实际编码核对后调整
_RISK_MAP = {
    4: "R1 保守型",
    5: "R2 稳健型",
    6: "R3 平衡型",
    7: "R4 进取型",
    8: "R5 激进型",
}


def get_risk_level(code) -> str:
    """风险等级数字转前端展示文案（R1-R5）"""
    if code is None:
        return "未测评"
    try:
        return _RISK_MAP.get(int(code), "未知")
    except (ValueError, TypeError):
        return "未知"
