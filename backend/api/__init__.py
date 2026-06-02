from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")

# 导入各模块路由，触发 @bp.route 注册
from . import manager_customers  # noqa: F401, E402
from . import manager_assign     # noqa: F401, E402
from . import staff_customers    # noqa: F401, E402
from . import manager_alerts     # noqa: F401, E402
from . import staff_overview     # noqa: F401, E402
from . import staff_news         # noqa: F401, E402
from . import staff_tasks        # noqa: F401, E402
