# AI 展业平台 — 接口设计文档

> **Base URL**：`http://localhost:5000/api`
> **格式**：JSON，响应统一包含 `code`（200=成功，4xx/5xx=错误）、`msg`、`data` 三个字段（部分旧接口仅返回 data 对象本身，见各节说明）。
> **Mock 模式**：设置环境变量 `MOCK_MODE=true` 启动后端，所有接口返回内存仿真数据，不连接 Oracle，写操作在进程内生效。

---

## 目录

1. [管理端 — 客户列表](#1-管理端--客户列表)
2. [管理端 — 员工负载与搜索](#2-管理端--员工负载与搜索)
3. [管理端 — 客户分配](#3-管理端--客户分配)
4. [管理端 — 每日提醒](#4-管理端--每日提醒)
5. [营销端 — 我的客户列表](#5-营销端--我的客户列表)
6. [营销端 — 工作台总览](#6-营销端--工作台总览)
7. [营销端 — 每日资讯](#7-营销端--每日资讯)
8. [营销端 — 任务](#8-营销端--任务)
9. [数据库表说明](#9-数据库表说明)
10. [通用字段枚举](#10-通用字段枚举)

---

## 1. 管理端 — 客户列表

### 1.1 GET `/manager/customers` — 客户列表

分页查询当前营业部所有客户，支持多维筛选。

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `page` | int | 否 | 页码，默认 1 |
| `page_size` | int | 否 | 每页条数，默认 20，上限 100 |
| `keyword` | string | 否 | 关键词，模糊匹配姓名/资金账号/手机号 |
| `assign_status` | string | 否 | `已分配` \| `未分配` |
| `asset_level` | string | 否 | `高价值` \| `中等价值` \| `低价值` |
| `contact_status` | string | 否 | `已认证` \| `未添加或未绑定` |
| `follow_status` | string | 否 | 见[跟进状态枚举](#follow_status) |
| `risk_level` | string | 否 | 见[风险等级枚举](#risk_level) |
| `hdly` | string | 否 | 开户渠道号，与 `hdly-options` 接口返回值对齐 |

**响应示例**

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "total": 286,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "fund_account":   "C10001",
        "cust_name":      "张三",
        "phone":          "138****6789",
        "t1_aum":         128.50,
        "asset_level":    "高价值",
        "risk_level":     "R3 平衡型",
        "contact_status": "已认证",
        "follow_status":  "近7日内联系过",
        "hdly":           "渠道A",
        "assignee_nm":    "李经理",
        "assign_time":    "2025-04-10 09:30",
        "operator_nm":    "王主管",
        "assign_source":  1
      }
    ]
  }
}
```

**字段说明**

| 字段 | 说明 |
|------|------|
| `t1_aum` | T-1日净资产，单位**万元** |
| `assign_source` | `0`=外部导入（不可撤回），`1`=手动/智能分配（可撤回），`null`=未分配 |
| `cust_name` | 管理端不脱敏返回客户姓名 |
| `phone` | 手机号脱敏，格式 `138****6789` |

---

### 1.2 GET `/manager/customers/hdly-options` — 开户渠道号选项

返回当前营业部所有客户的开户渠道号去重列表，供「客户来源」下拉框使用。

**响应示例**

```json
{
  "code": 200,
  "msg": "success",
  "data": ["互联网渠道", "营业厅渠道", "银行合作渠道"]
}
```

---

## 2. 管理端 — 员工负载与搜索

### 2.1 GET `/manager/employees/workload` — 员工负载列表

返回当前营业部全量员工负载，按客户数从高到低排序。用于侧边栏「员工负载分布」和分配弹窗初始化。

**响应示例**

```json
{
  "code": 200,
  "msg": "success",
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
```

**负载等级计算规则**

分位值按营业部内员工客户数从高到低排序（分位=0 代表负载最重）：

| 分位区间 | 负载等级 |
|---------|---------|
| [0.0, 0.2) | 高负载 |
| [0.2, 0.4) | 偏高 |
| [0.4, 0.6) | 适中 |
| [0.6, 0.8) | 偏低 |
| [0.8, 1.0] | 空闲 |

---

### 2.2 GET `/manager/employees/search` — 员工搜索

按姓名或 OA 号模糊搜索，返回匹配员工及其实时负载信息。

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `q` | string | 是 | 员工姓名或 OA 号，至少 1 个字符 |

**响应示例**

```json
{
  "code": 200,
  "msg": "success",
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
```

---

## 3. 管理端 — 客户分配

### 3.1 POST `/manager/customers/assign` — 手动分配

将指定客户分配给目标员工。

**Request Body**

```json
{
  "client_ids": ["C10024", "C10089"],
  "login_id":   "zhangsan",
  "emp_name":   "张三"
}
```

**前置校验**

- 客户已被手动/智能分配（`assign_source=1`）→ 返回 409，冲突列表放入 `blocked_manual`
- 客户为外部导入（`assign_source=0`）→ 返回 409，冲突列表放入 `blocked_rln`

**成功响应（200）**

```json
{
  "code": 200,
  "msg": "分配成功",
  "data": {
    "assigned": ["C10024", "C10089"]
  }
}
```

**冲突响应（409）**

```json
{
  "code": 409,
  "msg": "部分客户存在分配冲突，无法分配",
  "data": {
    "blocked_manual": ["C10024"],
    "blocked_rln":    [],
    "assignable":     ["C10089"]
  }
}
```

---

### 3.2 POST `/manager/customers/revoke` — 撤回分配

撤回客户分配关系，仅限 `assign_source=1`（手动/智能分配）的客户可操作。

**Request Body**

```json
{
  "client_ids": ["C10024", "C10089"]
}
```

**成功响应（200）**

```json
{
  "code": 200,
  "msg": "撤回成功",
  "data": {
    "revoked": ["C10024", "C10089"]
  }
}
```

**冲突响应（409）**

```json
{
  "code": 409,
  "msg": "部分客户不支持撤回，仅限手动分配的客户可撤回",
  "data": {
    "rejected": ["C10089"]
  }
}
```

---

### 3.3 POST `/manager/customers/smart-assign` — 智能分配

使用分层负载均衡算法，将客户自动分配给候选员工池。

**算法说明**

1. 按资产等级（高价值/中等价值/低价值）将客户分为三层
2. 按各员工当前客户数的反比计算权重，确定每人配额
3. 在各员工配额内，按全局层比例分配各层客户
4. 整除余量补给负载最轻的员工

**Request Body**

```json
{
  "client_ids":   ["C10024", "C10089", "C10101"],
  "employee_ids": ["zhangsan", "lisi"]
}
```

至少需要 2 位候选员工，`employee_ids` 少于 2 时返回 400。

**成功响应（200）**

```json
{
  "code": 200,
  "msg": "智能分配成功",
  "data": {
    "plan": [
      {
        "login_id":   "zhangsan",
        "emp_name":   "张三",
        "client_ids": ["C10024", "C10101"],
        "count":      2
      },
      {
        "login_id":   "lisi",
        "emp_name":   "李四",
        "client_ids": ["C10089"],
        "count":      1
      }
    ]
  }
}
```

---

## 4. 管理端 — 每日提醒

### 4.1 GET `/manager/alerts` — 获取提醒列表

返回指定员工近 30 天内所有未完成的提醒，按日期倒序排列。

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `login_id` | string | 是 | 员工 OA 号 |

**响应示例**

```json
{
  "code": 200,
  "data": [
    {
      "alert_id":      1,
      "employee_id":   "oa001",
      "alert_content": "跟进高净值客户 张伟，近7日未回访",
      "alert_date":    "2026-05-29",
      "is_done":       0
    }
  ]
}
```

---

### 4.2 POST `/manager/alerts` — 新增提醒

新增一条提醒，同时自动清理该员工 30 天前的旧记录。

**Request Body**

```json
{
  "login_id":      "oa001",
  "alert_content": "本月末佣金达标检查，核实低频客户持仓"
}
```

`alert_content` 最长 500 字，超出返回 400。

**成功响应（200）**

```json
{
  "code": 200,
  "data": {
    "alert_id":      4,
    "employee_id":   "oa001",
    "alert_content": "本月末佣金达标检查，核实低频客户持仓",
    "alert_date":    "2026-05-29",
    "is_done":       0
  }
}
```

---

### 4.3 PATCH `/manager/alerts/<alert_id>/done` — 标记提醒已完成

**路径参数**：`alert_id` — 提醒 ID（整数）

**成功响应（200）**

```json
{
  "code": 200,
  "data": { "alert_id": 1 }
}
```

提醒不存在时返回 404。

---

## 5. 营销端 — 我的客户列表

### 5.1 GET `/staff/customers` — 我的客户列表

查询当前员工名下的客户，支持多维筛选和多字段排序。

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `login_id` | string | 是 | 当前员工 OA 号 |
| `page` | int | 否 | 页码，默认 1 |
| `page_size` | int | 否 | 每页条数，默认 20，上限 200 |
| `keyword` | string | 否 | 模糊匹配姓名/资金账号 |
| `contact_status` | string | 否 | `已认证` \| `未添加或未绑定` |
| `asset_level` | string | 否 | `高价值` \| `中等价值` \| `低价值` |
| `follow_status` | string | 否 | 见[跟进状态枚举](#follow_status) |
| `risk_level` | string | 否 | 见[风险等级枚举](#risk_level) |
| `sort_field` | string | 否 | 排序字段，见下表，默认 `t1_aum` |
| `sort_dir` | string | 否 | `asc` \| `desc`，默认 `desc` |

**可排序字段**

`t1_aum` / `age` / `open_date` / `annual_return` / `commission_this_year` / `commission_last_year` / `commission_rate` / `trade_exp_months`

**响应示例**

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "total": 48,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "fund_account":          "C10001",
        "cust_name":             "张三",
        "phone":                 "138****6789",
        "gender":                "男",
        "age":                   45,
        "open_date":             "2019-03-15",
        "trade_exp_months":      86,
        "relation_type":         "存量客户",
        "contact_status":        "已认证",
        "follow_status":         "近7日内联系过",
        "t1_aum":                128.50,
        "aum_change_pct":        2.3,
        "asset_level":           "高价值",
        "risk_level":            "R3 平衡型",
        "hdly":                  "互联网渠道",
        "annual_return":         12300.00,
        "commission_this_year":  4560.00,
        "commission_last_year":  8900.00,
        "commission_rate":       0.00025,
        "assignee_nm":           "李经理",
        "remark":                null
      }
    ]
  }
}
```

**字段说明**

| 字段 | 说明 |
|------|------|
| `t1_aum` | T-1日净资产，单位**万元** |
| `aum_change_pct` | AUM 月变化率（%），当月最新日 vs 上月最新日，保留 1 位小数 |
| `trade_exp_months` | 交易经验月数，由开户日期前端/后端计算至今 |
| `annual_return` | 本年收益，单位元 |
| `commission_this_year` | 本年佣金，单位元 |
| `commission_last_year` | 去年佣金，单位元 |
| `commission_rate` | 佣金费率（小数，如 0.00025） |
| `remark` | 分配时的备注，格式：`分配备注："XXX"` |

---

## 6. 营销端 — 工作台总览

### 6.1 GET `/staff/overview` — 工作台总览数据

返回 AUM 月净增卡、今日外呼卡、任务进度卡三块数据。

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `login_id` | string | 是 | 当前员工 OA 号 |

**响应示例**

```json
{
  "aum_card": {
    "current_aum":       15230000.0,
    "last_month_aum":    14800000.0,
    "net_increase":        430000.0,
    "net_increase_rate":      2.91,
    "display_increase":    "43.0万"
  },
  "call_card": {
    "connected":    56,
    "total":        89,
    "wechat_add":   24,
    "bound":        12,
    "bound_total": 1248,
    "intention":     8
  },
  "task_card": {
    "todo":    25,
    "done":    16,
    "overdue":  3,
    "rate":    64
  }
}
```

**字段说明**

| 字段 | 说明 |
|------|------|
| `current_aum` / `last_month_aum` / `net_increase` | 单位**元** |
| `net_increase_rate` | 月净增率（%） |
| `display_increase` | 前端展示用净增额，已转万元 |
| `wechat_add` / `bound` / `intention` | 加微/绑定/意向，真实环境暂无数据表，返回 `null` |
| `rate` | 任务完成率（%） |

> 注：此接口响应直接返回数据对象，不包裹标准 `code/msg/data` 结构（历史兼容）。

---

## 7. 营销端 — 每日资讯

### 7.1 GET `/staff/news/today` — 今日资讯（首页 Banner）

返回今日最新资讯，最多 5 条，用于工作台首页轮播 Banner。

**响应示例**

```json
{
  "news": [
    {
      "id":       1,
      "title":    "央行发布二季度货币政策报告，稳息基调不变",
      "category": "市场",
      "link":     null
    }
  ]
}
```

---

### 7.2 GET `/staff/news` — 资讯列表（弹窗用）

支持按标题、分类、月份筛选和分页，用于「每日资讯」弹窗页面。

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 否 | 标题关键词，模糊搜索 |
| `category` | string | 否 | 分类精确过滤，如 `市场`、`政策` |
| `month` | string | 否 | 年月过滤，格式 `YYYY-MM` |
| `page` | int | 否 | 页码，默认 1 |
| `page_size` | int | 否 | 每页条数，默认 20，上限 100 |

**响应示例**

```json
{
  "news": [
    {
      "id":       1,
      "title":    "央行发布二季度货币政策报告，稳息基调不变",
      "category": "市场",
      "link":     null,
      "date":     "2026-05-29"
    }
  ],
  "total":      12,
  "page":        1,
  "page_size":  20,
  "categories": ["产品", "宏观", "市场", "政策"]
}
```

---

## 8. 营销端 — 任务

### 8.1 GET `/staff/tasks/urgent-summary` — 今日高优任务聚合

返回今日高优（`priority=高`）且未完成（`status` 为 `待处理` 或 `处理中`）的任务，按分类聚合汇总，用于工作台「高优任务快速入口」区块。

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `login_id` | string | 是 | 当前员工 OA 号 |

**响应示例**

```json
{
  "total": 6,
  "summary": [
    { "task_type": "跟进类",     "count": 2, "earliest_due": "10:00" },
    { "task_type": "建联类",     "count": 1, "earliest_due": "12:00" },
    { "task_type": "合规类",     "count": 1, "earliest_due": "17:00" },
    { "task_type": "周期类",     "count": 1, "earliest_due": "今日"  },
    { "task_type": "营销活动类", "count": 1, "earliest_due": "2026-06-04" }
  ]
}
```

**`earliest_due` 格式规则**

- 当日有明确截止时分 → `HH:MM`
- 当日到期但无截止时分 → `今日`
- 跨日到期 → `YYYY-MM-DD`

结果按截止紧迫度升序排列（`HH:MM` > `今日` > 日期）。

---

### 8.2 GET `/staff/tasks` — 任务列表（任务大厅用）

分页查询任务，支持按分类和状态过滤。

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `login_id` | string | 是 | 当前员工 OA 号 |
| `task_type` | string | 否 | 一级分类过滤：`建联类`/`跟进类`/`周期类`/`营销活动类`/`合规类` |
| `status` | string | 否 | 状态过滤：`待处理`/`处理中`/`已完成`/`已关闭` |
| `page` | int | 否 | 页码，默认 1 |
| `page_size` | int | 否 | 每页条数，默认 20，上限 100 |

**响应示例**

```json
{
  "tasks": [
    {
      "id":            1,
      "task_type":     "跟进类",
      "task_sub_type": "意向跟进",
      "task_name":     "意向客户跟进",
      "priority":      "高",
      "source":        "系统自动",
      "issue_date":    "2026-05-29",
      "due_date":      "2026-05-29",
      "due_time":      "10:00",
      "status":        "待处理",
      "finish_date":   null,
      "cust_no":       "C001001",
      "cust_name":     "王*明"
    }
  ],
  "total":     20,
  "page":       1,
  "page_size": 20
}
```

**字段说明**

| 字段 | 说明 |
|------|------|
| `task_sub_type` | 任务子类型，如「意向跟进」「AI外呼」「流失预警」等 |
| `source` | 任务来源：`系统自动` \| `主管下发` |
| `due_time` | 当日截止时分（`HH:MM`），无精确时分时为 `null` |
| `cust_no` / `cust_name` | 营销活动类/合规类无关联客户时为 `null` |
| `cust_name` | DB 模式下脱敏（第2字替换为 `*`）；Mock 模式同样脱敏 |

**真实 DB 排序规则**：`priority` 优先级（高→中→低）+ `due_date` 升序。

---

## 9. 数据库表说明

| 表名 | Schema | 用途 |
|------|--------|------|
| `T_CLIENT_INFO` | `custgroup` | 客户基础信息（姓名、手机、性别、年龄、开户日期） |
| `T_CUSTOMER_ASSIGN_REL` | `custgroup` | 客户分配关系（归属员工、分配时间、来源） |
| `T_CUSTOMER_ASSIGN_LOG` | `custgroup` | 分配操作流水（分配/撤回历史记录） |
| `T_EMP_WORKLOAD` | `custgroup` | 员工负载快照（客户数、分位值、负载等级） |
| `T_CALL_LOG` | `custgroup` | 外呼流水（通话时间、接通结果） |
| `AIPC_MAN_ALERT` | `custgroup` | 管理端每日提醒 |
| `AIPC_STAFF_TASK` | `custgroup` | 营销端任务表 |
| `AIPC_DAILY_NEWS` | `custgroup` | 每日资讯 |
| `T_DDW_F20_D_CUST_AUM_BD` | `DDW_PROD` | 客户日 AUM（按 `BIZ_DT` 分区） |
| `T_DDW_F21_C_Y_AST_PRFT` | `DDW_PROD` | 客户年度收益 |
| `T_DDW_F11_C_Y_INCM_AGGR` | `DDW_PROD` | 客户年度佣金 |
| `T_DDW_F22_C_Y_KH360` | `DDW_PROD` | 客户佣金费率 |
| `T_DDW_F22_LCSC_CUST_RLN` | `DDW_PROD` | 客户关系类型 |
| `t_ddw_f27_c_bsc_inf` | `DDW_PROD` | 客户开户渠道（HDLY） |
| `T_S01_EHT_CIM_T_EHT_ACCOU_BIND` | `S01_PROD` | 企微绑定记录（建联状态来源） |
| `clientprefer` | `hs_asset` | 客户风险测评结果 |
| `t_edw_t01_sim_new_cust_tab` | `EDW_PROD` | 员工主表 |

---

## 10. 通用字段枚举

### `follow_status` — 跟进状态 {#follow_status}

基于最近一次外呼距今天数计算：

| 值 | 说明 |
|----|------|
| `近3日内联系过` | 最近外呼 ≤ 3 天 |
| `近7日内联系过` | 最近外呼 4–7 天 |
| `近15日内联系过` | 最近外呼 8–15 天 |
| `近30日内联系过` | 最近外呼 16–30 天 |
| `未联系` | 超过 30 天或无外呼记录 |

### `risk_level` — 风险等级 {#risk_level}

来自 `hs_asset.clientprefer.corp_risk_level`，经 `utils/formatters.py` 的 `_RISK_MAP` 映射：

`R1 保守型` / `R2 谨慎型` / `R3 平衡型` / `R4 积极型` / `R5 进取型` / `未测评`

> 上线前需与实际数据库编码核对 `_RISK_MAP` 映射关系。

### `asset_level` — 资产等级

基于 `t1_aum`（万元）计算：

| 阈值 | 等级 |
|------|------|
| ≥ 100 万 | 高价值 |
| ≥ 10 万 | 中等价值 |
| < 10 万 | 低价值 |

### `priority` — 任务优先级

`高` / `中` / `低`

> 仅优先级为**低**的任务可由 AI 代劳处理，前端对非低优先级任务禁用「AI处理」按钮。

### 通用错误码

| code | 含义 |
|------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 409 | 业务冲突（分配冲突、不可撤回等） |
| 500 | 服务器内部错误 |
