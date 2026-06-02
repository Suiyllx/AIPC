<template>
    <div class="performance-page">
        <!-- 侧边导航 -->
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
                        <p class="text-xs text-slate-500 truncate">最后登录: 2026-05-08</p>
                    </div>
                </div>
            </div>
        </aside>

        <!-- 主体内容 -->
        <main class="flex-1 overflow-x-hidden overflow-y-auto bg-[#F8FAFC]">
            <!-- 顶部导航栏 -->
            <header
                class="h-16 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-6 shrink-0 sticky top-0 z-40">
                <div class="flex items-center gap-4">
                    <button class="p-2 hover:bg-slate-100 rounded-lg transition-colors" @click="toggleSidebar">
                        <iconify-icon class="text-xl text-slate-600" icon="lucide:menu"></iconify-icon>
                    </button>
                    <div class="h-6 w-px bg-slate-200"></div>
                    <span class="text-sm font-medium text-slate-500">今天是 2026年05月07日</span>
                </div>
                <div class="flex items-center gap-4">
                    <!-- 角色切换 -->
                    <div class="flex items-center gap-1 bg-slate-100 rounded-lg p-1 text-xs font-medium">
                        <span class="px-2.5 py-1 bg-white text-slate-900 rounded-md shadow-sm">营销人员</span>
                        <router-link class="px-2.5 py-1 text-slate-500 hover:text-slate-700 rounded-md transition-all" to="/manager">管理人员</router-link>
                    </div>
                    <button class="p-2 hover:bg-slate-100 rounded-lg relative transition-colors">
                        <iconify-icon class="text-xl text-slate-600" icon="lucide:bell"></iconify-icon>
                        <span class="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
                    </button>
                </div>
            </header>

            <div class="p-8 space-y-8">
                <!-- 页面标题与时间筛选 -->
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <h1 class="text-xl font-bold text-gray-900">绩效看板</h1>
                        <span class="px-3 py-1 bg-blue-50 text-blue-600 text-xs font-medium rounded-full">数据更新：2026-05-07 10:30</span>
                    </div>
                    <div class="flex bg-gray-100 p-1 rounded-lg">
                        <button
                            class="px-4 py-1.5 text-sm font-medium rounded-md hover:bg-white hover:shadow-sm transition-all">今天</button>
                        <button
                            class="px-4 py-1.5 text-sm font-medium rounded-md bg-white shadow-sm transition-all">本月</button>
                        <button
                            class="px-4 py-1.5 text-sm font-medium rounded-md hover:bg-white hover:shadow-sm transition-all">近7天</button>
                        <button
                            class="px-4 py-1.5 text-sm font-medium rounded-md hover:bg-white hover:shadow-sm transition-all flex items-center gap-1">
                            <iconify-icon icon="solar:calendar-linear"></iconify-icon>自定义
                        </button>
                    </div>
                </div>

                <!-- 1. 顶部三大业绩总览 -->
                <section class="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    <!-- 核心业绩卡片 -->
                    <div
                        class="lg:col-span-2 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-3xl p-8 text-white relative overflow-hidden shadow-xl shadow-blue-100">
                        <div class="relative z-10 flex flex-col h-full justify-between">
                            <div class="flex justify-between items-start">
                                <div>
                                    <p class="text-blue-100 text-sm font-medium mb-1">本月累计业绩得分</p>
                                    <h2 class="text-5xl font-bold">2,840<span
                                            class="text-xl ml-2 text-blue-200">分</span></h2>
                                </div>
                                <div
                                    class="bg-white/20 backdrop-blur-md rounded-2xl p-4 text-center min-w-[100px]">
                                    <p class="text-[10px] text-blue-100 uppercase tracking-wider">本月目标完成度</p>
                                    <p class="text-2xl font-bold mt-1">82.5%</p>
                                </div>
                            </div>
                            <div class="grid grid-cols-2 gap-4 mt-8 pt-6 border-t border-white/10">
                                <div>
                                    <p class="text-blue-200 text-xs mb-1 uppercase">今日业绩得分</p>
                                    <p class="text-2xl font-bold">+156</p>
                                </div>
                                <div class="flex items-end justify-between">
                                    <div>
                                        <p class="text-blue-200 text-xs mb-1 uppercase">当前排名</p>
                                        <div class="flex items-baseline space-x-2">
                                            <span class="text-2xl font-bold">第 8 名</span>
                                            <span class="text-xs text-blue-100">(团队第 2)</span>
                                        </div>
                                    </div>
                                    <iconify-icon class="text-4xl text-white/30"
                                        icon="solar:chart-square-bold"></iconify-icon>
                                </div>
                            </div>
                        </div>
                        <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
                    </div>

                    <!-- 今日业务增量 4格 -->
                    <div class="lg:col-span-2 grid grid-cols-2 gap-4">
                        <div class="bg-white p-6 rounded-2xl border border-gray-100 card-shadow flex flex-col justify-between">
                            <div class="flex justify-between items-start">
                                <div class="p-2 bg-emerald-50 text-emerald-600 rounded-lg">
                                    <iconify-icon class="text-2xl"
                                        icon="solar:users-group-two-rounded-bold-duotone"></iconify-icon>
                                </div>
                                <span
                                    class="text-xs font-medium text-emerald-600 flex items-center bg-emerald-50 px-2 py-0.5 rounded-full">
                                    <iconify-icon class="mr-1" icon="solar:trending-up-linear"></iconify-icon>+12%
                                </span>
                            </div>
                            <div class="mt-4">
                                <p class="text-gray-500 text-sm font-medium">今日新增客户 / 加微</p>
                                <div class="flex items-baseline space-x-2 mt-1">
                                    <span class="text-2xl font-bold text-gray-900">42 / 28</span>
                                </div>
                            </div>
                        </div>
                        <div class="bg-white p-6 rounded-2xl border border-gray-100 card-shadow flex flex-col justify-between">
                            <div class="flex justify-between items-start">
                                <div class="p-2 bg-orange-50 text-orange-600 rounded-lg">
                                    <iconify-icon class="text-2xl" icon="solar:link-bold-duotone"></iconify-icon>
                                </div>
                                <span
                                    class="text-xs font-medium text-orange-600 flex items-center bg-orange-50 px-2 py-0.5 rounded-full">
                                    <iconify-icon class="mr-1" icon="solar:trending-up-linear"></iconify-icon>+5%
                                </span>
                            </div>
                            <div class="mt-4">
                                <p class="text-gray-500 text-sm font-medium">今日账号绑定量</p>
                                <div class="flex items-baseline space-x-2 mt-1">
                                    <span class="text-2xl font-bold text-gray-900">18</span>
                                </div>
                            </div>
                        </div>
                        <div
                            class="bg-white p-6 rounded-2xl border border-gray-100 card-shadow flex flex-col justify-between col-span-2">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-4">
                                    <div class="p-2 bg-blue-50 text-blue-600 rounded-lg">
                                        <iconify-icon class="text-2xl"
                                            icon="solar:round-transfer-horizontal-bold-duotone"></iconify-icon>
                                    </div>
                                    <div>
                                        <p class="text-gray-500 text-sm font-medium">今日入金客户 / 金额</p>
                                        <p class="text-2xl font-bold text-gray-900">12 位 / ¥1,280,000</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <p class="text-xs text-gray-400 mb-1">本月目标进度</p>
                                    <div class="w-32 h-2 bg-gray-100 rounded-full overflow-hidden">
                                        <div class="bg-blue-600 h-full w-3/4"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- 2. 核心绩效指标看板 (10个KPI) -->
                <section>
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-bold text-gray-900">核心绩效指标看板</h3>
                        <button class="text-blue-600 text-sm font-medium hover:underline">查看明细</button>
                    </div>
                    <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 card-shadow kpi-card">
                            <p class="text-gray-500 text-xs font-medium truncate mb-2">任务完成率</p>
                            <div class="flex items-end justify-between">
                                <span class="text-xl font-bold text-gray-900">92.5%</span>
                                <span class="text-[10px] text-emerald-600 font-bold">↑ 2.1%</span>
                            </div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 card-shadow kpi-card">
                            <p class="text-gray-500 text-xs font-medium truncate mb-2">企微添加率</p>
                            <div class="flex items-end justify-between">
                                <span class="text-xl font-bold text-gray-900">65.2%</span>
                                <span class="text-[10px] text-red-500 font-bold">↓ 0.8%</span>
                            </div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 card-shadow kpi-card">
                            <p class="text-gray-500 text-xs font-medium truncate mb-2">微信绑定率</p>
                            <div class="flex items-end justify-between">
                                <span class="text-xl font-bold text-gray-900">42.8%</span>
                                <span class="text-[10px] text-emerald-600 font-bold">↑ 5.3%</span>
                            </div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 card-shadow kpi-card">
                            <p class="text-gray-500 text-xs font-medium truncate mb-2">AI外呼成功率</p>
                            <div class="flex items-end justify-between">
                                <span class="text-xl font-bold text-gray-900">18.5%</span>
                                <span class="text-[10px] text-emerald-600 font-bold">↑ 1.2%</span>
                            </div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 card-shadow kpi-card">
                            <p class="text-gray-500 text-xs font-medium truncate mb-2">人工外呼接听率</p>
                            <div class="flex items-end justify-between">
                                <span class="text-xl font-bold text-gray-900">45.0%</span>
                                <span class="text-[10px] text-gray-400 font-bold">持平</span>
                            </div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 card-shadow kpi-card">
                            <p class="text-gray-500 text-xs font-medium truncate mb-2">新客引流转化率</p>
                            <div class="flex items-end justify-between">
                                <span class="text-xl font-bold text-gray-900">12.3%</span>
                                <span class="text-[10px] text-emerald-600 font-bold">↑ 0.5%</span>
                            </div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 card-shadow kpi-card">
                            <p class="text-gray-500 text-xs font-medium truncate mb-2">新客90天入金率</p>
                            <div class="flex items-end justify-between">
                                <span class="text-xl font-bold text-gray-900">38.2%</span>
                                <span class="text-[10px] text-emerald-600 font-bold">↑ 4.2%</span>
                            </div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 card-shadow kpi-card">
                            <p class="text-gray-500 text-xs font-medium truncate mb-2">客户活跃留存率</p>
                            <div class="flex items-end justify-between">
                                <span class="text-xl font-bold text-gray-900">76.5%</span>
                                <span class="text-[10px] text-emerald-600 font-bold">↑ 1.1%</span>
                            </div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 card-shadow kpi-card">
                            <p class="text-gray-500 text-xs font-medium truncate mb-2">AUM新增规模</p>
                            <div class="flex items-end justify-between">
                                <span class="text-xl font-bold text-gray-900">¥12.5M</span>
                                <span class="text-[10px] text-emerald-600 font-bold">↑ 2.8M</span>
                            </div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 card-shadow kpi-card">
                            <p class="text-gray-500 text-xs font-medium truncate mb-2">产品销售额</p>
                            <div class="flex items-end justify-between">
                                <span class="text-xl font-bold text-gray-900">¥8.4M</span>
                                <span class="text-[10px] text-red-500 font-bold">↓ 0.2M</span>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- 3 & 4. 任务绩效 + 建联绩效 -->
                <div class="grid grid-cols-1 xl:grid-cols-2 gap-8">
                    <!-- 3. 任务绩效 -->
                    <section class="bg-white p-8 rounded-3xl border border-gray-100 card-shadow">
                        <div class="flex items-center justify-between mb-6">
                            <div class="flex items-center space-x-3">
                                <div
                                    class="w-10 h-10 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center">
                                    <iconify-icon class="text-2xl"
                                        icon="solar:clipboard-list-bold-duotone"></iconify-icon>
                                </div>
                                <div>
                                    <h3 class="font-bold text-gray-900">任务绩效</h3>
                                    <p class="text-xs text-gray-500">数据源自任务大厅</p>
                                </div>
                            </div>
                            <div class="text-right">
                                <p class="text-xs text-gray-400">AI 代决贡献</p>
                                <p class="text-sm font-bold text-emerald-600">+125 任务 / 效率提升 35%</p>
                            </div>
                        </div>
                        <div class="grid grid-cols-4 gap-4 mb-8">
                            <div class="text-center p-4 bg-gray-50 rounded-2xl">
                                <p class="text-xs text-gray-500 mb-1">总任务数</p>
                                <p class="text-xl font-bold text-gray-900">842</p>
                            </div>
                            <div class="text-center p-4 bg-gray-50 rounded-2xl">
                                <p class="text-xs text-gray-500 mb-1">完成数</p>
                                <p class="text-xl font-bold text-blue-600">778</p>
                            </div>
                            <div class="text-center p-4 bg-gray-50 rounded-2xl">
                                <p class="text-xs text-gray-500 mb-1">难点数</p>
                                <p class="text-xl font-bold text-red-500">12</p>
                            </div>
                            <div class="text-center p-4 bg-gray-50 rounded-2xl">
                                <p class="text-xs text-gray-500 mb-1">高优完成率</p>
                                <p class="text-xl font-bold text-orange-500">100%</p>
                            </div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div class="h-64" id="taskTrendChart"></div>
                            <div class="h-64" id="taskTypeChart"></div>
                        </div>
                    </section>

                    <!-- 4. 建联绩效 -->
                    <section class="bg-white p-8 rounded-3xl border border-gray-100 card-shadow">
                        <div class="flex items-center justify-between mb-6">
                            <div class="flex items-center space-x-3">
                                <div
                                    class="w-10 h-10 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center">
                                    <iconify-icon class="text-2xl"
                                        icon="solar:share-circle-bold-duotone"></iconify-icon>
                                </div>
                                <div>
                                    <h3 class="font-bold text-gray-900">建联绩效</h3>
                                    <p class="text-xs text-gray-500">企微添加与外呼转化</p>
                                </div>
                            </div>
                            <div class="flex items-center space-x-4 bg-emerald-50 px-4 py-2 rounded-xl">
                                <div class="text-center">
                                    <p class="text-[10px] text-emerald-700">AI 外呼成功率</p>
                                    <p class="text-sm font-bold text-emerald-800">22.4%</p>
                                </div>
                                <div class="w-px h-6 bg-emerald-200"></div>
                                <div class="text-center">
                                    <p class="text-[10px] text-emerald-700">人工回呼接听率</p>
                                    <p class="text-sm font-bold text-emerald-800">48.5%</p>
                                </div>
                            </div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div class="space-y-4">
                                <div class="h-48" id="connectFunnelChart"></div>
                                <div class="bg-gray-50 p-4 rounded-xl">
                                    <p class="text-xs font-bold text-gray-700 mb-3">三类客户结构占比</p>
                                    <div class="flex h-3 rounded-full overflow-hidden bg-gray-200">
                                        <div class="bg-blue-600 w-[45%]"></div>
                                        <div class="bg-blue-400 w-[35%]"></div>
                                        <div class="bg-blue-200 w-[20%]"></div>
                                    </div>
                                    <div class="flex justify-between mt-2 text-[10px] text-gray-500">
                                        <span>未加微 (45%)</span>
                                        <span>已加未绑 (35%)</span>
                                        <span>已绑定 (20%)</span>
                                    </div>
                                </div>
                            </div>
                            <div class="h-64" id="callTrendChart"></div>
                        </div>
                    </section>
                </div>

                <!-- 5. 转化绩效 -->
                <section class="bg-white p-8 rounded-3xl border border-gray-100 card-shadow">
                    <div class="flex items-center justify-between mb-8">
                        <div class="flex items-center space-x-3">
                            <div
                                class="w-10 h-10 bg-orange-50 text-orange-600 rounded-xl flex items-center justify-center">
                                <iconify-icon class="text-2xl" icon="solar:banknote-bold-duotone"></iconify-icon>
                            </div>
                            <div>
                                <h3 class="font-bold text-gray-900">转化绩效</h3>
                                <p class="text-xs text-gray-500">资金入金与资产增长</p>
                            </div>
                        </div>
                        <button
                            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-600 text-sm font-medium rounded-xl transition-colors">导出报表</button>
                    </div>
                    <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
                        <div class="lg:col-span-1 space-y-4">
                            <div class="p-4 bg-orange-50/50 rounded-2xl border border-orange-100">
                                <p class="text-xs text-gray-500 mb-1">有效引流客数</p>
                                <p class="text-2xl font-bold text-gray-900">128 <span
                                        class="text-xs font-normal text-gray-400 ml-1">客</span></p>
                            </div>
                            <div class="p-4 bg-blue-50/50 rounded-2xl border border-blue-100">
                                <p class="text-xs text-gray-500 mb-1">首次入金客户数</p>
                                <p class="text-2xl font-bold text-gray-900">92 <span
                                        class="text-xs font-normal text-gray-400 ml-1">人</span></p>
                            </div>
                            <div class="p-4 bg-emerald-50/50 rounded-2xl border border-emerald-100">
                                <p class="text-xs text-gray-500 mb-1">交易客户数 / 交易量</p>
                                <p class="text-xl font-bold text-gray-900">456 人 / ¥85M</p>
                            </div>
                            <div class="p-4 bg-indigo-50/50 rounded-2xl border border-indigo-100">
                                <p class="text-xs text-gray-500 mb-1">AUM 月新增</p>
                                <p class="text-2xl font-bold text-gray-900">+¥15.4M</p>
                            </div>
                        </div>
                        <div class="lg:col-span-2 h-80" id="conversionTrendChart"></div>
                        <div class="lg:col-span-1">
                            <p class="text-sm font-bold text-gray-800 mb-4">产品销售排行</p>
                            <div class="space-y-4">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center space-x-3">
                                        <span
                                            class="w-6 h-6 flex items-center justify-center bg-blue-600 text-white text-[10px] font-bold rounded-lg">1</span>
                                        <span class="text-sm text-gray-700">稳收益财富 A</span>
                                    </div>
                                    <span class="text-sm font-bold">¥4.2M</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center space-x-3">
                                        <span
                                            class="w-6 h-6 flex items-center justify-center bg-blue-500 text-white text-[10px] font-bold rounded-lg">2</span>
                                        <span class="text-sm text-gray-700">稳涨存收储蓄险</span>
                                    </div>
                                    <span class="text-sm font-bold">¥2.8M</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center space-x-3">
                                        <span
                                            class="w-6 h-6 flex items-center justify-center bg-blue-400 text-white text-[10px] font-bold rounded-lg">3</span>
                                        <span class="text-sm text-gray-700">晨光+ 银行龙达</span>
                                    </div>
                                    <span class="text-sm font-bold">¥1.1M</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center space-x-3">
                                        <span
                                            class="w-6 h-6 flex items-center justify-center bg-gray-100 text-gray-500 text-[10px] font-bold rounded-lg">4</span>
                                        <span class="text-sm text-gray-700">定享精选组合</span>
                                    </div>
                                    <span class="text-sm font-bold">¥0.5M</span>
                                </div>
                            </div>
                            <button
                                class="w-full mt-6 py-2 text-sm text-blue-600 font-medium border border-blue-100 rounded-xl hover:bg-blue-50 transition-colors">查看全部产品</button>
                        </div>
                    </div>
                </section>

                <!-- 6、7、8. 服务绩效 + 个人排行榜 + AI绩效诊断 -->
                <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
                    <!-- 6. 服务绩效 -->
                    <section class="bg-white p-8 rounded-3xl border border-gray-100 card-shadow flex flex-col">
                        <div class="flex items-center space-x-3 mb-6">
                            <div
                                class="w-10 h-10 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center">
                                <iconify-icon class="text-2xl" icon="solar:heart-bold-duotone"></iconify-icon>
                            </div>
                            <h3 class="font-bold text-gray-900">服务绩效</h3>
                        </div>
                        <div class="space-y-6 flex-1">
                            <div class="grid grid-cols-2 gap-4">
                                <div class="p-4 bg-gray-50 rounded-2xl">
                                    <p class="text-xs text-gray-500 mb-1">企微触达量</p>
                                    <p class="text-lg font-bold">3,240 <span
                                            class="text-[10px] text-gray-400 font-normal">次</span></p>
                                </div>
                                <div class="p-4 bg-gray-50 rounded-2xl">
                                    <p class="text-xs text-gray-500 mb-1">触达点击率</p>
                                    <p class="text-lg font-bold">24.5%</p>
                                </div>
                            </div>
                            <div class="space-y-4">
                                <div class="flex items-center justify-between">
                                    <span class="text-sm text-gray-600">客户回复时长</span>
                                    <span class="text-sm font-bold text-emerald-600">平均 4.2 min</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <span class="text-sm text-gray-600">客户好评率</span>
                                    <div class="flex items-center space-x-1">
                                        <span class="text-sm font-bold">98.2%</span>
                                        <div class="flex text-yellow-400 text-xs">
                                            <iconify-icon icon="solar:star-bold"></iconify-icon>
                                            <iconify-icon icon="solar:star-bold"></iconify-icon>
                                            <iconify-icon icon="solar:star-bold"></iconify-icon>
                                            <iconify-icon icon="solar:star-bold"></iconify-icon>
                                            <iconify-icon icon="solar:star-bold"></iconify-icon>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex items-center justify-between">
                                    <span class="text-sm text-gray-600">连续零违规天数</span>
                                    <span class="text-sm font-bold text-blue-600">365 天</span>
                                </div>
                                <div
                                    class="flex items-center justify-between p-3 bg-emerald-50 text-emerald-700 rounded-xl">
                                    <div class="flex items-center space-x-2 text-xs">
                                        <iconify-icon icon="solar:check-circle-bold"></iconify-icon>
                                        <span>本月无投诉及异常记录</span>
                                    </div>
                                    <span class="text-xs font-bold">状态：正常</span>
                                </div>
                            </div>
                        </div>
                    </section>

                    <!-- 7. 个人排行榜 -->
                    <section class="bg-white p-8 rounded-3xl border border-gray-100 card-shadow">
                        <div class="flex items-center justify-between mb-6">
                            <div class="flex items-center space-x-3">
                                <div
                                    class="w-10 h-10 bg-yellow-50 text-yellow-600 rounded-xl flex items-center justify-center">
                                    <iconify-icon class="text-2xl"
                                        icon="solar:medal-ribbon-star-bold-duotone"></iconify-icon>
                                </div>
                                <h3 class="font-bold text-gray-900">个人排行榜</h3>
                            </div>
                            <select class="text-xs bg-gray-50 border-none rounded-lg focus:ring-0 outline-none p-1">
                                <option>本月业绩总分</option>
                                <option>企微添加榜</option>
                                <option>外呼成功榜</option>
                                <option>入金转化榜</option>
                            </select>
                        </div>
                        <!-- 本人排名卡片 -->
                        <div
                            class="p-5 bg-gradient-to-r from-gray-900 to-gray-800 rounded-2xl text-white mb-6">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-4">
                                    <div class="relative">
                                        <div
                                            class="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center border-2 border-white/20">
                                            <iconify-icon class="text-white text-2xl"
                                                icon="solar:user-bold-duotone"></iconify-icon>
                                        </div>
                                        <div
                                            class="absolute -bottom-1 -right-1 w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center border-2 border-gray-900">
                                            <span class="text-[10px] font-bold">8</span>
                                        </div>
                                    </div>
                                    <div>
                                        <p class="text-sm font-bold">张超超 (本人)</p>
                                        <p class="text-[10px] text-gray-400">距离前一名仅差 45 分</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <p class="text-xs text-gray-400 uppercase tracking-tighter">领先营业部</p>
                                    <p class="text-lg font-bold text-blue-400">82% <span
                                            class="text-xs font-normal">排名</span></p>
                                </div>
                            </div>
                        </div>
                        <div class="space-y-4">
                            <div
                                class="flex items-center justify-between p-3 hover:bg-gray-50 rounded-xl transition-colors">
                                <div class="flex items-center space-x-4">
                                    <span class="w-6 text-center font-bold text-yellow-500 italic">01</span>
                                    <div
                                        class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
                                        <iconify-icon class="text-gray-400 text-xl"
                                            icon="solar:user-bold-duotone"></iconify-icon>
                                    </div>
                                    <div>
                                        <p class="text-sm font-bold text-gray-800">李建峰</p>
                                        <p class="text-[10px] text-gray-500">财富中心 A 组</p>
                                    </div>
                                </div>
                                <span class="text-sm font-bold text-gray-900">4,280 分</span>
                            </div>
                            <div
                                class="flex items-center justify-between p-3 hover:bg-gray-50 rounded-xl transition-colors">
                                <div class="flex items-center space-x-4">
                                    <span class="w-6 text-center font-bold text-gray-400 italic">02</span>
                                    <div
                                        class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
                                        <iconify-icon class="text-gray-400 text-xl"
                                            icon="solar:user-bold-duotone"></iconify-icon>
                                    </div>
                                    <div>
                                        <p class="text-sm font-bold text-gray-800">沈梦霞</p>
                                        <p class="text-[10px] text-gray-500">私钥客户部</p>
                                    </div>
                                </div>
                                <span class="text-sm font-bold text-gray-900">3,950 分</span>
                            </div>
                            <div
                                class="flex items-center justify-between p-3 hover:bg-gray-50 rounded-xl transition-colors">
                                <div class="flex items-center space-x-4">
                                    <span class="w-6 text-center font-bold text-orange-400 italic">03</span>
                                    <div
                                        class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
                                        <iconify-icon class="text-gray-400 text-xl"
                                            icon="solar:user-bold-duotone"></iconify-icon>
                                    </div>
                                    <div>
                                        <p class="text-sm font-bold text-gray-800">王远达</p>
                                        <p class="text-[10px] text-gray-500">财富中心 B 组</p>
                                    </div>
                                </div>
                                <span class="text-sm font-bold text-gray-900">3,720 分</span>
                            </div>
                        </div>
                    </section>

                    <!-- 8. AI绩效诊断与改进建议 -->
                    <section class="bg-white p-8 rounded-3xl border border-gray-100 card-shadow flex flex-col">
                        <div class="flex items-center justify-between mb-6">
                            <div class="flex items-center space-x-3">
                                <div
                                    class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center">
                                    <iconify-icon class="text-2xl"
                                        icon="solar:magic-stick-3-bold-duotone"></iconify-icon>
                                </div>
                                <h3 class="font-bold text-gray-900">AI 绩效诊断</h3>
                            </div>
                            <span
                                class="px-2 py-1 bg-indigo-50 text-indigo-600 text-[10px] font-bold rounded">AI 智能分析中</span>
                        </div>
                        <div class="space-y-5 flex-1 overflow-y-auto pr-2">
                            <div>
                                <p class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">多维诊断</p>
                                <div class="grid grid-cols-1 gap-2">
                                    <div class="flex items-start space-x-3 p-3 bg-emerald-50 rounded-xl">
                                        <iconify-icon class="text-emerald-600 mt-0.5 shrink-0"
                                            icon="solar:double-alt-arrow-up-bold"></iconify-icon>
                                        <div>
                                            <p class="text-xs font-bold text-emerald-800">优势项：高价值转化</p>
                                            <p class="text-[10px] text-emerald-600 mt-1">入金客均价高于平均 240%，大额资金建联成效显著。</p>
                                        </div>
                                    </div>
                                    <div class="flex items-start space-x-3 p-3 bg-orange-50 rounded-xl">
                                        <iconify-icon class="text-orange-600 mt-0.5 shrink-0"
                                            icon="solar:double-alt-arrow-down-bold"></iconify-icon>
                                        <div>
                                            <p class="text-xs font-bold text-orange-800">薄弱项：小微客户覆盖</p>
                                            <p class="text-[10px] text-orange-600 mt-1">长尾客户加微率低于团队平均 15%，建议启用 AI 批量辅助。</p>
                                        </div>
                                    </div>
                                    <div class="flex items-start space-x-3 p-3 bg-red-50 rounded-xl">
                                        <iconify-icon class="text-red-600 mt-0.5 shrink-0"
                                            icon="solar:danger-bold"></iconify-icon>
                                        <div>
                                            <p class="text-xs font-bold text-red-800">异常：人工外呼接听偏低</p>
                                            <p class="text-[10px] text-red-600 mt-1">昨日 14:00-16:00 接听率仅 12%，建议调整至 10:00 时段。</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="pt-2">
                                <p class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">AI 改进建议</p>
                                <ul class="space-y-3">
                                    <li class="flex items-center space-x-3">
                                        <div class="w-1.5 h-1.5 bg-indigo-600 rounded-full shrink-0"></div>
                                        <span class="text-xs text-gray-700">今日优先处理 <span
                                                class="font-bold text-gray-900">5 条高优入金任务</span></span>
                                    </li>
                                    <li class="flex items-center space-x-3">
                                        <div class="w-1.5 h-1.5 bg-indigo-600 rounded-full shrink-0"></div>
                                        <span class="text-xs text-gray-700">推荐话术：<span class="italic text-gray-500">"针对近期市场波动，为您…"</span></span>
                                    </li>
                                    <li class="flex items-center space-x-3">
                                        <div class="w-1.5 h-1.5 bg-indigo-600 rounded-full shrink-0"></div>
                                        <span class="text-xs text-gray-700">明日规划：设定 <span
                                                class="font-bold text-gray-900">30 个加微目标</span>，可用批量代决</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <button
                            class="w-full mt-6 py-3 bg-indigo-600 text-white text-sm font-bold rounded-2xl hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-100">
                            生成详细诊断报告
                        </button>
                    </section>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const sidebarCollapsed = ref(false)

const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
    setTimeout(() => chartInstances.forEach(c => c.resize()), 300)
}

let chartInstances = []

onMounted(() => {
    // 任务完成趋势
    const taskTrend = echarts.init(document.getElementById('taskTrendChart'))
    taskTrend.setOption({
        title: { text: '任务完成趋势', textStyle: { fontSize: 12, color: '#666' } },
        tooltip: { trigger: 'axis' },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: ['05-01', '05-02', '05-03', '05-04', '05-05', '05-06', '05-07'], axisLine: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { type: 'dashed' } } },
        series: [{
            data: [120, 132, 101, 134, 90, 230, 210],
            type: 'line', smooth: true, showSymbol: false,
            lineStyle: { width: 3, color: '#3B82F6' },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(59,130,246,0.2)' },
                    { offset: 1, color: 'rgba(59,130,246,0)' }
                ])
            }
        }]
    })

    // 任务类型占比
    const taskType = echarts.init(document.getElementById('taskTypeChart'))
    taskType.setOption({
        title: { text: '任务类型占比', left: 'center', textStyle: { fontSize: 12, color: '#666' } },
        tooltip: { trigger: 'item' },
        legend: { bottom: '0', itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 10 } },
        series: [{
            name: '任务类型', type: 'pie', radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
            label: { show: false },
            data: [
                { value: 40, name: '建联任务', itemStyle: { color: '#3B82F6' } },
                { value: 30, name: '生命周期', itemStyle: { color: '#60A5FA' } },
                { value: 20, name: '营销活动', itemStyle: { color: '#93C5FD' } },
                { value: 10, name: '主管分配', itemStyle: { color: '#BFDBFE' } }
            ]
        }]
    })

    // 建联转化漏斗
    const connectFunnel = echarts.init(document.getElementById('connectFunnelChart'))
    connectFunnel.setOption({
        tooltip: { trigger: 'item', formatter: '{a} <br/>{b} : {c}%' },
        series: [{
            name: '建联转化', type: 'funnel',
            left: '10%', top: 10, bottom: 10, width: '80%',
            min: 0, max: 100, minSize: '0%', maxSize: '100%',
            sort: 'descending', gap: 2,
            label: { show: true, position: 'inside', formatter: '{b} {c}%', fontSize: 10 },
            data: [
                { value: 100, name: '待建联', itemStyle: { color: '#BFDBFE' } },
                { value: 65, name: '已加企微', itemStyle: { color: '#60A5FA' } },
                { value: 42, name: '已绑定', itemStyle: { color: '#3B82F6' } }
            ]
        }]
    })

    // 日外呼与成功趋势
    const callTrend = echarts.init(document.getElementById('callTrendChart'))
    callTrend.setOption({
        title: { text: '日外呼与成功趋势', textStyle: { fontSize: 12, color: '#666' } },
        tooltip: { trigger: 'axis' },
        legend: { right: 0, textStyle: { fontSize: 10 } },
        xAxis: { type: 'category', data: ['05-01', '05-02', '05-03', '05-04', '05-05', '05-06', '05-07'] },
        yAxis: { type: 'value' },
        series: [
            { name: '拨出量', type: 'bar', data: [80, 70, 40, 95, 120, 110, 130], itemStyle: { color: '#BFDBFE' } },
            { name: '成功量', type: 'line', data: [15, 12, 8, 18, 25, 22, 28], itemStyle: { color: '#10B981' }, smooth: true }
        ]
    })

    // 入金/交易/AUM增长趋势
    const conversionTrend = echarts.init(document.getElementById('conversionTrendChart'))
    conversionTrend.setOption({
        title: { text: '入金/交易/AUM 增长趋势', textStyle: { fontSize: 12, color: '#666' } },
        tooltip: { trigger: 'axis' },
        legend: { right: 0, textStyle: { fontSize: 10 } },
        xAxis: { type: 'category', data: ['W1', 'W2', 'W3', 'W4', 'W5', 'W6'] },
        yAxis: [
            { type: 'value', name: '金额 (万)' },
            { type: 'value', name: '增长率', axisLabel: { formatter: '{value}%' } }
        ],
        series: [
            { name: '入金金额', type: 'bar', data: [120, 150, 80, 200, 250, 310], itemStyle: { color: '#FDBA74' } },
            { name: 'AUM新增', type: 'line', data: [50, 70, 40, 110, 150, 180], itemStyle: { color: '#3B82F6' } },
            { name: '增长率', type: 'line', yAxisIndex: 1, data: [10, 12, 5, 15, 20, 25], itemStyle: { color: '#EF4444' } }
        ]
    })

    chartInstances = [taskTrend, taskType, connectFunnel, callTrend, conversionTrend]

    const handleResize = () => chartInstances.forEach(c => c.resize())
    window.addEventListener('resize', handleResize)
    onUnmounted(() => {
        window.removeEventListener('resize', handleResize)
        chartInstances.forEach(c => c.dispose())
    })
})
</script>

<style scoped>
.performance-page {
    font-family: 'Inter', 'Microsoft YaHei', sans-serif;
    background-color: #F8FAFC;
    height: 100vh;
    overflow: hidden;
    display: flex;
}

#sidebar {
    width: 256px;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

#sidebar.collapsed {
    width: 80px;
}

#sidebar.collapsed :deep(.logo-text),
#sidebar.collapsed :deep(.nav-text),
#sidebar.collapsed :deep(.user-info-text) {
    display: none;
}

#sidebar.collapsed :deep(.nav-item) {
    justify-content: center;
    padding-left: 0;
    padding-right: 0;
}

#sidebar.collapsed :deep(.nav-item iconify-icon) {
    margin-right: 0;
}

#sidebar.collapsed :deep(.logo-container) {
    justify-content: center;
}

.card-shadow {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.kpi-card {
    transition: transform 0.2s;
}

.kpi-card:hover {
    transform: translateY(-2px);
}

main {
    height: 100vh;
    overflow-y: auto;
}

:deep(::-webkit-scrollbar) { width: 6px; }
:deep(::-webkit-scrollbar-track) { background: transparent; }
:deep(::-webkit-scrollbar-thumb) { background: #e2e8f0; border-radius: 10px; }
:deep(::-webkit-scrollbar-thumb:hover) { background: #cbd5e1; }
</style>
