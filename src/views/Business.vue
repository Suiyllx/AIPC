<template>
    <div class="business-hall">
        <!-- 侧边导航 (主导航) -->
        <aside class="bg-white border-r border-slate-200 flex flex-col h-screen shrink-0 relative z-50"
            :class="{ collapsed: sidebarCollapsed }" id="sidebar">
            <div class="h-16 flex items-center px-6 border-b border-slate-100 logo-container">
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shrink-0">
                        <iconify-icon class="text-white text-xl" icon="lucide:sparkles"></iconify-icon>
                    </div>
                    <span class="text-lg font-bold text-slate-900 logo-text truncate">AI展业平台</span>
                </div>
            </div>
            <nav class="flex-1 px-4 space-y-1 mt-4">
                <router-link
                    class="nav-item flex items-center px-4 py-3 text-gray-500 hover:bg-blue-50 hover:text-blue-600 rounded-xl transition-all group"
                    active-class="bg-blue-600 text-white shadow-lg shadow-blue-200"
                    to="/">
                    <iconify-icon class="text-2xl mr-3 shrink-0" icon="solar:widget-5-bold-duotone"></iconify-icon>
                    <span class="nav-text font-medium whitespace-nowrap">工作台总览</span>
                </router-link>
                <router-link
                    class="nav-item flex items-center px-4 py-3 text-gray-500 hover:bg-blue-50 hover:text-blue-600 rounded-xl transition-all group"
                    active-class="bg-blue-600 text-white shadow-lg shadow-blue-200"
                    to="/tasks">
                    <iconify-icon class="text-2xl mr-3 shrink-0" icon="solar:clipboard-check-bold-duotone"></iconify-icon>
                    <span class="nav-text font-medium whitespace-nowrap">任务大厅</span>
                </router-link>
                <router-link
                    class="nav-item flex items-center px-4 py-3 text-gray-500 hover:bg-blue-50 hover:text-blue-600 rounded-xl transition-all group"
                    active-class="bg-blue-600 text-white shadow-lg shadow-blue-200"
                    to="/business">
                    <iconify-icon class="text-2xl mr-3 shrink-0" icon="solar:shop-2-bold-duotone"></iconify-icon>
                    <span class="nav-text font-medium whitespace-nowrap">展业大厅</span>
                </router-link>
                <router-link
                    class="nav-item flex items-center px-4 py-3 text-gray-500 hover:bg-blue-50 hover:text-blue-600 rounded-xl transition-all group"
                    active-class="bg-blue-600 text-white shadow-lg shadow-blue-200"
                    to="/performance">
                    <iconify-icon class="text-2xl mr-3 shrink-0" icon="solar:ranking-bold-duotone"></iconify-icon>
                    <span class="nav-text font-medium whitespace-nowrap">绩效看板</span>
                </router-link>
            </nav>
            <div class="p-4 border-t border-slate-100">
                <div class="flex items-center gap-3 p-2 rounded-lg bg-slate-50">
                    <img alt="User Avatar" class="w-9 h-9 rounded-full border border-white shadow-sm shrink-0"
                        src="https://modao.cc/agent-py/media/generated_images/2026-05-07/e55878641a804c228989fafb3cca03cd.jpg#desc=User%20Avatar" />
                    <div class="user-info-text overflow-hidden">
                        <p class="text-sm font-semibold text-slate-900 truncate">张超越</p>
                        <p class="text-xs text-slate-500 truncate">最后登录: 2026-05-07</p>
                    </div>
                </div>
            </div>
        </aside>

        <!-- 主体内容 -->
        <main class="flex-1 flex flex-col min-w-0 bg-[#F8FAFC]">
            <!-- 顶部导航栏 -->
            <header
                class="h-16 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-6 shrink-0 sticky top-0 z-40">
                <div class="flex items-center gap-4">
                    <button class="p-2 hover:bg-slate-100 rounded-lg transition-colors" @click="toggleSidebar">
                        <iconify-icon class="text-xl text-slate-600" icon="lucide:menu"></iconify-icon>
                    </button>
                    <div class="h-6 w-px bg-slate-200"></div>
                    <span class="text-sm font-medium text-slate-500">今天是 {{ todayStr }}</span>
                </div>
                <div class="flex items-center gap-4">
                    <!-- 角色切换 -->
                    <div class="flex items-center gap-1 bg-slate-100 rounded-lg p-1 text-xs font-medium">
                        <span class="px-2.5 py-1 bg-white text-slate-900 rounded-md shadow-sm">营销人员</span>
                        <router-link class="px-2.5 py-1 text-slate-500 hover:text-slate-700 rounded-md transition-all" to="/manager">管理人员</router-link>
                    </div>
                    <!-- 每日提醒铃铛 -->
                    <div class="relative alert-panel-wrapper">
                        <button @click="alertPanelOpen = !alertPanelOpen"
                                class="p-2 hover:bg-slate-100 rounded-lg relative transition-colors">
                            <iconify-icon class="text-xl text-slate-600" icon="lucide:bell"></iconify-icon>
                            <span v-if="unreadAlertCount > 0"
                                  class="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
                        </button>
                        <!-- 提醒面板 -->
                        <div v-if="alertPanelOpen"
                             class="absolute right-0 top-12 w-96 bg-white border border-gray-200 rounded-xl shadow-2xl z-50 flex flex-col"
                             style="max-height: 520px;">
                            <!-- 面板标题 -->
                            <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
                                <span class="text-sm font-semibold text-gray-800">每日提醒</span>
                                <span class="text-xs text-gray-400">近30天未完成（{{ unreadAlertCount }} 条）</span>
                            </div>
                            <!-- 提醒列表 -->
                            <div class="flex-1 overflow-y-auto divide-y divide-gray-100">
                                <div v-if="alerts.length === 0" class="py-10 text-center text-gray-400 text-sm">
                                    暂无未完成提醒
                                </div>
                                <div v-for="alert in alerts" :key="alert.alert_id"
                                     class="flex items-start gap-3 px-4 py-3 hover:bg-gray-50 transition-colors">
                                    <button @click="markAlertDone(alert)"
                                            class="mt-0.5 w-4 h-4 rounded border border-gray-300 flex-shrink-0 hover:border-blue-400 transition-colors flex items-center justify-center">
                                        <iconify-icon v-if="alert._marking" icon="svg-spinners:ring-resize" class="text-blue-400 text-xs"></iconify-icon>
                                    </button>
                                    <div class="flex-1 min-w-0">
                                        <p class="text-sm text-gray-700 leading-snug">{{ alert.alert_content }}</p>
                                        <p class="text-xs text-gray-400 mt-1">{{ alert.alert_date }}</p>
                                    </div>
                                </div>
                            </div>
                            <!-- 新增提醒输入框 -->
                            <div class="px-4 py-3 border-t border-gray-100">
                                <div class="flex gap-2">
                                    <input v-model="newAlertContent"
                                           @keydown.enter="addAlert"
                                           placeholder="新增提醒…"
                                           class="flex-1 bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-lg px-3 py-2 outline-none placeholder-gray-400 focus:ring-1 focus:ring-blue-500" />
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

            <!-- 二级 Tab 导航 -->
            <div class="bg-white border-b border-gray-100 px-6 flex items-center overflow-x-auto shrink-0 no-scrollbar">
                <button
                    class="hall-tab flex items-center space-x-2 px-4 py-3.5 text-sm font-medium whitespace-nowrap transition-all border-b-2 -mb-px"
                    :class="currentPage === 'customer-list' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    @click="switchHallPage('customer-list')">
                    <iconify-icon icon="solar:users-group-rounded-linear"></iconify-icon>
                    <span>我的客户列表</span>
                </button>
                <button
                    class="hall-tab flex items-center space-x-2 px-4 py-3.5 text-sm font-medium whitespace-nowrap transition-all border-b-2 -mb-px"
                    :class="currentPage === 'sop' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    @click="switchHallPage('sop')">
                    <iconify-icon icon="solar:notebook-bold-duotone"></iconify-icon>
                    <span>标准展业流程 (SOP)</span>
                </button>
                <button
                    class="hall-tab flex items-center space-x-2 px-4 py-3.5 text-sm font-medium whitespace-nowrap transition-all border-b-2 -mb-px"
                    :class="currentPage === 'bulk-calling' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    @click="switchHallPage('bulk-calling')">
                    <iconify-icon icon="solar:phone-calling-bold-duotone"></iconify-icon>
                    <span>批量外呼 (双呼)</span>
                </button>
                <button
                    class="hall-tab flex items-center space-x-2 px-4 py-3.5 text-sm font-medium whitespace-nowrap transition-all border-b-2 -mb-px"
                    :class="currentPage === 'ai-chat' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    @click="switchHallPage('ai-chat')">
                    <iconify-icon icon="solar:magic-stick-3-bold-duotone"></iconify-icon>
                    <span>智能问答 (AI)</span>
                </button>
                <button
                    class="hall-tab flex items-center space-x-2 px-4 py-3.5 text-sm font-medium whitespace-nowrap transition-all border-b-2 -mb-px"
                    :class="currentPage === 'marketing-materials' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    @click="switchHallPage('marketing-materials')">
                    <iconify-icon icon="solar:gallery-bold-duotone"></iconify-icon>
                    <span>营销素材中心</span>
                </button>
                <button
                    class="hall-tab flex items-center space-x-2 px-4 py-3.5 text-sm font-medium whitespace-nowrap transition-all border-b-2 -mb-px"
                    :class="currentPage === 'product-center' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    @click="switchHallPage('product-center')">
                    <iconify-icon icon="solar:box-bold-duotone"></iconify-icon>
                    <span>产品查询与推荐</span>
                </button>
                <button
                    class="hall-tab flex items-center space-x-2 px-4 py-3.5 text-sm font-medium whitespace-nowrap transition-all border-b-2 -mb-px"
                    :class="currentPage === 'activity-center' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    @click="switchHallPage('activity-center')">
                    <iconify-icon icon="solar:star-bold-duotone"></iconify-icon>
                    <span>营销活动中心</span>
                </button>
                <button
                    class="hall-tab flex items-center space-x-2 px-4 py-3.5 text-sm font-medium whitespace-nowrap transition-all border-b-2 -mb-px"
                    :class="currentPage === 'wechat-config' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    @click="switchHallPage('wechat-config')">
                    <iconify-icon icon="solar:settings-bold-duotone"></iconify-icon>
                    <span>企微侧边栏配置</span>
                </button>
                <button
                    class="hall-tab flex items-center space-x-2 px-4 py-3.5 text-sm font-medium whitespace-nowrap transition-all border-b-2 -mb-px"
                    :class="currentPage === 'ai-batch' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    @click="switchHallPage('ai-batch')">
                    <iconify-icon icon="solar:cpu-bolt-bold-duotone"></iconify-icon>
                    <span>AI 批量处理</span>
                </button>
            </div>

            <!-- 内容区域 -->
            <div class="flex-1 p-8 overflow-hidden flex flex-col">
                <!-- 我的客户列表 (DEFAULT PAGE) -->
                <div class="page-content space-y-6" :class="{ active: currentPage === 'customer-list' }"
                    id="page-customer-list">
                    <div class="flex items-center justify-between">
                        <div>
                            <h1 class="text-2xl font-bold text-gray-800 tracking-tight">我的客户列表</h1>
                            <p class="text-sm text-gray-400 mt-1">管理您名下的 428 位客户，支持多维度筛选与批量操作</p>
                        </div>
                        <div class="flex items-center space-x-3">
                            <button
                                @click="showColumnEditor = true"
                                class="px-4 py-2 bg-blue-50 border border-blue-200 text-blue-600 text-sm font-bold rounded-xl flex items-center shadow-sm hover:bg-blue-100 transition-all">
                                <iconify-icon class="mr-2" icon="solar:settings-minimalistic-linear"></iconify-icon> 编辑表头
                            </button>
                        </div>
                    </div>

                    <!-- 搜索与操作栏 -->
                    <div class="flex items-center gap-4">
                        <div class="flex-1 relative max-w-2xl">
                            <iconify-icon
                                class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-xl pointer-events-none"
                                icon="solar:magnifer-linear"></iconify-icon>
                            <input
                                v-model="keyword"
                                class="w-full bg-white border border-gray-200 rounded-xl py-2.5 pl-12 pr-4 text-sm focus:ring-2 focus:ring-blue-100 focus:border-transparent transition-all outline-none"
                                placeholder="搜索客户姓名、资金账号..." type="text" />
                        </div>
                        <button
                            @click="showToastMsg('功能开发中，敬请期待')"
                            class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2.5 rounded-xl text-sm font-bold shadow-lg shadow-blue-100 hover:bg-blue-700 transition-all shrink-0">
                            <iconify-icon class="text-lg" icon="solar:add-circle-linear"></iconify-icon>
                            <span>新建触达任务</span>
                        </button>
                    </div>

                    <!-- 筛选区 -->
                    <div class="data-card p-5">
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                            <!-- 建联状态 -->
                            <div class="space-y-1.5">
                                <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">建联状态</label>
                                <select v-model="filterForm.contactStatus"
                                    class="w-full bg-gray-50 border border-gray-200 rounded-lg text-xs font-semibold text-gray-700 focus:ring-2 focus:ring-blue-100 focus:border-blue-400 py-2 px-3 outline-none transition-all">
                                    <option value="">全部</option>
                                    <option value="已认证">已认证</option>
                                    <option value="未添加或未绑定">未添加或未绑定</option>
                                </select>
                            </div>
                            <!-- 资产等级 -->
                            <div class="space-y-1.5">
                                <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">资产等级</label>
                                <select v-model="filterForm.assetLevel"
                                    class="w-full bg-gray-50 border border-gray-200 rounded-lg text-xs font-semibold text-gray-700 focus:ring-2 focus:ring-blue-100 focus:border-blue-400 py-2 px-3 outline-none transition-all">
                                    <option value="">全部</option>
                                    <option value="高价值">高价值</option>
                                    <option value="中等价值">中等价值</option>
                                    <option value="低价值">低价值</option>
                                </select>
                            </div>
                            <!-- 跟进状态 -->
                            <div class="space-y-1.5">
                                <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">跟进状态</label>
                                <select v-model="filterForm.follow_status"
                                    class="w-full bg-gray-50 border border-gray-200 rounded-lg text-xs font-semibold text-gray-700 focus:ring-2 focus:ring-blue-100 focus:border-blue-400 py-2 px-3 outline-none transition-all">
                                    <option value="">全部</option>
                                    <option value="未联系">未联系</option>
                                    <option value="近3日内联系过">近3日内联系过</option>
                                    <option value="近7日内联系过">近7日内联系过</option>
                                    <option value="近15日内联系过">近15日内联系过</option>
                                    <option value="近30日内联系过">近30日内联系过</option>
                                </select>
                            </div>
                            <!-- 风险等级 -->
                            <div class="space-y-1.5">
                                <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">风险等级</label>
                                <select v-model="filterForm.riskLevel"
                                    class="w-full bg-gray-50 border border-gray-200 rounded-lg text-xs font-semibold text-gray-700 focus:ring-2 focus:ring-blue-100 focus:border-blue-400 py-2 px-3 outline-none transition-all">
                                    <option value="">全部</option>
                                    <option value="未测评">未测评</option>
                                    <option value="R1 保守型">R1 保守型</option>
                                    <option value="R2 稳健型">R2 稳健型</option>
                                    <option value="R3 平衡型">R3 平衡型</option>
                                    <option value="R4 进取型">R4 进取型</option>
                                    <option value="R5 激进型">R5 激进型</option>
                                </select>
                            </div>
                        </div>
                        <div class="flex items-center justify-end gap-2">
                            <button @click="resetFilter"
                                class="px-4 py-2 border border-gray-200 text-gray-500 text-xs font-bold rounded-lg hover:bg-gray-50 transition-all flex items-center gap-1.5">
                                <iconify-icon icon="solar:restart-bold" width="13"></iconify-icon>
                                重置
                            </button>
                        </div>
                    </div>

                    <!-- 批量操作栏 -->
                    <div
                        class="flex items-center justify-between py-2 px-4 bg-blue-50/50 border border-blue-100 rounded-2xl">
                        <div class="flex items-center space-x-4">
                            <div class="flex items-center">
                                <input class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-0"
                                    type="checkbox" />
                                <span class="ml-2 text-sm font-bold text-gray-600">全选 (已选 0)</span>
                            </div>
                            <div class="h-4 w-px bg-blue-200"></div>
                            <button @click="showToastMsg('功能开发中，敬请期待')"
                                class="flex items-center space-x-1.5 text-xs font-bold text-blue-600 hover:text-blue-700">
                                <iconify-icon icon="solar:phone-calling-linear"></iconify-icon>
                                <span>批量加入外呼</span>
                            </button>
                            <button @click="showToastMsg('功能开发中，敬请期待')"
                                class="flex items-center space-x-1.5 text-xs font-bold text-blue-600 hover:text-blue-700">
                                <iconify-icon icon="solar:magic-stick-linear"></iconify-icon>
                                <span>AI 批量生成摘要</span>
                            </button>
                            <button @click="showToastMsg('功能开发中，敬请期待')"
                                class="flex items-center space-x-1.5 text-xs font-bold text-blue-600 hover:text-blue-700">
                                <iconify-icon icon="solar:forward-linear"></iconify-icon>
                                <span>加入任务大厅跟进</span>
                            </button>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="text-[10px] text-gray-400 font-bold uppercase shrink-0">排序:</span>
                            <select v-model="sortField"
                                class="bg-white border border-gray-200 rounded-lg text-[11px] font-semibold text-gray-600 focus:ring-0 px-2 py-1 cursor-pointer outline-none">
                                <option value="t1_aum">AUM 资产</option>
                                <option value="follow_status">跟进状态</option>
                                <option value="open_date">开户日期</option>
                                <option value="age">年龄</option>
                                <option value="annual_return">本年收益</option>
                                <option value="commission_this_year">本年佣金贡献</option>
                                <option value="commission_last_year">去年佣金贡献</option>
                                <option value="commission_rate">佣金费率</option>
                                <option value="trade_exp_months">交易经验（月）</option>
                            </select>
                            <button @click="sortDir = sortDir === 'asc' ? 'desc' : 'asc'"
                                class="flex items-center gap-1 px-2 py-1 border border-gray-200 bg-white rounded-lg text-[11px] font-semibold text-gray-600 hover:bg-gray-50 transition-all">
                                <iconify-icon :icon="sortDir === 'asc' ? 'solar:sort-from-top-to-bottom-bold' : 'solar:sort-from-bottom-to-top-bold'" width="12"></iconify-icon>
                                {{ sortDir === 'asc' ? '正序' : '倒序' }}
                            </button>
                        </div>
                    </div>

                    <!-- 客户列表 -->
                    <div class="data-card overflow-hidden">
                        <div class="overflow-x-auto no-scrollbar">
                            <table class="w-full border-collapse min-w-max">
                                <thead>
                                    <tr class="border-b border-gray-200">
                                        <!-- 复选框列 -->
                                        <th class="pl-5 pr-3 py-3.5 w-10 bg-gray-50/80"></th>
                                        <!-- 客户基本信息（固定） -->
                                        <th class="px-4 py-3.5 text-[10px] font-bold text-gray-400 uppercase tracking-widest whitespace-nowrap text-left bg-gray-50/80 min-w-[210px]">
                                            客户基本信息
                                        </th>
                                        <!-- 动态列：对齐方式由 col.align 决定 -->
                                        <th v-for="col in enabledColumns" :key="col.key"
                                            class="px-4 py-3.5 text-[10px] font-bold text-gray-400 uppercase tracking-widest whitespace-nowrap bg-gray-50/80"
                                            :class="{
                                                'text-right':  col.align === 'right',
                                                'text-center': col.align === 'center',
                                                'text-left':   col.align === 'left'
                                            }">
                                            {{ col.label }}
                                        </th>
                                        <!-- 操作（固定右列，sticky） -->
                                        <th class="pl-3 pr-5 py-3.5 text-[10px] font-bold text-gray-400 uppercase tracking-widest text-center whitespace-nowrap bg-gray-50/80 sticky right-0 border-l border-gray-100 min-w-[110px]">
                                            操作
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-gray-100">
                                    <tr v-for="customer in customers" :key="customer.id"
                                        class="hover:bg-blue-50/30 transition-colors cursor-pointer group"
                                        @click="openCustomer360(customer)">

                                        <!-- 复选框 -->
                                        <td class="pl-5 pr-3 py-4 align-middle" @click.stop>
                                            <input class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-0 cursor-pointer" type="checkbox" />
                                        </td>

                                        <!-- 客户基本信息 -->
                                        <td class="px-4 py-4 align-middle min-w-[180px]">
                                            <div class="flex items-center gap-3">
                                                <div class="w-9 h-9 rounded-full bg-blue-100 flex items-center justify-center shrink-0 text-blue-600 font-bold text-sm">
                                                    {{ customer.cust_name?.[0] ?? '?' }}
                                                </div>
                                                <div class="min-w-0">
                                                    <p class="text-sm font-bold text-gray-800 truncate mb-0.5">{{ customer.cust_name }}</p>
                                                    <p class="text-[10px] text-gray-400 truncate">{{ customer.phone }} · {{ customer.fund_account }}</p>
                                                </div>
                                            </div>
                                        </td>

                                        <!-- 动态列 -->
                                        <template v-for="col in enabledColumns" :key="col.key">

                                            <!-- 建联状态（同管理页口径：已认证 / 未添加或未绑定） -->
                                            <td v-if="col.key === 'contactStatus'" class="px-4 py-4 align-middle text-center">
                                                <span class="inline-flex items-center justify-center px-2.5 py-1 text-[10px] font-bold rounded-lg whitespace-nowrap"
                                                      :class="customer.contact_status === '已认证'
                                                              ? 'bg-emerald-50 text-emerald-600 border border-emerald-100'
                                                              : 'bg-zinc-100 text-zinc-500'">
                                                    {{ customer.contact_status || '—' }}
                                                </span>
                                            </td>

                                            <!-- T-1日AUM资产 -->
                                            <td v-else-if="col.key === 'aum'" class="px-4 py-4 align-middle text-right">
                                                <p class="text-sm font-bold text-gray-800 tracking-tight whitespace-nowrap">
                                                    {{ customer.t1_aum != null ? customer.t1_aum.toFixed(1) + ' 万' : '—' }}
                                                </p>
                                                <p v-if="customer.aum_change_pct != null" class="text-[10px] font-semibold mt-0.5 whitespace-nowrap"
                                                   :class="customer.aum_change_pct >= 0 ? 'text-green-500' : 'text-red-500'">
                                                    {{ customer.aum_change_pct >= 0 ? '+' : '' }}{{ customer.aum_change_pct }}% 本月
                                                </p>
                                            </td>

                                            <!-- 跟进状态（5档，同管理页） -->
                                            <td v-else-if="col.key === 'follow_status'" class="px-4 py-4 align-middle text-center">
                                                <span class="text-xs font-semibold whitespace-nowrap"
                                                      :class="getFollowClass(customer.follow_status)">
                                                    {{ customer.follow_status || '未联系' }}
                                                </span>
                                            </td>

                                            <!-- 风险等级 -->
                                            <td v-else-if="col.key === 'riskLevel'" class="px-4 py-4 align-middle text-center">
                                                <span class="text-xs font-bold whitespace-nowrap"
                                                      :class="getRiskColor(customer.risk_level)">
                                                    {{ customer.risk_level || '—' }}
                                                </span>
                                            </td>

                                            <!-- 本年收益 -->
                                            <td v-else-if="col.key === 'annualReturn'" class="px-4 py-4 align-middle text-right">
                                                <span v-if="customer.annual_return != null"
                                                      class="text-sm font-bold whitespace-nowrap"
                                                      :class="customer.annual_return >= 0 ? 'text-green-600' : 'text-red-500'">
                                                    {{ customer.annual_return >= 0 ? '+' : '' }}{{ (customer.annual_return / 10000).toFixed(2) }} 万
                                                </span>
                                                <span v-else class="text-xs text-gray-400">—</span>
                                            </td>

                                            <!-- 资产等级 -->
                                            <td v-else-if="col.key === 'assetLevel'" class="px-4 py-4 align-middle text-center">
                                                <span class="inline-flex items-center justify-center px-2.5 py-1 text-[10px] font-bold rounded-lg whitespace-nowrap"
                                                      :class="getAssetLevelClass(customer.asset_level)">
                                                    {{ customer.asset_level || '—' }}
                                                </span>
                                            </td>

                                            <!-- 佣金费率 -->
                                            <td v-else-if="col.key === 'commission_rate'" class="px-4 py-4 align-middle text-center">
                                                <span class="text-xs text-gray-700 whitespace-nowrap">
                                                    {{ customer.commission_rate != null ? (customer.commission_rate * 100).toFixed(4) + '%' : '—' }}
                                                </span>
                                            </td>

                                            <!-- 备注 -->
                                            <td v-else-if="col.key === 'remark'" class="px-4 py-4 align-middle">
                                                <p class="text-xs text-gray-500 truncate max-w-[160px]">{{ customer.remark || '—' }}</p>
                                            </td>

                                            <!-- 纯文本列（fallback，col.key 直接对应 API 字段名） -->
                                            <td v-else class="px-4 py-4 align-middle text-xs text-gray-700 whitespace-nowrap"
                                                :class="{
                                                    'text-right':  col.align === 'right',
                                                    'text-center': col.align === 'center'
                                                }">
                                                {{ customer[col.key] ?? '—' }}
                                            </td>
                                        </template>

                                        <!-- 操作（sticky 右列） -->
                                        <td class="pl-3 pr-5 py-4 align-middle sticky right-0 bg-white group-hover:bg-blue-50/30 border-l border-gray-100 transition-colors" @click.stop>
                                            <div class="flex items-center justify-center gap-1">
                                                <button class="p-1.5 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-600 hover:text-white transition-all" title="立即外呼">
                                                    <iconify-icon class="text-base" icon="solar:phone-bold"></iconify-icon>
                                                </button>
                                                <button class="p-1.5 rounded-lg transition-all"
                                                        :class="customer.contact_status === '已认证'
                                                            ? 'bg-green-50 text-green-600 hover:bg-green-600 hover:text-white'
                                                            : 'bg-gray-100 text-gray-300 cursor-not-allowed'"
                                                        title="发送企微">
                                                    <iconify-icon class="text-base" icon="solar:chat-round-bold"></iconify-icon>
                                                </button>
                                                <button class="p-1.5 text-gray-400 hover:bg-gray-100 hover:text-blue-600 rounded-lg transition-all" title="更多">
                                                    <iconify-icon class="text-base" icon="solar:menu-dots-bold"></iconify-icon>
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <!-- Pagination -->
                        <div class="px-6 py-4 bg-gray-50/30 flex items-center justify-between border-t border-gray-100">
                            <span class="text-xs text-gray-400">
                                显示 {{ (listPage - 1) * pageSize + 1 }} - {{ Math.min(listPage * pageSize, totalCount) }} / 共 {{ totalCount }} 条客户记录
                            </span>
                            <div class="flex items-center space-x-1">
                                <button class="p-2 hover:bg-gray-100 rounded-lg text-gray-400 disabled:opacity-30"
                                        :disabled="listPage <= 1"
                                        @click="listPage--; fetchCustomers()">
                                    <iconify-icon icon="solar:alt-arrow-left-linear"></iconify-icon>
                                </button>
                                <template v-for="p in Math.max(1, Math.ceil(totalCount / pageSize))" :key="p">
                                    <button v-if="Math.abs(p - listPage) <= 2"
                                            class="w-8 h-8 rounded-lg text-xs font-bold"
                                            :class="p === listPage ? 'bg-blue-600 text-white' : 'hover:bg-gray-100 text-gray-600'"
                                            @click="listPage = p; fetchCustomers()">
                                        {{ p }}
                                    </button>
                                </template>
                                <button class="p-2 hover:bg-gray-100 rounded-lg text-gray-400 disabled:opacity-30"
                                        :disabled="listPage >= Math.ceil(totalCount / pageSize)"
                                        @click="listPage++; fetchCustomers()">
                                    <iconify-icon icon="solar:alt-arrow-right-linear"></iconify-icon>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 客户 360° 全景视图 -->
                <div class="page-content space-y-6" :class="{ active: currentPage === 'customer-360' }"
                    id="page-customer-360">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-4">
                            <button
                                class="p-2 bg-white border border-gray-100 text-gray-400 rounded-xl hover:text-blue-600 transition-all"
                                @click="switchHallPage('customer-list')">
                                <iconify-icon class="text-xl" icon="solar:alt-arrow-left-bold"></iconify-icon>
                            </button>
                            <div>
                                <h1 class="text-2xl font-bold text-gray-800 tracking-tight">客户 360° 全景视图</h1>
                                <p class="text-sm text-gray-400 mt-1">当前查看: <span class="font-bold text-gray-600">{{ selectedCustomer?.cust_name ?? '—' }}{{ selectedCustomer?.fund_account ? ' (' + selectedCustomer.fund_account + ')' : '' }}</span></p>
                            </div>
                        </div>
                        <div class="flex items-center space-x-3">
                            <button
                                class="px-4 py-2 bg-blue-600 text-white text-sm font-bold rounded-xl shadow-lg shadow-blue-100 flex items-center">
                                <iconify-icon class="mr-2 text-lg" icon="solar:phone-calling-bold"></iconify-icon> 发起通话
                            </button>
                            <button
                                class="px-4 py-2 bg-white border border-gray-100 text-gray-600 text-sm font-bold rounded-xl shadow-sm flex items-center">
                                <iconify-icon class="mr-2 text-lg" icon="solar:settings-linear"></iconify-icon> 客户设置
                            </button>
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-6 h-[calc(100vh-18rem)] overflow-hidden">
                        <!-- 左侧：基础信息与资产 -->
                        <div class="col-span-12 lg:col-span-4 space-y-6 overflow-y-auto no-scrollbar pr-2">
                            <!-- 基础信息卡 -->
                            <div class="data-card p-6">
                                <div class="flex items-start justify-between mb-6">
                                    <div class="flex items-center space-x-4">
                                        <div class="w-16 h-16 rounded-3xl border-4 border-blue-50 shadow-sm bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-2xl shrink-0">
                                            {{ selectedCustomer?.cust_name?.[0] ?? '?' }}
                                        </div>
                                        <div>
                                            <h3 class="text-xl font-bold text-gray-800">{{ selectedCustomer?.cust_name ?? '—' }}</h3>
                                            <div class="flex flex-wrap gap-1 mt-1.5">
                                                <span v-if="selectedCustomer?.risk_level"
                                                    class="px-1.5 py-0.5 bg-amber-100 text-amber-600 text-[10px] font-bold rounded">{{ selectedCustomer.risk_level }}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <button class="p-2 text-blue-600 hover:bg-blue-50 rounded-xl">
                                        <iconify-icon class="text-xl" icon="solar:pen-new-square-linear"></iconify-icon>
                                    </button>
                                </div>
                                <div class="grid grid-cols-2 gap-4">
                                    <div class="p-3 bg-gray-50 rounded-2xl">
                                        <p class="text-[10px] text-gray-400 font-bold uppercase">手机号</p>
                                        <p class="text-sm font-bold text-gray-700 mt-1">{{ selectedCustomer?.phone ?? '—' }}</p>
                                    </div>
                                    <div class="p-3 bg-gray-50 rounded-2xl">
                                        <p class="text-[10px] text-gray-400 font-bold uppercase">归属人</p>
                                        <p class="text-sm font-bold text-gray-700 mt-1">{{ selectedCustomer?.assignee_nm ?? '—' }}</p>
                                    </div>
                                    <div class="p-3 bg-gray-50 rounded-2xl">
                                        <p class="text-[10px] text-gray-400 font-bold uppercase">开户时长</p>
                                        <p class="text-sm font-bold text-gray-700 mt-1">{{ calcAccountAge(selectedCustomer?.open_date) }}</p>
                                    </div>
                                    <div class="p-3 bg-gray-50 rounded-2xl">
                                        <p class="text-[10px] text-gray-400 font-bold uppercase">风险等级</p>
                                        <p class="text-sm font-bold mt-1" :class="riskTextColor(selectedCustomer?.risk_level)">{{ selectedCustomer?.risk_level ?? '—' }}</p>
                                    </div>
                                </div>
                            </div>
                            <!-- 资产概览卡 -->
                            <div class="data-card p-6">
                                <h3 class="text-sm font-bold text-gray-800 mb-4 flex items-center">
                                    <iconify-icon class="mr-2 text-blue-600"
                                        icon="solar:wallet-bold-duotone"></iconify-icon>
                                    资产概览 (AUM)
                                </h3>
                                <div class="text-center py-4 border-b border-gray-50 mb-4">
                                    <p class="text-[11px] text-gray-400 font-bold uppercase">总资产</p>
                                    <p class="text-3xl font-bold text-gray-800 tracking-tighter">￥1,280,450.00</p>
                                    <div class="flex items-center justify-center space-x-2 mt-2">
                                        <span class="text-xs text-green-500 font-bold">+￥42,100.22</span>
                                        <span class="text-[10px] text-gray-400">本月变动</span>
                                    </div>
                                </div>
                                <div class="space-y-3">
                                    <div class="flex items-center justify-between">
                                        <span class="text-xs text-gray-500">股票持仓</span>
                                        <span class="text-xs font-bold text-gray-700">￥840,200.00 (65%)</span>
                                    </div>
                                    <div class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden">
                                        <div class="bg-blue-600 h-full w-[65%]"></div>
                                    </div>
                                    <div class="flex items-center justify-between">
                                        <span class="text-xs text-gray-500">公募基金</span>
                                        <span class="text-xs font-bold text-gray-700">￥320,000.00 (25%)</span>
                                    </div>
                                    <div class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden">
                                        <div class="bg-indigo-600 h-full w-[25%]"></div>
                                    </div>
                                    <div class="flex items-center justify-between">
                                        <span class="text-xs text-gray-500">理财/闲钱</span>
                                        <span class="text-xs font-bold text-gray-700">￥120,250.00 (10%)</span>
                                    </div>
                                    <div class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden">
                                        <div class="bg-amber-600 h-full w-[10%]"></div>
                                    </div>
                                </div>
                            </div>
                            <!-- 创收贡献卡 -->
                            <div class="data-card p-6">
                                <h3 class="text-sm font-bold text-gray-800 mb-4">本年创收贡献</h3>
                                <div class="h-48 w-full" id="contributionChart"></div>
                            </div>
                            <!-- 客户多维画像雷达图 -->
                            <div class="data-card p-6">
                                <h3 class="text-sm font-bold text-gray-800 mb-1">客户多维画像</h3>
                                <p class="text-[10px] text-gray-400 mb-3">8 维度综合评估</p>
                                <div class="h-52 w-full" id="customerRadarChart"></div>
                            </div>
                        </div>
                        <!-- 中间：互动历史与轨迹 -->
                        <div class="col-span-12 lg:col-span-5 space-y-6 flex flex-col h-full overflow-hidden">
                            <div class="data-card flex-1 flex flex-col overflow-hidden">
                                <div class="px-6 py-4 border-b border-gray-50 flex items-center justify-between">
                                    <div class="flex items-center space-x-4">
                                        <h3 class="text-sm font-bold text-gray-800">互动轨迹与建联历史</h3>
                                        <div class="flex space-x-1">
                                            <button
                                                class="px-3 py-1 bg-blue-50 text-blue-600 text-[10px] font-bold rounded-full">全部</button>
                                            <button
                                                class="px-3 py-1 text-gray-400 text-[10px] font-bold rounded-full hover:bg-gray-50 transition-all">企微</button>
                                            <button
                                                class="px-3 py-1 text-gray-400 text-[10px] font-bold rounded-full hover:bg-gray-50 transition-all">通话</button>
                                            <button
                                                class="px-3 py-1 text-gray-400 text-[10px] font-bold rounded-full hover:bg-gray-50 transition-all">交易</button>
                                        </div>
                                    </div>
                                    <button class="text-xs font-bold text-blue-600">查看详情</button>
                                </div>
                                <div class="flex-1 overflow-y-auto p-6 space-y-8 scroll-smooth no-scrollbar">
                                    <!-- Timeline Item 1 -->
                                    <div class="relative pl-8">
                                        <div
                                            class="absolute left-0 top-1 w-4 h-4 bg-blue-600 rounded-full border-4 border-blue-100 z-10">
                                        </div>
                                        <div class="absolute left-1.5 top-5 w-0.5 h-full bg-gray-100 -z-0"></div>
                                        <div class="mb-1 flex items-center justify-between">
                                            <span class="text-xs font-bold text-gray-800">客户咨询：理财收益结算</span>
                                            <span class="text-[10px] text-gray-400">2026-05-07 10:25</span>
                                        </div>
                                        <div class="bg-blue-50/50 p-3 rounded-2xl border border-blue-50">
                                            <p class="text-xs text-gray-600 leading-relaxed">客户在企微咨询了“智富盈 1
                                                号”的收益结算时间，并表达了理财到期后的转投意愿。AI 建议：推荐 6 个月期固收增强产品。</p>
                                        </div>
                                    </div>
                                    <!-- Timeline Item 2 -->
                                    <div class="relative pl-8">
                                        <div
                                            class="absolute left-0 top-1 w-4 h-4 bg-green-500 rounded-full border-4 border-green-100 z-10">
                                        </div>
                                        <div class="absolute left-1.5 top-5 w-0.5 h-full bg-gray-100 -z-0"></div>
                                        <div class="mb-1 flex items-center justify-between">
                                            <span class="text-xs font-bold text-gray-800">外呼通话：新客回访</span>
                                            <span class="text-[10px] text-gray-400">2026-05-04 15:30</span>
                                        </div>
                                        <div class="bg-green-50/50 p-3 rounded-2xl border border-green-50">
                                            <p class="text-xs text-gray-600 leading-relaxed">通话时长 05:22。客户对当前持仓满意，近期有
                                                10w 闲置资金可动用。已标记“入金潜力”。</p>
                                            <button class="mt-2 flex items-center text-[10px] font-bold text-green-600">
                                                <iconify-icon class="mr-1" icon="solar:play-circle-bold"></iconify-icon>
                                                播放通话录音
                                            </button>
                                        </div>
                                    </div>
                                    <!-- Timeline Item 3 -->
                                    <div class="relative pl-8">
                                        <div
                                            class="absolute left-0 top-1 w-4 h-4 bg-amber-500 rounded-full border-4 border-amber-100 z-10">
                                        </div>
                                        <div class="absolute left-1.5 top-5 w-0.5 h-20 bg-gray-100 -z-0"></div>
                                        <div class="mb-1 flex items-center justify-between">
                                            <span class="text-xs font-bold text-gray-800">交易提醒：大额转入</span>
                                            <span class="text-[10px] text-gray-400">2026-04-28 09:12</span>
                                        </div>
                                        <div class="bg-amber-50/50 p-3 rounded-2xl border border-amber-50">
                                            <p class="text-xs text-gray-600 font-bold tracking-tight">转入金额: +￥200,000.00
                                            </p>
                                            <p class="text-[10px] text-gray-400 mt-1">银证转账转入，来自招商银行</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- 右侧：AI 展业工具面板 -->
                        <div class="col-span-12 lg:col-span-3 space-y-6 overflow-y-auto no-scrollbar pl-2">
                            <!-- AI 辅助卡 -->
                            <div
                                class="data-card p-6 bg-gradient-to-br from-indigo-50 to-blue-50 border-blue-100 relative overflow-hidden">
                                <iconify-icon class="absolute -top-4 -right-4 text-8xl text-blue-200/50"
                                    icon="solar:magic-stick-3-bold-duotone"></iconify-icon>
                                <h3 class="text-sm font-bold text-blue-800 mb-4 relative z-10">AI 智能辅助</h3>
                                <div class="space-y-4 relative z-10">
                                    <div class="p-3 bg-white/80 rounded-2xl shadow-sm">
                                        <p class="text-[10px] text-blue-600 font-bold uppercase tracking-wider mb-1">AI
                                            客户摘要</p>
                                        <p class="text-xs text-gray-700 font-medium italic">“稳健增长型 V5
                                            客户，资金充足，本周有理财到期提醒，建议今日触达。”</p>
                                    </div>
                                    <div class="p-3 bg-white/80 rounded-2xl shadow-sm">
                                        <p class="text-[10px] text-blue-600 font-bold uppercase tracking-wider mb-1">AI
                                            推荐话术</p>
                                        <p class="text-[11px] text-gray-700 leading-relaxed">“张先生您好，看到您持有的智富盈 1
                                            号即将到期，目前刚好有同系列的...”</p>
                                        <div class="flex justify-end mt-2">
                                            <button class="text-[10px] font-bold text-blue-600 flex items-center">
                                                <iconify-icon class="mr-1" icon="solar:copy-bold"></iconify-icon> 复制话术
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- 智能提醒卡 -->
                            <div class="data-card p-6">
                                <h3 class="text-sm font-bold text-gray-800 mb-4">待办提醒</h3>
                                <div class="space-y-3">
                                    <div
                                        class="flex items-start space-x-3 p-3 bg-red-50 rounded-2xl border border-red-100">
                                        <iconify-icon class="text-red-500 text-lg mt-0.5"
                                            icon="solar:bell-bing-bold"></iconify-icon>
                                        <div>
                                            <p class="text-xs font-bold text-red-800">理财到期提醒</p>
                                            <p class="text-[10px] text-red-600 mt-0.5">智富盈 1 号将在 3 天后到期 (50w)</p>
                                        </div>
                                    </div>
                                    <div
                                        class="flex items-start space-x-3 p-3 bg-blue-50 rounded-2xl border border-blue-100">
                                        <iconify-icon class="text-blue-500 text-lg mt-0.5"
                                            icon="solar:calendar-bold"></iconify-icon>
                                        <div>
                                            <p class="text-xs font-bold text-blue-800">持仓异动预警</p>
                                            <p class="text-[10px] text-blue-600 mt-0.5">持有的某白酒基金跌幅超过 5%</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- 推荐产品卡 -->
                            <div class="data-card p-6">
                                <h3 class="text-sm font-bold text-gray-800 mb-4">AI 匹配推荐</h3>
                                <div class="bg-gray-50 rounded-2xl p-4 border border-gray-100">
                                    <p class="text-xs font-bold text-gray-800">中信建投智胜 180 天</p>
                                    <div class="flex items-center justify-between mt-1">
                                        <span class="text-[10px] text-gray-400">业绩比较基准</span>
                                        <span class="text-sm font-bold text-blue-600">4.2% ~ 5.5%</span>
                                    </div>
                                    <div class="mt-3 flex space-x-2">
                                        <button
                                            class="flex-1 bg-white border border-blue-100 text-[10px] font-bold text-blue-600 py-1.5 rounded-lg">查看详情</button>
                                        <button
                                            class="flex-1 bg-blue-600 text-[10px] font-bold text-white py-1.5 rounded-lg">一键邀约</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 标准展业流程 (SOP) 模块 -->
                <div class="page-content space-y-6" id="page-sop" :class="{ active: currentPage === 'sop' }">
                    <div class="flex items-center justify-between">
                        <div>
                            <h1 class="text-2xl font-bold text-gray-800 tracking-tight">标准展业流程 (SOP)</h1>
                            <p class="text-sm text-gray-400 mt-1">结构化展业动作，AI 驱动智能匹配，提升合规触达效率</p>
                        </div>
                        <div class="flex items-center space-x-3">
                            <button class="px-4 py-2 bg-white border border-gray-100 text-gray-600 text-sm font-bold rounded-xl shadow-sm flex items-center">
                                <iconify-icon class="mr-2 text-lg" icon="solar:add-circle-linear"></iconify-icon> 新建 SOP
                            </button>
                            <button class="px-6 py-2.5 bg-blue-600 text-white text-sm font-bold rounded-xl shadow-lg shadow-blue-200 flex items-center">
                                <iconify-icon class="mr-2 text-lg" icon="solar:magic-stick-3-bold-duotone"></iconify-icon> AI 一键匹配
                            </button>
                        </div>
                    </div>

                    <!-- SOP 执行统计 -->
                    <div class="grid grid-cols-12 gap-4">
                        <!-- 卡片1：任务类型分布（宽卡） -->
                        <div class="col-span-6 data-card p-5">
                            <div class="flex items-center justify-between mb-4">
                                <div>
                                    <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">SOP 执行总览</span>
                                    <div class="flex items-baseline space-x-2 mt-1">
                                        <span class="text-2xl font-bold text-gray-800">25</span>
                                        <span class="text-xs text-gray-400">个流程</span>
                                        <span class="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full ml-1">12 进行中</span>
                                    </div>
                                </div>
                                <div class="w-9 h-9 bg-blue-50 rounded-xl flex items-center justify-center shrink-0">
                                    <iconify-icon class="text-blue-600 text-lg" icon="solar:play-circle-bold-duotone"></iconify-icon>
                                </div>
                            </div>
                            <!-- 5大类型分布 -->
                            <div class="flex items-end space-x-2">
                                <div v-for="tab in sopTabs" :key="tab.key"
                                    class="flex-1 flex flex-col items-center cursor-pointer group"
                                    @click="currentSopTab = tab.key">
                                    <!-- 数量 -->
                                    <span class="text-xs font-bold text-gray-700 mb-1 group-hover:text-blue-600 transition-colors">{{ sopTabCount(tab.key) }}</span>
                                    <!-- 进度条 -->
                                    <div class="w-full rounded-full overflow-hidden bg-gray-100" style="height:6px;">
                                        <div class="h-full rounded-full transition-all"
                                            :class="currentSopTab === tab.key ? 'bg-blue-500' : 'bg-gray-300 group-hover:bg-blue-300'"
                                            :style="{ width: (sopTabCount(tab.key) / 25 * 100) + '%' }">
                                        </div>
                                    </div>
                                    <!-- 标签 -->
                                    <span class="text-[9px] mt-1 font-medium transition-colors"
                                        :class="currentSopTab === tab.key ? 'text-blue-600 font-bold' : 'text-gray-400 group-hover:text-gray-600'">
                                        {{ tab.label.replace('类','') }}
                                    </span>
                                    <!-- 进行中小点 -->
                                    <span v-if="sopTabRunning(tab.key) > 0"
                                        class="text-[9px] font-bold text-green-600 bg-green-50 px-1.5 py-0.5 rounded-full mt-0.5">
                                        {{ sopTabRunning(tab.key) }}在跑
                                    </span>
                                    <span v-else class="text-[9px] text-transparent mt-0.5">-</span>
                                </div>
                            </div>
                        </div>

                        <!-- 卡片2：本月完成 + AI效能 -->
                        <div class="col-span-3 data-card p-5 flex flex-col justify-between">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">本月完成</span>
                                <div class="w-8 h-8 bg-green-50 rounded-xl flex items-center justify-center">
                                    <iconify-icon class="text-green-600 text-base" icon="solar:check-circle-bold-duotone"></iconify-icon>
                                </div>
                            </div>
                            <div>
                                <p class="text-2xl font-bold text-gray-800">47</p>
                                <p class="text-xs text-green-600 mt-1 font-medium">完成率 82%</p>
                            </div>
                            <div class="mt-3 pt-3 border-t border-gray-100">
                                <div class="flex items-center justify-between">
                                    <span class="text-[10px] text-gray-400">AI 代劳步骤</span>
                                    <span class="text-[10px] font-bold text-purple-600">61%</span>
                                </div>
                                <div class="mt-1 w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                    <div class="h-full bg-purple-400 rounded-full" style="width:61%"></div>
                                </div>
                            </div>
                        </div>

                        <!-- 卡片3：核心指标 -->
                        <div class="col-span-3 data-card p-5 flex flex-col justify-between">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">核心指标</span>
                                <div class="w-8 h-8 bg-indigo-50 rounded-xl flex items-center justify-center">
                                    <iconify-icon class="text-indigo-600 text-base" icon="solar:magic-stick-3-bold-duotone"></iconify-icon>
                                </div>
                            </div>
                            <div class="space-y-3">
                                <div>
                                    <div class="flex items-baseline justify-between">
                                        <span class="text-[10px] text-gray-400">AI 匹配准确率</span>
                                        <span class="text-sm font-bold text-indigo-600">94.3%</span>
                                    </div>
                                    <div class="mt-1 w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                        <div class="h-full bg-indigo-400 rounded-full" style="width:94.3%"></div>
                                    </div>
                                </div>
                                <div>
                                    <div class="flex items-baseline justify-between">
                                        <span class="text-[10px] text-gray-400">触达转化率</span>
                                        <span class="text-sm font-bold text-amber-600">38.6%</span>
                                    </div>
                                    <div class="mt-1 w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                        <div class="h-full bg-amber-400 rounded-full" style="width:38.6%"></div>
                                    </div>
                                </div>
                            </div>
                            <p class="text-[9px] text-gray-400 mt-2">↑ 较上月均有提升</p>
                        </div>
                    </div>

                    <!-- 主体：SOP 列表 + 右侧面板 -->
                    <div class="grid grid-cols-12 gap-6">
                        <!-- 左侧：任务类型 Tab + SOP 列表 -->
                        <div class="col-span-12 lg:col-span-8 space-y-4">
                            <div class="data-card overflow-hidden">
                                <!-- 任务类型 Tab 导航 -->
                                <div class="flex border-b border-gray-100 overflow-x-auto">
                                    <button v-for="tab in sopTabs" :key="tab.key"
                                        class="px-4 py-3.5 text-sm font-medium whitespace-nowrap transition-all border-b-2 -mb-px flex items-center space-x-1.5"
                                        :class="currentSopTab === tab.key ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                                        @click="currentSopTab = tab.key">
                                        <span>{{ tab.label }}</span>
                                        <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full"
                                            :class="currentSopTab === tab.key ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-500'">
                                            {{ sopTabCount(tab.key) }}
                                        </span>
                                        <span v-if="sopTabRunning(tab.key) > 0"
                                            class="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-green-100 text-green-600">
                                            {{ sopTabRunning(tab.key) }}进行中
                                        </span>
                                    </button>
                                </div>

                                <!-- SOP 列表（按产品分组） -->
                                <div class="p-5 space-y-6">
                                    <div v-for="group in currentTabSopGroups" :key="group.product">
                                        <!-- 产品分组标题 -->
                                        <div class="flex items-center space-x-2 mb-3">
                                            <span class="text-xs font-bold px-2.5 py-1 rounded-full" :class="group.productTagClass">{{ group.product }}</span>
                                            <div class="flex-1 h-px bg-gray-100"></div>
                                            <span class="text-[10px] text-gray-400">{{ group.sops.length }} 个流程</span>
                                        </div>

                                        <!-- SOP 卡片列表 -->
                                        <div class="space-y-2">
                                            <div v-for="sop in group.sops" :key="sop.id"
                                                class="border border-gray-100 rounded-2xl overflow-hidden hover:border-blue-200 transition-all">
                                                <!-- SOP 卡片头部（可点击展开） -->
                                                <div class="flex items-center px-4 py-3 cursor-pointer hover:bg-gray-50/60 transition-colors"
                                                    @click="toggleSop(sop.id)">
                                                    <!-- 图标 -->
                                                    <div class="w-9 h-9 rounded-xl flex items-center justify-center mr-3 shrink-0" :class="group.iconBg">
                                                        <iconify-icon class="text-base" :class="group.iconColor" :icon="sop.icon"></iconify-icon>
                                                    </div>
                                                    <!-- SOP 名称 + 徽标 -->
                                                    <div class="flex-1 min-w-0">
                                                        <div class="flex items-center flex-wrap gap-1.5 mb-0.5">
                                                            <span class="text-sm font-bold text-gray-800">{{ sop.name }}</span>
                                                            <!-- 自动触发徽标 -->
                                                            <span v-if="sop.autoTrigger"
                                                                class="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-amber-100 text-amber-700 flex items-center">
                                                                <iconify-icon class="mr-0.5" icon="solar:bolt-bold"></iconify-icon>系统自动触发
                                                            </span>
                                                            <!-- 风险等级限制 -->
                                                            <span v-if="sop.minRisk"
                                                                class="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-red-50 text-red-500">
                                                                {{ sop.minRisk }}+
                                                            </span>
                                                        </div>
                                                        <p class="text-[10px] text-gray-400 truncate">{{ sop.desc }}</p>
                                                    </div>
                                                    <!-- 统计数字 -->
                                                    <div class="flex items-center space-x-4 mr-3 shrink-0">
                                                        <div class="text-center">
                                                            <p class="text-sm font-bold text-gray-700">{{ sop.eligibleCount }}</p>
                                                            <p class="text-[9px] text-gray-400">适用客户</p>
                                                        </div>
                                                        <div class="text-center">
                                                            <p class="text-sm font-bold text-gray-700">{{ sop.stepCount }}</p>
                                                            <p class="text-[9px] text-gray-400">步骤</p>
                                                        </div>
                                                        <div class="text-center" v-if="sop.runningCount > 0">
                                                            <p class="text-sm font-bold text-green-600">{{ sop.runningCount }}</p>
                                                            <p class="text-[9px] text-gray-400">进行中</p>
                                                        </div>
                                                    </div>
                                                    <!-- 展开箭头 -->
                                                    <iconify-icon
                                                        class="text-gray-400 text-base transition-transform duration-200 shrink-0"
                                                        :class="expandedSopId === sop.id ? 'rotate-180' : ''"
                                                        icon="solar:alt-arrow-down-linear">
                                                    </iconify-icon>
                                                </div>

                                                <!-- 展开：步骤流程 -->
                                                <div v-if="expandedSopId === sop.id"
                                                    class="border-t border-gray-100 bg-gray-50/60 px-4 pt-4 pb-4">
                                                    <!-- 步骤横向流程图 -->
                                                    <div class="flex items-start overflow-x-auto pb-2 space-x-0">
                                                        <template v-for="(step, idx) in sop.steps" :key="step.seq">
                                                            <!-- 步骤节点 -->
                                                            <div class="flex flex-col items-center shrink-0" style="min-width:100px; max-width:120px;">
                                                                <!-- 序号圆圈 -->
                                                                <div class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white mb-2 shrink-0"
                                                                    :class="step.aiCapable ? 'bg-purple-500' : step.required ? 'bg-red-500' : 'bg-blue-400'">
                                                                    {{ step.seq }}
                                                                </div>
                                                                <!-- 步骤内容框 -->
                                                                <div class="w-full rounded-xl p-2 border text-center"
                                                                    :class="step.aiCapable ? 'bg-purple-50 border-purple-100' : step.required ? 'bg-red-50 border-red-100' : 'bg-white border-gray-100'">
                                                                    <p class="text-[11px] font-bold text-gray-800 mb-1">{{ step.action }}</p>
                                                                    <span class="text-[9px] font-bold px-1.5 py-0.5 rounded-full"
                                                                        :class="getTaskTypeChipClass(step.taskType)">{{ step.taskType }}</span>
                                                                    <p class="text-[9px] text-gray-400 mt-1">{{ step.timing }}</p>
                                                                    <span class="text-[9px] font-bold mt-1 block"
                                                                        :class="step.aiCapable ? 'text-purple-600' : step.required ? 'text-red-500' : 'text-gray-400'">
                                                                        {{ step.aiCapable ? 'AI 代劳' : step.required ? '人工必须' : '人工跟进' }}
                                                                    </span>
                                                                </div>
                                                            </div>
                                                            <!-- 箭头连接线 -->
                                                            <div v-if="idx < sop.steps.length - 1"
                                                                class="flex items-center justify-center shrink-0 pt-3" style="width:24px;">
                                                                <iconify-icon class="text-gray-300 text-base" icon="solar:arrow-right-linear"></iconify-icon>
                                                            </div>
                                                        </template>
                                                    </div>
                                                    <!-- 底部操作栏 -->
                                                    <div class="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
                                                        <p class="text-[10px] text-gray-500">
                                                            适用 <span class="font-bold text-gray-700">{{ sop.eligibleCount }}</span> 位客户
                                                            <span v-if="sop.minRisk" class="ml-1 text-red-400">（需{{ sop.minRisk }}+ 风险等级）</span>
                                                        </p>
                                                        <div class="flex items-center space-x-2">
                                                            <button class="px-3 py-1.5 text-[11px] font-bold text-gray-500 border border-gray-200 rounded-lg hover:bg-gray-100 transition-colors">
                                                                查看执行记录
                                                            </button>
                                                            <button class="px-3 py-1.5 text-[11px] font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">
                                                                选客户执行
                                                            </button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 右侧 AI 推荐面板 -->
                        <div class="col-span-12 lg:col-span-4 space-y-4">
                            <!-- AI 推荐 -->
                            <div class="data-card p-6 bg-gradient-to-br from-indigo-50 to-blue-50 border-blue-100 relative overflow-hidden">
                                <iconify-icon class="absolute -top-4 -right-4 text-8xl text-blue-200/50" icon="solar:magic-stick-3-bold-duotone"></iconify-icon>
                                <h3 class="text-sm font-bold text-blue-800 mb-4 relative z-10">AI 智能 SOP 推荐</h3>
                                <div class="space-y-3 relative z-10">
                                    <div v-for="rec in aiSopRecs" :key="rec.name" class="p-3 bg-white/80 rounded-2xl shadow-sm">
                                        <div class="flex items-center justify-between mb-1">
                                            <p class="text-xs font-bold text-gray-800">{{ rec.name }}</p>
                                            <span class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">匹配 {{ rec.match }}%</span>
                                        </div>
                                        <span class="text-[9px] font-bold px-1.5 py-0.5 rounded-full mb-1 inline-block" :class="rec.tagClass">{{ rec.name.replace('SOP','').trim() }}</span>
                                        <p class="text-[10px] text-gray-500">{{ rec.reason }}</p>
                                        <button class="mt-2 w-full py-1.5 bg-blue-600 text-white text-[10px] font-bold rounded-lg hover:bg-blue-700 transition-colors">立即执行</button>
                                    </div>
                                </div>
                            </div>

                            <!-- 最近执行记录 -->
                            <div class="data-card p-6">
                                <h3 class="text-sm font-bold text-gray-800 mb-4">最近执行记录</h3>
                                <div class="space-y-3">
                                    <div v-for="log in sopLogs" :key="log.sopName + log.clientName" class="flex items-start space-x-3">
                                        <div class="w-2 h-2 rounded-full mt-1.5 shrink-0" :class="log.done ? 'bg-green-400' : 'bg-blue-400'"></div>
                                        <div class="flex-1 min-w-0">
                                            <p class="text-xs font-bold text-gray-700 truncate">{{ log.sopName }}</p>
                                            <p class="text-[10px] text-gray-500 mt-0.5">{{ log.clientName }} · {{ log.step }}</p>
                                            <p class="text-[9px] text-gray-400 mt-0.5">{{ log.time }}</p>
                                        </div>
                                        <span class="text-[10px] font-bold shrink-0" :class="log.done ? 'text-green-600' : 'text-blue-600'">{{ log.done ? '已完成' : '进行中' }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 批量外呼 (双呼) 模块 -->
                <!-- 批量外呼 (双呼) 模块 -->
                <div class="page-content space-y-6" id="page-bulk-calling" :class="{ active: currentPage === 'bulk-calling' }">
                    <div class="flex items-center justify-between">
                        <div>
                            <h1 class="text-2xl font-bold text-gray-800 tracking-tight">批量外呼 (双呼系统)</h1>
                            <p class="text-sm text-gray-400 mt-1">并发拨号，接通后 1 秒转接，AI 辅助通话全过程</p>
                        </div>
                        <div class="flex items-center space-x-3">
                            <button
                                class="px-6 py-2.5 bg-blue-600 text-white text-sm font-bold rounded-xl shadow-lg shadow-blue-200 flex items-center">
                                <iconify-icon class="mr-2 text-lg" icon="solar:play-bold"></iconify-icon> 开始批量拨号
                            </button>
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-8 h-full">
                        <div class="col-span-8 space-y-6">
                            <div
                                class="data-card p-6 h-[400px] flex flex-col items-center justify-center border-dashed border-2 border-blue-200 bg-blue-50/10">
                                <div class="text-center">
                                    <div
                                        class="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
                                        <iconify-icon class="text-4xl text-blue-600"
                                            icon="solar:phone-calling-bold"></iconify-icon>
                                    </div>
                                    <h3 class="text-lg font-bold text-gray-800">等待外呼任务启动</h3>
                                    <p class="text-sm text-gray-400 mt-2 max-w-sm">请从客户列表勾选需要外呼的客户，或者从“任务大厅”导入外呼清单。</p>
                                    <button
                                        class="mt-6 px-8 py-3 bg-white border border-gray-100 text-blue-600 font-bold rounded-2xl shadow-sm hover:bg-gray-50 transition-all">导入外呼清单</button>
                                </div>
                            </div>
                            <div class="data-card p-6">
                                <h3 class="text-sm font-bold text-gray-800 mb-4">外呼队列 (0/15)</h3>
                                <div class="flex flex-col items-center py-10 text-gray-300">
                                    <iconify-icon class="text-6xl mb-2" icon="solar:list-bold-duotone"></iconify-icon>
                                    <p class="text-xs font-bold">暂无待拨号任务</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-span-4 space-y-6">
                            <div class="data-card p-6">
                                <h3 class="text-sm font-bold text-gray-800 mb-4 flex items-center">
                                    <iconify-icon class="mr-2 text-blue-600"
                                        icon="solar:shield-check-bold-duotone"></iconify-icon>
                                    外呼合规设置
                                </h3>
                                <div class="space-y-4">
                                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-2xl">
                                        <span class="text-xs text-gray-600">外呼时段限制 (09:00 - 20:00)</span>
                                        <iconify-icon class="text-green-500"
                                            icon="solar:check-circle-bold"></iconify-icon>
                                    </div>
                                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-2xl">
                                        <span class="text-xs text-gray-600">黑名单客户自动拦截</span>
                                        <iconify-icon class="text-green-500"
                                            icon="solar:check-circle-bold"></iconify-icon>
                                    </div>
                                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-2xl">
                                        <span class="text-xs text-gray-600">敏感词实时监测 (AI)</span>
                                        <iconify-icon class="text-green-500"
                                            icon="solar:check-circle-bold"></iconify-icon>
                                    </div>
                                </div>
                            </div>
                            <div class="data-card p-6 bg-gradient-to-br from-gray-900 to-gray-800 text-white">
                                <h3 class="text-sm font-bold mb-4">外呼 AI 辅助能力</h3>
                                <ul class="space-y-3 text-[11px] text-gray-400">
                                    <li class="flex items-center"><iconify-icon class="mr-2 text-blue-400"
                                            icon="solar:check-read-linear"></iconify-icon> 实时生成通话纪要</li>
                                    <li class="flex items-center"><iconify-icon class="mr-2 text-blue-400"
                                            icon="solar:check-read-linear"></iconify-icon> 自动识别客户意向标签</li>
                                    <li class="flex items-center"><iconify-icon class="mr-2 text-blue-400"
                                            icon="solar:check-read-linear"></iconify-icon> 通话后自动创建跟进任务</li>
                                    <li class="flex items-center"><iconify-icon class="mr-2 text-blue-400"
                                            icon="solar:check-read-linear"></iconify-icon> 智能过滤空号/停机/黑名单</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- 其他模块占位 (智能问答, 素材中心等) -->
                <div class="page-content space-y-6" id="page-ai-chat" :class="{ active: currentPage === 'ai-chat' }">
                    <div class="flex items-center justify-between mb-8">
                        <h1 class="text-2xl font-bold text-gray-800">智能问答 (AI 展业助手)</h1>
                    </div>
                    <div class="data-card h-[600px] flex flex-col overflow-hidden">
                        <div class="flex-1 p-6 overflow-y-auto no-scrollbar space-y-4">
                            <div class="flex justify-start">
                                <div class="max-w-[80%] bg-blue-50 p-4 rounded-2xl text-sm text-gray-700 font-medium">
                                    您好！我是您的展业 AI 助手。您可以问我任何关于产品介绍、异议处理、企微话术或合规禁忌的问题。
                                </div>
                            </div>
                        </div>
                        <div class="p-6 border-t border-gray-100 bg-gray-50/50">
                            <div class="relative">
                                <input
                                    class="w-full bg-white border border-gray-200 rounded-2xl py-4 pl-6 pr-24 shadow-sm focus:ring-2 focus:ring-blue-100 transition-all outline-none"
                                    placeholder="请输入您的问题，例如：如何向高净值客户推荐 ETF 策略？" type="text" />
                                <button
                                    class="absolute right-3 top-2.5 bg-blue-600 text-white px-6 py-2 rounded-xl text-sm font-bold hover:bg-blue-700 transition-all">发送</button>
                            </div>
                            <div class="flex items-center space-x-2 mt-4">
                                <span class="text-[10px] text-gray-400 font-bold uppercase">常用场景:</span>
                                <button
                                    class="px-3 py-1 bg-white border border-gray-100 rounded-full text-[10px] text-gray-600 font-bold hover:bg-gray-50">产品介绍</button>
                                <button
                                    class="px-3 py-1 bg-white border border-gray-100 rounded-full text-[10px] text-gray-600 font-bold hover:bg-gray-50">异议处理</button>
                                <button
                                    class="px-3 py-1 bg-white border border-gray-100 rounded-full text-[10px] text-gray-600 font-bold hover:bg-gray-50">市场政策</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="page-content space-y-6" id="page-marketing-materials" :class="{ active: currentPage === 'marketing-materials' }">
                    <h1 class="text-2xl font-bold text-gray-800">营销素材中心</h1>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                        <!-- Placeholder material cards -->
                        <div class="data-card overflow-hidden group">
                            <img alt="Material" class="w-full h-40 object-cover bg-blue-50"
                                src="https://modao.cc/agent-py/media/generated_images/2026-05-08/a882eb2419144200ad91384b36189402.jpg#desc=User%20Avatar" />
                            <div class="p-4">
                                <h3 class="text-sm font-bold text-gray-800 truncate">理财节活动海报</h3>
                                <p class="text-[10px] text-gray-400 mt-1">更新于 2026-05-05 · 使用 1.2k 次</p>
                                <div class="mt-4 flex space-x-2">
                                    <button
                                        class="flex-1 py-1.5 bg-blue-50 text-blue-600 text-[10px] font-bold rounded-lg">预览</button>
                                    <button
                                        class="flex-1 py-1.5 bg-blue-600 text-white text-[10px] font-bold rounded-lg flex items-center justify-center">
                                        <iconify-icon class="mr-1" icon="logos:whatsapp-icon"></iconify-icon> 发企微
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- Repeat 3 more times -->
                        <div class="data-card overflow-hidden group"><img class="w-full h-40 bg-gray-50"
                                src="https://modao.cc/agent-py/media/generated_images/2026-05-08/a882eb2419144200ad91384b36189402.jpg#desc=User%20Avatar" />
                            <div class="p-4">
                                <h3 class="text-sm font-bold text-gray-800">最新美股研报摘要</h3>
                                <p class="text-[10px] text-gray-400 mt-1">更新于 2026-05-07</p>
                                <div class="mt-4 flex space-x-2"><button
                                        class="flex-1 py-1.5 bg-blue-50 text-blue-600 text-[10px] font-bold rounded-lg">复制</button><button
                                        class="flex-1 py-1.5 bg-blue-600 text-white text-[10px] font-bold rounded-lg">发企微</button>
                                </div>
                            </div>
                        </div>
                        <div class="data-card overflow-hidden group"><img class="w-full h-40 bg-gray-50"
                                src="https://modao.cc/agent-py/media/generated_images/2026-05-08/a882eb2419144200ad91384b36189402.jpg#desc=User%20Avatar" />
                            <div class="p-4">
                                <h3 class="text-sm font-bold text-gray-800">养老金开户引导话术</h3>
                                <p class="text-[10px] text-gray-400 mt-1">更新于 2026-05-01</p>
                                <div class="mt-4 flex space-x-2"><button
                                        class="flex-1 py-1.5 bg-blue-50 text-blue-600 text-[10px] font-bold rounded-lg">复制</button><button
                                        class="flex-1 py-1.5 bg-blue-600 text-white text-[10px] font-bold rounded-lg">发企微</button>
                                </div>
                            </div>
                        </div>
                        <div class="data-card overflow-hidden group"><img class="w-full h-40 bg-gray-50"
                                src="https://modao.cc/agent-py/media/generated_images/2026-05-08/a882eb2419144200ad91384b36189402.jpg#desc=User%20Avatar" />
                            <div class="p-4">
                                <h3 class="text-sm font-bold text-gray-800">新客理财节短视频</h3>
                                <p class="text-[10px] text-gray-400 mt-1">更新于 2026-05-06</p>
                                <div class="mt-4 flex space-x-2"><button
                                        class="flex-1 py-1.5 bg-blue-50 text-blue-600 text-[10px] font-bold rounded-lg">预览</button><button
                                        class="flex-1 py-1.5 bg-blue-600 text-white text-[10px] font-bold rounded-lg">发企微</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="page-content space-y-6" id="page-product-center" :class="{ active: currentPage === 'product-center' }">
                    <h1 class="text-2xl font-bold text-gray-800">产品查询与推荐</h1>
                    <div class="data-card p-6 flex flex-wrap gap-4 items-center">
                        <button class="px-4 py-2 bg-blue-600 text-white text-xs font-bold rounded-xl">全品类</button>
                        <button
                            class="px-4 py-2 bg-white border border-gray-100 text-gray-600 text-xs font-bold rounded-xl hover:bg-gray-50">固收理财</button>
                        <button
                            class="px-4 py-2 bg-white border border-gray-100 text-gray-600 text-xs font-bold rounded-xl hover:bg-gray-50">公募基金</button>
                        <button
                            class="px-4 py-2 bg-white border border-gray-100 text-gray-600 text-xs font-bold rounded-xl hover:bg-gray-50">股票/ETF</button>
                        <button
                            class="px-4 py-2 bg-white border border-gray-100 text-gray-600 text-xs font-bold rounded-xl hover:bg-gray-50">两融业务</button>
                        <div class="flex-1 min-w-[200px] relative">
                            <iconify-icon class="absolute left-3 top-2.5 text-gray-400"
                                icon="solar:magnifer-linear"></iconify-icon>
                            <input class="w-full bg-gray-50 border-none rounded-xl py-2 pl-10 pr-4 text-xs"
                                placeholder="搜代码、搜名称..." type="text" />
                        </div>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="data-card p-6 flex space-x-6 items-center">
                            <div
                                class="w-24 h-24 bg-blue-50 rounded-2xl flex flex-col items-center justify-center text-blue-600 font-bold">
                                <span class="text-[10px] uppercase">R2 风险</span>
                                <span class="text-xl">4.52%</span>
                                <span class="text-[8px]">七日年化</span>
                            </div>
                            <div class="flex-1">
                                <h3 class="font-bold text-gray-800">建投智富盈 30 天</h3>
                                <p class="text-[10px] text-gray-400 mt-1">适合稳健型、闲钱理财客群</p>
                                <div class="flex flex-wrap gap-1 mt-3">
                                    <span
                                        class="px-1.5 py-0.5 bg-blue-100 text-blue-600 text-[9px] font-bold rounded">AI
                                        核心推荐</span>
                                    <span
                                        class="px-1.5 py-0.5 bg-gray-100 text-gray-500 text-[9px] font-bold rounded">起购
                                        1 元</span>
                                </div>
                            </div>
                            <div class="space-y-2">
                                <button
                                    class="w-full px-4 py-2 bg-blue-600 text-white text-[10px] font-bold rounded-lg">查看详情</button>
                                <button
                                    class="w-full px-4 py-2 bg-white border border-blue-100 text-blue-600 text-[10px] font-bold rounded-lg">推荐话术</button>
                            </div>
                        </div>
                        <div class="data-card p-6 flex space-x-6 items-center">
                            <div
                                class="w-24 h-24 bg-red-50 rounded-2xl flex flex-col items-center justify-center text-red-600 font-bold">
                                <span class="text-[10px] uppercase">R4 风险</span>
                                <span class="text-xl">+12.4%</span>
                                <span class="text-[8px]">近一年收益</span>
                            </div>
                            <div class="flex-1">
                                <h3 class="font-bold text-gray-800">中信建投精选混合 A</h3>
                                <p class="text-[10px] text-gray-400 mt-1">专注权益投资，明星经理掌舵</p>
                                <div class="flex flex-wrap gap-1 mt-3">
                                    <span
                                        class="px-1.5 py-0.5 bg-red-100 text-red-600 text-[9px] font-bold rounded">权益首选</span>
                                    <span
                                        class="px-1.5 py-0.5 bg-gray-100 text-gray-500 text-[9px] font-bold rounded">定投优选</span>
                                </div>
                            </div>
                            <div class="space-y-2">
                                <button
                                    class="w-full px-4 py-2 bg-blue-600 text-white text-[10px] font-bold rounded-lg">查看详情</button>
                                <button
                                    class="w-full px-4 py-2 bg-white border border-blue-100 text-blue-600 text-[10px] font-bold rounded-lg">推荐话术</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="page-content space-y-6" id="page-activity-center" :class="{ active: currentPage === 'activity-center' }">
                    <h1 class="text-2xl font-bold text-gray-800">营销活动中心</h1>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <div class="data-card overflow-hidden">
                            <div
                                class="h-48 bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center relative p-8">
                                <iconify-icon class="absolute -bottom-4 -right-4 text-9xl text-white/20"
                                    icon="solar:gift-bold"></iconify-icon>
                                <div class="relative z-10 text-white text-center">
                                    <h3 class="text-xl font-bold">理财开户大礼包</h3>
                                    <p class="text-xs mt-2 opacity-80 font-medium">新客入金最高领 188 元激励金</p>
                                </div>
                            </div>
                            <div class="p-6">
                                <div class="flex justify-between items-center mb-4">
                                    <span class="text-[10px] font-bold text-gray-400">进行中 (至 2026-06-30)</span>
                                    <span
                                        class="px-2 py-1 bg-green-50 text-green-600 text-[10px] font-bold rounded-full">高转化活动</span>
                                </div>
                                <p class="text-xs text-gray-600 mb-6 leading-relaxed">适用于近期新开户但未入金客户，一键邀约入金可获得任务积分。</p>
                                <button
                                    class="w-full py-3 bg-gray-900 text-white text-sm font-bold rounded-2xl shadow-xl hover:bg-gray-800 transition-all flex items-center justify-center">
                                    <iconify-icon class="mr-2 text-lg" icon="solar:letter-bold"></iconify-icon> 一键发送邀约
                                    (企微)
                                </button>
                            </div>
                        </div>
                        <!-- Activity 2 -->
                        <div class="data-card overflow-hidden">
                            <div
                                class="h-48 bg-gradient-to-br from-blue-400 to-indigo-500 flex items-center justify-center relative p-8">
                                <iconify-icon class="absolute -bottom-4 -right-4 text-9xl text-white/20"
                                    icon="solar:cup-first-bold"></iconify-icon>
                                <div class="relative z-10 text-white text-center">
                                    <h3 class="text-xl font-bold">财富尊享私享会</h3>
                                    <p class="text-xs mt-2 opacity-80 font-medium">深度研报解读 · 顶级投研对话</p>
                                </div>
                            </div>
                            <div class="p-6">
                                <div class="flex justify-between items-center mb-4">
                                    <span class="text-[10px] font-bold text-gray-400">报名中 (05-15 14:00)</span>
                                    <span
                                        class="px-2 py-1 bg-blue-50 text-blue-600 text-[10px] font-bold rounded-full">高端客户专享</span>
                                </div>
                                <p class="text-xs text-gray-600 mb-6 leading-relaxed">适用于 AUM 50w
                                    以上高净值客户。线下沙龙，名额有限，建议重点邀约。</p>
                                <button
                                    class="w-full py-3 bg-blue-600 text-white text-sm font-bold rounded-2xl shadow-xl hover:bg-blue-700 transition-all flex items-center justify-center">
                                    <iconify-icon class="mr-2 text-lg"
                                        icon="solar:users-group-rounded-bold"></iconify-icon> 生成精准邀约话术
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="page-content space-y-6" id="page-wechat-config" :class="{ active: currentPage === 'wechat-config' }">
                    <h1 class="text-2xl font-bold text-gray-800">企微侧边栏配置</h1>
                    <div class="data-card p-8 max-w-4xl">
                        <div class="flex space-x-12">
                            <div
                                class="w-64 h-[500px] border-8 border-gray-900 rounded-[3rem] p-4 relative bg-white shadow-2xl shrink-0">
                                <div class="w-24 h-1.5 bg-gray-900 rounded-full mx-auto mb-6"></div>
                                <div class="flex items-center space-x-2 mb-4">
                                    <iconify-icon class="text-xl" icon="logos:whatsapp-icon"></iconify-icon>
                                    <span class="text-sm font-bold">企微聊天窗口</span>
                                </div>
                                <div class="bg-gray-100 h-[380px] rounded-xl relative overflow-hidden">
                                    <!-- Mock Sidebar -->
                                    <div
                                        class="absolute right-0 top-0 w-24 h-full bg-white border-l border-gray-200 p-2 space-y-3">
                                        <div
                                            class="w-full aspect-square bg-blue-50 rounded-lg flex items-center justify-center text-blue-600">
                                            <iconify-icon class="text-xl" icon="solar:user-bold"></iconify-icon></div>
                                        <div
                                            class="w-full aspect-square bg-gray-50 rounded-lg flex items-center justify-center text-gray-400">
                                            <iconify-icon class="text-xl" icon="solar:chat-line-bold"></iconify-icon>
                                        </div>
                                        <div
                                            class="w-full aspect-square bg-gray-50 rounded-lg flex items-center justify-center text-gray-400">
                                            <iconify-icon class="text-xl" icon="solar:box-bold"></iconify-icon></div>
                                        <div
                                            class="w-full aspect-square bg-gray-50 rounded-lg flex items-center justify-center text-gray-400">
                                            <iconify-icon class="text-xl" icon="solar:gallery-bold"></iconify-icon>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="flex-1 space-y-8">
                                <div>
                                    <h3 class="text-lg font-bold text-gray-800">配置您在企微侧边栏的工具</h3>
                                    <p class="text-sm text-gray-400 mt-1">勾选后工具将自动同步至您的企业微信侧边栏面板，实现一键展业。</p>
                                </div>
                                <div class="space-y-4">
                                    <label
                                        class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl border border-gray-100 cursor-pointer hover:bg-white transition-all">
                                        <div class="flex items-center space-x-4">
                                            <div
                                                class="w-10 h-10 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center">
                                                <iconify-icon class="text-xl"
                                                    icon="solar:user-rounded-bold"></iconify-icon></div>
                                            <div>
                                                <p class="text-sm font-bold text-gray-800">客户 360° 快捷入口</p>
                                                <p class="text-[10px] text-gray-400">在聊天时快速查看客户画像与资产</p>
                                            </div>
                                        </div>
                                        <input checked="" class="w-5 h-5 rounded-full text-blue-600 focus:ring-0"
                                            type="checkbox" />
                                    </label>
                                    <label
                                        class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl border border-gray-100 cursor-pointer hover:bg-white transition-all">
                                        <div class="flex items-center space-x-4">
                                            <div
                                                class="w-10 h-10 bg-amber-100 text-amber-600 rounded-xl flex items-center justify-center">
                                                <iconify-icon class="text-xl"
                                                    icon="solar:chat-line-bold"></iconify-icon></div>
                                            <div>
                                                <p class="text-sm font-bold text-gray-800">快捷话术 (AI 实时推荐)</p>
                                                <p class="text-[10px] text-gray-400">按聊天语境自动匹配最佳话术</p>
                                            </div>
                                        </div>
                                        <input checked="" class="w-5 h-5 rounded-full text-blue-600 focus:ring-0"
                                            type="checkbox" />
                                    </label>
                                    <label
                                        class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl border border-gray-100 cursor-pointer hover:bg-white transition-all">
                                        <div class="flex items-center space-x-4">
                                            <div
                                                class="w-10 h-10 bg-indigo-100 text-indigo-600 rounded-xl flex items-center justify-center">
                                                <iconify-icon class="text-xl" icon="solar:box-bold"></iconify-icon>
                                            </div>
                                            <div>
                                                <p class="text-sm font-bold text-gray-800">产品快捷推荐</p>
                                                <p class="text-[10px] text-gray-400">聊天窗口直接发送产品海报与详情</p>
                                            </div>
                                        </div>
                                        <input class="w-5 h-5 rounded-full text-blue-600 focus:ring-0"
                                            type="checkbox" />
                                    </label>
                                </div>
                                <button
                                    class="w-full py-4 bg-blue-600 text-white font-bold rounded-2xl shadow-xl shadow-blue-100">保存并更新配置</button>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- AI 批量处理 -->
                <div class="page-content space-y-6" id="page-ai-batch" :class="{ active: currentPage === 'ai-batch' }">
                  <div class="flex items-center justify-between">
                    <div>
                      <h1 class="text-xl font-bold text-gray-800 flex items-center gap-2">
                        <iconify-icon icon="solar:cpu-bolt-bold-duotone" class="text-indigo-600 text-2xl"></iconify-icon>
                        AI 批量处理
                      </h1>
                      <p class="text-sm text-slate-500 mt-1">以下为系统自动筛选的低优先级任务，可交由 AI 代为执行，执行结果将自动留痕</p>
                    </div>
                    <button
                      @click="confirmAiBatch"
                      :disabled="aiBatchSelected.length === 0"
                      class="px-6 py-2.5 bg-indigo-600 text-white text-sm font-bold rounded-xl shadow-lg shadow-indigo-100 hover:bg-indigo-700 transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                      <iconify-icon icon="lucide:play-circle" width="16"></iconify-icon>
                      确认执行 {{ aiBatchSelected.length > 0 ? `(${aiBatchSelected.length}项)` : '' }}
                    </button>
                  </div>

                  <!-- 统计条 -->
                  <div class="grid grid-cols-3 gap-4">
                    <div class="bg-white border border-slate-200 rounded-2xl p-4 flex items-center gap-3">
                      <div class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center shrink-0">
                        <iconify-icon icon="lucide:list-checks" width="20"></iconify-icon>
                      </div>
                      <div>
                        <p class="text-2xl font-bold text-slate-900">{{ aiBatchTasks.length }}</p>
                        <p class="text-xs text-slate-400">低优任务总数</p>
                      </div>
                    </div>
                    <div class="bg-white border border-slate-200 rounded-2xl p-4 flex items-center gap-3">
                      <div class="w-10 h-10 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center shrink-0">
                        <iconify-icon icon="lucide:check-square" width="20"></iconify-icon>
                      </div>
                      <div>
                        <p class="text-2xl font-bold text-emerald-600">{{ aiBatchSelected.length }}</p>
                        <p class="text-xs text-slate-400">已选中</p>
                      </div>
                    </div>
                    <div class="bg-white border border-slate-200 rounded-2xl p-4 flex items-center gap-3">
                      <div class="w-10 h-10 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center shrink-0">
                        <iconify-icon icon="lucide:clock" width="20"></iconify-icon>
                      </div>
                      <div>
                        <p class="text-2xl font-bold text-slate-900">≈ {{ aiBatchTasks.length * 3 }}min</p>
                        <p class="text-xs text-slate-400">预计节省时间</p>
                      </div>
                    </div>
                  </div>

                  <!-- 全选操作栏 -->
                  <div class="flex items-center justify-between bg-indigo-50 border border-indigo-100 rounded-xl px-4 py-2.5">
                    <label class="flex items-center gap-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        class="w-4 h-4 rounded text-indigo-600 focus:ring-0"
                        :checked="aiBatchSelected.length === aiBatchTasks.length && aiBatchTasks.length > 0"
                        @change="toggleSelectAll"
                      />
                      <span class="text-sm font-medium text-indigo-700">全选 / 取消全选</span>
                    </label>
                    <span class="text-xs text-indigo-500">共 {{ aiBatchTasks.length }} 项低优先级任务</span>
                  </div>

                  <!-- 任务列表 -->
                  <div class="space-y-3">
                    <div v-if="aiBatchTasks.length === 0" class="text-center text-slate-400 py-16">
                      <iconify-icon icon="lucide:check-circle-2" width="36" class="mb-3 opacity-30"></iconify-icon>
                      <p class="text-sm">暂无低优先级任务</p>
                    </div>
                    <div
                      v-for="t in aiBatchTasks"
                      :key="t.id"
                      class="bg-white border rounded-xl px-5 py-4 flex items-center gap-4 cursor-pointer transition-all"
                      :class="aiBatchSelected.includes(t.id) ? 'border-indigo-300 shadow-sm shadow-indigo-50' : 'border-slate-200 hover:border-slate-300'"
                      @click="toggleBatchItem(t.id)"
                    >
                      <input
                        type="checkbox"
                        class="w-4 h-4 rounded text-indigo-600 focus:ring-0 shrink-0"
                        :checked="aiBatchSelected.includes(t.id)"
                        @click.stop
                        @change="toggleBatchItem(t.id)"
                      />
                      <div class="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
                           :class="taskTypeIconBg(t.task_type)">
                        <iconify-icon :icon="taskTypeIcon(t.task_type)" width="16" :class="taskTypeIconColor(t.task_type)"></iconify-icon>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-bold text-slate-900 flex items-center gap-1.5 flex-wrap">
                          {{ t.task_name }}<template v-if="t.cust_name"> · {{ t.cust_name }}</template>
                          <span class="px-1.5 py-0.5 bg-slate-100 text-slate-500 text-[9px] rounded font-bold">低优</span>
                        </p>
                        <p class="text-[10px] text-slate-400 mt-0.5">{{ t.task_type }} · {{ t.task_sub_type }} · 截止 {{ t.due_date }}</p>
                      </div>
                      <span class="text-[10px] px-2 py-1 bg-slate-100 text-slate-500 rounded-lg font-medium shrink-0">{{ t.status }}</span>
                    </div>
                  </div>

                  <!-- AI 执行说明 -->
                  <div class="bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-100 rounded-2xl p-5 flex gap-4">
                    <iconify-icon icon="lucide:info" width="18" class="text-indigo-500 shrink-0 mt-0.5"></iconify-icon>
                    <div class="text-xs text-indigo-700 space-y-1 leading-relaxed">
                      <p class="font-bold text-indigo-900">AI 执行说明</p>
                      <p>· AI 将按照系统 SOP 自动完成选中任务，包括外呼、信息推送、客户触达等操作</p>
                      <p>· 所有操作均会自动留痕，记录于对应客户的服务档案中</p>
                      <p>· AI 执行期间您可继续处理其他工作，执行完成后将通知您查看结果</p>
                    </div>
                  </div>
                </div>

                <!-- 其他页面模块（ai-chat / marketing-materials 等）可按相同逻辑补充 -->

                <!-- Toast 提示 -->
                <Teleport to="body">
                    <Transition enter-active-class="transition ease-out duration-200"
                                enter-from-class="opacity-0 translate-y-2"
                                enter-to-class="opacity-100 translate-y-0"
                                leave-active-class="transition ease-in duration-150"
                                leave-from-class="opacity-100 translate-y-0"
                                leave-to-class="opacity-0 translate-y-2">
                        <div v-if="showToast"
                             class="fixed bottom-8 left-1/2 -translate-x-1/2 z-[300] px-5 py-3 bg-gray-800 text-white text-sm font-medium rounded-xl shadow-xl flex items-center gap-2">
                            <iconify-icon icon="solar:info-circle-linear" class="text-blue-400 text-base shrink-0"></iconify-icon>
                            {{ toastMsg }}
                        </div>
                    </Transition>
                </Teleport>

                <!-- 表头编辑器抽屉 -->
                <Teleport to="body">
                    <div v-if="showColumnEditor" class="fixed inset-0 z-[200] flex items-stretch justify-end">
                        <!-- 遮罩 -->
                        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showColumnEditor = false"></div>
                        <!-- 抽屉面板 -->
                        <div class="relative w-[400px] bg-white h-full flex flex-col shadow-2xl">
                            <!-- 头部 -->
                            <div class="px-6 py-5 border-b border-gray-100 flex items-center justify-between shrink-0">
                                <div>
                                    <h2 class="text-base font-bold text-gray-900">自定义表头</h2>
                                    <p class="text-[11px] text-gray-400 mt-0.5">选择在客户列表中展示的字段</p>
                                </div>
                                <button @click="showColumnEditor = false" class="p-2 hover:bg-gray-100 rounded-lg transition-colors text-gray-400">
                                    <iconify-icon icon="lucide:x" width="18"></iconify-icon>
                                </button>
                            </div>
                            <!-- 已选提示条 -->
                            <div class="px-6 py-2.5 bg-blue-50 border-b border-blue-100 shrink-0 flex items-center justify-between">
                                <p class="text-xs text-blue-700 font-medium">
                                    已选 <span class="font-bold text-blue-900">{{ enabledColumns.length }}</span> 个字段
                                </p>
                                <p class="text-[10px] text-blue-500">建议不超过 8 个以保证显示效果</p>
                            </div>
                            <!-- 字段分组列表 -->
                            <div class="flex-1 overflow-y-auto p-5 space-y-5">
                                <div v-for="(cols, groupName) in columnGroups" :key="groupName" class="space-y-1.5">
                                    <h3 class="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-2 mb-2">{{ groupName }}</h3>
                                    <label v-for="col in cols" :key="col.key"
                                           class="flex items-center justify-between px-3 py-2.5 rounded-xl cursor-pointer transition-all"
                                           :class="col.enabled ? 'bg-blue-50 border border-blue-100' : 'hover:bg-gray-50 border border-transparent'">
                                        <div class="flex items-center gap-2.5">
                                            <div class="w-1.5 h-1.5 rounded-full transition-colors shrink-0"
                                                 :class="col.enabled ? 'bg-blue-500' : 'bg-gray-300'"></div>
                                            <span class="text-sm font-medium" :class="col.enabled ? 'text-blue-800' : 'text-gray-700'">{{ col.label }}</span>
                                        </div>
                                        <!-- 自定义 Toggle Switch -->
                                        <div class="relative shrink-0 rounded-full cursor-pointer transition-colors"
                                             style="width:36px;height:20px;"
                                             :style="{ backgroundColor: col.enabled ? '#2563eb' : '#d1d5db' }"
                                             @click.prevent="col.enabled = !col.enabled">
                                            <span class="absolute top-0.5 bg-white rounded-full shadow-sm transition-transform"
                                                  style="width:16px;height:16px;left:2px;"
                                                  :style="{ transform: col.enabled ? 'translateX(16px)' : 'translateX(0)' }"></span>
                                        </div>
                                    </label>
                                </div>
                            </div>
                            <!-- 底部操作 -->
                            <div class="p-5 border-t border-gray-100 flex gap-3 shrink-0">
                                <button @click="resetColumns"
                                        class="flex-1 py-2.5 border border-gray-200 text-gray-600 text-sm font-bold rounded-xl hover:bg-gray-50 transition-all">
                                    重置默认
                                </button>
                                <button @click="showColumnEditor = false"
                                        class="flex-1 py-2.5 bg-blue-600 text-white text-sm font-bold rounded-xl hover:bg-blue-700 shadow-lg shadow-blue-100 transition-all">
                                    确认应用
                                </button>
                            </div>
                        </div>
                    </div>
                </Teleport>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'

const route            = useRoute()
const sidebarCollapsed = ref(false)
const currentPage      = ref('customer-list')

// ─── AI 批量处理 ───────────────────────────────────────────────
const LOGIN_ID_BATCH  = 'oa001'
const API_BASE_BATCH  = import.meta.env.VITE_API_BASE ?? ''
const aiBatchTasks    = ref([])       // 所有低优未完成任务
const aiBatchSelected = ref([])       // 已选中的任务 id 列表

async function loadAiBatchTasks() {
  try {
    const res  = await fetch(`${API_BASE_BATCH}/api/staff/tasks?login_id=${LOGIN_ID_BATCH}&page_size=100`)
    const data = await res.json()
    const low  = (data.tasks || []).filter(t =>
      t.priority === '低' && ['待处理', '处理中'].includes(t.status)
    )
    aiBatchTasks.value    = low
    aiBatchSelected.value = low.map(t => t.id)   // 默认全选
  } catch (e) {
    console.warn('[ai-batch] fetch failed:', e)
  }
}

function toggleSelectAll() {
  if (aiBatchSelected.value.length === aiBatchTasks.value.length) {
    aiBatchSelected.value = []
  } else {
    aiBatchSelected.value = aiBatchTasks.value.map(t => t.id)
  }
}

function toggleBatchItem(id) {
  const idx = aiBatchSelected.value.indexOf(id)
  if (idx === -1) aiBatchSelected.value.push(id)
  else aiBatchSelected.value.splice(idx, 1)
}

function confirmAiBatch() {
  if (aiBatchSelected.value.length === 0) return
  // TODO: 调用后端批量执行接口；目前 mock 提示
  alert(`已向 AI 发起 ${aiBatchSelected.value.length} 项任务的批量执行指令，执行结果将自动留痕`)
}

// 任务类型图标映射
function taskTypeIcon(type) {
  const map = { '建联类': 'lucide:phone-call', '跟进类': 'lucide:user-check', '周期类': 'lucide:refresh-cw', '营销活动类': 'lucide:megaphone', '合规类': 'lucide:shield-check' }
  return map[type] || 'lucide:clipboard-list'
}
function taskTypeIconBg(type) {
  const map = { '建联类': 'bg-blue-50', '跟进类': 'bg-emerald-50', '周期类': 'bg-purple-50', '营销活动类': 'bg-orange-50', '合规类': 'bg-amber-50' }
  return map[type] || 'bg-slate-50'
}
function taskTypeIconColor(type) {
  const map = { '建联类': 'text-blue-500', '跟进类': 'text-emerald-500', '周期类': 'text-purple-500', '营销活动类': 'text-orange-500', '合规类': 'text-amber-500' }
  return map[type] || 'text-slate-500'
}

let contributionChartInstance = null
let radarChartInstance = null

const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
}

// ─── 客户 360 ────────────────────────────────────────────────
const selectedCustomer = ref(null)

const openCustomer360 = (customer) => {
    selectedCustomer.value = customer
    switchHallPage('customer-360')
}

const calcAccountAge = (openDate) => {
    if (!openDate) return '—'
    const days = Math.floor((Date.now() - new Date(openDate)) / 86400000)
    return days.toLocaleString() + ' 天'
}

const riskTextColor = (risk) => {
    if (!risk) return 'text-gray-700'
    if (risk.startsWith('R5') || risk.startsWith('R4')) return 'text-red-600'
    if (risk.startsWith('R3')) return 'text-amber-600'
    return 'text-green-600'
}

const switchHallPage = (pageName) => {
    currentPage.value = pageName
    if (pageName === 'ai-batch' && aiBatchTasks.value.length === 0) {
      loadAiBatchTasks()
    }
    if (pageName === 'customer-360') {
        nextTick(() => {
            contributionChartInstance?.resize()
            radarChartInstance?.resize()
        })
    }
}

// ─── 筛选状态 ────────────────────────────────────────────────
const filterForm = reactive({ contactStatus: '', assetLevel: '', follow_status: '', riskLevel: '' })
const resetFilter = () => {
    filterForm.contactStatus = ''
    filterForm.assetLevel    = ''
    filterForm.follow_status = ''
    filterForm.riskLevel     = ''
    listPage.value = 1
    fetchCustomers()
}
watch(filterForm, () => { listPage.value = 1; fetchCustomers() })

// ─── 分页 & 加载 ─────────────────────────────────────────────
const listPage = ref(1)
const pageSize  = ref(20)
const totalCount  = ref(0)
const loading     = ref(false)

// ─── 关键词搜索 ────────────────────────────────────────────────
const keyword = ref('')
let _kwTimer = null
watch(keyword, () => {
    clearTimeout(_kwTimer)
    _kwTimer = setTimeout(() => { listPage.value = 1; fetchCustomers() }, 300)
})

// ─── 每日提醒 ──────────────────────────────────────────────────
const alertPanelOpen  = ref(false)
const alerts          = ref([])
const newAlertContent = ref('')
const unreadAlertCount = computed(() => alerts.value.length)

const _onClickOutsideAlert = (e) => {
    const panel = document.querySelector('.alert-panel-wrapper')
    if (panel && !panel.contains(e.target)) alertPanelOpen.value = false
}

const fetchAlerts = async () => {
    try {
        const res  = await fetch(`/api/manager/alerts?login_id=${STAFF_LOGIN_ID}`)
        const json = await res.json()
        if (json.code === 200) alerts.value = json.data
    } catch (e) { console.error('fetchAlerts error', e) }
}

const markAlertDone = async (alert) => {
    alert._marking = true
    try {
        const res  = await fetch(`/api/manager/alerts/${alert.alert_id}/done`, { method: 'PATCH' })
        const json = await res.json()
        if (json.code === 200) alerts.value = alerts.value.filter(a => a.alert_id !== alert.alert_id)
    } catch (e) { console.error('markAlertDone error', e) }
    finally { alert._marking = false }
}

const addAlert = async () => {
    const content = newAlertContent.value.trim()
    if (!content) return
    try {
        const res  = await fetch('/api/manager/alerts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login_id: STAFF_LOGIN_ID, alert_content: content }),
        })
        const json = await res.json()
        if (json.code === 200) { alerts.value.unshift(json.data); newAlertContent.value = '' }
    } catch (e) { console.error('addAlert error', e) }
}

// ─── 当前日期 ──────────────────────────────────────────────────
const todayStr = (() => {
    const d = new Date()
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}年${m}月${day}日`
})()

// ─── API 调用 ─────────────────────────────────────────────────
const STAFF_LOGIN_ID = 'oa001'   // TODO: 接入认证系统后替换为当前登录员工 OA

const fetchCustomers = async () => {
    loading.value = true
    try {
        const params = new URLSearchParams({ login_id: STAFF_LOGIN_ID, page: listPage.value, page_size: pageSize.value })
        if (keyword.value)              params.set('keyword',        keyword.value)
        if (filterForm.contactStatus)   params.set('contact_status', filterForm.contactStatus)
        if (filterForm.assetLevel)      params.set('asset_level',    filterForm.assetLevel)
        if (filterForm.follow_status)   params.set('follow_status',  filterForm.follow_status)
        if (filterForm.riskLevel)       params.set('risk_level',     filterForm.riskLevel)
        params.set('sort_field', sortField.value)
        params.set('sort_dir',   sortDir.value)

        const res  = await fetch(`/api/staff/customers?${params}`)
        const json = await res.json()
        if (json.code === 200) {
            customers.value = json.data.list
            totalCount.value = json.data.total
        }
    } catch (e) {
        console.error('fetchCustomers error', e)
    } finally {
        loading.value = false
    }
}

// ─── 排序状态 ────────────────────────────────────────────────
const sortField = ref('t1_aum')
const sortDir = ref('desc')

// ─── Toast 提示 ───────────────────────────────────────────────
const showToast = ref(false)
const toastMsg  = ref('')
let _toastTimer = null
const showToastMsg = (msg, duration = 3000) => {
    toastMsg.value  = msg
    showToast.value = true
    clearTimeout(_toastTimer)
    _toastTimer = setTimeout(() => { showToast.value = false }, duration)
}

// ─── 表头自定义 ───────────────────────────────────────────────
const showColumnEditor = ref(false)

const allColumns = ref([
    // 建联信息
    { key: 'contactStatus',        label: '建联状态',           group: '建联信息',   align: 'center', enabled: true  },
    { key: 'phone',                label: '联系电话',           group: '建联信息',   align: 'left',   enabled: false },
    { key: 'follow_status',        label: '跟进状态',           group: '建联信息',   align: 'center', enabled: true  },
    // 基础信息（key 与 API 响应字段名完全对应）
    { key: 'hdly',                 label: '来源渠道',           group: '基础信息',   align: 'left',   enabled: true  },
    { key: 'relation_type',        label: '关系类型',           group: '基础信息',   align: 'left',   enabled: false },
    { key: 'gender',               label: '性别',               group: '基础信息',   align: 'center', enabled: false },
    { key: 'open_date',            label: '开户日期',           group: '基础信息',   align: 'left',   enabled: false },
    { key: 'age',                  label: '年龄',               group: '基础信息',   align: 'center', enabled: false },
    { key: 'remark',               label: '备注',               group: '基础信息',   align: 'left',   enabled: true  },
    // 资产与收益
    { key: 'aum',                  label: 'T-1日AUM资产（万）', group: '资产与收益', align: 'right',  enabled: true  },
    { key: 'assetLevel',           label: '资产等级',           group: '资产与收益', align: 'center', enabled: true  },
    { key: 'annualReturn',         label: '本年收益',           group: '资产与收益', align: 'right',  enabled: false },
    // 佣金信息
    { key: 'commission_this_year', label: '本年佣金贡献',       group: '佣金信息',   align: 'right',  enabled: false },
    { key: 'commission_last_year', label: '去年佣金贡献',       group: '佣金信息',   align: 'right',  enabled: false },
    { key: 'commission_rate',      label: '佣金费率',           group: '佣金信息',   align: 'center', enabled: false },
    // 交易信息
    { key: 'trade_exp_months',     label: '交易经验（月）',     group: '交易信息',   align: 'center', enabled: false },
    { key: 'riskLevel',            label: '风险等级',           group: '交易信息',   align: 'center', enabled: true  },
])

const columnGroups = computed(() => {
    const groups = {}
    allColumns.value.forEach(col => {
        if (!groups[col.group]) groups[col.group] = []
        groups[col.group].push(col)
    })
    return groups
})

const enabledColumns = computed(() => allColumns.value.filter(c => c.enabled))

const defaultEnabledKeys = ['contactStatus', 'follow_status', 'hdly', 'remark', 'aum', 'assetLevel', 'riskLevel']
function resetColumns() {
    allColumns.value.forEach(col => { col.enabled = defaultEnabledKeys.includes(col.key) })
}

// ─── 颜色辅助函数 ──────────────────────────────────────────────
const getFollowClass = (status) => {
    if (status === '近3日内联系过')  return 'text-emerald-500'
    if (status === '近7日内联系过')  return 'text-teal-500'
    if (status === '近15日内联系过') return 'text-amber-500'
    if (status === '近30日内联系过') return 'text-orange-500'
    return 'text-zinc-400'
}
const getAssetLevelClass = (level) => {
    if (level === '高价值')   return 'bg-rose-50 text-rose-600 border border-rose-100'
    if (level === '中等价值') return 'bg-amber-50 text-amber-600 border border-amber-100'
    return 'bg-gray-100 text-gray-500 border border-gray-200'
}
const getRiskColor = (risk) => {
    if (!risk) return 'text-gray-400'
    if (risk.startsWith('R5')) return 'text-red-600'
    if (risk.startsWith('R4')) return 'text-red-500'
    if (risk.startsWith('R3')) return 'text-amber-500'
    if (risk.startsWith('R2')) return 'text-blue-600'
    if (risk.startsWith('R1')) return 'text-green-600'
    return 'text-gray-400'
}

// ─── 客户数据（由 fetchCustomers 填充）────────────────────────
const customers = ref([])

// ─── SOP 模块响应式数据 ─────────────────────────────────────────
const currentSopTab = ref('connect')
const expandedSopId  = ref(null)

const sopTabs = [
    { key: 'connect',    label: '建联类'     },
    { key: 'follow',     label: '跟进类'     },
    { key: 'cycle',      label: '周期类'     },
    { key: 'activity',   label: '营销活动类' },
    { key: 'compliance', label: '合规类'     },
]

const productMeta = {
    '通用':     { labelColor: 'text-gray-400',    productTagClass: 'bg-gray-100 text-gray-600',      iconBg: 'bg-gray-50',    iconColor: 'text-gray-500'    },
    '股票':     { labelColor: 'text-blue-400',    productTagClass: 'bg-blue-50 text-blue-600',       iconBg: 'bg-blue-50',    iconColor: 'text-blue-600'    },
    '基金/ETF': { labelColor: 'text-emerald-400', productTagClass: 'bg-emerald-50 text-emerald-700', iconBg: 'bg-emerald-50', iconColor: 'text-emerald-600' },
    '投顾':     { labelColor: 'text-indigo-400',  productTagClass: 'bg-indigo-50 text-indigo-600',   iconBg: 'bg-indigo-50',  iconColor: 'text-indigo-600'  },
    '两融':     { labelColor: 'text-orange-400',  productTagClass: 'bg-orange-50 text-orange-600',   iconBg: 'bg-orange-50',  iconColor: 'text-orange-600'  },
    '期权':     { labelColor: 'text-purple-400',  productTagClass: 'bg-purple-50 text-purple-600',   iconBg: 'bg-purple-50',  iconColor: 'text-purple-600'  },
    '期货':     { labelColor: 'text-red-400',     productTagClass: 'bg-red-50 text-red-500',         iconBg: 'bg-red-50',     iconColor: 'text-red-500'     },
}

const sopData = [
    // ── 建联类 ──────────────────────────────────────────────────────
    { id: 'sop_c01', taskType: 'connect', product: '通用', name: '新客激活SOP',
      icon: 'solar:star-bold-duotone', desc: '开户后30天内完成首次触达，引导首笔交易，建立基础信任关系',
      minRisk: null, eligibleCount: 23, stepCount: 5, autoTrigger: false, runningCount: 7,
      steps: [
        { seq: 1, action: '欢迎外呼',     taskType: '建联类', timing: 'D+0',  aiCapable: true,  required: false },
        { seq: 2, action: '推送开户礼包', taskType: '建联类', timing: 'D+1',  aiCapable: true,  required: false },
        { seq: 3, action: '引导首笔交易', taskType: '跟进类', timing: 'D+3',  aiCapable: false, required: false },
        { seq: 4, action: '产品匹配推荐', taskType: '跟进类', timing: 'D+7',  aiCapable: false, required: false },
        { seq: 5, action: '激活结案',     taskType: '建联类', timing: 'D+14', aiCapable: true,  required: false },
      ]},
    { id: 'sop_c02', taskType: 'connect', product: '基金/ETF', name: '基金定投引导SOP',
      icon: 'solar:graph-new-up-bold-duotone', desc: '面向有理财需求但未开始定投的客户，分步引导建立定投习惯',
      minRisk: 'R3', eligibleCount: 31, stepCount: 4, autoTrigger: false, runningCount: 5,
      steps: [
        { seq: 1, action: '概念科普外呼', taskType: '建联类', timing: 'D+0', aiCapable: true,  required: false },
        { seq: 2, action: '推送定投方案', taskType: '建联类', timing: 'D+1', aiCapable: true,  required: false },
        { seq: 3, action: '跟进开通意向', taskType: '跟进类', timing: 'D+3', aiCapable: false, required: false },
        { seq: 4, action: '辅助开通定投', taskType: '跟进类', timing: 'D+5', aiCapable: false, required: false },
      ]},
    { id: 'sop_c03', taskType: 'connect', product: '两融', name: '两融开户引导SOP',
      icon: 'solar:double-alt-arrow-up-bold-duotone', desc: '面向资产达标、R4+风险等级、无两融账户的客户，完成两融开户全流程',
      minRisk: 'R4', eligibleCount: 18, stepCount: 6, autoTrigger: false, runningCount: 4,
      steps: [
        { seq: 1, action: '外呼介绍两融', taskType: '建联类', timing: 'D+0',  aiCapable: true,  required: false },
        { seq: 2, action: '发送开户材料', taskType: '建联类', timing: 'D+2',  aiCapable: true,  required: false },
        { seq: 3, action: '跟进申请进度', taskType: '跟进类', timing: 'D+5',  aiCapable: false, required: false },
        { seq: 4, action: '辅助完成申请', taskType: '跟进类', timing: 'D+7',  aiCapable: false, required: false },
        { seq: 5, action: '完成双录',     taskType: '合规类', timing: 'D+10', aiCapable: false, required: true  },
        { seq: 6, action: '首笔融资引导', taskType: '跟进类', timing: 'D+14', aiCapable: true,  required: false },
      ]},
    { id: 'sop_c04', taskType: 'connect', product: '期权', name: '期权资格引导SOP',
      icon: 'solar:chart-bold-duotone', desc: '面向R4+风险等级、有股票持仓的客户，引导完成期权开户资格认证',
      minRisk: 'R4', eligibleCount: 12, stepCount: 5, autoTrigger: false, runningCount: 3,
      steps: [
        { seq: 1, action: '外呼介绍期权',   taskType: '建联类', timing: 'D+0',  aiCapable: true,  required: false },
        { seq: 2, action: '推送知识备考包', taskType: '建联类', timing: 'D+1',  aiCapable: true,  required: false },
        { seq: 3, action: '跟进测试意向',   taskType: '跟进类', timing: 'D+5',  aiCapable: false, required: false },
        { seq: 4, action: '辅助资质申请',   taskType: '跟进类', timing: 'D+10', aiCapable: false, required: false },
        { seq: 5, action: '首个策略推荐',   taskType: '跟进类', timing: 'D+14', aiCapable: false, required: true  },
      ]},
    { id: 'sop_c05', taskType: 'connect', product: '期货', name: '期货资格引导SOP',
      icon: 'solar:chart-2-bold-duotone', desc: '面向R5风险等级、有大宗商品交易意向的客户，完成期货开户资格认证',
      minRisk: 'R5', eligibleCount: 6, stepCount: 5, autoTrigger: false, runningCount: 1,
      steps: [
        { seq: 1, action: '外呼评估意向', taskType: '建联类', timing: 'D+0',  aiCapable: false, required: false },
        { seq: 2, action: '适当性评估',   taskType: '合规类', timing: 'D+1',  aiCapable: false, required: true  },
        { seq: 3, action: '推送开户材料', taskType: '建联类', timing: 'D+3',  aiCapable: true,  required: false },
        { seq: 4, action: '辅助完成开户', taskType: '跟进类', timing: 'D+7',  aiCapable: false, required: false },
        { seq: 5, action: '品种策略介绍', taskType: '跟进类', timing: 'D+14', aiCapable: false, required: true  },
      ]},
    // ── 跟进类 ──────────────────────────────────────────────────────
    { id: 'sop_f01', taskType: 'follow', product: '基金/ETF', name: '基金到期续作SOP',
      icon: 'solar:refresh-circle-bold-duotone', desc: '产品到期前7天自动触发，引导客户完成续作或转投同类产品',
      minRisk: null, eligibleCount: 9, stepCount: 4, autoTrigger: false, runningCount: 9,
      steps: [
        { seq: 1, action: '到期前7天提醒', taskType: '跟进类', timing: '到期前D-7', aiCapable: true,  required: false },
        { seq: 2, action: '推荐续作产品',  taskType: '跟进类', timing: '到期前D-5', aiCapable: true,  required: false },
        { seq: 3, action: '外呼确认意向',  taskType: '跟进类', timing: '到期前D-3', aiCapable: false, required: false },
        { seq: 4, action: '协助办理续作',  taskType: '跟进类', timing: '到期前D-1', aiCapable: false, required: false },
      ]},
    { id: 'sop_f02', taskType: 'follow', product: '基金/ETF', name: '持仓亏损安抚SOP',
      icon: 'solar:shield-warning-bold-duotone', desc: '客户基金持仓跌幅超过5%时触发，及时安抚并提供调仓建议',
      minRisk: null, eligibleCount: 14, stepCount: 4, autoTrigger: true, runningCount: 2,
      steps: [
        { seq: 1, action: '亏损预警推送', taskType: '跟进类', timing: '触发当日', aiCapable: true,  required: false },
        { seq: 2, action: '安抚外呼',     taskType: '跟进类', timing: '触发当日', aiCapable: false, required: false },
        { seq: 3, action: '推荐调仓方案', taskType: '跟进类', timing: 'D+1',      aiCapable: false, required: false },
        { seq: 4, action: '跟进处理结果', taskType: '跟进类', timing: 'D+3',      aiCapable: false, required: false },
      ]},
    { id: 'sop_f03', taskType: 'follow', product: '投顾', name: '投顾签约转化SOP',
      icon: 'solar:user-speak-bold-duotone', desc: '面向资产规模较高、多次接受产品推荐的客户，引导签约投顾服务',
      minRisk: 'R3', eligibleCount: 7, stepCount: 5, autoTrigger: false, runningCount: 2,
      steps: [
        { seq: 1, action: '投顾价值介绍', taskType: '跟进类', timing: 'D+0',  aiCapable: true,  required: false },
        { seq: 2, action: '约面谈/视频',  taskType: '跟进类', timing: 'D+3',  aiCapable: false, required: false },
        { seq: 3, action: '提供配置方案', taskType: '跟进类', timing: 'D+5',  aiCapable: false, required: true  },
        { seq: 4, action: '跟进签约决策', taskType: '跟进类', timing: 'D+7',  aiCapable: false, required: false },
        { seq: 5, action: '完成签约',     taskType: '合规类', timing: 'D+10', aiCapable: false, required: true  },
      ]},
    { id: 'sop_f04', taskType: 'follow', product: '两融', name: '融资额度激活SOP',
      icon: 'solar:card-bold-duotone', desc: '两融额度闲置超30天时触发，推动首次使用或恢复使用融资额度',
      minRisk: 'R4', eligibleCount: 11, stepCount: 4, autoTrigger: true, runningCount: 6,
      steps: [
        { seq: 1, action: '推送市场机会', taskType: '跟进类', timing: '触发当日', aiCapable: true,  required: false },
        { seq: 2, action: '外呼激活沟通', taskType: '跟进类', timing: 'D+1',      aiCapable: false, required: false },
        { seq: 3, action: '推荐融资标的', taskType: '跟进类', timing: 'D+2',      aiCapable: false, required: true  },
        { seq: 4, action: '跟进使用结果', taskType: '跟进类', timing: 'D+7',      aiCapable: false, required: false },
      ]},
    { id: 'sop_f05', taskType: 'follow', product: '期权', name: '持仓保护策略SOP',
      icon: 'solar:shield-bold-duotone', desc: '面向持有大量单只股票的客户，推荐保护性认沽期权对冲下跌风险',
      minRisk: 'R4', eligibleCount: 8, stepCount: 4, autoTrigger: false, runningCount: 2,
      steps: [
        { seq: 1, action: '持仓分析推送', taskType: '跟进类', timing: 'D+0',       aiCapable: true,  required: false },
        { seq: 2, action: '策略讲解外呼', taskType: '跟进类', timing: 'D+1',       aiCapable: false, required: true  },
        { seq: 3, action: '推荐具体合约', taskType: '跟进类', timing: 'D+2',       aiCapable: false, required: true  },
        { seq: 4, action: '到期前跟进',   taskType: '周期类', timing: '到期前D-5', aiCapable: true,  required: false },
      ]},
    { id: 'sop_f06', taskType: 'follow', product: '期权', name: '备兑开仓增收SOP',
      icon: 'solar:money-bag-bold-duotone', desc: '面向持有大量股票且不打算短期卖出的客户，推荐备兑开仓赚取权利金',
      minRisk: 'R4', eligibleCount: 5, stepCount: 4, autoTrigger: false, runningCount: 1,
      steps: [
        { seq: 1, action: '备兑策略介绍', taskType: '跟进类', timing: 'D+0',       aiCapable: true,  required: false },
        { seq: 2, action: '外呼确认意向', taskType: '跟进类', timing: 'D+2',       aiCapable: false, required: false },
        { seq: 3, action: '推荐合约月份', taskType: '跟进类', timing: 'D+3',       aiCapable: false, required: true  },
        { seq: 4, action: '到期处理跟进', taskType: '周期类', timing: '到期前D-3', aiCapable: true,  required: false },
      ]},
    // ── 周期类 ──────────────────────────────────────────────────────
    { id: 'sop_y01', taskType: 'cycle', product: '通用', name: '流失预警挽留SOP',
      icon: 'solar:user-minus-bold-duotone', desc: '识别连续30天无操作客户，启动多轮专项挽留触达',
      minRisk: null, eligibleCount: 19, stepCount: 5, autoTrigger: true, runningCount: 8,
      steps: [
        { seq: 1, action: '流失识别推送',   taskType: '周期类', timing: '系统触发', aiCapable: true,  required: false },
        { seq: 2, action: '需求挖掘沟通',   taskType: '跟进类', timing: 'D+3',      aiCapable: false, required: false },
        { seq: 3, action: '个性化方案推荐', taskType: '跟进类', timing: 'D+5',      aiCapable: false, required: false },
        { seq: 4, action: '二次跟进',       taskType: '周期类', timing: 'D+10',     aiCapable: true,  required: false },
        { seq: 5, action: '挽留结案',       taskType: '周期类', timing: 'D+14',     aiCapable: false, required: false },
      ]},
    { id: 'sop_y02', taskType: 'cycle', product: '股票', name: '账户沉默唤醒SOP',
      icon: 'solar:bell-bold-duotone', desc: '股票账户连续60天无交易，通过市场热点资讯触发激活',
      minRisk: null, eligibleCount: 33, stepCount: 3, autoTrigger: true, runningCount: 12,
      steps: [
        { seq: 1, action: '热点资讯推送',   taskType: '周期类', timing: '触发当日', aiCapable: true,  required: false },
        { seq: 2, action: '外呼激活沟通',   taskType: '周期类', timing: 'D+2',      aiCapable: true,  required: false },
        { seq: 3, action: '个性化标的推荐', taskType: '跟进类', timing: 'D+5',      aiCapable: false, required: false },
      ]},
    { id: 'sop_y03', taskType: 'cycle', product: '基金/ETF', name: '定投复投引导SOP',
      icon: 'solar:repeat-bold-duotone', desc: '对完成一期定投的客户，每季度引导增加定投金额或开启新定投计划',
      minRisk: 'R3', eligibleCount: 27, stepCount: 3, autoTrigger: false, runningCount: 11,
      steps: [
        { seq: 1, action: '定投成果回顾',   taskType: '周期类', timing: '每季度',  aiCapable: true,  required: false },
        { seq: 2, action: '增额/新开建议', taskType: '周期类', timing: '季度+D3', aiCapable: true,  required: false },
        { seq: 3, action: '外呼确认跟进',   taskType: '跟进类', timing: '季度+D5', aiCapable: false, required: false },
      ]},
    { id: 'sop_y04', taskType: 'cycle', product: '投顾', name: '投顾年度续签SOP',
      icon: 'solar:diploma-bold-duotone', desc: '投顾协议到期前60天启动，完成年度服务回顾与续签引导',
      minRisk: null, eligibleCount: 4, stepCount: 4, autoTrigger: true, runningCount: 2,
      steps: [
        { seq: 1, action: '年度报告推送', taskType: '周期类', timing: '到期前D-60', aiCapable: true,  required: false },
        { seq: 2, action: '续签价值沟通', taskType: '跟进类', timing: '到期前D-30', aiCapable: false, required: false },
        { seq: 3, action: '提供新年方案', taskType: '跟进类', timing: '到期前D-14', aiCapable: false, required: true  },
        { seq: 4, action: '完成续签',     taskType: '合规类', timing: '到期前D-7',  aiCapable: false, required: true  },
      ]},
    { id: 'sop_y05', taskType: 'cycle', product: '两融', name: '维保比例预警SOP',
      icon: 'solar:danger-bold-duotone', desc: '维保比例低于150%时系统自动触发，保障客户资产安全并完成合规留痕',
      minRisk: null, eligibleCount: 0, stepCount: 5, autoTrigger: true, runningCount: 1,
      steps: [
        { seq: 1, action: '系统预警推送',   taskType: '合规类', timing: '立即触发',   aiCapable: false, required: false },
        { seq: 2, action: '紧急外呼通知',   taskType: '合规类', timing: '触发后1H内', aiCapable: false, required: true  },
        { seq: 3, action: '建议补仓/减仓', taskType: '跟进类', timing: '当日',        aiCapable: false, required: true  },
        { seq: 4, action: '跟进处理结果',   taskType: '合规类', timing: 'D+1',        aiCapable: false, required: false },
        { seq: 5, action: '结案合规留档',   taskType: '合规类', timing: 'D+2',        aiCapable: false, required: true  },
      ]},
    { id: 'sop_y06', taskType: 'cycle', product: '两融', name: '两融权益升级SOP',
      icon: 'solar:crown-bold-duotone', desc: '对活跃两融客户每季度评估信用额度提升资格，推动额度升级',
      minRisk: 'R4', eligibleCount: 8, stepCount: 3, autoTrigger: false, runningCount: 3,
      steps: [
        { seq: 1, action: '额度资格评估', taskType: '周期类', timing: '每季度',  aiCapable: true,  required: false },
        { seq: 2, action: '升级权益推送', taskType: '周期类', timing: '季度+D1', aiCapable: true,  required: false },
        { seq: 3, action: '外呼确认申请', taskType: '跟进类', timing: '季度+D3', aiCapable: false, required: false },
      ]},
    { id: 'sop_y07', taskType: 'cycle', product: '期权', name: '期权合约到期处理SOP',
      icon: 'solar:calendar-bold-duotone', desc: '期权合约到期前5天触发，确保客户及时决策行权、平仓或展期',
      minRisk: null, eligibleCount: 6, stepCount: 3, autoTrigger: true, runningCount: 4,
      steps: [
        { seq: 1, action: '到期前5天提醒', taskType: '周期类', timing: '到期前D-5', aiCapable: true,  required: false },
        { seq: 2, action: '策略决策沟通',   taskType: '跟进类', timing: '到期前D-2', aiCapable: false, required: true  },
        { seq: 3, action: '执行并结案',     taskType: '合规类', timing: '到期当日',   aiCapable: false, required: true  },
      ]},
    { id: 'sop_y08', taskType: 'cycle', product: '期货', name: '期货移仓换月SOP',
      icon: 'solar:transfer-horizontal-bold-duotone', desc: '期货合约最后交易日前10天触发，引导客户完成移仓换月操作',
      minRisk: null, eligibleCount: 3, stepCount: 3, autoTrigger: true, runningCount: 2,
      steps: [
        { seq: 1, action: '移仓提醒推送', taskType: '周期类', timing: 'D-10', aiCapable: true,  required: false },
        { seq: 2, action: '外呼确认操作', taskType: '跟进类', timing: 'D-5',  aiCapable: false, required: true  },
        { seq: 3, action: '执行跟进',     taskType: '合规类', timing: 'D-2',  aiCapable: false, required: true  },
      ]},
    // ── 营销活动类 ──────────────────────────────────────────────────
    { id: 'sop_a01', taskType: 'activity', product: '通用', name: '主题活动邀约SOP',
      icon: 'solar:calendar-mark-bold-duotone', desc: '适用于各类营销活动的标准邀约流程，覆盖活动前中后三个节点',
      minRisk: null, eligibleCount: 68, stepCount: 4, autoTrigger: false, runningCount: 15,
      steps: [
        { seq: 1, action: '活动前7天预告',   taskType: '营销活动类', timing: '活动前D-7', aiCapable: true,  required: false },
        { seq: 2, action: '活动前3天邀约',   taskType: '营销活动类', timing: '活动前D-3', aiCapable: true,  required: false },
        { seq: 3, action: '活动前1天提醒',   taskType: '营销活动类', timing: '活动前D-1', aiCapable: true,  required: false },
        { seq: 4, action: '活动后转化跟进', taskType: '跟进类',     timing: '活动后D+1', aiCapable: false, required: false },
      ]},
    { id: 'sop_a02', taskType: 'activity', product: '通用', name: '节日关怀SOP',
      icon: 'solar:gift-bold-duotone', desc: '春节、中秋、国庆等重要节点的标准关怀流程，维系客户情感连接',
      minRisk: null, eligibleCount: 156, stepCount: 2, autoTrigger: false, runningCount: 0,
      steps: [
        { seq: 1, action: '节日祝福推送', taskType: '营销活动类', timing: '节日前D-1', aiCapable: true, required: false },
        { seq: 2, action: '节后产品跟进', taskType: '跟进类',     timing: '节后D+2',  aiCapable: true, required: false },
      ]},
    { id: 'sop_a03', taskType: 'activity', product: '基金/ETF', name: '新品发行邀约SOP',
      icon: 'solar:box-bold-duotone', desc: '新基金/ETF产品发行时，针对风险等级匹配客户的精准邀约流程',
      minRisk: 'R3', eligibleCount: 42, stepCount: 3, autoTrigger: false, runningCount: 5,
      steps: [
        { seq: 1, action: '产品亮点推送', taskType: '营销活动类', timing: '募集期D+0', aiCapable: true,  required: false },
        { seq: 2, action: '外呼精准邀约', taskType: '营销活动类', timing: 'D+1',       aiCapable: false, required: false },
        { seq: 3, action: '认购截止提醒', taskType: '营销活动类', timing: '截止前D-2', aiCapable: true,  required: false },
      ]},
    // ── 合规类 ──────────────────────────────────────────────────────
    { id: 'sop_p01', taskType: 'compliance', product: '通用', name: '风险测评更新SOP',
      icon: 'solar:shield-user-bold-duotone', desc: '客户风险测评结果即将到期时触发，确保客户适当性评估及时更新',
      minRisk: null, eligibleCount: 21, stepCount: 3, autoTrigger: true, runningCount: 8,
      steps: [
        { seq: 1, action: '测评到期提醒', taskType: '合规类', timing: '到期前D-30', aiCapable: true,  required: false },
        { seq: 2, action: '引导完成测评', taskType: '合规类', timing: '到期前D-14', aiCapable: true,  required: false },
        { seq: 3, action: '结果更新确认', taskType: '合规类', timing: '完成后',     aiCapable: false, required: true  },
      ]},
    { id: 'sop_p02', taskType: 'compliance', product: '两融', name: '两融双录SOP',
      icon: 'solar:videocamera-record-bold-duotone', desc: '融资融券开户和重要操作时的双录合规流程，确保监管留痕完整',
      minRisk: null, eligibleCount: 0, stepCount: 4, autoTrigger: true, runningCount: 2,
      steps: [
        { seq: 1, action: '双录预约',     taskType: '合规类', timing: '开户申请后', aiCapable: false, required: true },
        { seq: 2, action: '双录执行',     taskType: '合规类', timing: '约定时间',   aiCapable: false, required: true },
        { seq: 3, action: '材料审核上传', taskType: '合规类', timing: '双录后D+1',  aiCapable: false, required: true },
        { seq: 4, action: '合规确认结案', taskType: '合规类', timing: '上传后',     aiCapable: false, required: true },
      ]},
    { id: 'sop_p03', taskType: 'compliance', product: '期权', name: '期权适当性年检SOP',
      icon: 'solar:diploma-bold-duotone', desc: '期权客户年度适当性确认，确保客户持续满足期权交易资格要求',
      minRisk: null, eligibleCount: 15, stepCount: 3, autoTrigger: true, runningCount: 3,
      steps: [
        { seq: 1, action: '年检提醒推送', taskType: '合规类', timing: '周年前D-30', aiCapable: true,  required: false },
        { seq: 2, action: '引导线上确认', taskType: '合规类', timing: '周年前D-14', aiCapable: true,  required: false },
        { seq: 3, action: '资格更新记录', taskType: '合规类', timing: '完成后',     aiCapable: false, required: true  },
      ]},
    { id: 'sop_p04', taskType: 'compliance', product: '期货', name: '期货适当性评估SOP',
      icon: 'solar:shield-check-bold-duotone', desc: '期货开户前的投资者适当性评估流程，确保客户符合期货交易资格',
      minRisk: null, eligibleCount: 6, stepCount: 3, autoTrigger: false, runningCount: 1,
      steps: [
        { seq: 1, action: '适当性问卷',   taskType: '合规类', timing: '申请当日', aiCapable: false, required: true },
        { seq: 2, action: '知识测试',     taskType: '合规类', timing: 'D+1',      aiCapable: false, required: true },
        { seq: 3, action: '资格认定存档', taskType: '合规类', timing: '通过后',   aiCapable: false, required: true },
      ]},
]

const currentTabSopGroups = computed(() => {
    const PRODUCT_ORDER = ['通用', '股票', '基金/ETF', '投顾', '两融', '期权', '期货']
    const tabSops = sopData.filter(s => s.taskType === currentSopTab.value)
    const grouped = {}
    tabSops.forEach(sop => {
        if (!grouped[sop.product]) grouped[sop.product] = []
        grouped[sop.product].push(sop)
    })
    return PRODUCT_ORDER
        .filter(p => grouped[p])
        .map(p => ({ product: p, sops: grouped[p], ...productMeta[p] }))
})

const sopTabCount   = (key) => sopData.filter(s => s.taskType === key).length
const sopTabRunning = (key) => sopData.filter(s => s.taskType === key).reduce((sum, s) => sum + s.runningCount, 0)

const toggleSop = (id) => { expandedSopId.value = expandedSopId.value === id ? null : id }

const getTaskTypeChipClass = (taskType) => {
    const map = {
        '建联类': 'bg-blue-100 text-blue-600', '跟进类': 'bg-emerald-100 text-emerald-600',
        '周期类': 'bg-purple-100 text-purple-600', '营销活动类': 'bg-orange-100 text-orange-600',
        '合规类': 'bg-amber-100 text-amber-700',
    }
    return map[taskType] || 'bg-gray-100 text-gray-500'
}

const aiSopRecs = [
    { name: '两融开户引导SOP', match: 96, reason: '李建国 资产128万·R4，当前无两融账户，适合开发两融业务', tagClass: 'bg-orange-50 text-orange-600' },
    { name: '基金到期续作SOP', match: 94, reason: '张超越 持有智富盈1号将在3天后到期，需及时跟进续作',    tagClass: 'bg-emerald-50 text-emerald-700' },
    { name: '持仓保护策略SOP', match: 88, reason: '王芳 持有贵州茅台200股，可推荐保护性认沽期权策略',    tagClass: 'bg-purple-50 text-purple-600' },
]

const sopLogs = [
    { sopName: '新客激活SOP',     clientName: '王晓丽',  step: '第3步/共5步', time: '今日 09:32',  done: false, tagClass: 'bg-gray-100 text-gray-600'      },
    { sopName: '基金到期续作SOP', clientName: '李明浩',  step: '已完成',       time: '今日 08:15',  done: true,  tagClass: 'bg-emerald-50 text-emerald-700' },
    { sopName: '两融开户引导SOP', clientName: '赵建国',  step: '第5步/共6步', time: '昨日 16:40',  done: false, tagClass: 'bg-orange-50 text-orange-600'   },
    { sopName: '期权资格引导SOP', clientName: '批量5客', step: '第1步/共5步', time: '05-10 10:00', done: false, tagClass: 'bg-purple-50 text-purple-600'   },
]

const handleResize = () => {
    contributionChartInstance?.resize()
    radarChartInstance?.resize()
}

onMounted(() => {
    fetchCustomers()
    fetchAlerts()
    document.addEventListener('click', _onClickOutsideAlert)

    // 检测从工作台总览跳转过来的 ai-batch 模式
    if (route.query.mode === 'ai-batch') {
      currentPage.value = 'ai-batch'
      loadAiBatchTasks()
    }

    contributionChartInstance = echarts.init(document.getElementById('contributionChart'))
    contributionChartInstance.setOption({
        tooltip: { trigger: 'axis', textStyle: { fontSize: 10 } },
        grid: { left: '10%', right: '10%', bottom: '10%', top: '10%' },
        xAxis: {
            type: 'category',
            data: ['1月', '2月', '3月', '4月', '5月'],
            axisLabel: { fontSize: 10 }
        },
        yAxis: {
            type: 'value',
            axisLabel: { fontSize: 10, formatter: '{value} 元' }
        },
        series: [{
            name: '创收金额',
            type: 'bar',
            data: [12000, 15000, 18000, 14000, 21000],
            itemStyle: { color: '#2563eb' },
            barWidth: '40%'
        }]
    })

    radarChartInstance = echarts.init(document.getElementById('customerRadarChart'))
    radarChartInstance.setOption({
        tooltip: { trigger: 'item', textStyle: { fontSize: 10 } },
        radar: {
            indicator: [
                { name: '资产实力', max: 100 },
                { name: '交易活跃', max: 100 },
                { name: '风险承受', max: 100 },
                { name: '私域建程', max: 100 },
                { name: '响应程度', max: 100 },
                { name: '产品接受', max: 100 },
                { name: '资金流动', max: 100 },
                { name: '服务依赖', max: 100 },
            ],
            radius: '65%',
            shape: 'polygon',
            splitNumber: 4,
            axisName: { fontSize: 9, color: '#6b7280', fontWeight: 'bold' },
            splitLine: { lineStyle: { color: '#e5e7eb', width: 1 } },
            splitArea: { show: true, areaStyle: { color: ['rgba(248,250,252,0.8)', 'rgba(241,245,249,0.8)'] } },
            axisLine: { lineStyle: { color: '#e5e7eb' } }
        },
        series: [{
            name: '客户画像',
            type: 'radar',
            data: [{
                value: [85, 72, 78, 60, 88, 65, 90, 70],
                name: '张超越',
                symbolSize: 4,
                areaStyle: { color: 'rgba(37,99,235,0.12)' },
                lineStyle: { color: '#2563eb', width: 2 }
            }]
        }]
    })

    window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    document.removeEventListener('click', _onClickOutsideAlert)
    contributionChartInstance?.dispose()
    radarChartInstance?.dispose()
})
</script>

<style scoped>
/* 基础样式复用原有CSS，添加scoped适配 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.business-hall {
    font-family: 'Inter', 'Microsoft YaHei', sans-serif;
    background-color: #F8FAFC;
    height: 100vh;
    overflow: hidden;
    display: flex;
}

/* 全局样式穿透（解决scoped下第三方组件/全局样式生效问题） */
:deep(.scrollbar-hide::-webkit-scrollbar) {
    display: none;
}

:deep(#sidebar) {
    width: 256px;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(#sidebar.collapsed) {
    width: 80px;
}

:deep(#sidebar.collapsed .logo-text),
:deep(#sidebar.collapsed .nav-text),
:deep(#sidebar.collapsed .user-info-text) {
    display: none;
}

:deep(#sidebar.collapsed .nav-item) {
    justify-content: center;
    padding-left: 0;
    padding-right: 0;
}

:deep(#sidebar.collapsed .nav-item iconify-icon) {
    margin-right: 0;
}

:deep(#sidebar.collapsed .logo-container) {
    justify-content: center;
}


:deep(.data-card) {
    background: white;
    border-radius: 1.5rem;
    border: 1px solid #f1f5f9;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

:deep(.page-content) {
    display: none;
    height: 100%;
    overflow-y: auto;
}

:deep(.page-content.active) {
    display: block;
}

/* 自定义滚动条 */
:deep(::-webkit-scrollbar) {
    width: 6px;
}

:deep(::-webkit-scrollbar-track) {
    background: transparent;
}

:deep(::-webkit-scrollbar-thumb) {
    background: #e2e8f0;
    border-radius: 10px;
}

:deep(::-webkit-scrollbar-thumb:hover) {
    background: #cbd5e1;
}
</style>