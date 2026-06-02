<template>
    <div class="manager-page">
        <!-- 侧边栏 -->
        <aside class="manager-sidebar flex flex-col z-50 shrink-0" :class="{ collapsed: sidebarCollapsed }" id="mgr-sidebar">
            <div class="h-16 flex items-center px-5 border-b border-zinc-800 logo-container">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shrink-0 shadow-lg shadow-indigo-500/20">
                        <iconify-icon class="text-2xl text-white" icon="solar:shield-star-bold-duotone"></iconify-icon>
                    </div>
                    <span class="font-bold text-lg text-zinc-100 logo-text truncate">AI展业平台</span>
                </div>
            </div>
            <nav class="flex-1 px-4 py-5 space-y-6 overflow-y-auto custom-scrollbar">
                <div>
                    <p class="px-2 mb-3 text-[10px] font-semibold text-zinc-500 uppercase tracking-wider nav-text">管理工作站</p>
                    <div class="space-y-1">
                        <router-link to="/manager"
                            class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-xl text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 transition-all"
                            active-class="bg-indigo-600/15 text-indigo-400 border border-indigo-600/20">
                            <iconify-icon class="text-xl shrink-0" icon="solar:widget-5-bold-duotone"></iconify-icon>
                            <span class="nav-text text-sm font-medium whitespace-nowrap">首页大厅</span>
                        </router-link>
                        <a href="#" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-xl text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 transition-all">
                            <iconify-icon class="text-xl shrink-0" icon="solar:clapperboard-edit-bold-duotone"></iconify-icon>
                            <span class="nav-text text-sm font-medium whitespace-nowrap">任务大厅 (管理版)</span>
                        </a>
                        <router-link to="/manager/customers"
                            class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-xl text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 transition-all"
                            active-class="bg-indigo-600/15 text-indigo-400 border border-indigo-600/20">
                            <iconify-icon class="text-xl shrink-0" icon="solar:users-group-rounded-bold-duotone"></iconify-icon>
                            <span class="nav-text text-sm font-medium whitespace-nowrap">客户分配管理</span>
                        </router-link>
                        <a href="#" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-xl text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 transition-all">
                            <iconify-icon class="text-xl shrink-0" icon="solar:graph-bold-duotone"></iconify-icon>
                            <span class="nav-text text-sm font-medium whitespace-nowrap">团队绩效分析</span>
                        </a>
                        <a href="#" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-xl text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 transition-all">
                            <iconify-icon class="text-xl shrink-0" icon="solar:users-group-two-rounded-bold-duotone"></iconify-icon>
                            <span class="nav-text text-sm font-medium whitespace-nowrap">员工负载监控</span>
                        </a>
                    </div>
                </div>
                <div>
                    <p class="px-2 mb-3 text-[10px] font-semibold text-zinc-500 uppercase tracking-wider nav-text">营销中心</p>
                    <div class="space-y-1">
                        <a href="#" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-xl text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 transition-all">
                            <iconify-icon class="text-xl shrink-0" icon="solar:magic-stick-3-bold-duotone"></iconify-icon>
                            <span class="nav-text text-sm font-medium whitespace-nowrap">AI营销工具箱</span>
                        </a>
                        <a href="#" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-xl text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 transition-all">
                            <iconify-icon class="text-xl shrink-0" icon="solar:phone-calling-bold-duotone"></iconify-icon>
                            <span class="nav-text text-sm font-medium whitespace-nowrap">外呼管理</span>
                        </a>
                    </div>
                </div>
            </nav>
            <div class="p-4 border-t border-zinc-800">
                <div class="flex items-center gap-3 p-2 rounded-xl bg-zinc-900/50">
                    <img class="w-10 h-10 rounded-lg object-cover shrink-0 border border-zinc-700"
                        src="https://modao.cc/agent-py/media/generated_images/2026-05-15/00e949e862be40aa9923f1315bb96db2.jpg" alt="Manager"/>
                    <div class="user-info-text overflow-hidden">
                        <p class="text-sm font-semibold text-zinc-100 truncate">陈经理</p>
                        <p class="text-xs text-zinc-500 truncate">营销部门主管</p>
                    </div>
                </div>
            </div>
        </aside>

        <!-- 主体内容 -->
        <main class="flex-1 flex flex-col min-w-0 overflow-hidden">
            <!-- 顶部导航 -->
            <header class="h-16 border-b border-zinc-800 bg-zinc-950/50 backdrop-blur-md flex items-center justify-between px-8 shrink-0 z-40">
                <div class="flex items-center gap-4">
                    <button class="p-2 rounded-lg hover:bg-zinc-800 text-zinc-400 transition-colors" @click="toggleSidebar">
                        <iconify-icon class="text-2xl" icon="solar:hamburger-menu-bold"></iconify-icon>
                    </button>
                    <h1 class="text-base font-semibold text-zinc-100">客户分配管理</h1>
                    <span class="text-sm text-zinc-500">{{ today }}</span>
                </div>
                <div class="flex items-center gap-3">
                    <div class="flex items-center gap-1 bg-zinc-800 rounded-lg p-1 text-xs font-medium">
                        <router-link class="px-2.5 py-1 text-zinc-400 hover:text-white rounded-md transition-all" to="/">营销人员</router-link>
                        <span class="px-2.5 py-1 bg-zinc-700 text-white rounded-md">管理人员</span>
                    </div>
                    <!-- 每日提醒铃铛 -->
                    <div class="relative alert-panel-wrapper">
                        <button @click="toggleAlertPanel"
                                class="p-2 rounded-lg hover:bg-zinc-800 text-zinc-400 transition-colors relative">
                            <iconify-icon class="text-xl" icon="solar:bell-bing-bold"></iconify-icon>
                            <span v-if="unreadAlertCount > 0"
                                  class="absolute top-1.5 right-1.5 w-2 h-2 bg-rose-500 rounded-full border-2 border-zinc-950"></span>
                        </button>
                        <!-- 提醒面板 -->
                        <div v-if="alertPanelOpen"
                             class="absolute right-0 top-12 w-96 bg-zinc-900 border border-zinc-800 rounded-xl shadow-2xl z-50 flex flex-col"
                             style="max-height: 520px;">
                            <!-- 面板标题 -->
                            <div class="flex items-center justify-between px-4 py-3 border-b border-zinc-800">
                                <span class="text-sm font-semibold text-zinc-200">每日提醒</span>
                                <span class="text-xs text-zinc-500">近30天未完成（{{ unreadAlertCount }} 条）</span>
                            </div>
                            <!-- 提醒列表 -->
                            <div class="flex-1 overflow-y-auto divide-y divide-zinc-800/60">
                                <div v-if="alerts.length === 0" class="py-10 text-center text-zinc-500 text-sm">
                                    暂无未完成提醒
                                </div>
                                <div v-for="alert in alerts" :key="alert.alert_id"
                                     class="flex items-start gap-3 px-4 py-3 hover:bg-zinc-800/40 transition-colors">
                                    <button @click="markAlertDone(alert)"
                                            class="mt-0.5 w-4 h-4 rounded border border-zinc-600 flex-shrink-0 hover:border-blue-400 transition-colors flex items-center justify-center">
                                        <iconify-icon v-if="alert._marking" icon="svg-spinners:ring-resize" class="text-blue-400 text-xs"></iconify-icon>
                                    </button>
                                    <div class="flex-1 min-w-0">
                                        <p class="text-sm text-zinc-200 leading-snug">{{ alert.alert_content }}</p>
                                        <p class="text-xs text-zinc-500 mt-1">{{ alert.alert_date }}</p>
                                    </div>
                                </div>
                            </div>
                            <!-- 新增提醒输入框 -->
                            <div class="px-4 py-3 border-t border-zinc-800">
                                <div class="flex gap-2">
                                    <input v-model="newAlertContent"
                                           @keydown.enter="addAlert"
                                           placeholder="新增提醒…"
                                           class="flex-1 bg-zinc-800 text-zinc-200 text-sm rounded-lg px-3 py-2 outline-none placeholder-zinc-500 focus:ring-1 focus:ring-blue-500" />
                                    <button @click="addAlert"
                                            :disabled="!newAlertContent.trim()"
                                            class="px-3 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white text-sm rounded-lg transition-colors">
                                        添加
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <div class="flex-1 flex overflow-hidden">
                <!-- 左侧主区域 -->
                <div class="flex-1 flex flex-col overflow-hidden">
                    <!-- 筛选栏 -->
                    <section class="p-5 border-b border-zinc-800 bg-zinc-900/20 shrink-0">
                        <div class="grid grid-cols-6 gap-3 mb-4">
                            <div v-for="filter in filterDefs" :key="filter.key" class="space-y-1">
                                <label class="text-[10px] text-zinc-500 font-medium">{{ filter.label }}</label>
                                <select
                                    v-model="filterValues[filter.key]"
                                    class="w-full bg-zinc-800/50 border border-zinc-700 rounded-lg text-zinc-200 text-xs px-3 py-2 outline-none focus:border-indigo-500 transition-all">
                                    <option value="">全部</option>
                                    <option v-for="opt in filter.opts" :key="opt" :value="opt">{{ opt }}</option>
                                </select>
                            </div>
                        </div>
                        <div class="flex items-center justify-between gap-4">
                            <div class="relative flex-1 max-w-md">
                                <iconify-icon class="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500 text-sm" icon="solar:magnifer-linear"></iconify-icon>
                                <input
                                    v-model="filterValues.keyword"
                                    class="w-full bg-zinc-800/50 border border-zinc-700 rounded-lg text-zinc-200 text-sm pl-10 pr-4 py-2 outline-none focus:border-indigo-500 transition-all"
                                    placeholder="搜索客户姓名、资金账号、手机号..."
                                    type="text"/>
                            </div>
                            <div class="flex items-center gap-2">
                                <button class="px-4 py-2 rounded-lg border border-zinc-700 text-zinc-300 text-sm hover:bg-zinc-800 transition-all flex items-center gap-1.5" @click="resetFilters">
                                    <iconify-icon icon="solar:restart-bold" width="13"></iconify-icon>
                                    重置
                                </button>
                                <div class="w-px h-6 bg-zinc-800 mx-1"></div>
                                <button class="p-2 rounded-lg border border-zinc-700 text-zinc-400 hover:text-white transition-all" title="导出当前客户明细"
                                    @click="exportCustomers">
                                    <iconify-icon class="text-lg" :class="{ 'animate-spin': exporting }" :icon="exporting ? 'solar:spinner-bold' : 'solar:export-linear'"></iconify-icon>
                                </button>
                                <button class="p-2 rounded-lg border border-zinc-700 text-zinc-400 hover:text-white transition-all" title="刷新" @click="fetchCustomers">
                                    <iconify-icon class="text-lg" :class="{ 'animate-spin': loading }" icon="solar:refresh-linear"></iconify-icon>
                                </button>
                            </div>
                        </div>
                    </section>

                    <!-- 批量操作栏 -->
                    <section class="px-5 py-3 flex items-center justify-between border-b border-zinc-800 bg-zinc-900/10 shrink-0">
                        <div class="flex items-center gap-3">
                            <div class="flex items-center gap-2 px-3 py-1.5 bg-zinc-800/50 rounded-lg border border-zinc-700">
                                <input class="w-4 h-4 rounded border-zinc-600 text-indigo-600 bg-zinc-900" id="selectAll" type="checkbox" v-model="selectAll" @change="toggleSelectAll"/>
                                <label class="text-sm text-zinc-400" for="selectAll">已选 <span class="text-indigo-400 font-bold">{{ selectedCount }}</span> 个客户</label>
                            </div>
                            <button class="flex items-center gap-2 px-4 py-2 rounded-lg bg-zinc-700 text-zinc-200 text-sm font-medium hover:bg-zinc-600 transition-all" @click="openManualModal">
                                <iconify-icon icon="solar:user-plus-bold"></iconify-icon>
                                手动分配
                            </button>
                            <button class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-500/20" @click="openAIModal">
                                <iconify-icon class="text-base" icon="solar:magic-stick-3-bold"></iconify-icon>
                                智能分配
                            </button>
                            <button class="flex items-center gap-2 px-4 py-2 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-500 text-sm font-medium hover:bg-rose-500/20 transition-all" @click="revokeSelected">
                                <iconify-icon icon="solar:trash-bin-trash-bold"></iconify-icon>
                                撤回客户
                            </button>
                        </div>
                        <button class="flex items-center gap-2 px-4 py-2 rounded-lg border border-zinc-700 text-zinc-400 text-sm hover:text-white transition-all" @click="showHistoryModal = true">
                            <iconify-icon icon="solar:history-bold"></iconify-icon>
                            分配记录
                        </button>
                    </section>

                    <!-- 客户表格 -->
                    <div class="flex-1 overflow-auto custom-scrollbar">
                        <!-- 加载状态 -->
                        <div v-if="loading && customers.length === 0" class="flex items-center justify-center h-full">
                            <div class="flex flex-col items-center gap-3 text-zinc-500">
                                <iconify-icon class="text-3xl animate-spin" icon="solar:spinner-bold"></iconify-icon>
                                <span class="text-sm">加载中...</span>
                            </div>
                        </div>
                        <!-- 空状态 -->
                        <div v-else-if="!loading && customers.length === 0" class="flex items-center justify-center h-full">
                            <div class="flex flex-col items-center gap-3 text-zinc-600">
                                <iconify-icon class="text-4xl" icon="solar:users-group-rounded-bold-duotone"></iconify-icon>
                                <span class="text-sm">暂无符合条件的客户</span>
                            </div>
                        </div>
                        <table v-else class="w-full text-left border-collapse min-w-max">
                            <thead class="sticky top-0 bg-zinc-900 z-10">
                                <tr class="text-[10px] text-zinc-500 uppercase tracking-wider border-b border-zinc-800">
                                    <th class="px-5 py-4 w-10 shrink-0"></th>
                                    <th class="px-4 py-4 whitespace-nowrap">资金账号</th>
                                    <th class="px-4 py-4 whitespace-nowrap">客户姓名</th>
                                    <th class="px-4 py-4 whitespace-nowrap">手机号（脱敏）</th>
                                    <th class="px-4 py-4 whitespace-nowrap text-right">T-1日AUM资产（万）</th>
                                    <th class="px-4 py-4 whitespace-nowrap">资产等级</th>
                                    <th class="px-4 py-4 whitespace-nowrap">风险等级</th>
                                    <th class="px-4 py-4 whitespace-nowrap">建联状态</th>
                                    <th class="px-4 py-4 whitespace-nowrap">跟进状态</th>
                                    <th class="px-4 py-4 whitespace-nowrap">归属人</th>
                                    <th class="px-4 py-4 whitespace-nowrap">分配时间</th>
                                    <th class="px-4 py-4 whitespace-nowrap">分配人</th>
                                    <th class="px-5 py-4 text-right whitespace-nowrap sticky right-0 bg-zinc-900 border-l border-zinc-800">操作</th>
                                </tr>
                            </thead>
                            <tbody class="text-sm divide-y divide-zinc-800">
                                <tr v-for="c in customers" :key="c.fund_account"
                                    class="hover:bg-zinc-800/30 transition-colors"
                                    :class="{ 'border-l-2 border-rose-500 bg-rose-500/3': !c.assignee_nm }">
                                    <td class="px-5 py-4 align-middle">
                                        <input class="w-4 h-4 rounded border-zinc-600 text-indigo-600 bg-zinc-900" type="checkbox" v-model="c.selected"/>
                                    </td>
                                    <td class="px-4 py-4 text-zinc-400 font-mono text-xs whitespace-nowrap align-middle">{{ c.fund_account }}</td>
                                    <td class="px-4 py-4 font-medium text-zinc-100 whitespace-nowrap align-middle">{{ c.cust_name }}</td>
                                    <td class="px-4 py-4 text-zinc-400 whitespace-nowrap align-middle">{{ c.phone }}</td>
                                    <td class="px-4 py-4 font-semibold text-zinc-200 text-right whitespace-nowrap align-middle">{{ c.t1_aum }}</td>
                                    <td class="px-4 py-4 align-middle">
                                        <span class="px-2 py-0.5 rounded text-xs font-bold whitespace-nowrap" :class="getLevelClass(c.asset_level)">{{ c.asset_level }}</span>
                                    </td>
                                    <td class="px-4 py-4 text-zinc-400 text-xs whitespace-nowrap align-middle">{{ c.risk_level }}</td>
                                    <td class="px-4 py-4 text-xs whitespace-nowrap align-middle" :class="getContactClass(c.contact_status)">{{ c.contact_status }}</td>
                                    <td class="px-4 py-4 text-xs whitespace-nowrap align-middle" :class="getFollowClass(c.follow_status)">{{ c.follow_status }}</td>
                                    <td class="px-4 py-4 text-xs whitespace-nowrap align-middle" :class="c.assignee_nm ? 'text-zinc-300' : 'text-rose-500 font-medium'">{{ c.assignee_nm || '—' }}</td>
                                    <td class="px-4 py-4 text-xs text-zinc-400 whitespace-nowrap align-middle">{{ c.assign_time || '—' }}</td>
                                    <td class="px-4 py-4 text-xs text-zinc-400 whitespace-nowrap align-middle">{{ c.operator_nm || '—' }}</td>
                                    <td class="px-5 py-4 text-right whitespace-nowrap align-middle sticky right-0 bg-zinc-900 border-l border-zinc-800">
                                        <!-- 未分配：快速分配 -->
                                        <button v-if="!c.assignee_nm"
                                            class="text-indigo-400 hover:text-indigo-300 text-sm font-medium transition-colors"
                                            @click="quickAssign(c)">快速分配</button>
                                        <!-- 手动分配（可撤回） -->
                                        <button v-else-if="c.assign_source === 1"
                                            class="text-rose-400 hover:text-rose-300 text-sm font-medium transition-colors"
                                            @click="revokeOne(c)">撤回</button>
                                        <!-- 外部导入（不可撤回） -->
                                        <span v-else class="text-zinc-600 text-xs italic">外部导入</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- 分页 -->
                    <footer class="px-5 py-3.5 border-t border-zinc-800 bg-zinc-900/50 flex items-center justify-between shrink-0">
                        <div class="text-sm text-zinc-500">
                            显示 <span class="text-zinc-300">{{ displayRange }}</span> /
                            共 <span class="text-zinc-300">{{ total }}</span> 条
                        </div>
                        <div class="flex items-center gap-2">
                            <button
                                class="p-2 rounded-lg border border-zinc-800 text-zinc-500 hover:text-zinc-300 disabled:opacity-30 transition-all"
                                :disabled="currentPage <= 1"
                                @click="goToPage(currentPage - 1)">
                                <iconify-icon icon="solar:alt-arrow-left-linear"></iconify-icon>
                            </button>
                            <template v-for="p in pageNumbers" :key="p">
                                <span v-if="p === '...'" class="text-zinc-600 px-1">...</span>
                                <button v-else
                                    class="w-8 h-8 rounded-lg text-sm font-medium transition-all"
                                    :class="p === currentPage
                                        ? 'bg-indigo-600 text-white'
                                        : 'border border-zinc-800 text-zinc-400 hover:bg-zinc-800'"
                                    @click="goToPage(p)">{{ p }}</button>
                            </template>
                            <button
                                class="p-2 rounded-lg border border-zinc-800 text-zinc-500 hover:text-zinc-300 disabled:opacity-30 transition-all"
                                :disabled="currentPage >= totalPages"
                                @click="goToPage(currentPage + 1)">
                                <iconify-icon icon="solar:alt-arrow-right-linear"></iconify-icon>
                            </button>
                        </div>
                    </footer>
                </div>

                <!-- 右侧辅助面板 -->
                <aside class="w-72 border-l border-zinc-800 flex flex-col overflow-hidden bg-zinc-950/30 shrink-0">
                    <!-- 员工负载 -->
                    <div class="p-5 border-b border-zinc-800 shrink-0">
                        <div class="flex items-center justify-between mb-3">
                            <h3 class="font-semibold text-zinc-100 text-sm flex items-center gap-2">
                                <iconify-icon class="text-indigo-400 text-lg" icon="solar:users-group-rounded-bold-duotone"></iconify-icon>
                                员工负载分布
                            </h3>
                            <button class="text-zinc-500 hover:text-indigo-400 transition-colors" @click="fetchStaffWorkload">
                                <iconify-icon icon="solar:refresh-linear"></iconify-icon>
                            </button>
                        </div>
                        <div class="space-y-2">
                            <div v-for="(staff, idx) in paginatedStaffList" :key="staff.login_id"
                                class="flex items-center justify-between p-3 rounded-xl bg-zinc-900/50 border border-zinc-800 transition-all">
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center text-xs font-bold"
                                         :class="getAvatarClass(idx + (staffPage - 1) * staffPageSize)">
                                        {{ staff.emp_name[0] }}
                                    </div>
                                    <div>
                                        <p class="text-sm font-medium text-zinc-200">{{ staff.emp_name }}</p>
                                        <p class="text-[10px] text-zinc-500">客户: {{ staff.cust_count }}</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <span class="text-[10px] font-bold px-1.5 py-0.5 rounded border" :class="getLoadStatusClass(staff.load_level)">{{ staff.load_level }}</span>
                                </div>
                            </div>
                            <!-- 空状态 -->
                            <div v-if="staffList.length === 0" class="text-center text-zinc-600 text-xs py-4">暂无员工数据</div>
                        </div>
                        <!-- 翻页 -->
                        <div class="flex items-center justify-between mt-3 pt-3 border-t border-zinc-800">
                            <span class="text-[10px] text-zinc-600">
                                {{ (staffPage - 1) * staffPageSize + 1 }}–{{ Math.min(staffPage * staffPageSize, staffList.length) }} / {{ staffList.length }} 人
                            </span>
                            <div class="flex items-center gap-1">
                                <button class="p-1 rounded hover:bg-zinc-800 text-zinc-500 hover:text-zinc-200 disabled:opacity-30 transition-all"
                                        :disabled="staffPage <= 1" @click="staffPage--">
                                    <iconify-icon icon="solar:alt-arrow-left-linear" class="text-xs"></iconify-icon>
                                </button>
                                <span class="text-[10px] text-zinc-500 px-1.5">{{ staffPage }} / {{ staffTotalPages }}</span>
                                <button class="p-1 rounded hover:bg-zinc-800 text-zinc-500 hover:text-zinc-200 disabled:opacity-30 transition-all"
                                        :disabled="staffPage >= staffTotalPages" @click="staffPage++">
                                    <iconify-icon icon="solar:alt-arrow-right-linear" class="text-xs"></iconify-icon>
                                </button>
                            </div>
                        </div>
                    </div>
                    <!-- 分配记录 -->
                    <div class="flex-1 p-5 flex flex-col overflow-hidden">
                        <h3 class="font-semibold text-zinc-100 text-sm flex items-center gap-2 mb-4">
                            <iconify-icon class="text-amber-500 text-lg" icon="solar:history-bold-duotone"></iconify-icon>
                            最近分配记录
                        </h3>
                        <div class="flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-1">
                            <div v-if="assignmentLogs.length === 0" class="text-center text-zinc-600 text-xs py-4">
                                暂无分配记录
                            </div>
                            <div v-for="log in assignmentLogs" :key="log.ts" class="relative pl-6 pb-4 border-l border-zinc-800">
                                <div class="absolute left-[-5px] top-0 w-2.5 h-2.5 rounded-full" :class="log.dotClass"></div>
                                <p class="text-[10px] text-zinc-500 mb-1">{{ _relTime(log.ts) }}</p>
                                <p class="text-xs text-zinc-300 leading-relaxed" v-html="log.text"></p>
                            </div>
                        </div>
                        <a href="#" class="mt-3 text-center text-xs text-zinc-500 hover:text-indigo-400 transition-colors" @click.prevent="showHistoryModal = true">查看全部记录</a>
                    </div>
                </aside>
            </div>
        </main>

        <!-- 分配方案详情弹窗 -->
        <div v-if="showAIDetailModal" class="fixed inset-0 z-[110] flex items-center justify-center p-4 modal-backdrop">
            <div class="w-full max-w-4xl bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl flex flex-col" style="max-height: 88vh;">
                <div class="px-6 py-4 border-b border-zinc-800 flex items-center justify-between shrink-0 bg-indigo-600/5">
                    <div>
                        <h2 class="text-base font-bold text-zinc-100 flex items-center gap-2">
                            <iconify-icon class="text-indigo-400 text-xl" icon="solar:document-text-bold-duotone"></iconify-icon>
                            分配方案详情
                        </h2>
                        <p class="text-[11px] text-zinc-500 mt-0.5">AI 生成 · 共 {{ aiDetailTotalCount }} 个客户 → {{ aiDetailPlans.length }} 名员工</p>
                    </div>
                    <button class="p-1.5 text-zinc-500 hover:text-white rounded-lg hover:bg-zinc-800 transition-colors" @click="showAIDetailModal = false">
                        <iconify-icon class="text-xl" icon="solar:close-circle-bold"></iconify-icon>
                    </button>
                </div>
                <div class="px-6 py-3 border-b border-zinc-800 bg-zinc-900/60 flex items-center gap-6 shrink-0">
                    <div v-for="stat in aiDetailStats" :key="stat.label" class="flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full shrink-0" :class="stat.dot"></span>
                        <span class="text-xs text-zinc-400">{{ stat.label }}</span>
                        <span class="text-sm font-bold text-zinc-200">{{ stat.value }}</span>
                    </div>
                </div>
                <div class="flex-1 overflow-y-auto custom-scrollbar p-5 space-y-4">
                    <div v-for="(group, gIdx) in aiDetailPlans" :key="group.staffName"
                        class="rounded-2xl border overflow-hidden"
                        :class="gIdx === 0 ? 'border-indigo-600/30 bg-indigo-600/3' : 'border-zinc-800 bg-zinc-900/40'">
                        <div class="px-5 py-3.5 flex items-center justify-between border-b"
                            :class="gIdx === 0 ? 'border-indigo-600/20 bg-indigo-600/8' : 'border-zinc-800 bg-zinc-800/30'">
                            <div class="flex items-center gap-3">
                                <div class="w-9 h-9 rounded-full flex items-center justify-center text-sm font-bold shrink-0"
                                    :class="gIdx === 0 ? 'bg-indigo-600 text-white' : 'bg-zinc-700 text-zinc-300'">
                                    {{ group.staffAvatar }}
                                </div>
                                <div>
                                    <p class="text-sm font-bold text-zinc-100">{{ group.staffName }}</p>
                                    <p class="text-[10px] text-zinc-500 mt-0.5">{{ group.loadChange }} &nbsp;·&nbsp; 接收 {{ group.customers.length }} 个客户</p>
                                </div>
                            </div>
                            <div class="flex items-center gap-3 text-right">
                                <div>
                                    <p class="text-[10px] text-zinc-500">高价值客户</p>
                                    <p class="text-sm font-bold text-rose-400">{{ group.customers.filter(c => c.level === '高价值').length }} 个</p>
                                </div>
                                <div class="w-px h-8 bg-zinc-700"></div>
                                <div>
                                    <p class="text-[10px] text-zinc-500">分配依据</p>
                                    <p class="text-xs font-medium text-zinc-300">{{ group.reason }}</p>
                                </div>
                            </div>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left border-collapse min-w-max">
                                <thead>
                                    <tr class="text-[10px] text-zinc-600 uppercase tracking-wider border-b border-zinc-800">
                                        <th class="px-5 py-2.5 whitespace-nowrap">资金账号</th>
                                        <th class="px-4 py-2.5 whitespace-nowrap">客户姓名</th>
                                        <th class="px-4 py-2.5 whitespace-nowrap text-right">AUM（万）</th>
                                        <th class="px-4 py-2.5 whitespace-nowrap">资产等级</th>
                                        <th class="px-4 py-2.5 whitespace-nowrap">风险等级</th>
                                        <th class="px-4 py-2.5 whitespace-nowrap">建联状态</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-zinc-800/60">
                                    <tr v-for="c in group.customers" :key="c.fundAccount" class="hover:bg-zinc-800/20 transition-colors text-xs">
                                        <td class="px-5 py-3 text-zinc-400 font-mono whitespace-nowrap">{{ c.fundAccount }}</td>
                                        <td class="px-4 py-3 text-zinc-200 font-medium whitespace-nowrap">{{ c.name }}</td>
                                        <td class="px-4 py-3 text-zinc-200 font-semibold text-right whitespace-nowrap">{{ c.aum }}</td>
                                        <td class="px-4 py-3 whitespace-nowrap">
                                            <span class="px-2 py-0.5 rounded text-[10px] font-bold" :class="c.levelClass">{{ c.level }}</span>
                                        </td>
                                        <td class="px-4 py-3 text-zinc-400 whitespace-nowrap">{{ c.risk }}</td>
                                        <td class="px-4 py-3 whitespace-nowrap" :class="c.contactClass">{{ c.contact }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="px-6 py-4 border-t border-zinc-800 bg-zinc-900/50 flex items-center justify-end gap-3 shrink-0">
                    <button class="px-5 py-2 rounded-lg border border-zinc-700 text-zinc-300 text-sm font-medium hover:bg-zinc-800 transition-all" @click="showAIDetailModal = false">
                        返回方案
                    </button>
                    <button class="px-7 py-2 rounded-lg text-sm font-medium bg-indigo-600 text-white hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-600/20"
                            @click="showAIDetailModal = false; aiStaffValid && confirmAllocation()">
                        确认并执行分配
                    </button>
                </div>
            </div>
        </div>

        <!-- 手动分配弹窗 -->
        <div v-if="showManualModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 modal-backdrop">
            <div class="w-full max-w-2xl bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl overflow-hidden">
                <div class="px-6 py-4 border-b border-zinc-800 flex items-center justify-between">
                    <h2 class="text-base font-bold text-zinc-100">手动分配客户（已选 <span class="text-indigo-400">{{ Math.max(selectedCount, 1) }}</span> 个）</h2>
                    <button class="text-zinc-500 hover:text-white transition-colors" @click="showManualModal = false">
                        <iconify-icon class="text-2xl" icon="solar:close-circle-bold"></iconify-icon>
                    </button>
                </div>
                <div class="p-6 space-y-5">
                    <div>
                        <p class="text-[10px] text-zinc-500 font-medium mb-2 uppercase tracking-wider">待分配客户</p>
                        <div class="flex flex-wrap gap-2">
                            <div v-for="c in selectedCustomers" :key="c.fund_account"
                                class="flex items-center gap-2 px-3 py-1.5 bg-zinc-800 rounded-lg border border-zinc-700">
                                <span class="text-sm text-zinc-200">{{ c.cust_name }}</span>
                                <span class="text-[10px] px-1.5 py-0.5 rounded" :class="getLevelClass(c.asset_level)">{{ c.asset_level }}</span>
                            </div>
                            <div v-if="selectedCustomers.length === 0" class="text-xs text-zinc-500 italic">请先在列表中勾选客户</div>
                        </div>
                    </div>
                    <div class="space-y-3">
                        <div class="flex items-center justify-between">
                            <p class="text-[10px] text-zinc-500 font-medium uppercase tracking-wider">选择接收员工</p>
                            <div class="relative w-44">
                                <iconify-icon class="absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-500 text-xs" icon="solar:magnifer-linear"></iconify-icon>
                                <input v-model="manualSearchQ" class="w-full bg-zinc-800/50 border border-zinc-700 rounded-lg text-zinc-200 text-xs pl-8 pr-3 py-1.5 outline-none focus:border-indigo-500 transition-all" placeholder="搜索员工姓名..." type="text"/>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3 max-h-52 overflow-y-auto custom-scrollbar pr-1">
                            <label v-for="staff in filteredStaffForManual" :key="staff.login_id"
                                class="relative flex items-center justify-between p-3 rounded-xl border bg-zinc-900 transition-all cursor-pointer"
                                :class="staff.disabled ? 'border-zinc-800 opacity-50 cursor-not-allowed' : selectedStaff === staff.login_id ? 'border-indigo-500 bg-indigo-600/8' : 'border-zinc-800 hover:bg-zinc-800'">
                                <input v-if="!staff.disabled" class="hidden" name="staffSelect" type="radio" v-model="selectedStaff" :value="staff.login_id"/>
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center text-xs font-bold text-zinc-400">{{ staff.emp_name[0] }}</div>
                                    <div>
                                        <p class="text-sm font-medium text-zinc-200">{{ staff.emp_name }}</p>
                                        <p class="text-[10px]" :class="staff.disabled ? 'text-rose-500 font-bold' : 'text-zinc-500'">{{ staff.load_level }} · {{ staff.cust_count }} 个客户</p>
                                    </div>
                                </div>
                                <span v-if="staff.disabled" class="text-[10px] text-zinc-600 italic">不可选</span>
                                <iconify-icon v-else-if="selectedStaff === staff.login_id" class="text-indigo-500 text-xl" icon="solar:check-circle-bold"></iconify-icon>
                            </label>
                        </div>
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] text-zinc-500 font-medium uppercase tracking-wider">分配备注</label>
                        <textarea v-model="assignRemark" class="w-full bg-zinc-800/50 border border-zinc-700 rounded-lg text-zinc-200 text-sm p-3 h-20 outline-none focus:border-indigo-500 transition-all resize-none" placeholder="输入分配说明（如：高价值客户，请重点跟进）"></textarea>
                    </div>
                </div>
                <div class="px-6 py-4 border-t border-zinc-800 bg-zinc-900/50 flex items-center justify-end gap-3">
                    <button class="px-5 py-2 rounded-lg border border-zinc-700 text-zinc-300 text-sm font-medium hover:bg-zinc-800 transition-all" @click="showManualModal = false">取消</button>
                    <button class="px-7 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-600/20"
                            :disabled="!selectedStaff || selectedCustomers.length === 0 || assigning"
                            :class="(!selectedStaff || selectedCustomers.length === 0) ? 'opacity-50 cursor-not-allowed' : ''"
                            @click="confirmManualAssign">
                        {{ assigning ? '分配中...' : '确认分配' }}
                    </button>
                </div>
            </div>
        </div>

        <!-- 分配记录弹窗 -->
        <div v-if="showHistoryModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 modal-backdrop">
            <div class="w-full max-w-5xl bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl flex flex-col" style="max-height: 85vh;">
                <div class="px-6 py-4 border-b border-zinc-800 flex items-center justify-between shrink-0">
                    <h2 class="text-base font-bold text-zinc-100 flex items-center gap-2">
                        <iconify-icon class="text-amber-400 text-xl" icon="solar:history-bold-duotone"></iconify-icon>
                        分配记录
                        <span v-if="hasHistoryFilter" class="text-[10px] font-normal px-2 py-0.5 bg-indigo-500/10 text-indigo-400 rounded-full">筛选中</span>
                    </h2>
                    <div class="flex items-center gap-2">
                        <button @click="exportHistory" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-zinc-700 text-zinc-400 text-xs font-medium hover:text-zinc-200 hover:border-zinc-500 transition-all">
                            <iconify-icon icon="solar:export-linear" class="text-sm"></iconify-icon>
                            导出
                        </button>
                        <button class="p-1.5 text-zinc-500 hover:text-white transition-colors rounded-lg hover:bg-zinc-800" @click="showHistoryModal = false">
                            <iconify-icon class="text-xl" icon="solar:close-circle-bold"></iconify-icon>
                        </button>
                    </div>
                </div>
                <div class="px-6 py-3.5 border-b border-zinc-800 flex items-center gap-4 shrink-0 bg-zinc-900/50">
                    <span class="text-xs text-zinc-500 shrink-0 font-medium">查看月份：</span>
                    <div class="flex gap-2 flex-wrap">
                        <button v-for="month in historyMonths" :key="month.value"
                            class="px-3 py-1 rounded-lg text-xs font-medium transition-all whitespace-nowrap"
                            :class="selectedHistoryMonth === month.value ? 'bg-indigo-600 text-white shadow-sm shadow-indigo-500/30' : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700 hover:text-zinc-200'"
                            @click="selectedHistoryMonth = month.value">
                            {{ month.label }}
                        </button>
                    </div>
                </div>
                <div class="px-6 py-3 border-b border-zinc-800 flex items-center gap-2.5 shrink-0">
                    <div class="relative w-36 shrink-0">
                        <iconify-icon class="absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-500 text-xs pointer-events-none" icon="solar:user-bold"></iconify-icon>
                        <input v-model="historyFilter.operator" class="w-full bg-zinc-800/60 border border-zinc-700 rounded-lg text-zinc-200 text-xs pl-7 pr-3 py-2 outline-none focus:border-indigo-500 transition-all placeholder-zinc-600" placeholder="操作人员" type="text"/>
                    </div>
                    <div class="relative flex-1">
                        <iconify-icon class="absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-500 text-xs pointer-events-none" icon="solar:user-circle-bold"></iconify-icon>
                        <input v-model="historyFilter.customerKeyword" class="w-full bg-zinc-800/60 border border-zinc-700 rounded-lg text-zinc-200 text-xs pl-7 pr-3 py-2 outline-none focus:border-indigo-500 transition-all placeholder-zinc-600" placeholder="客户姓名 / 资金账号" type="text"/>
                    </div>
                    <div class="relative flex-1">
                        <iconify-icon class="absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-500 text-xs pointer-events-none" icon="solar:users-group-rounded-bold"></iconify-icon>
                        <input v-model="historyFilter.receiverKeyword" class="w-full bg-zinc-800/60 border border-zinc-700 rounded-lg text-zinc-200 text-xs pl-7 pr-3 py-2 outline-none focus:border-indigo-500 transition-all placeholder-zinc-600" placeholder="接收员工姓名 / OA" type="text"/>
                    </div>
                    <button v-if="hasHistoryFilter" class="px-3 py-2 rounded-lg border border-zinc-700 text-zinc-400 text-xs font-medium hover:text-rose-400 hover:border-rose-500/40 transition-all shrink-0" @click="resetHistoryFilter">重置</button>
                </div>
                <div class="flex-1 overflow-auto custom-scrollbar">
                    <table class="w-full text-left border-collapse min-w-max">
                        <thead class="sticky top-0 bg-zinc-900 z-10">
                            <tr class="text-[10px] text-zinc-500 uppercase tracking-wider border-b border-zinc-800">
                                <th class="px-5 py-3.5 whitespace-nowrap">操作人员</th>
                                <th class="px-4 py-3.5 whitespace-nowrap">操作时间</th>
                                <th class="px-4 py-3.5 whitespace-nowrap">资金账号</th>
                                <th class="px-4 py-3.5 whitespace-nowrap">客户姓名</th>
                                <th class="px-4 py-3.5 whitespace-nowrap">接收员工姓名</th>
                                <th class="px-4 py-3.5 whitespace-nowrap">接收员工OA</th>
                                <th class="px-4 py-3.5 whitespace-nowrap">操作内容</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-zinc-800">
                            <tr v-for="log in filteredHistoryLogs" :key="log.id" class="hover:bg-zinc-800/30 transition-colors text-sm">
                                <td class="px-5 py-3.5 text-zinc-300 font-medium whitespace-nowrap text-xs">{{ log.operator }}</td>
                                <td class="px-4 py-3.5 text-zinc-400 whitespace-nowrap text-xs font-mono">{{ log.operateTime }}</td>
                                <td class="px-4 py-3.5 text-zinc-400 whitespace-nowrap text-xs font-mono">{{ log.fundAccount }}</td>
                                <td class="px-4 py-3.5 text-zinc-200 font-medium whitespace-nowrap text-xs">{{ log.customerName }}</td>
                                <td class="px-4 py-3.5 whitespace-nowrap text-xs">
                                    <span v-if="log.receiverName" class="text-zinc-300">{{ log.receiverName }}</span>
                                    <span v-else class="text-zinc-600 italic">—</span>
                                </td>
                                <td class="px-4 py-3.5 whitespace-nowrap text-xs">
                                    <span v-if="log.receiverOA" class="text-zinc-400 font-mono">{{ log.receiverOA }}</span>
                                    <span v-else class="text-zinc-600 italic">—</span>
                                </td>
                                <td class="px-4 py-3.5 whitespace-nowrap">
                                    <span class="px-2 py-0.5 rounded text-[10px] font-bold" :class="log.actionClass">{{ log.action }}</span>
                                </td>
                            </tr>
                            <tr v-if="filteredHistoryLogs.length === 0">
                                <td colspan="7" class="text-center py-14">
                                    <iconify-icon class="text-3xl text-zinc-700 mb-2 block mx-auto" :icon="hasHistoryFilter ? 'solar:filter-bold-duotone' : 'solar:history-bold-duotone'"></iconify-icon>
                                    <p class="text-zinc-600 text-sm">{{ hasHistoryFilter ? '没有符合筛选条件的记录' : '当月暂无分配记录' }}</p>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="px-6 py-3 border-t border-zinc-800 bg-zinc-900/50 flex items-center justify-between shrink-0">
                    <span class="text-xs text-zinc-500">共 <span class="text-zinc-300 font-medium">{{ filteredHistoryLogs.length }}</span> 条记录</span>
                    <span class="text-[10px] text-zinc-600">数据范围：最近 12 个月</span>
                </div>
            </div>
        </div>

        <!-- AI智能分配弹窗 -->
        <div v-if="showAIModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 modal-backdrop">
            <div class="w-full max-w-3xl bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl overflow-hidden">
                <div class="px-6 py-4 border-b border-zinc-800 flex items-center justify-between bg-indigo-600/5">
                    <h2 class="text-base font-bold text-zinc-100 flex items-center gap-2">
                        <iconify-icon class="text-indigo-400 text-xl" icon="solar:magic-stick-3-bold"></iconify-icon>
                        AI智能分配方案
                    </h2>
                    <button class="text-zinc-500 hover:text-white transition-colors" @click="showAIModal = false">
                        <iconify-icon class="text-2xl" icon="solar:close-circle-bold"></iconify-icon>
                    </button>
                </div>
                <div class="p-7 space-y-7">
                    <div>
                        <p class="text-[10px] text-zinc-500 font-medium mb-4 uppercase tracking-wider">配置AI分配规则</p>
                        <div class="grid grid-cols-3 gap-4">
                            <label v-for="rule in aiRules" :key="rule.label"
                                class="flex flex-col gap-2 p-4 rounded-xl border bg-zinc-900 hover:border-indigo-600/50 cursor-pointer transition-all"
                                :class="rule.checked ? 'border-indigo-600 bg-indigo-600/5' : 'border-zinc-800'">
                                <div class="flex items-center justify-between">
                                    <iconify-icon class="text-2xl" :class="rule.checked ? 'text-indigo-400' : 'text-zinc-500'" :icon="rule.icon"></iconify-icon>
                                    <input class="w-4 h-4 rounded border-zinc-700 text-indigo-600 bg-zinc-900 focus:ring-0" type="checkbox" v-model="rule.checked"/>
                                </div>
                                <span class="text-sm font-medium text-zinc-200">{{ rule.label }}</span>
                                <span class="text-[10px] text-zinc-500">{{ rule.desc }}</span>
                            </label>
                        </div>
                    </div>
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <p class="text-[10px] text-zinc-500 font-medium uppercase tracking-wider flex items-center gap-2">
                                选择接收员工
                                <span class="normal-case font-semibold text-[11px] px-2 py-0.5 rounded-full"
                                      :class="selectedAIStaff.length >= 2 ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'">
                                    已选 {{ selectedAIStaff.length }} 位（至少 2 位）
                                </span>
                            </p>
                            <div class="relative w-40">
                                <iconify-icon class="absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-500 text-xs" icon="solar:magnifer-linear"></iconify-icon>
                                <input v-model="aiSearchQ" class="w-full bg-zinc-800/50 border border-zinc-700 rounded-lg text-zinc-200 text-xs pl-8 pr-3 py-1.5 outline-none focus:border-indigo-500 transition-all" placeholder="搜索员工..." type="text"/>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-2.5 max-h-44 overflow-y-auto custom-scrollbar pr-1">
                            <div v-for="staff in filteredStaffForAI" :key="staff.login_id"
                                class="relative flex items-center justify-between p-3 rounded-xl border bg-zinc-900 transition-all"
                                :class="staff.disabled
                                    ? 'border-zinc-800 opacity-50 cursor-not-allowed'
                                    : selectedAIStaff.includes(staff.login_id)
                                        ? 'border-indigo-500 bg-indigo-600/8 cursor-pointer'
                                        : 'border-zinc-800 hover:bg-zinc-800 cursor-pointer'"
                                @click="!staff.disabled && toggleAIStaff(staff.login_id)">
                                <div class="flex items-center gap-2.5">
                                    <div class="w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center text-xs font-bold"
                                         :class="selectedAIStaff.includes(staff.login_id) ? 'bg-indigo-600 text-white' : 'text-zinc-400'">
                                        {{ staff.emp_name[0] }}
                                    </div>
                                    <div>
                                        <p class="text-sm font-medium text-zinc-200">{{ staff.emp_name }}</p>
                                        <p class="text-[10px]" :class="staff.disabled ? 'text-rose-500 font-semibold' : 'text-zinc-500'">{{ staff.load_level }} · {{ staff.cust_count }} 客户</p>
                                    </div>
                                </div>
                                <span v-if="staff.disabled" class="text-[10px] text-zinc-600 italic shrink-0">不可选</span>
                                <iconify-icon v-else-if="selectedAIStaff.includes(staff.login_id)" class="text-indigo-400 text-lg shrink-0" icon="solar:check-circle-bold"></iconify-icon>
                                <div v-else class="w-4 h-4 rounded border border-zinc-700 shrink-0"></div>
                            </div>
                        </div>
                        <p v-if="selectedAIStaff.length > 0 && selectedAIStaff.length < 2" class="mt-2 text-xs text-rose-400 flex items-center gap-1.5">
                            <iconify-icon icon="solar:danger-triangle-bold"></iconify-icon>
                            请至少选择 2 位员工参与智能分配
                        </p>
                    </div>
                    <div v-if="aiSchemeGenerated" class="space-y-4">
                        <p class="text-[10px] text-zinc-500 font-medium uppercase tracking-wider">AI生成方案预览</p>
                        <div class="space-y-3">
                            <div v-for="plan in aiPlans" :key="plan.name" class="p-4 rounded-xl border flex items-center justify-between" :class="plan.borderClass">
                                <div class="flex items-center gap-4">
                                    <div class="w-10 h-10 rounded-full bg-zinc-800 flex items-center justify-center text-sm font-bold text-zinc-400">{{ plan.avatar }}</div>
                                    <div>
                                        <p class="text-sm font-medium text-zinc-100">{{ plan.name }} <span class="text-xs text-zinc-500 ml-2">分配 {{ plan.count }} 个客户</span></p>
                                        <p class="text-xs text-zinc-500 mt-0.5">{{ plan.reason }}</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <p class="text-xs font-medium" :class="plan.loadColor">{{ plan.loadChange }}</p>
                                    <p class="text-[10px] text-zinc-500">含 {{ plan.highValue }} 个高价值客户</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="!aiSchemeGenerated" class="flex justify-center">
                        <button class="flex items-center gap-3 px-10 py-4 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold transition-all shadow-xl shadow-indigo-600/30"
                                :class="{ 'opacity-75 cursor-wait': aiGenerating }"
                                @click="generateAIScheme" :disabled="aiGenerating">
                            <iconify-icon class="text-2xl" :class="{ 'animate-spin': aiGenerating }" :icon="aiGenerating ? 'solar:spinner-bold' : 'solar:magic-stick-3-bold'"></iconify-icon>
                            {{ aiGenerating ? 'AI方案生成中...' : '一键生成AI分配方案' }}
                        </button>
                    </div>
                </div>
                <div v-if="aiSchemeGenerated" class="px-6 py-4 border-t border-zinc-800 bg-zinc-900/50 flex items-center justify-between gap-3">
                    <div>
                        <p v-if="!aiStaffValid" class="text-xs text-rose-400 flex items-center gap-1.5">
                            <iconify-icon icon="solar:danger-triangle-bold"></iconify-icon>
                            请至少选择 2 位接收员工后再执行分配
                        </p>
                        <button v-else class="flex items-center gap-2 px-4 py-2 rounded-lg border border-indigo-600/40 text-indigo-400 text-sm font-medium hover:bg-indigo-600/10 transition-all" @click="showAIDetailModal = true">
                            <iconify-icon icon="solar:document-text-bold-duotone" class="text-base"></iconify-icon>
                            查看分配详情
                        </button>
                    </div>
                    <div class="flex items-center gap-3">
                        <button class="px-5 py-2 rounded-lg border border-zinc-700 text-zinc-300 text-sm font-medium hover:bg-zinc-800 transition-all" @click="showAIModal = false">取消方案</button>
                        <button class="px-7 py-2 rounded-lg text-sm font-medium transition-all shadow-lg"
                                :class="aiStaffValid ? 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-indigo-600/20' : 'bg-zinc-700 text-zinc-500 cursor-not-allowed'"
                                :disabled="!aiStaffValid"
                                @click="aiStaffValid && confirmAllocation()">
                            确认并执行分配
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { api } from '@/api/index.js'

// ── UI 状态 ──────────────────────────────────────────────────────────────────
const sidebarCollapsed = ref(false)
const toggleSidebar = () => { sidebarCollapsed.value = !sidebarCollapsed.value }

const showManualModal  = ref(false)
const showAIModal      = ref(false)
const showHistoryModal = ref(false)
const showAIDetailModal = ref(false)
const aiGenerating     = ref(false)
const aiSchemeGenerated = ref(false)
const assigning        = ref(false)

// 今日日期显示
const today = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\//g, '年').replace(/(\d{2})$/, '$1日')

// ── 客户列表状态 ──────────────────────────────────────────────────────────────
const customers   = ref([])
const total       = ref(0)
const currentPage = ref(1)
const PAGE_SIZE   = 20
const loading     = ref(false)
const exporting   = ref(false)
const selectAll   = ref(false)

// ── 筛选状态 ─────────────────────────────────────────────────────────────────
const filterValues = reactive({
    assign_status:  '',
    asset_level:    '',
    contact_status: '',
    hdly:           '',
    follow_status:  '',
    risk_level:     '',
    keyword:        '',
})

// 客户来源选项（动态从接口取）
const hdlyOptions = ref([])

// 筛选下拉配置（静态枚举 + 动态 HDLY）
const filterDefs = computed(() => [
    { key: 'assign_status',  label: '客户归属状态', opts: ['已分配', '未分配'] },
    { key: 'asset_level',    label: '客户级别',     opts: ['高价值', '中等价值', '低价值'] },
    { key: 'contact_status', label: '建联状态',     opts: ['已认证', '未添加或未绑定'] },
    { key: 'hdly',           label: '客户来源',     opts: hdlyOptions.value },
    { key: 'follow_status',  label: '跟进状态',     opts: ['未联系', '近3日内联系过', '近7日内联系过', '近15日内联系过', '近30日内联系过'] },
    { key: 'risk_level',     label: '风险级别',     opts: ['R1 保守型', 'R2 稳健型', 'R3 平衡型', 'R4 进取型', 'R5 激进型', '未测评'] },
])

// ── 分页计算 ──────────────────────────────────────────────────────────────────
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)))

const displayRange = computed(() => {
    if (total.value === 0) return '0'
    const start = (currentPage.value - 1) * PAGE_SIZE + 1
    const end   = Math.min(currentPage.value * PAGE_SIZE, total.value)
    return `${start}-${end}`
})

const pageNumbers = computed(() => {
    const tp  = totalPages.value
    const cur = currentPage.value
    const pages = []
    if (tp <= 7) {
        for (let i = 1; i <= tp; i++) pages.push(i)
    } else if (cur <= 4) {
        for (let i = 1; i <= 5; i++) pages.push(i)
        pages.push('...')
        pages.push(tp)
    } else if (cur >= tp - 3) {
        pages.push(1)
        pages.push('...')
        for (let i = tp - 4; i <= tp; i++) pages.push(i)
    } else {
        pages.push(1)
        pages.push('...')
        for (let i = cur - 1; i <= cur + 1; i++) pages.push(i)
        pages.push('...')
        pages.push(tp)
    }
    return pages
})

// ── 员工数据 ──────────────────────────────────────────────────────────────────
const staffList    = ref([])
const staffPage    = ref(1)
const staffPageSize = 4
const staffTotalPages = computed(() => Math.max(1, Math.ceil(staffList.value.length / staffPageSize)))
const paginatedStaffList = computed(() =>
    staffList.value.slice((staffPage.value - 1) * staffPageSize, staffPage.value * staffPageSize)
)

// 手动分配弹窗
const selectedStaff  = ref('')
const manualSearchQ  = ref('')
const assignRemark   = ref('')
const filteredStaffForManual = computed(() =>
    staffList.value.filter(s =>
        !manualSearchQ.value ||
        s.emp_name.includes(manualSearchQ.value) ||
        s.login_id.toLowerCase().includes(manualSearchQ.value.toLowerCase())
    )
)

// AI 分配弹窗
const selectedAIStaff = ref([])
const aiSearchQ       = ref('')
const aiStaffValid    = computed(() => selectedAIStaff.value.length >= 2)
const filteredStaffForAI = computed(() =>
    staffList.value.filter(s =>
        !aiSearchQ.value ||
        s.emp_name.includes(aiSearchQ.value) ||
        s.login_id.toLowerCase().includes(aiSearchQ.value.toLowerCase())
    )
)

// 已选客户
const selectedCount    = computed(() => customers.value.filter(c => c.selected).length)
const selectedCustomers = computed(() => customers.value.filter(c => c.selected))

// ── API 调用 ──────────────────────────────────────────────────────────────────
const fetchCustomers = async () => {
    loading.value = true
    try {
        const res = await api.getCustomers({
            page:           currentPage.value,
            page_size:      PAGE_SIZE,
            keyword:        filterValues.keyword,
            assign_status:  filterValues.assign_status,
            asset_level:    filterValues.asset_level,
            contact_status: filterValues.contact_status,
            follow_status:  filterValues.follow_status,
            hdly:           filterValues.hdly,
            risk_level:     filterValues.risk_level,
        })
        customers.value = (res.data.list || []).map(c => ({ ...c, selected: false }))
        total.value     = res.data.total || 0
        selectAll.value = false
    } catch (e) {
        console.error('获取客户列表失败:', e.message)
    } finally {
        loading.value = false
    }
}

const fetchHdlyOptions = async () => {
    try {
        const res = await api.getHdlyOptions()
        hdlyOptions.value = res.data || []
    } catch (e) {
        console.error('获取渠道号选项失败:', e.message)
    }
}

const fetchStaffWorkload = async () => {
    try {
        const res = await api.getEmployeesWorkload()
        staffList.value = res.data || []
    } catch (e) {
        console.error('获取员工负载失败:', e.message)
    }
}

// ── 筛选操作 ──────────────────────────────────────────────────────────────────
const resetFilters = () => {
    Object.keys(filterValues).forEach(k => { filterValues[k] = '' })
    currentPage.value = 1
    fetchCustomers()
}

// 关键词实时搜索：输入停顿 300ms 后自动触发（防抖）
let _keywordTimer = null
watch(() => filterValues.keyword, () => {
    clearTimeout(_keywordTimer)
    _keywordTimer = setTimeout(() => {
        currentPage.value = 1
        fetchCustomers()
    }, 300)
})

// 下拉筛选条件变化时立即触发
const filterKeys = Object.keys(filterValues).filter(k => k !== 'keyword')
filterKeys.forEach(key => {
    watch(() => filterValues[key], () => {
        currentPage.value = 1
        fetchCustomers()
    })
})

// ── 分页操作 ──────────────────────────────────────────────────────────────────
const goToPage = (p) => {
    if (p < 1 || p > totalPages.value) return
    currentPage.value = p
    fetchCustomers()
}

// ── 全选 ──────────────────────────────────────────────────────────────────────
const toggleSelectAll = () => {
    customers.value.forEach(c => { c.selected = selectAll.value })
}

// ── CSS 辅助函数 ──────────────────────────────────────────────────────────────
const getLevelClass = (level) => {
    if (level === '高价值')   return 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
    if (level === '中等价值') return 'bg-indigo-500/10 text-indigo-400'
    return 'bg-zinc-800 text-zinc-400'
}

const getContactClass = (status) => {
    if (status === '已认证') return 'text-emerald-500'
    return 'text-zinc-500'
}

const getFollowClass = (status) => {
    if (status === '近3日内联系过')  return 'text-emerald-400'
    if (status === '近7日内联系过')  return 'text-teal-400'
    if (status === '近15日内联系过') return 'text-amber-400'
    if (status === '近30日内联系过') return 'text-orange-400'
    return 'text-zinc-600'   // 未联系
}

const AVATAR_COLORS = ['text-indigo-400', 'text-emerald-400', 'text-rose-400', 'text-amber-400', 'text-purple-400', 'text-cyan-400', 'text-green-400', 'text-sky-400']
const getAvatarClass = (idx) => AVATAR_COLORS[idx % AVATAR_COLORS.length]

const getLoadStatusClass = (level) => {
    if (level === '高负载') return 'bg-rose-500/10 text-rose-500 border-rose-500/20'
    if (level === '偏高')   return 'bg-amber-500/10 text-amber-500 border-amber-500/20'
    if (level === '适中')   return 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20'
    if (level === '偏低')   return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
    if (level === '空闲')   return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
    return 'bg-zinc-800 text-zinc-400 border-zinc-700'
}

// ── 分配操作 ──────────────────────────────────────────────────────────────────
const openManualModal = () => {
    selectedStaff.value = ''
    assignRemark.value  = ''
    manualSearchQ.value = ''
    showManualModal.value = true
}

const quickAssign = (customer) => {
    // 选中该客户并打开手动分配弹窗
    customers.value.forEach(c => { c.selected = false })
    customer.selected = true
    openManualModal()
}

const quickAssignToStaff = (staff) => {
    if (staff.load_level === '高负载') return
    showManualModal.value = true
    selectedStaff.value = staff.login_id
}

const confirmManualAssign = async () => {
    if (!selectedStaff.value || selectedCustomers.value.length === 0) return
    const emp = staffList.value.find(s => s.login_id === selectedStaff.value)
    if (!emp) return

    assigning.value = true
    const names = selectedCustomers.value.map(c => c.cust_name)
    try {
        await api.assignCustomers({
            client_ids: selectedCustomers.value.map(c => c.fund_account),
            login_id:   emp.login_id,
            emp_name:   emp.emp_name,
        })
        showManualModal.value = false
        // 写侧边栏日志
        const nameStr = names.length === 1
            ? `<span class="text-indigo-400">${names[0]}</span>`
            : `<span class="text-indigo-400">${names[0]}</span> 等 ${names.length} 位客户`
        _pushLog(`陈经理 将 ${nameStr} 分配给 <span class="text-zinc-100">${emp.emp_name}</span>`)
        await Promise.all([fetchCustomers(), fetchStaffWorkload()])
    } catch (e) {
        alert('分配失败：' + e.message)
    } finally {
        assigning.value = false
    }
}

const revokeOne = async (customer) => {
    if (!confirm(`确认撤回客户 ${customer.cust_name} 的分配关系？`)) return
    try {
        await api.revokeCustomers({ client_ids: [customer.fund_account] })
        _pushLog(`陈经理 撤回了 <span class="text-indigo-400">${customer.cust_name}</span> 与 <span class="text-zinc-100">${customer.assignee_nm}</span> 的分配关系`)
        await Promise.all([fetchCustomers(), fetchStaffWorkload()])
    } catch (e) {
        alert('撤回失败：' + e.message)
    }
}

const revokeSelected = async () => {
    const revokable = selectedCustomers.value.filter(c => c.assign_source === 1)
    if (revokable.length === 0) {
        alert('未选中任何可撤回的客户（仅手动分配的客户可撤回）')
        return
    }
    if (!confirm(`确认撤回 ${revokable.length} 个客户的分配关系？`)) return
    try {
        await api.revokeCustomers({ client_ids: revokable.map(c => c.fund_account) })
        _pushLog(`陈经理 批量撤回了 <span class="text-indigo-400">${revokable.length} 个客户</span> 的分配关系`)
        await Promise.all([fetchCustomers(), fetchStaffWorkload()])
    } catch (e) {
        alert('批量撤回失败：' + e.message)
    }
}

// ── AI 分配 ───────────────────────────────────────────────────────────────────
const openAIModal = () => {
    showAIModal.value       = true
    aiSchemeGenerated.value = false
    aiGenerating.value      = false
    selectedAIStaff.value   = []
    aiSearchQ.value         = ''
    aiPlans.value           = []
}

const toggleAIStaff = (loginId) => {
    const idx = selectedAIStaff.value.indexOf(loginId)
    if (idx >= 0) selectedAIStaff.value.splice(idx, 1)
    else selectedAIStaff.value.push(loginId)
}

// 前端负载均衡分配算法（与后端 _smart_distribute 逻辑一致）
const _computePlan = (customers, employees) => {
    if (!employees.length || !customers.length) return []

    // 按客户数升序（负载低的优先）
    const emps = [...employees].sort((a, b) => a.cust_count - b.cust_count)
    const weights = emps.map(e => 1 / (e.cust_count + 1))
    const wSum    = weights.reduce((s, w) => s + w, 0)
    const n       = customers.length
    const quotas  = weights.map(w => Math.floor(n * w / wSum))
    let rem = n - quotas.reduce((s, q) => s + q, 0)
    // 余量补给权重最高的员工
    const byW = emps.map((_, i) => i).sort((a, b) => weights[b] - weights[a])
    for (let i = 0; i < rem; i++) quotas[byW[i % byW.length]]++

    // 高价值优先分配
    const ordered = [
        ...customers.filter(c => c.asset_level === '高价值'),
        ...customers.filter(c => c.asset_level === '中等价值'),
        ...customers.filter(c => c.asset_level === '低价值'),
    ]

    const plans = []
    let offset = 0
    emps.forEach((emp, idx) => {
        const qty = quotas[idx]
        if (qty === 0) return
        const allocated = ordered.slice(offset, offset + qty)
        offset += qty
        const hvCount = allocated.filter(c => c.asset_level === '高价值').length
        const reasons = {
            '空闲': '负载空闲，优先承接新客户',
            '偏低': '负载偏低，适合接收更多客户',
            '适中': '负载适中，均衡分配',
            '偏高': '负载均衡调配',
            '高负载': '负载均衡调配',
        }
        plans.push({
            avatar:      emp.emp_name[0],
            name:        emp.emp_name,
            login_id:    emp.login_id,
            count:       qty,
            reason:      '原因：' + (reasons[emp.load_level] || '均衡分配'),
            borderClass: idx === 0 ? 'border-indigo-600/30 bg-indigo-600/5' : 'border-zinc-800 bg-zinc-900/50',
            loadColor:   'text-emerald-500',
            loadChange:  `负载 ${emp.cust_count} → ${emp.cust_count + qty}`,
            highValue:   hvCount,
            customers:   allocated,   // 完整客户对象，供详情弹窗使用
        })
    })
    return plans
}

const generateAIScheme = () => {
    if (!aiStaffValid.value || selectedCustomers.value.length === 0) return
    aiGenerating.value = true
    setTimeout(() => {
        const emps = staffList.value.filter(s => selectedAIStaff.value.includes(s.login_id))
        aiPlans.value           = _computePlan(selectedCustomers.value, emps)
        aiGenerating.value      = false
        aiSchemeGenerated.value = true
    }, 1200)
}

const confirmAllocation = async () => {
    if (!aiPlans.value.length) {
        showManualModal.value = showAIModal.value = showAIDetailModal.value = false
        return
    }
    try {
        const clientIds   = aiPlans.value.flatMap(p => p.customers.map(c => c.fund_account))
        const employeeIds = aiPlans.value.map(p => p.login_id)
        await api.smartAssign({ client_ids: clientIds, employee_ids: employeeIds })

        // 侧边栏日志
        const total    = clientIds.length
        const empNames = aiPlans.value.map(p => p.name).join('、')
        _pushLog(`陈经理 <span class="text-indigo-400 font-medium">AI智能分配</span> 了 <span class="text-indigo-400">${total} 个客户</span> 至 ${empNames}`)

        showManualModal.value = showAIModal.value = showAIDetailModal.value = false
        await Promise.all([fetchCustomers(), fetchStaffWorkload()])
    } catch (e) {
        alert('智能分配失败：' + e.message)
    }
}

// ── AI 方案详情（从 aiPlans 动态派生） ────────────────────────────────────────
const aiPlans = ref([])

const aiDetailPlans = computed(() =>
    aiPlans.value.map(p => ({
        staffName:   p.name,
        staffAvatar: p.avatar,
        loadChange:  p.loadChange,
        reason:      p.reason,
        customers:   p.customers.map(c => ({
            fundAccount:  c.fund_account,
            name:         c.cust_name,
            aum:          c.t1_aum,
            level:        c.asset_level,
            levelClass:   getLevelClass(c.asset_level),
            risk:         c.risk_level,
            contact:      c.contact_status,
            contactClass: getContactClass(c.contact_status),
        })),
    }))
)

const aiDetailTotalCount = computed(() => aiDetailPlans.value.reduce((s, g) => s + g.customers.length, 0))

const aiDetailStats = computed(() => {
    const all = aiDetailPlans.value.flatMap(g => g.customers)
    return [
        { label: '总客户',   value: all.length + ' 个',                                          dot: 'bg-indigo-500' },
        { label: '高价值',   value: all.filter(c => c.level === '高价值').length   + ' 个',      dot: 'bg-rose-500'   },
        { label: '中等价值', value: all.filter(c => c.level === '中等价值').length + ' 个',      dot: 'bg-indigo-400' },
        { label: '低价值',   value: all.filter(c => c.level === '低价值').length   + ' 个',      dot: 'bg-zinc-500'   },
    ]
})

const aiRules = ref([
    { label: '员工负载均衡', icon: 'solar:scale-bold-duotone',         desc: '优先分配给空闲员工，避免超载',   checked: true  },
    { label: '客户价值匹配', icon: 'solar:star-bold-duotone',          desc: '高价值客户匹配至高产能员工',     checked: false },
    { label: '员工擅长偏好', icon: 'solar:medal-ribbon-bold-duotone',  desc: '按客户风险偏好匹配对应员工',     checked: false },
])

// ── 分配记录弹窗（数据暂 Mock，待接入 /api/manager/assign-logs 接口） ──────────
const showHistoryModal_   = ref(false)  // alias 防止命名冲突
const selectedHistoryMonth = ref('2026-05')
const historyFilter = reactive({ operator: '', customerKeyword: '', receiverKeyword: '' })
const hasHistoryFilter = computed(() => !!(historyFilter.operator || historyFilter.customerKeyword || historyFilter.receiverKeyword))
const resetHistoryFilter = () => { historyFilter.operator = ''; historyFilter.customerKeyword = ''; historyFilter.receiverKeyword = '' }

const historyMonths = computed(() => {
    const months = []
    const now = new Date()
    for (let i = 0; i < 12; i++) {
        const d = new Date(now.getFullYear(), now.getMonth() - i, 1)
        const y = d.getFullYear()
        const m = String(d.getMonth() + 1).padStart(2, '0')
        months.push({ value: `${y}-${m}`, label: i === 0 ? `${y}年${m}月（当月）` : `${y}年${m}月` })
    }
    return months
})

const historyLogs = ref([
    { id: 1,  month: '2026-05', operator: '陈经理', operateTime: '2026-05-21 10:32', fundAccount: 'C10024', customerName: '张晨曦', receiverName: '陈梅云', receiverOA: 'OA20231104', action: '手动分配', actionClass: 'bg-indigo-500/10 text-indigo-400' },
    { id: 2,  month: '2026-05', operator: '陈经理', operateTime: '2026-05-20 14:15', fundAccount: 'C10089', customerName: '李梦婷', receiverName: '李明晨', receiverOA: 'OA20220315', action: '智能分配', actionClass: 'bg-purple-500/10 text-purple-400' },
    { id: 3,  month: '2026-05', operator: '陈经理', operateTime: '2026-05-19 09:48', fundAccount: 'C10189', customerName: '孙鹏',   receiverName: '刘至',   receiverOA: 'OA20210801', action: '智能分配', actionClass: 'bg-purple-500/10 text-purple-400' },
    { id: 4,  month: '2026-05', operator: '系统',   operateTime: '2026-05-12 00:00', fundAccount: 'C10256', customerName: '周丽华', receiverName: null,     receiverOA: null,         action: '关系撤销', actionClass: 'bg-rose-500/10 text-rose-400' },
    { id: 5,  month: '2026-04', operator: '陈经理', operateTime: '2026-04-28 16:22', fundAccount: 'C10102', customerName: '刘建国', receiverName: '陈梅云', receiverOA: 'OA20231104', action: '手动分配', actionClass: 'bg-indigo-500/10 text-indigo-400' },
    { id: 6,  month: '2026-04', operator: '陈经理', operateTime: '2026-04-15 11:05', fundAccount: 'C10123', customerName: '赵美粒', receiverName: '王涛',   receiverOA: 'OA20190520', action: '智能分配', actionClass: 'bg-purple-500/10 text-purple-400' },
    { id: 7,  month: '2026-03', operator: '陈经理', operateTime: '2026-03-18 10:00', fundAccount: 'C10201', customerName: '王静茹', receiverName: '赵晓燕', receiverOA: 'OA20200612', action: '手动分配', actionClass: 'bg-indigo-500/10 text-indigo-400' },
])

const filteredHistoryLogs = computed(() =>
    historyLogs.value.filter(log => {
        if (log.month !== selectedHistoryMonth.value) return false
        if (historyFilter.operator && !log.operator.includes(historyFilter.operator)) return false
        if (historyFilter.customerKeyword) {
            const kw = historyFilter.customerKeyword.toLowerCase()
            if (!log.customerName.toLowerCase().includes(kw) && !log.fundAccount.toLowerCase().includes(kw)) return false
        }
        if (historyFilter.receiverKeyword) {
            const kw = historyFilter.receiverKeyword.toLowerCase()
            const nameHit = log.receiverName?.toLowerCase().includes(kw) ?? false
            const oaHit   = log.receiverOA?.toLowerCase().includes(kw) ?? false
            if (!nameHit && !oaHit) return false
        }
        return true
    })
)

// ── 导出客户明细 ──────────────────────────────────────────────────────────────
const exportCustomers = async () => {
    if (exporting.value) return
    exporting.value = true
    try {
        // 拉取当前筛选条件下的全量数据（page_size=9999）
        const res = await api.getCustomers({
            page:           1,
            page_size:      9999,
            keyword:        filterValues.keyword,
            assign_status:  filterValues.assign_status,
            asset_level:    filterValues.asset_level,
            contact_status: filterValues.contact_status,
            follow_status:  filterValues.follow_status,
            hdly:           filterValues.hdly,
            risk_level:     filterValues.risk_level,
        })
        const rows = res.data.list || []
        if (rows.length === 0) {
            alert('当前筛选条件下没有客户数据可导出')
            return
        }

        const headers = ['资金账号', '客户姓名', '手机号', 'T-1日AUM资产（万）',
                         '资产等级', '风险等级', '建联状态', '跟进状态',
                         '客户来源', '归属人', '分配时间', '分配操作人']
        const dataRows = rows.map(c => [
            c.fund_account,
            c.cust_name,
            c.phone,
            c.t1_aum,
            c.asset_level,
            c.risk_level,
            c.contact_status,
            c.follow_status   || '',
            c.hdly            || '',
            c.assignee_nm     || '',
            c.assign_time     || '',
            c.operator_nm     || '',
        ])

        const escape = v => `"${String(v ?? '').replace(/"/g, '""')}"`
        const csv = '﻿' + [headers, ...dataRows]
            .map(r => r.map(escape).join(','))
            .join('\r\n')

        const ts   = new Date().toISOString().slice(0, 19).replace(/[-:T]/g, '').replace('T', '_')
        const name = `客户详情_${ts}.csv`
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
        const url  = URL.createObjectURL(blob)
        const a    = Object.assign(document.createElement('a'), { href: url, download: name })
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
    } catch (e) {
        alert('导出失败：' + e.message)
    } finally {
        exporting.value = false
    }
}

const exportHistory = () => {
    const headers = ['操作人员', '操作时间', '资金账号', '客户姓名', '接收员工姓名', '接收员工OA', '操作内容']
    const rows = filteredHistoryLogs.value.map(log => [log.operator, log.operateTime, log.fundAccount, log.customerName, log.receiverName ?? '—', log.receiverOA ?? '—', log.action])
    const csv  = '﻿' + [headers, ...rows].map(r => r.map(v => `"${String(v).replace(/"/g, '""')}"`).join(',')).join('\r\n')
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href = url; a.download = `分配记录_${selectedHistoryMonth.value}.csv`
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url)
}

// ── 侧边栏分配记录（实时写入） ─────────────────────────────────────────────────
const assignmentLogs = ref([])   // { ts: Number, dotClass: String, text: String }
const _clockNow = ref(Date.now())
let _clockTimer = null

const _relTime = (ts) => {
    const s = Math.floor((_clockNow.value - ts) / 1000)
    if (s < 10)    return '刚刚'
    if (s < 3600)  return `${Math.floor(s / 60) || 1}分钟前`
    if (s < 86400) return `${Math.floor(s / 3600)}小时前`
    return '昨天'
}

const _pushLog = (text, fresh = true) => {
    assignmentLogs.value.unshift({
        ts:       Date.now(),
        dotClass: fresh ? 'bg-indigo-600 ring-4 ring-indigo-600/10' : 'bg-zinc-700',
        text,
    })
    if (assignmentLogs.value.length > 20) assignmentLogs.value.pop()
}

// ── 每日提醒 ──────────────────────────────────────────────────────────────────
const ALERT_LOGIN_ID = 'oa001'   // TODO: 接入认证后换成当前登录人 OA

const alertPanelOpen   = ref(false)
const alerts           = ref([])
const newAlertContent  = ref('')

const unreadAlertCount = computed(() => alerts.value.length)

const toggleAlertPanel = () => {
    alertPanelOpen.value = !alertPanelOpen.value
}

// 点击面板外部关闭
const _onClickOutsideAlert = (e) => {
    const panel = document.querySelector('.alert-panel-wrapper')
    if (panel && !panel.contains(e.target)) {
        alertPanelOpen.value = false
    }
}

const fetchAlerts = async () => {
    try {
        const res  = await fetch(`/api/manager/alerts?login_id=${ALERT_LOGIN_ID}`)
        const json = await res.json()
        if (json.code === 200) alerts.value = json.data
    } catch (e) {
        console.error('fetchAlerts error', e)
    }
}

const markAlertDone = async (alert) => {
    alert._marking = true
    try {
        const res  = await fetch(`/api/manager/alerts/${alert.alert_id}/done`, { method: 'PATCH' })
        const json = await res.json()
        if (json.code === 200) {
            alerts.value = alerts.value.filter(a => a.alert_id !== alert.alert_id)
        }
    } catch (e) {
        console.error('markAlertDone error', e)
    } finally {
        alert._marking = false
    }
}

const addAlert = async () => {
    const content = newAlertContent.value.trim()
    if (!content) return
    try {
        const res  = await fetch('/api/manager/alerts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login_id: ALERT_LOGIN_ID, alert_content: content }),
        })
        const json = await res.json()
        if (json.code === 200) {
            alerts.value.unshift(json.data)
            newAlertContent.value = ''
        }
    } catch (e) {
        console.error('addAlert error', e)
    }
}

// ── 生命周期 ──────────────────────────────────────────────────────────────────
onMounted(async () => {
    _clockTimer = setInterval(() => { _clockNow.value = Date.now() }, 30000)
    document.addEventListener('click', _onClickOutsideAlert)
    await Promise.all([
        fetchCustomers(),
        fetchHdlyOptions(),
        fetchStaffWorkload(),
        fetchAlerts(),
    ])
})

onUnmounted(() => {
    clearInterval(_clockTimer)
    document.removeEventListener('click', _onClickOutsideAlert)
})
</script>

<style scoped>
.manager-page {
    font-family: 'Inter', -apple-system, sans-serif;
    background-color: #09090b;
    color: #f4f4f5;
    height: 100vh;
    overflow: hidden;
    display: flex;
}

.manager-sidebar {
    width: 256px;
    height: 100vh;
    background: #09090b;
    border-right: 1px solid #27272a;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.manager-sidebar.collapsed { width: 76px; }

.manager-sidebar.collapsed .logo-text,
.manager-sidebar.collapsed .nav-text,
.manager-sidebar.collapsed .user-info-text { display: none; }

.manager-sidebar.collapsed .nav-item { justify-content: center; padding-left: 0; padding-right: 0; }
.manager-sidebar.collapsed .logo-container { justify-content: center; }

.custom-scrollbar::-webkit-scrollbar { width: 5px; height: 5px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #27272a; border-radius: 10px; }

.modal-backdrop { background-color: rgba(0,0,0,0.75); backdrop-filter: blur(4px); }
</style>
