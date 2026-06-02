/**
 * API 客户端
 * 开发时通过 vite proxy 转发到 Flask 5000 端口
 * 生产时部署在同域下，无需修改
 */

const BASE = '/api'

async function request(url, options = {}) {
  const res = await fetch(BASE + url, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  const json = await res.json()
  if (!res.ok || json.code >= 400) {
    const err = new Error(json.msg || `HTTP ${res.status}`)
    err.data = json.data
    err.code = json.code
    throw err
  }
  return json
}

export const api = {
  // ── 客户列表 ──────────────────────────────────────────────────────────────
  /**
   * GET /api/manager/customers
   * params: { page, page_size, keyword, assign_status, asset_level,
   *           contact_status, follow_status, hdly, risk_level }
   */
  getCustomers(params = {}) {
    const q = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => {
      if (v !== null && v !== undefined && v !== '') q.set(k, v)
    })
    return request('/manager/customers?' + q.toString())
  },

  /** GET /api/manager/customers/hdly-options */
  getHdlyOptions() {
    return request('/manager/customers/hdly-options')
  },

  // ── 员工 ──────────────────────────────────────────────────────────────────
  /** GET /api/manager/employees/workload — 全量员工负载列表（侧边栏/分配弹窗使用） */
  getEmployeesWorkload() {
    return request('/manager/employees/workload')
  },

  /**
   * GET /api/manager/employees/search?q=xxx — 员工模糊搜索
   * 至少传 1 个字符
   */
  searchEmployees(q) {
    return request('/manager/employees/search?q=' + encodeURIComponent(q))
  },

  // ── 分配操作 ──────────────────────────────────────────────────────────────
  /**
   * POST /api/manager/customers/assign
   * body: { client_ids: [...], login_id: '...', emp_name: '...' }
   */
  assignCustomers(body) {
    return request('/manager/customers/assign', {
      method: 'POST',
      body: JSON.stringify(body),
    })
  },

  /**
   * POST /api/manager/customers/revoke
   * body: { client_ids: [...] }
   */
  revokeCustomers(body) {
    return request('/manager/customers/revoke', {
      method: 'POST',
      body: JSON.stringify(body),
    })
  },

  /**
   * POST /api/manager/customers/smart-assign
   * body: { client_ids: [...], employee_ids: [...] }
   */
  smartAssign(body) {
    return request('/manager/customers/smart-assign', {
      method: 'POST',
      body: JSON.stringify(body),
    })
  },
}
