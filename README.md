# AI 展业平台

面向营销人员与管理人员的 AI 驱动展业工具，集成客户管理、智能任务调度、标准化 SOP、批量外呼、绩效看板等核心模块。

---

## 技术栈

### 前端

| 类别 | 技术 |
|------|------|
| 框架 | Vue 3 (Composition API / `<script setup>`) |
| 路由 | Vue Router 4 |
| 构建工具 | Vite 5 |
| 图表库 | ECharts 6 |
| CSS 框架 | Tailwind CSS |
| 图标 | Iconify Web Components |

### 后端

| 类别 | 技术 |
|------|------|
| 框架 | Python 3.9+ / Flask 3 |
| 跨域 | flask-cors |
| 数据库驱动 | cx_Oracle 8 |
| 配置管理 | python-dotenv |

---

## 环境要求

| 环境 | 版本要求 |
|------|----------|
| Node.js | ≥ 18.0（推荐 20 LTS） |
| npm | ≥ 9.0 |
| Python | ≥ 3.9（推荐 3.11+） |
| Oracle Client | 与 cx_Oracle 版本匹配（建议 19c） |

---

## 启动方式

### 前端

```bash
# 安装依赖
npm install

# 启动开发服务器（默认 http://localhost:3000）
npm run dev

# 构建生产包，输出至 dist/
npm run build
```

### 后端

```bash
cd backend
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置数据库连接
cp .env.example .env
# 编辑 .env，填写 ORACLE_HOST / ORACLE_USER / ORACLE_PASSWORD 等

# 启动开发服务器（默认 http://localhost:5000）
python app.py
```

本地调试无需 Oracle，启用 Mock 模式：

```bash
MOCK_MODE=true python app.py
```

生产环境（Gunicorn）：

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

---

## 项目结构

```
Project/
├── backend/
│   ├── app.py                      # Flask 工厂函数 + 入口
│   ├── config.py                   # 环境变量配置
│   ├── requirements.txt
│   ├── .env.example
│   ├── api/
│   │   ├── __init__.py             # Blueprint 注册
│   │   ├── manager_customers.py    # 管理端：客户列表 + 分配管理
│   │   ├── manager_assign.py       # 管理端：分配 / 撤回 / 智能分配
│   │   ├── manager_alerts.py       # 管理端：每日提醒
│   │   ├── staff_customers.py      # 营销端：我的客户列表
│   │   ├── staff_overview.py       # 营销端：工作台总览数据
│   │   ├── staff_news.py           # 营销端：每日营销资讯
│   │   └── staff_tasks.py          # 营销端：任务数据
│   └── utils/
│       ├── __init__.py
│       └── formatters.py           # 脱敏 / 分级等工具函数
│
├── src/
│   ├── views/
│   │   ├── Index.vue               # 工作台总览（营销人员）
│   │   ├── Tasks.vue               # 任务大厅（营销人员）
│   │   ├── Business.vue            # 展业大厅（营销人员）
│   │   ├── Performance.vue         # 业绩看板（营销人员）
│   │   ├── ManagerDashboard.vue    # 首页大厅（管理人员）
│   │   └── ManagerCustomers.vue    # 客户分配管理（管理人员）
│   ├── router/
│   │   └── index.js
│   ├── App.vue
│   └── main.js
│
├── index.html
├── vite.config.js
├── package.json
├── README.md
└── API_DOC.md                      # 接口设计文档
```

---

## 页面路由

| 角色 | 路径 | 页面 |
|------|------|------|
| 营销人员 | `/` | 工作台总览 |
| 营销人员 | `/tasks` | 任务大厅 |
| 营销人员 | `/business` | 展业大厅 |
| 营销人员 | `/performance` | 业绩看板 |
| 管理人员 | `/manager` | 首页大厅 |
| 管理人员 | `/manager/customers` | 客户分配管理 |

---

## 功能模块概览

### 营销人员端

#### 工作台总览 `/`
- 今日任务数、AUM、AI代劳数、外呼接通数等核心指标
- 高优任务快速入口（截止时间最近的前3条）
- 每日营销资讯（接口实时拉取）
- 每日提醒面板（增删、标记完成）

#### 任务大厅 `/tasks`
- Tab 分类：我的待办 / 建联类 / 跟进类 / 周期类 / 营销活动类 / 合规类 / 已完成已关闭 / AI批量任务中心
- Tab 徽标实时显示各类任务数量
- 筛选：关键词搜索（姓名/手机）、优先级、建联状态、任务来源、可AI代劳开关，支持一键重置
- 表格自动排序：优先级（高→中→低）+ 截止时间升序
- AI处理按钮：仅低优先级任务可用，其余灰显禁用
- 操作列：详情弹窗（任务信息 + AI摘要 + 推荐话术）、AI批量处理、去处理侧滑面板

#### 展业大厅 `/business`
- 我的客户列表：多维筛选（建联状态/资产等级/跟进状态/风险等级）自动联动，关键词实时搜索，10个排序字段，自定义表头（19个可选字段）
- 客户360°全景：从列表点击进入，展示客户基础信息（姓名、手机、归属人、开户时长、风险等级）+ 资产概览 + 行为雷达图 + AI摘要 + SOP推荐
- 其他 Tab：SOP流程 / 批量外呼 / AI问答 / 营销素材 / 产品中心 / 活动中心 / 企微配置 / AI批量处理

#### 业绩看板 `/performance`
- 业绩数据可视化

### 管理人员端

#### 首页大厅 `/manager`
- 团队概览、待办提醒

#### 客户分配管理 `/manager/customers`
- 多维筛选 + 关键词实时搜索（防抖300ms），下拉筛选自动联动，无需点击「筛选」按钮
- 手动分配：选客户 → 选员工 → 确认（已分配客户拒绝操作，返回冲突详情）
- 撤回分配：仅手动/智能分配的客户可撤回（外部导入不可操作）
- 智能分配：分层负载均衡算法，本地预览方案后确认执行
- 分配记录：月份切换 + 多条件筛选 + CSV导出
- 员工负载分布：分页展示，实时负载等级（高负载/偏高/适中/偏低/空闲）

---

## 注意事项

- **Mock 模式**：设置环境变量 `MOCK_MODE=true` 启动后端，所有接口返回仿真数据，不连接 Oracle，写操作在进程内存中生效，适合本地前端联调。
- **CDN 依赖**：Tailwind CSS 和 Iconify 通过 CDN 引入，需要网络连接，离线环境需替换为本地包。
- **Oracle Client**：运行后端前需在服务器安装对应版本的 Oracle Instant Client，版本需与 `cx_Oracle` 匹配。
- **环境变量安全**：`.env` 文件包含数据库密码，不要提交到 Git，已在 `.gitignore` 中排除。
- **AUM 单位**：后端统一以**万元**为单位返回，前端直接展示，无需二次换算。
- **风险等级映射**：后端 `utils/formatters.py` 中的 `_RISK_MAP` 基于 DB 编码映射，上线前需与实际数据库编码核对。
- **手机号脱敏**：后端统一脱敏（`138****6789`），前端不做额外处理。客户360页面展示脱敏后号码。
