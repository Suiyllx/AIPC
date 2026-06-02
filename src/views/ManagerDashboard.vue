<template>
    <div class="manager-page">
        <!-- 侧边栏 -->
        <aside class="manager-sidebar flex flex-col z-50 shrink-0" :class="{ collapsed: sidebarCollapsed }" id="mgr-sidebar">
            <!-- Logo -->
            <div class="h-16 flex items-center px-5 border-b border-zinc-800 logo-container">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shrink-0 shadow-lg shadow-indigo-500/20">
                        <iconify-icon class="text-2xl text-white" icon="solar:shield-star-bold-duotone"></iconify-icon>
                    </div>
                    <span class="font-bold text-lg text-zinc-100 logo-text truncate">AI展业平台</span>
                </div>
            </div>
            <!-- 导航 -->
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
            <!-- 用户信息 -->
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
        <main class="flex-1 overflow-y-auto bg-[#09090b] custom-scrollbar">
            <!-- 顶部导航 -->
            <header class="h-16 border-b border-zinc-800 bg-zinc-950/50 backdrop-blur-md flex items-center justify-between px-8 sticky top-0 z-40">
                <div class="flex items-center gap-4">
                    <button class="p-2 rounded-lg hover:bg-zinc-800 text-zinc-400 transition-colors" @click="toggleSidebar">
                        <iconify-icon class="text-2xl" icon="solar:hamburger-menu-bold"></iconify-icon>
                    </button>
                    <span class="text-base font-semibold text-zinc-100">2026年05月15日</span>
                </div>
                <div class="flex items-center gap-3">
                    <!-- 角色切换 -->
                    <div class="flex items-center gap-1 bg-zinc-800 rounded-lg p-1 text-xs font-medium">
                        <router-link class="px-2.5 py-1 text-zinc-400 hover:text-white rounded-md transition-all" to="/">营销人员</router-link>
                        <span class="px-2.5 py-1 bg-zinc-700 text-white rounded-md">管理人员</span>
                    </div>
                    <button class="p-2 rounded-lg hover:bg-zinc-800 text-zinc-400 transition-colors relative">
                        <iconify-icon class="text-xl" icon="solar:bell-bing-bold"></iconify-icon>
                        <span class="absolute top-2 right-2 w-2 h-2 bg-rose-500 rounded-full border-2 border-zinc-950"></span>
                    </button>
                    <button class="p-2 rounded-lg hover:bg-zinc-800 text-zinc-400 transition-colors">
                        <iconify-icon class="text-xl" icon="solar:settings-bold"></iconify-icon>
                    </button>
                    <div class="h-6 w-px bg-zinc-800"></div>
                    <router-link to="/manager/customers"
                        class="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-all shadow-lg shadow-indigo-600/20">
                        <iconify-icon icon="solar:add-circle-bold"></iconify-icon>
                        <span>快速分配任务</span>
                    </router-link>
                </div>
            </header>

            <!-- 页面内容 -->
            <div class="p-8 space-y-8">
                <!-- 1. 概览卡片 + 趋势图 -->
                <section class="grid grid-cols-1 xl:grid-cols-3 gap-6">
                    <div class="xl:col-span-2 grid grid-cols-2 sm:grid-cols-3 gap-4">
                        <div class="glass-card p-5 rounded-2xl flex flex-col justify-between">
                            <div class="flex justify-between items-start">
                                <span class="text-zinc-400 text-xs">本月团队业绩总额</span>
                                <div class="p-2 bg-indigo-500/10 rounded-lg"><iconify-icon class="text-indigo-400" icon="solar:star-bold"></iconify-icon></div>
                            </div>
                            <div class="mt-4">
                                <h3 class="text-2xl font-bold text-zinc-100">1,284 <span class="text-sm font-normal text-zinc-500">万</span></h3>
                                <div class="flex items-center gap-2 mt-1.5">
                                    <span class="text-emerald-500 text-xs font-medium">目标完成率 72.8%</span>
                                    <div class="flex-1 h-1 bg-zinc-800 rounded-full overflow-hidden">
                                        <div class="h-full bg-emerald-500" style="width: 72.8%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="glass-card p-5 rounded-2xl flex flex-col justify-between">
                            <div class="flex justify-between items-start">
                                <span class="text-zinc-400 text-xs">本月外呼总量</span>
                                <div class="p-2 bg-amber-500/10 rounded-lg"><iconify-icon class="text-amber-400" icon="solar:phone-calling-bold"></iconify-icon></div>
                            </div>
                            <div class="mt-4">
                                <h3 class="text-2xl font-bold text-zinc-100">22,481 <span class="text-sm font-normal text-zinc-500">次</span></h3>
                                <p class="text-zinc-500 text-xs mt-1">接通率 <span class="text-indigo-400">46.2%</span></p>
                            </div>
                        </div>
                        <div class="glass-card p-5 rounded-2xl flex flex-col justify-between">
                            <div class="flex justify-between items-start">
                                <span class="text-zinc-400 text-xs">本月企微添加数</span>
                                <div class="p-2 bg-emerald-500/10 rounded-lg"><iconify-icon class="text-emerald-400" icon="solar:users-group-two-rounded-bold"></iconify-icon></div>
                            </div>
                            <div class="mt-4">
                                <h3 class="text-2xl font-bold text-zinc-100">386 <span class="text-sm font-normal text-zinc-500">人</span></h3>
                                <p class="text-zinc-500 text-xs mt-1">绑定率 <span class="text-emerald-400">284 人</span></p>
                            </div>
                        </div>
                        <div class="glass-card p-5 rounded-2xl flex flex-col justify-between">
                            <div class="flex justify-between items-start">
                                <span class="text-zinc-400 text-xs">本月开新客</span>
                                <div class="p-2 bg-rose-500/10 rounded-lg"><iconify-icon class="text-rose-400" icon="solar:user-plus-bold"></iconify-icon></div>
                            </div>
                            <div class="mt-4">
                                <h3 class="text-2xl font-bold text-zinc-100">72 <span class="text-sm font-normal text-zinc-500">户</span></h3>
                                <p class="text-zinc-500 text-xs mt-1">首次入金 <span class="text-rose-400">54 户</span></p>
                            </div>
                        </div>
                        <div class="glass-card p-5 rounded-2xl flex flex-col justify-between">
                            <div class="flex justify-between items-start">
                                <span class="text-zinc-400 text-xs">团队任务完成率</span>
                                <div class="p-2 bg-blue-500/10 rounded-lg"><iconify-icon class="text-blue-400" icon="solar:checklist-bold"></iconify-icon></div>
                            </div>
                            <div class="mt-4">
                                <h3 class="text-2xl font-bold text-zinc-100">78.5%</h3>
                                <p class="text-zinc-500 text-xs mt-1">较上月 <span class="text-rose-400">↓ 3.2%</span></p>
                            </div>
                        </div>
                        <div class="glass-card p-5 rounded-2xl flex flex-col justify-between border-rose-500/30 bg-rose-500/5">
                            <div class="flex justify-between items-start">
                                <span class="text-rose-400 text-xs font-medium">流失预警客户</span>
                                <div class="p-2 bg-rose-500/20 rounded-lg"><iconify-icon class="text-rose-400" icon="solar:users-group-rounded-bold"></iconify-icon></div>
                            </div>
                            <div class="mt-4">
                                <h3 class="text-2xl font-bold text-rose-400">286 <span class="text-sm font-normal opacity-70">人</span></h3>
                                <router-link to="/manager/customers" class="mt-1 text-xs text-rose-400 underline underline-offset-2 hover:text-rose-300 inline-block">立即分配</router-link>
                            </div>
                        </div>
                    </div>
                    <!-- 趋势图 -->
                    <div class="glass-card p-6 rounded-2xl flex flex-col">
                        <div class="flex justify-between items-center mb-5">
                            <h4 class="font-semibold text-zinc-200 text-sm">本月业绩日趋势</h4>
                            <div class="flex bg-zinc-800 rounded-lg p-1">
                                <button class="px-3 py-1 text-xs font-medium rounded-md bg-zinc-700 text-white">本月</button>
                                <button class="px-3 py-1 text-xs font-medium rounded-md text-zinc-400 hover:text-zinc-200">上月</button>
                            </div>
                        </div>
                        <div class="flex-1 min-h-[200px]" id="performanceTrendChart"></div>
                    </div>
                </section>

                <!-- 2. 客户健康看板 + 任务执行看板 -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <section class="glass-card p-6 rounded-2xl">
                        <div class="flex justify-between items-center mb-5">
                            <h4 class="font-bold text-base text-zinc-100 flex items-center gap-2">
                                <iconify-icon class="text-emerald-500 text-xl" icon="solar:heart-pulse-bold-duotone"></iconify-icon>
                                客户健康看板
                            </h4>
                            <span class="text-[10px] text-zinc-500">更新于 10分钟前</span>
                        </div>
                        <div class="grid grid-cols-2 gap-5">
                            <div class="space-y-3">
                                <div v-for="item in customerHealthItems" :key="item.label" class="p-3 rounded-xl bg-zinc-950/50 border border-zinc-800">
                                    <p class="text-[10px] text-zinc-500 mb-1">{{ item.label }}</p>
                                    <p class="text-lg font-bold" :class="item.color">{{ item.value }}</p>
                                </div>
                            </div>
                            <div class="flex flex-col">
                                <div class="flex-1 min-h-[200px]" id="customerStructureChart"></div>
                                <div class="mt-2 space-y-1.5">
                                    <div v-for="leg in customerLegend" :key="leg.label" class="flex justify-between text-xs">
                                        <span class="text-zinc-500 flex items-center gap-1.5">
                                            <span class="w-2 h-2 rounded-full inline-block" :class="leg.dot"></span>{{ leg.label }}
                                        </span>
                                        <span class="text-zinc-300 font-medium">{{ leg.pct }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>

                    <section class="glass-card p-6 rounded-2xl">
                        <div class="flex justify-between items-center mb-5">
                            <h4 class="font-bold text-base text-zinc-100 flex items-center gap-2">
                                <iconify-icon class="text-indigo-500 text-xl" icon="solar:clipboard-check-bold-duotone"></iconify-icon>
                                任务执行看板
                            </h4>
                            <button class="text-indigo-400 text-xs font-medium hover:underline">查看详情</button>
                        </div>
                        <div class="grid grid-cols-2 gap-5">
                            <div class="space-y-5">
                                <div class="space-y-2">
                                    <div class="flex justify-between items-end">
                                        <span class="text-sm text-zinc-400">任务完成率</span>
                                        <span class="text-lg font-bold text-indigo-400">78.5%</span>
                                    </div>
                                    <div class="h-2 bg-zinc-800 rounded-full overflow-hidden">
                                        <div class="h-full bg-indigo-500 shadow-[0_0_10px_rgba(79,70,229,0.5)]" style="width: 78.5%"></div>
                                    </div>
                                </div>
                                <div class="grid grid-cols-2 gap-3">
                                    <div class="p-4 rounded-xl bg-zinc-950/50 border border-zinc-800">
                                        <p class="text-[10px] text-zinc-500 mb-1">待分配任务</p>
                                        <p class="text-xl font-bold text-zinc-100 mb-2">124</p>
                                        <router-link to="/manager/customers" class="block w-full py-1.5 bg-indigo-600/20 text-indigo-400 text-[10px] text-center rounded-lg hover:bg-indigo-600/30 transition-all">去分配</router-link>
                                    </div>
                                    <div class="p-4 rounded-xl bg-zinc-950/50 border border-rose-500/30">
                                        <p class="text-[10px] text-zinc-500 mb-1">监控中任务</p>
                                        <p class="text-xl font-bold text-rose-500 mb-2">18</p>
                                        <button class="w-full py-1.5 bg-rose-500/20 text-rose-400 text-[10px] rounded-lg hover:bg-rose-500/30 transition-all">告警</button>
                                    </div>
                                </div>
                            </div>
                            <div class="min-h-[200px]" id="taskTypeChart"></div>
                        </div>
                    </section>
                </div>

                <!-- 3. 团队人员看板 -->
                <section class="glass-card p-6 rounded-2xl">
                    <div class="flex justify-between items-center mb-5">
                        <h4 class="font-bold text-base text-zinc-100 flex items-center gap-2">
                            <iconify-icon class="text-amber-500 text-xl" icon="solar:users-group-rounded-bold-duotone"></iconify-icon>
                            团队人员看板（业绩排行）
                        </h4>
                        <div class="flex gap-2">
                            <span class="px-2 py-1 rounded bg-rose-500/10 text-rose-500 text-[10px] font-bold">2人满载预警</span>
                            <span class="px-2 py-1 rounded bg-emerald-500/10 text-emerald-500 text-[10px] font-bold">3人绩效稳健</span>
                        </div>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left">
                            <thead class="text-[10px] text-zinc-500 uppercase tracking-wider border-b border-zinc-800">
                                <tr>
                                    <th class="pb-3 px-2">员工</th>
                                    <th class="pb-3 px-2">待办</th>
                                    <th class="pb-3 px-2">完成数</th>
                                    <th class="pb-3 px-2 text-center">完成率</th>
                                    <th class="pb-3 px-2">外呼量</th>
                                    <th class="pb-3 px-2">加微数</th>
                                    <th class="pb-3 px-2 text-right">负载状态</th>
                                </tr>
                            </thead>
                            <tbody class="text-sm divide-y divide-zinc-800/50">
                                <tr v-for="member in teamMembers" :key="member.name" class="hover:bg-zinc-800/20 transition-all">
                                    <td class="py-3.5 px-2 flex items-center gap-3">
                                        <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold" :class="member.avatarClass">{{ member.avatar }}</div>
                                        <span class="font-medium text-zinc-200">{{ member.name }}</span>
                                    </td>
                                    <td class="py-3.5 px-2 text-zinc-400">{{ member.pending }}</td>
                                    <td class="py-3.5 px-2 text-zinc-400">{{ member.done }}</td>
                                    <td class="py-3.5 px-2">
                                        <div class="w-24 mx-auto h-1.5 bg-zinc-800 rounded-full">
                                            <div class="h-full rounded-full" :class="member.barColor" :style="{ width: member.rate }"></div>
                                        </div>
                                        <p class="text-[10px] text-center mt-1 text-zinc-500">{{ member.rate }}</p>
                                    </td>
                                    <td class="py-3.5 px-2 text-zinc-400">{{ member.calls }}</td>
                                    <td class="py-3.5 px-2 text-zinc-400">{{ member.wechat }}</td>
                                    <td class="py-3.5 px-2 text-right">
                                        <span class="px-2 py-1 rounded-full text-xs font-bold" :class="member.statusClass">{{ member.status }}</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="mt-5 p-4 rounded-xl bg-amber-500/5 border border-amber-500/20 flex items-center gap-4">
                        <div class="p-2 bg-amber-500/20 rounded-lg text-amber-400">
                            <iconify-icon class="text-xl" icon="solar:lightbulb-bold"></iconify-icon>
                        </div>
                        <div>
                            <p class="text-sm font-semibold text-amber-400">薄弱项分析</p>
                            <p class="text-xs text-zinc-400">团队整体外呼接通率偏低（46.2%），建议优化外呼时段并利用AI话术辅助提升沟通效率。</p>
                        </div>
                    </div>
                </section>

                <!-- 4. 转化漏斗 + 服务合规 -->
                <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
                    <section class="glass-card p-6 rounded-2xl xl:col-span-2">
                        <div class="flex justify-between items-center mb-5">
                            <h4 class="font-bold text-base text-zinc-100 flex items-center gap-2">
                                <iconify-icon class="text-indigo-400 text-xl" icon="solar:filter-bold-duotone"></iconify-icon>
                                转化漏斗看板（全链路）
                            </h4>
                            <span class="text-xs text-zinc-500">目标：入金转化率提升至 30%</span>
                        </div>
                        <div class="w-full h-72" id="conversionFunnelChart"></div>
                        <div class="mt-4 grid grid-cols-4 gap-4 text-center">
                            <div v-for="item in funnelStats" :key="item.label" class="space-y-1">
                                <p class="text-[10px] text-zinc-500 uppercase">{{ item.label }}</p>
                                <p class="text-sm font-bold" :class="item.color">{{ item.value }}</p>
                            </div>
                        </div>
                    </section>

                    <section class="glass-card p-6 rounded-2xl">
                        <div class="flex justify-between items-center mb-5">
                            <h4 class="font-bold text-base text-zinc-100 flex items-center gap-2">
                                <iconify-icon class="text-emerald-500 text-xl" icon="solar:shield-check-bold-duotone"></iconify-icon>
                                服务合规一览
                            </h4>
                        </div>
                        <div class="space-y-3">
                            <div v-for="item in complianceItems" :key="item.label" class="flex items-center justify-between p-4 rounded-xl bg-zinc-950/50" :class="item.borderClass">
                                <div class="flex items-center gap-3">
                                    <iconify-icon class="text-xl" :class="item.iconColor" :icon="item.icon"></iconify-icon>
                                    <div>
                                        <p class="text-xs text-zinc-500">{{ item.label }}</p>
                                        <p class="text-base font-bold text-zinc-100">{{ item.value }}</p>
                                    </div>
                                </div>
                                <span class="text-[10px] font-bold px-2 py-1 rounded" :class="item.badgeClass">{{ item.badge }}</span>
                            </div>
                            <div class="p-3 bg-zinc-900 rounded-lg text-center">
                                <p class="text-xs text-zinc-500">客户投诉记录: <span class="text-emerald-500 font-bold">0 条</span></p>
                            </div>
                        </div>
                    </section>
                </div>

                <!-- 5. 快捷操作 -->
                <section class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <button v-for="action in quickActions" :key="action.label"
                        class="glass-card p-5 rounded-2xl flex flex-col items-center gap-3 hover:border-zinc-700 transition-all group"
                        :class="action.hoverClass" @click="action.to ? $router.push(action.to) : null">
                        <div class="w-12 h-12 rounded-xl flex items-center justify-center transition-all" :class="action.iconBg">
                            <iconify-icon class="text-2xl" :class="action.iconColor" :icon="action.icon"></iconify-icon>
                        </div>
                        <span class="font-bold text-zinc-200 text-sm">{{ action.label }}</span>
                    </button>
                </section>

                <!-- 6. 公告栏 -->
                <footer class="glass-card p-4 rounded-2xl overflow-hidden">
                    <div class="flex items-center gap-4">
                        <div class="shrink-0 bg-indigo-600 px-3 py-1 rounded-lg text-xs font-bold text-white">系统公告</div>
                        <div class="flex-1 overflow-hidden">
                            <div class="animate-marquee inline-block whitespace-nowrap">
                                <span class="mx-8 text-sm text-zinc-400">📢 【2026年Q2岗位活动】已上线，请及时分配客户资源，助力业绩增长！</span>
                                <span class="mx-8 text-sm text-zinc-400">📢 合规培训通知：请于5月15日前完成全员话术合规复训，并提交学习心得。</span>
                                <span class="mx-8 text-sm text-zinc-400">📢 【智能客户分配V2】功能已上线，支持AI自动均衡分配，解决员工负载不均问题。</span>
                            </div>
                        </div>
                    </div>
                </footer>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const sidebarCollapsed = ref(false)
const toggleSidebar = () => { sidebarCollapsed.value = !sidebarCollapsed.value }

const customerHealthItems = [
    { label: '团队总客户数', value: '6,842', color: 'text-zinc-100' },
    { label: '流失池客户（待分配）', value: '286', color: 'text-rose-500' },
    { label: '超30天未跟进', value: '124', color: 'text-amber-500' },
    { label: '高价值待激活', value: '58', color: 'text-indigo-400' },
]
const customerLegend = [
    { label: '已绑定', dot: 'bg-indigo-500', pct: '40%' },
    { label: '已加未绑', dot: 'bg-emerald-500', pct: '28%' },
    { label: '未加企微', dot: 'bg-zinc-600', pct: '32%' },
]
const teamMembers = [
    { name: '张大海', avatar: '张', avatarClass: 'bg-indigo-500/20 text-indigo-400', pending: 23, done: 45, rate: '66%', barColor: 'bg-indigo-500', calls: 320, wechat: 12, status: '正常', statusClass: 'bg-emerald-500/10 text-emerald-500' },
    { name: '陈梅云', avatar: '陈', avatarClass: 'bg-emerald-500/20 text-emerald-400', pending: 12, done: 58, rate: '83%', barColor: 'bg-emerald-500', calls: 280, wechat: 18, status: '偏低', statusClass: 'bg-amber-500/10 text-amber-500' },
    { name: '李明晨', avatar: '李', avatarClass: 'bg-rose-500/20 text-rose-400', pending: 35, done: 42, rate: '55%', barColor: 'bg-amber-500', calls: 410, wechat: 8, status: '满载', statusClass: 'bg-rose-500/10 text-rose-500 font-bold' },
    { name: '王涛', avatar: '王', avatarClass: 'bg-zinc-500/20 text-zinc-400', pending: 18, done: 52, rate: '74%', barColor: 'bg-indigo-500', calls: 350, wechat: 15, status: '正常', statusClass: 'bg-emerald-500/10 text-emerald-500' },
    { name: '刘至', avatar: '刘', avatarClass: 'bg-purple-500/20 text-purple-400', pending: 8, done: 62, rate: '89%', barColor: 'bg-emerald-500', calls: 260, wechat: 22, status: '偏低', statusClass: 'bg-amber-500/10 text-amber-500' },
    { name: '赵强', avatar: '赵', avatarClass: 'bg-orange-500/20 text-orange-400', pending: 28, done: 38, rate: '58%', barColor: 'bg-amber-500', calls: 380, wechat: 6, status: '满载', statusClass: 'bg-rose-500/10 text-rose-500 font-bold' },
]
const funnelStats = [
    { label: '触达率', value: '100%', color: 'text-zinc-200' },
    { label: '建联转化', value: '66%', color: 'text-emerald-400' },
    { label: '绑定转化', value: '40%', color: 'text-indigo-400' },
    { label: '入金转化', value: '24%', color: 'text-amber-400' },
]
const complianceItems = [
    { label: '首访及时率', value: '92.5%', icon: 'solar:clock-circle-bold', iconColor: 'text-emerald-500', borderClass: 'border border-emerald-500/20', badge: '良好', badgeClass: 'bg-emerald-500/10 text-emerald-500' },
    { label: '合规零违规天数', value: '365 天', icon: 'solar:calendar-bold', iconColor: 'text-emerald-500', borderClass: 'border border-emerald-500/20', badge: '达标', badgeClass: 'bg-emerald-500/10 text-emerald-500' },
    { label: '录音抽检合格率', value: '98.2%', icon: 'solar:record-bold', iconColor: 'text-indigo-400', borderClass: 'border border-zinc-800', badge: '合格', badgeClass: 'bg-indigo-500/10 text-indigo-400' },
    { label: '企微触达开启率', value: '62.3%', icon: 'solar:chat-round-check-bold', iconColor: 'text-amber-400', borderClass: 'border border-zinc-800', badge: '待提升', badgeClass: 'bg-amber-500/10 text-amber-500' },
]
const quickActions = [
    { label: '分配客户', icon: 'solar:user-plus-bold', iconBg: 'bg-indigo-500/10 group-hover:bg-indigo-500', iconColor: 'text-indigo-400 group-hover:text-white', hoverClass: 'hover:bg-indigo-600/10 hover:border-indigo-500/50', to: '/manager/customers' },
    { label: '下发任务', icon: 'solar:clipboard-list-bold', iconBg: 'bg-indigo-500/10 group-hover:bg-indigo-500', iconColor: 'text-indigo-400 group-hover:text-white', hoverClass: 'hover:bg-indigo-600/10 hover:border-indigo-500/50', to: null },
    { label: '批量监督', icon: 'solar:bell-bing-bold', iconBg: 'bg-rose-500/10 group-hover:bg-rose-500', iconColor: 'text-rose-400 group-hover:text-white', hoverClass: 'hover:bg-rose-500/10 hover:border-rose-500/50', to: null },
    { label: '数据导出', icon: 'solar:export-bold', iconBg: 'bg-zinc-800 group-hover:bg-zinc-100', iconColor: 'text-zinc-400 group-hover:text-zinc-900', hoverClass: 'hover:bg-zinc-800 hover:border-zinc-700', to: null },
]

let charts = []

const handleResize = () => charts.forEach(c => c.resize())

onMounted(() => {
    // 业绩趋势图
    const trendChart = echarts.init(document.getElementById('performanceTrendChart'))
    trendChart.setOption({
        backgroundColor: 'transparent',
        tooltip: { trigger: 'axis', backgroundColor: '#18181b', borderColor: '#27272a', textStyle: { color: '#e4e4e7', fontSize: 11 } },
        grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
        xAxis: { type: 'category', data: ['05-01', '05-05', '05-08', '05-10', '05-12', '05-14', '05-15'], axisLine: { lineStyle: { color: '#3f3f46' } }, axisLabel: { color: '#71717a', fontSize: 10 } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#27272a' } }, axisLabel: { color: '#71717a', fontSize: 10 } },
        series: [{ name: '团队业绩', type: 'line', smooth: true, data: [820, 932, 1100, 934, 1290, 1180, 1284], itemStyle: { color: '#4f46e5' }, lineStyle: { color: '#4f46e5', width: 2 }, areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(79,70,229,0.3)' }, { offset: 1, color: 'rgba(79,70,229,0)' }]) }, symbolSize: 5 }]
    })

    // 客户结构环图
    const customerChart = echarts.init(document.getElementById('customerStructureChart'))
    customerChart.setOption({
        tooltip: { trigger: 'item', backgroundColor: '#18181b', borderColor: '#27272a', textStyle: { color: '#e4e4e7', fontSize: 11 } },
        series: [{ name: '客户结构', type: 'pie', radius: ['60%', '85%'], avoidLabelOverlap: false, itemStyle: { borderRadius: 8, borderColor: '#09090b', borderWidth: 2 }, label: { show: false }, data: [{ value: 40, name: '已绑定', itemStyle: { color: '#4f46e5' } }, { value: 28, name: '已加未绑', itemStyle: { color: '#10b981' } }, { value: 32, name: '未加企微', itemStyle: { color: '#3f3f46' } }] }]
    })

    // 任务类型饼图
    const taskChart = echarts.init(document.getElementById('taskTypeChart'))
    taskChart.setOption({
        tooltip: { trigger: 'item', backgroundColor: '#18181b', borderColor: '#27272a', textStyle: { color: '#e4e4e7', fontSize: 11 } },
        legend: { bottom: '0%', left: 'center', textStyle: { color: '#71717a', fontSize: 10 }, itemWidth: 8, itemHeight: 8 },
        series: [{ name: '任务类型', type: 'pie', radius: '60%', center: ['50%', '43%'], data: [{ value: 45, name: '建联任务', itemStyle: { color: '#4f46e5' } }, { value: 30, name: '周期任务', itemStyle: { color: '#10b981' } }, { value: 25, name: '活动任务', itemStyle: { color: '#f59e0b' } }], label: { color: '#71717a', fontSize: 10 } }]
    })

    // 转化漏斗图
    const funnelChart = echarts.init(document.getElementById('conversionFunnelChart'))
    funnelChart.setOption({
        tooltip: { trigger: 'item', backgroundColor: '#18181b', borderColor: '#27272a', textStyle: { color: '#e4e4e7', fontSize: 11 } },
        series: [{ name: '转化漏斗', type: 'funnel', left: '10%', top: 10, bottom: 10, width: '80%', min: 0, max: 100, minSize: '20%', maxSize: '100%', sort: 'descending', gap: 4, label: { show: true, position: 'inside', formatter: '{b}: {c}', textStyle: { color: '#fff', fontSize: 12, fontWeight: 'bold' } }, labelLine: { show: false }, itemStyle: { opacity: 0.85, borderColor: '#09090b', borderWidth: 2 }, data: [{ value: 100, name: '触达客户', itemStyle: { color: '#3f3f46' } }, { value: 66, name: '已建联', itemStyle: { color: '#10b981' } }, { value: 40, name: '已绑定微信', itemStyle: { color: '#4f46e5' } }, { value: 24, name: '已入金客户', itemStyle: { color: '#f59e0b' } }] }]
    })

    charts = [trendChart, customerChart, taskChart, funnelChart]
    window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    charts.forEach(c => c.dispose())
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

.manager-sidebar.collapsed {
    width: 76px;
}

.manager-sidebar.collapsed .logo-text,
.manager-sidebar.collapsed .nav-text,
.manager-sidebar.collapsed .user-info-text {
    display: none;
}

.manager-sidebar.collapsed .nav-item {
    justify-content: center;
    padding-left: 0;
    padding-right: 0;
}

.manager-sidebar.collapsed .logo-container {
    justify-content: center;
}

.glass-card {
    background: rgba(24, 24, 27, 0.8);
    backdrop-filter: blur(12px);
    border: 1px solid #27272a;
    transition: border-color 0.2s;
}

.glass-card:hover {
    border-color: #3f3f46;
}

.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #27272a; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #3f3f46; }

.animate-marquee {
    animation: marquee 35s linear infinite;
}

@keyframes marquee {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}
</style>
