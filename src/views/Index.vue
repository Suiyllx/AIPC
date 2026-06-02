<template>
  <div class="flex h-screen overflow-hidden text-sm">
    <!-- 侧边栏 -->
    <aside class="bg-white border-r border-slate-200 flex flex-col h-screen shrink-0 relative z-50" id="sidebar">
    <div class="h-16 flex items-center px-6 border-b border-slate-100 logo-container">
    <a class="flex items-center gap-3" href="index.html">
    <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shrink-0">
    <iconify-icon class="text-white text-xl" icon="lucide:sparkles"></iconify-icon>
    </div>
    <span class="text-lg font-bold text-slate-900 logo-text truncate">AI展业平台</span>
    </a>
    </div>
    <nav class="flex-1 px-4 space-y-1 mt-4">
        <router-link
            class="nav-item flex items-center px-4 py-3 text-gray-500 hover:bg-blue-50 hover:text-blue-600 rounded-xl transition-all group"
            to="/"
            active-class="bg-blue-600 text-white shadow-lg shadow-blue-200"
        >
            <iconify-icon class="text-2xl mr-3 shrink-0" icon="solar:widget-5-bold-duotone"></iconify-icon>
            <span class="nav-text font-medium whitespace-nowrap">工作台总览</span>
        </router-link>
        <router-link
            class="nav-item flex items-center px-4 py-3 rounded-xl transition-all"
            to="/tasks"
            active-class="bg-blue-600 text-white shadow-lg shadow-blue-200"
        >
            <iconify-icon class="text-2xl mr-3 shrink-0" icon="solar:clipboard-check-bold-duotone"></iconify-icon>
            <span class="nav-text font-medium whitespace-nowrap">任务大厅</span>
        </router-link>
        <router-link
            class="nav-item flex items-center px-4 py-3 text-gray-500 hover:bg-blue-50 hover:text-blue-600 rounded-xl transition-all group"
            to="/business"
            active-class="bg-blue-600 text-white shadow-lg shadow-blue-200"
        >
            <iconify-icon class="text-2xl mr-3 shrink-0" icon="solar:shop-2-bold-duotone"></iconify-icon>
            <span class="nav-text font-medium whitespace-nowrap">展业大厅</span>
        </router-link>
        <router-link
            class="nav-item flex items-center px-4 py-3 text-gray-500 hover:bg-blue-50 hover:text-blue-600 rounded-xl transition-all group"
            to="/performance"
            active-class="bg-blue-600 text-white shadow-lg shadow-blue-200"
        >
            <iconify-icon class="text-2xl mr-3 shrink-0" icon="solar:graph-up-bold-duotone"></iconify-icon>
            <span class="nav-text font-medium whitespace-nowrap">业绩看板</span>
        </router-link>
    </nav>
    <div class="p-4 border-t border-slate-100">
    <div class="flex items-center gap-3 p-2 rounded-lg bg-slate-50">
    <img alt="User Avatar" class="w-9 h-9 rounded-full border border-white shadow-sm shrink-0" src="https://modao.cc/agent-py/media/generated_images/2026-05-08/a882eb2419144200ad91384b36189402.jpg#desc=User%20Avatar"/>
    <div class="user-info-text overflow-hidden">
    <p class="text-sm font-semibold text-slate-900 truncate">张超越</p>
    <p class="text-xs text-slate-500 truncate">最后登录: 2026-05-08</p>
    </div>
    </div>
    </div>
    </aside>

    <!-- 主体内容 -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden relative">
    <!-- 顶部导航栏 -->
    <header class="h-16 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-6 sticky top-0 z-40">
    <div class="flex items-center gap-4">
    <button class="p-2 hover:bg-slate-100 rounded-lg transition-colors" id="toggleSidebar">
    <iconify-icon class="text-xl text-slate-600" icon="lucide:menu"></iconify-icon>
    </button>
    <div class="h-6 w-px bg-slate-200"></div>
    <div class="flex items-center gap-2 text-slate-500">
    <span class="text-sm font-medium">今天是 {{ todayStr }}</span>
    </div>
    </div>
    <div class="flex items-center gap-4">
    <div class="flex items-center gap-1 bg-slate-100 rounded-lg p-1 text-xs font-medium">
        <span class="px-2.5 py-1 bg-white text-slate-900 rounded-md shadow-sm">营销人员</span>
        <router-link class="px-2.5 py-1 text-slate-500 hover:text-slate-700 rounded-md transition-all" to="/manager">管理人员</router-link>
    </div>
    <!-- 每日提醒面板 -->
    <div class="relative alert-panel-wrapper">
      <button
        @click="toggleAlertPanel"
        class="p-2 text-gray-400 hover:bg-gray-100 rounded-full relative"
      >
        <iconify-icon class="text-2xl" icon="solar:bell-bing-bold"></iconify-icon>
        <span
          v-if="unreadAlertCount > 0"
          class="absolute top-1 right-1 min-w-[16px] h-4 bg-red-500 text-white text-[9px] font-bold rounded-full flex items-center justify-center px-0.5"
        >{{ unreadAlertCount }}</span>
      </button>
      <div
        v-if="alertPanelOpen"
        class="absolute right-0 top-12 w-96 bg-white border border-slate-200 rounded-2xl shadow-2xl z-50 flex flex-col overflow-hidden"
        style="max-height: 480px;"
        @click.stop
      >
        <div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between shrink-0">
          <span class="font-bold text-slate-900 text-sm">每日提醒</span>
          <span class="text-xs text-slate-400">{{ alerts.length }} 条未完成</span>
        </div>
        <div class="flex-1 overflow-y-auto p-3 space-y-2 no-scrollbar">
          <div v-if="alerts.length === 0" class="text-center text-slate-400 text-xs py-8">暂无提醒</div>
          <div
            v-for="a in alerts"
            :key="a.id"
            class="flex items-start gap-3 p-3 rounded-xl bg-slate-50 hover:bg-slate-100 transition-colors group"
          >
            <div class="w-2 h-2 rounded-full bg-blue-500 shrink-0 mt-1.5"></div>
            <p class="flex-1 text-xs text-slate-700 leading-relaxed">{{ a.content }}</p>
            <button
              @click="markAlertDone(a.id)"
              class="shrink-0 text-[10px] text-slate-400 hover:text-green-600 font-bold opacity-0 group-hover:opacity-100 transition-opacity"
            >完成</button>
          </div>
        </div>
        <div class="p-3 border-t border-slate-100 shrink-0">
          <div class="flex gap-2">
            <input
              v-model="newAlertContent"
              @keyup.enter="addAlert"
              type="text"
              placeholder="添加新提醒…"
              class="flex-1 px-3 py-2 text-xs bg-slate-100 border-0 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              @click="addAlert"
              class="px-3 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg hover:bg-blue-700 transition-colors"
            >添加</button>
          </div>
        </div>
      </div>
    </div>
    <div class="h-6 w-px bg-slate-200"></div>
    </div>
    </header>

    <!-- 内容滚动区域 -->
    <main class="flex-1 overflow-y-auto p-6 space-y-5 no-scrollbar" style="background-color: #f8fafc;">

      <!-- 今日核心概览 -->
      <section>
        <div class="flex items-center mb-4">
          <h2 class="text-base font-bold text-slate-900 flex items-center gap-2">
            今日核心概览
            <span class="text-[10px] font-bold px-2 py-0.5 bg-blue-100 text-blue-600 rounded-full uppercase tracking-wider">Real-time</span>
          </h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- AUM净增 -->
          <div class="shadcn-card p-5 cursor-pointer group hover:border-blue-200">
            <div class="flex justify-between items-start mb-3">
              <div class="w-10 h-10 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center group-hover:bg-blue-600 group-hover:text-white transition-colors">
                <iconify-icon icon="lucide:trending-up" width="20"></iconify-icon>
              </div>
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">AUM</span>
            </div>
            <p class="text-xs text-slate-500 font-medium mb-1">月AUM净增率</p>
            <div class="flex items-end gap-2 mb-3">
              <span class="text-2xl font-bold text-slate-900">
                {{ overview.aum_card ? (overview.aum_card.net_increase_rate > 0 ? '+' : '') + overview.aum_card.net_increase_rate + '%' : '--' }}
              </span>
              <span
                v-if="overview.aum_card"
                :class="overview.aum_card.net_increase >= 0 ? 'text-green-500' : 'text-red-500'"
                class="text-xs font-bold mb-0.5"
              >vs 上月末</span>
            </div>
            <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden mb-2">
              <div
                class="h-full bg-blue-600 rounded-full transition-all duration-700"
                :style="{ width: overview.aum_card ? Math.min(Math.abs(overview.aum_card.net_increase_rate) * 5, 100) + '%' : '0%' }"
              ></div>
            </div>
            <p class="text-[10px] text-slate-500">
              累计净增:
              <span class="font-bold text-slate-700">
                {{ overview.aum_card ? overview.aum_card.display_increase : '--' }}
              </span>
            </p>
          </div>
          <!-- 建联现状 -->
          <div class="shadcn-card p-5 cursor-pointer group hover:border-emerald-200">
            <div class="flex justify-between items-start mb-3">
              <div class="w-10 h-10 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                <iconify-icon icon="lucide:users" width="20"></iconify-icon>
              </div>
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Connection</span>
            </div>
            <p class="text-xs text-slate-500 font-medium mb-2">今日建联现状</p>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <p class="text-xl font-bold text-slate-900">{{ overview.call_card?.connected ?? '--' }}</p>
                <p class="text-[10px] text-slate-400 font-medium">外呼接通</p>
              </div>
              <div>
                <p class="text-xl font-bold text-emerald-600">{{ overview.call_card?.intention ?? '--' }}</p>
                <p class="text-[10px] text-slate-400 font-medium">意向客户</p>
              </div>
              <div>
                <p class="text-xl font-bold text-slate-900">{{ overview.call_card?.wechat_add ?? '--' }}</p>
                <p class="text-[10px] text-slate-400 font-medium">今日加微</p>
              </div>
              <div>
                <p class="text-xl font-bold text-slate-900">{{ overview.call_card?.bound ?? '--' }}</p>
                <p class="text-[10px] text-slate-400 font-medium">绑定数</p>
              </div>
            </div>
          </div>
          <!-- 任务完成 -->
          <div class="shadcn-card p-5 cursor-pointer group hover:border-purple-200">
            <div class="flex justify-between items-start mb-3">
              <div class="w-10 h-10 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center group-hover:bg-purple-600 group-hover:text-white transition-colors">
                <iconify-icon icon="lucide:clipboard-check" width="20"></iconify-icon>
              </div>
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Tasks</span>
            </div>
            <p class="text-xs text-slate-500 font-medium mb-2">当日任务进度</p>
            <div class="flex items-center gap-4">
              <div class="relative w-16 h-16 shrink-0">
                <div class="w-full h-full" id="taskProgressChart"></div>
                <div class="absolute inset-0 flex items-center justify-center">
                  <span class="text-sm font-bold text-slate-900">{{ overview.task_card?.rate != null ? overview.task_card.rate + '%' : '--' }}</span>
                </div>
              </div>
              <div class="flex-1 space-y-1.5">
                <div class="flex justify-between text-xs">
                  <span class="text-slate-400">待办</span><span class="font-bold text-slate-900">{{ overview.task_card?.todo ?? '--' }}</span>
                </div>
                <div class="flex justify-between text-xs">
                  <span class="text-slate-400">完成</span><span class="font-bold text-slate-900">{{ overview.task_card?.done ?? '--' }}</span>
                </div>
                <div class="flex justify-between text-xs">
                  <span class="text-slate-400">逾期</span><span class="font-bold text-red-500">{{ overview.task_card?.overdue ?? '--' }}</span>
                </div>
              </div>
            </div>
          </div>
          <!-- 成长进度 -->
          <div class="shadcn-card p-5 cursor-pointer group border-l-4 border-l-indigo-500 hover:border-indigo-200" @click="activeTab = 'growth'">
            <div class="flex justify-between items-start mb-3">
              <div class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                <iconify-icon icon="lucide:graduation-cap" width="20"></iconify-icon>
              </div>
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Growth</span>
            </div>
            <p class="text-xs text-slate-500 font-medium mb-1">季度成长完成率</p>
            <div class="flex items-end gap-2 mb-3">
              <span class="text-2xl font-bold text-slate-900">45%</span>
              <span class="text-xs text-red-500 font-bold mb-0.5">未达标</span>
            </div>
            <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div class="h-full bg-indigo-500 rounded-full" style="width: 45%"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- 每日营销资讯 -->
      <section class="shadcn-card px-4 py-3 bg-slate-50/60 border-dashed">
        <div class="flex items-center gap-4">
          <div class="shrink-0 flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-600">
            <iconify-icon class="text-orange-500" icon="lucide:megaphone" width="14"></iconify-icon>
            每日资讯
          </div>
          <div class="flex-1 grid grid-cols-1 md:grid-cols-2 gap-4 min-w-0">
            <template v-if="todayNews.length > 0">
              <div
                v-for="n in todayNews.slice(0, 2)"
                :key="n.id"
                class="flex items-center justify-between gap-3 min-w-0"
              >
                <div class="flex items-center gap-2 overflow-hidden min-w-0">
                  <span :class="categoryClass(n.category)" class="shrink-0 px-1.5 py-0.5 text-[10px] rounded font-bold">{{ n.category }}</span>
                  <p class="text-xs text-slate-700 truncate">{{ n.title }}</p>
                </div>
                <button
                  @click="copyNews(n.title)"
                  class="shrink-0 text-[10px] text-blue-600 font-bold hover:underline"
                >复制素材</button>
              </div>
            </template>
            <template v-else>
              <p class="text-xs text-slate-400 col-span-2">今日暂无资讯</p>
            </template>
          </div>
          <button
            @click="openNewsModal"
            class="shrink-0 flex items-center gap-1 px-3 py-1.5 bg-blue-600 text-white text-xs font-bold rounded-lg hover:bg-blue-700 transition-colors"
          >
            查看更多
            <iconify-icon icon="lucide:chevron-right" width="12"></iconify-icon>
          </button>
        </div>
      </section>

      <!-- 资讯弹窗 (Teleport to body) -->
      <Teleport to="body">
        <Transition name="modal-fade">
          <div
            v-if="newsModalOpen"
            class="fixed inset-0 z-[200] flex items-center justify-center"
            @click.self="closeNewsModal"
          >
            <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>
            <div class="relative w-full max-w-3xl mx-4 bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden" style="max-height: 80vh;">
              <!-- 弹窗头部 -->
              <div class="px-6 py-5 border-b border-slate-100 flex items-center justify-between shrink-0">
                <div class="flex items-center gap-2">
                  <iconify-icon class="text-orange-500" icon="lucide:newspaper" width="18"></iconify-icon>
                  <h2 class="text-base font-bold text-slate-900">每日资讯</h2>
                  <span class="text-xs text-slate-400 font-normal ml-1">共 {{ newsTotal }} 条</span>
                </div>
                <button @click="closeNewsModal" class="p-1.5 hover:bg-slate-100 rounded-lg transition-colors">
                  <iconify-icon icon="lucide:x" width="18" class="text-slate-500"></iconify-icon>
                </button>
              </div>

              <!-- 筛选区 -->
              <div class="px-6 py-4 border-b border-slate-100 shrink-0 flex flex-wrap gap-3 bg-slate-50/60">
                <!-- 标题搜索 -->
                <div class="flex items-center gap-2 flex-1 min-w-[180px] bg-white border border-slate-200 rounded-lg px-3 py-2">
                  <iconify-icon icon="lucide:search" width="14" class="text-slate-400 shrink-0"></iconify-icon>
                  <input
                    v-model="newsFilter.title"
                    @input="debouncedFetchNews"
                    type="text"
                    placeholder="搜索资讯标题…"
                    class="flex-1 text-xs border-0 outline-none bg-transparent text-slate-700 placeholder-slate-400"
                  />
                </div>
                <!-- 分类筛选 -->
                <select
                  v-model="newsFilter.category"
                  @change="fetchNewsList(1)"
                  class="px-3 py-2 text-xs bg-white border border-slate-200 rounded-lg text-slate-700 outline-none cursor-pointer"
                >
                  <option value="">全部分类</option>
                  <option v-for="c in newsCategories" :key="c" :value="c">{{ c }}</option>
                </select>
                <!-- 月份筛选 -->
                <input
                  v-model="newsFilter.month"
                  @change="fetchNewsList(1)"
                  type="month"
                  class="px-3 py-2 text-xs bg-white border border-slate-200 rounded-lg text-slate-700 outline-none cursor-pointer"
                />
                <!-- 重置 -->
                <button
                  @click="resetNewsFilter"
                  class="px-3 py-2 text-xs text-slate-500 hover:text-blue-600 font-medium transition-colors"
                >重置</button>
              </div>

              <!-- 资讯列表 -->
              <div class="flex-1 overflow-y-auto no-scrollbar">
                <div v-if="newsList.length === 0" class="flex flex-col items-center justify-center py-16 text-slate-400">
                  <iconify-icon icon="lucide:inbox" width="32" class="mb-3 opacity-40"></iconify-icon>
                  <p class="text-sm">暂无资讯</p>
                </div>
                <div v-else class="divide-y divide-slate-100">
                  <div
                    v-for="n in newsList"
                    :key="n.id"
                    class="flex items-center gap-4 px-6 py-4 hover:bg-slate-50 transition-colors group"
                  >
                    <span :class="categoryClass(n.category)" class="shrink-0 px-2 py-0.5 text-[10px] rounded font-bold">{{ n.category }}</span>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm text-slate-800 font-medium truncate">{{ n.title }}</p>
                      <p class="text-[10px] text-slate-400 mt-0.5">{{ n.date }}</p>
                    </div>
                    <div class="shrink-0 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        v-if="n.link"
                        @click="openLink(n.link)"
                        class="text-[10px] text-blue-600 font-bold hover:underline"
                      >查看原文</button>
                      <button
                        @click="copyNews(n.title)"
                        class="text-[10px] text-slate-500 font-bold hover:text-blue-600 hover:underline"
                      >复制素材</button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 分页 -->
              <div v-if="newsTotal > newsPageSize" class="px-6 py-4 border-t border-slate-100 shrink-0 flex items-center justify-between">
                <span class="text-xs text-slate-400">第 {{ newsPage }} / {{ Math.ceil(newsTotal / newsPageSize) }} 页，共 {{ newsTotal }} 条</span>
                <div class="flex items-center gap-2">
                  <button
                    :disabled="newsPage <= 1"
                    @click="fetchNewsList(newsPage - 1)"
                    class="px-3 py-1.5 text-xs border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                  >上一页</button>
                  <button
                    :disabled="newsPage >= Math.ceil(newsTotal / newsPageSize)"
                    @click="fetchNewsList(newsPage + 1)"
                    class="px-3 py-1.5 text-xs border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                  >下一页</button>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>

      <!-- Tab 核心区域 -->
      <section class="space-y-5">
        <!-- Tab 切换导航 -->
        <div class="flex justify-center">
          <div class="bg-slate-100 p-1 rounded-xl flex gap-1 w-full max-w-sm shadow-inner">
            <button
              @click="activeTab = 'tasks'"
              :class="activeTab === 'tasks'
                ? 'flex-1 flex items-center justify-center gap-2 py-2.5 text-sm font-bold rounded-lg bg-white text-slate-900 shadow-sm'
                : 'flex-1 flex items-center justify-center gap-2 py-2.5 text-sm font-bold rounded-lg text-slate-500 hover:text-slate-700'"
            >
              <iconify-icon icon="lucide:clipboard-list" width="16"></iconify-icon>
              每日任务
            </button>
            <button
              @click="activeTab = 'growth'"
              :class="activeTab === 'growth'
                ? 'flex-1 flex items-center justify-center gap-2 py-2.5 text-sm font-bold rounded-lg bg-white text-slate-900 shadow-sm'
                : 'flex-1 flex items-center justify-center gap-2 py-2.5 text-sm font-bold rounded-lg text-slate-500 hover:text-slate-700'"
            >
              <iconify-icon icon="lucide:trending-up" width="16"></iconify-icon>
              成长赋能
            </button>
          </div>
        </div>

        <!-- Tab 1: 每日任务 -->
        <div v-show="activeTab === 'tasks'" class="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <!-- 左侧 2/3 -->
          <div class="lg:col-span-2 space-y-4">
            <!-- 高优任务 -->
            <div class="shadcn-card overflow-hidden border-l-4 border-l-red-500">
              <div class="px-5 py-3 bg-red-50 border-b border-red-100 flex items-center justify-between">
                <h3 class="text-xs font-bold text-red-700 flex items-center gap-2">
                  <iconify-icon icon="lucide:alert-circle" width="14"></iconify-icon>
                  高优任务
                  <span v-if="urgentSummary.total > 0">({{ urgentSummary.total }}项)</span>
                </h3>
                <span class="text-[10px] text-red-600 font-medium">需立即处理</span>
              </div>
              <!-- 无高优任务 -->
              <div v-if="urgentSummary.summary.length === 0" class="px-5 py-6 text-center text-slate-400 text-xs">
                <iconify-icon icon="lucide:check-circle-2" width="24" class="mb-2 opacity-40"></iconify-icon>
                <p>今日暂无高优任务，继续保持！</p>
              </div>
              <!-- 按分类聚合展示 -->
              <div v-else class="divide-y divide-slate-100">
                <div
                  v-for="(item, idx) in urgentSummary.summary"
                  :key="item.task_type"
                  class="px-5 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors"
                >
                  <div class="flex items-center gap-3">
                    <!-- 今日有具体时刻截止 → 红色脉冲；今日无时刻 → 橙色；未来日期 → 灰色 -->
                    <div
                      :class="urgencyDot(item.earliest_due)"
                      class="w-2 h-2 rounded-full shrink-0 animate-pulse"
                    ></div>
                    <div>
                      <p class="text-sm font-bold text-slate-900">
                        今日有 <span :class="urgencyTextColor(item.earliest_due)">{{ item.count }}</span> 个{{ item.task_type }}高优任务
                      </p>
                      <p class="text-xs text-slate-500 mt-0.5">
                        最早截止：<span :class="urgencyTextColor(item.earliest_due)" class="font-semibold">{{ item.earliest_due }}</span>
                      </p>
                    </div>
                  </div>
                  <button
                    @click="activeTab = 'tasks'"
                    :class="urgencyBtn(item.earliest_due)"
                    class="px-4 py-1.5 text-xs font-bold rounded-lg shadow-sm transition-all shrink-0 text-white"
                  >去处理</button>
                </div>
              </div>
            </div>

            <!-- 当日待办任务 (手风琴) -->
            <div class="space-y-2">
              <h3 class="text-sm font-bold text-slate-800 px-1">当日待办任务</h3>

              <!-- 建联任务 -->
              <div class="shadcn-card overflow-hidden">
                <button class="w-full px-5 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors" @click="toggleAccordion('contact')">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-blue-50 text-blue-600 rounded-lg flex items-center justify-center shrink-0">
                      <iconify-icon icon="lucide:phone-call" width="16"></iconify-icon>
                    </div>
                    <div class="text-left">
                      <p class="text-sm font-bold text-slate-900">建联任务</p>
                      <p class="text-[10px] text-slate-400">
                        {{ taskGroups.contact.pending }}项待处理
                        <template v-if="taskGroups.contact.subTypes.length"> · {{ taskGroups.contact.subTypes.join('、') }}</template>
                      </p>
                    </div>
                  </div>
                  <div class="flex items-center gap-3">
                    <span class="px-2 py-0.5 bg-blue-100 text-blue-600 text-[10px] rounded-full font-bold">待处理</span>
                    <iconify-icon icon="lucide:chevron-down" width="16" class="text-slate-400 transition-transform duration-200" :class="accordion.contact ? 'rotate-180' : ''"></iconify-icon>
                  </div>
                </button>
                <div v-show="accordion.contact" class="border-t border-slate-100 bg-slate-50/30">
                  <div class="p-4 space-y-3">
                    <div
                      v-for="t in taskGroups.contact.preview"
                      :key="t.id"
                      class="flex items-center justify-between p-3 bg-white border border-slate-200 rounded-lg shadow-sm"
                    >
                      <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center shrink-0">
                          <iconify-icon icon="lucide:user" width="14" class="text-blue-500"></iconify-icon>
                        </div>
                        <div>
                          <p class="text-xs font-bold text-slate-900 flex items-center gap-1.5 flex-wrap">
                            {{ t.task_name }}<template v-if="t.cust_name"> · {{ t.cust_name }}</template>
                            <span :class="priorityClass(t.priority)" class="px-1.5 py-0.5 text-[9px] rounded font-bold">{{ t.priority }}优</span>
                          </p>
                          <p class="text-[10px] text-slate-500">{{ t.task_sub_type }} · 截止 {{ t.due_date }}</p>
                        </div>
                      </div>
                      <button class="text-[10px] font-bold text-blue-600 hover:underline shrink-0">立即执行</button>
                    </div>
                    <button v-if="taskGroups.contact.pending > taskGroups.contact.preview.length" class="w-full py-2 text-[10px] text-slate-500 hover:text-blue-600 border border-dashed border-slate-200 rounded-lg transition-colors">
                      查看全部 {{ taskGroups.contact.pending }} 项建联任务
                    </button>
                  </div>
                </div>
              </div>

              <!-- 周期任务 -->
              <div class="shadcn-card overflow-hidden">
                <button class="w-full px-5 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors" @click="toggleAccordion('cycle')">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-purple-50 text-purple-600 rounded-lg flex items-center justify-center shrink-0">
                      <iconify-icon icon="lucide:refresh-cw" width="16"></iconify-icon>
                    </div>
                    <div class="text-left">
                      <p class="text-sm font-bold text-slate-900">周期任务</p>
                      <p class="text-[10px] text-slate-400">
                        {{ taskGroups.cycle.pending }}项待处理
                        <template v-if="taskGroups.cycle.subTypes.length"> · {{ taskGroups.cycle.subTypes.join('、') }}</template>
                      </p>
                    </div>
                  </div>
                  <div class="flex items-center gap-3">
                    <span class="px-2 py-0.5 bg-slate-100 text-slate-500 text-[10px] rounded-full font-bold">待处理</span>
                    <iconify-icon icon="lucide:chevron-down" width="16" class="text-slate-400 transition-transform duration-200" :class="accordion.cycle ? 'rotate-180' : ''"></iconify-icon>
                  </div>
                </button>
                <div v-show="accordion.cycle" class="border-t border-slate-100 bg-slate-50/30">
                  <div class="p-4 space-y-3">
                    <div
                      v-for="t in taskGroups.cycle.preview"
                      :key="t.id"
                      class="flex items-center justify-between p-3 bg-white border border-slate-200 rounded-lg shadow-sm"
                    >
                      <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-purple-50 flex items-center justify-center shrink-0">
                          <iconify-icon icon="lucide:refresh-cw" width="14" class="text-purple-500"></iconify-icon>
                        </div>
                        <div>
                          <p class="text-xs font-bold text-slate-900 flex items-center gap-1.5 flex-wrap">
                            {{ t.task_name }}<template v-if="t.cust_name"> · {{ t.cust_name }}</template>
                            <span :class="priorityClass(t.priority)" class="px-1.5 py-0.5 text-[9px] rounded font-bold">{{ t.priority }}优</span>
                          </p>
                          <p class="text-[10px] text-slate-500">{{ t.task_sub_type }} · 截止 {{ t.due_date }}</p>
                        </div>
                      </div>
                      <button class="text-[10px] font-bold text-purple-600 hover:underline shrink-0">立即执行</button>
                    </div>
                    <button v-if="taskGroups.cycle.pending > taskGroups.cycle.preview.length" class="w-full py-2 text-[10px] text-slate-500 hover:text-purple-600 border border-dashed border-slate-200 rounded-lg transition-colors">
                      查看全部 {{ taskGroups.cycle.pending }} 项周期任务
                    </button>
                  </div>
                </div>
              </div>
              <!-- 跟进任务 -->
              <div class="shadcn-card overflow-hidden">
                <button class="w-full px-5 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors" @click="toggleAccordion('follow')">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-emerald-50 text-emerald-600 rounded-lg flex items-center justify-center shrink-0">
                      <iconify-icon icon="lucide:user-check" width="16"></iconify-icon>
                    </div>
                    <div class="text-left">
                      <p class="text-sm font-bold text-slate-900">跟进任务</p>
                      <p class="text-[10px] text-slate-400">
                        {{ taskGroups.follow.pending }}项待处理
                        <template v-if="taskGroups.follow.subTypes.length"> · {{ taskGroups.follow.subTypes.join('、') }}</template>
                      </p>
                    </div>
                  </div>
                  <div class="flex items-center gap-3">
                    <span class="px-2 py-0.5 bg-emerald-100 text-emerald-600 text-[10px] rounded-full font-bold">待处理</span>
                    <iconify-icon icon="lucide:chevron-down" width="16" class="text-slate-400 transition-transform duration-200" :class="accordion.follow ? 'rotate-180' : ''"></iconify-icon>
                  </div>
                </button>
                <div v-show="accordion.follow" class="border-t border-slate-100 bg-slate-50/30">
                  <div class="p-4 space-y-3">
                    <div
                      v-for="t in taskGroups.follow.preview"
                      :key="t.id"
                      class="flex items-center justify-between p-3 bg-white border border-slate-200 rounded-lg shadow-sm"
                    >
                      <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-emerald-50 flex items-center justify-center shrink-0">
                          <iconify-icon icon="lucide:user-check" width="14" class="text-emerald-500"></iconify-icon>
                        </div>
                        <div>
                          <p class="text-xs font-bold text-slate-900 flex items-center gap-1.5 flex-wrap">
                            {{ t.task_name }}<template v-if="t.cust_name"> · {{ t.cust_name }}</template>
                            <span :class="priorityClass(t.priority)" class="px-1.5 py-0.5 text-[9px] rounded font-bold">{{ t.priority }}优</span>
                          </p>
                          <p class="text-[10px] text-slate-500">{{ t.task_sub_type }} · 截止 {{ t.due_date }}</p>
                        </div>
                      </div>
                      <button class="text-[10px] font-bold text-emerald-600 hover:underline shrink-0">立即执行</button>
                    </div>
                    <button v-if="taskGroups.follow.pending > taskGroups.follow.preview.length" class="w-full py-2 text-[10px] text-slate-500 hover:text-emerald-600 border border-dashed border-slate-200 rounded-lg transition-colors">
                      查看全部 {{ taskGroups.follow.pending }} 项跟进任务
                    </button>
                  </div>
                </div>
              </div>

              <!-- 营销活动任务 -->
              <div class="shadcn-card overflow-hidden">
                <button class="w-full px-5 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors" @click="toggleAccordion('marketing')">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-orange-50 text-orange-500 rounded-lg flex items-center justify-center shrink-0">
                      <iconify-icon icon="lucide:megaphone" width="16"></iconify-icon>
                    </div>
                    <div class="text-left">
                      <p class="text-sm font-bold text-slate-900">营销活动任务</p>
                      <p class="text-[10px] text-slate-400">
                        {{ taskGroups.marketing.pending }}项待处理
                        <template v-if="taskGroups.marketing.subTypes.length"> · {{ taskGroups.marketing.subTypes.join('、') }}</template>
                      </p>
                    </div>
                  </div>
                  <div class="flex items-center gap-3">
                    <span class="px-2 py-0.5 bg-orange-100 text-orange-500 text-[10px] rounded-full font-bold">待处理</span>
                    <iconify-icon icon="lucide:chevron-down" width="16" class="text-slate-400 transition-transform duration-200" :class="accordion.marketing ? 'rotate-180' : ''"></iconify-icon>
                  </div>
                </button>
                <div v-show="accordion.marketing" class="border-t border-slate-100 bg-slate-50/30">
                  <div class="p-4 space-y-3">
                    <div
                      v-for="t in taskGroups.marketing.preview"
                      :key="t.id"
                      class="flex items-center justify-between p-3 bg-white border border-slate-200 rounded-lg shadow-sm"
                    >
                      <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-orange-50 flex items-center justify-center shrink-0">
                          <iconify-icon icon="lucide:megaphone" width="14" class="text-orange-500"></iconify-icon>
                        </div>
                        <div>
                          <p class="text-xs font-bold text-slate-900 flex items-center gap-1.5 flex-wrap">
                            {{ t.task_name }}<template v-if="t.cust_name"> · {{ t.cust_name }}</template>
                            <span :class="priorityClass(t.priority)" class="px-1.5 py-0.5 text-[9px] rounded font-bold">{{ t.priority }}优</span>
                          </p>
                          <p class="text-[10px] text-slate-500">{{ t.task_sub_type }} · 截止 {{ t.due_date }}</p>
                        </div>
                      </div>
                      <button class="text-[10px] font-bold text-orange-500 hover:underline shrink-0">立即执行</button>
                    </div>
                    <button v-if="taskGroups.marketing.pending > taskGroups.marketing.preview.length" class="w-full py-2 text-[10px] text-slate-500 hover:text-orange-500 border border-dashed border-slate-200 rounded-lg transition-colors">
                      查看全部 {{ taskGroups.marketing.pending }} 项营销活动任务
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- AI 批量任务中心 -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl p-6 text-white shadow-lg relative overflow-hidden group">
              <div class="absolute -right-10 -top-10 w-40 h-40 bg-white/10 rounded-full blur-3xl group-hover:scale-150 transition-transform duration-700 pointer-events-none"></div>
              <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div class="space-y-2">
                  <div class="flex items-center gap-2">
                    <iconify-icon class="text-yellow-300" icon="lucide:sparkles" width="18"></iconify-icon>
                    <h3 class="text-base font-bold">AI 批量任务中心</h3>
                  </div>
                  <p class="text-blue-100 text-sm">
                    检测到 <span class="text-white font-bold underline decoration-yellow-300 decoration-2 underline-offset-4">{{ aiTaskStats.count }}</span> 项低优先级任务可交由 AI 代为执行
                  </p>
                  <div class="flex gap-2 flex-wrap">
                    <span class="px-2 py-0.5 bg-white/20 rounded-full text-[10px] font-bold">
                      占全部任务 {{ aiTaskStats.ratio }}%
                    </span>
                    <span class="px-2 py-0.5 bg-white/20 rounded-full text-[10px] font-bold">自动留痕</span>
                    <span class="px-2 py-0.5 bg-white/20 rounded-full text-[10px] font-bold">合规托管</span>
                  </div>
                </div>
                <button
                  @click="launchAiBatch"
                  :disabled="aiTaskStats.count === 0"
                  class="px-6 py-3 bg-white text-blue-600 font-bold rounded-xl shadow-xl hover:bg-blue-50 transition-all flex items-center gap-2 whitespace-nowrap shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  一键发起处理
                  <iconify-icon icon="lucide:arrow-right" width="16"></iconify-icon>
                </button>
              </div>
            </div>
          </div>

          <!-- 右侧 1/3: 每日提醒 + 合规任务 -->
          <div class="space-y-4">
            <!-- 每日提醒卡片 -->
            <div class="shadcn-card flex flex-col">
              <div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
                <h3 class="font-bold text-slate-900 flex items-center gap-2">
                  <iconify-icon class="text-blue-600" icon="lucide:bell-ring" width="16"></iconify-icon>
                  每日提醒
                </h3>
                <span class="text-[10px] text-slate-400">{{ alerts.length }} 条未完成</span>
              </div>
              <div class="p-3 space-y-2 overflow-y-auto no-scrollbar" style="max-height: 260px;">
                <div v-if="alerts.length === 0" class="text-center text-slate-400 text-xs py-6">暂无提醒</div>
                <div
                  v-for="a in alerts"
                  :key="a.id"
                  class="p-3 bg-blue-50/50 border border-blue-100 rounded-xl hover:bg-blue-50 transition-colors group"
                >
                  <div class="flex items-start gap-2">
                    <div class="w-1.5 h-1.5 rounded-full bg-blue-500 shrink-0 mt-1.5"></div>
                    <p class="flex-1 text-xs text-slate-700 leading-relaxed">{{ a.content }}</p>
                    <button
                      @click="markAlertDone(a.id)"
                      class="shrink-0 text-[10px] text-slate-400 hover:text-green-600 font-bold opacity-0 group-hover:opacity-100 transition-opacity"
                    >完成</button>
                  </div>
                </div>
              </div>
              <div class="p-3 border-t border-slate-100">
                <div class="flex gap-2">
                  <input
                    v-model="newAlertContent"
                    @keyup.enter="addAlert"
                    type="text"
                    placeholder="添加提醒…"
                    class="flex-1 px-3 py-2 text-xs bg-slate-100 border-0 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <button @click="addAlert" class="px-3 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg hover:bg-blue-700 transition-colors">添加</button>
                </div>
              </div>
            </div>

            <!-- 合规任务卡片 -->
            <div class="shadcn-card overflow-hidden">
              <div class="px-5 py-3 bg-amber-50 border-b border-amber-100 flex items-center justify-between">
                <h3 class="text-xs font-bold text-amber-700 flex items-center gap-2">
                  <iconify-icon icon="lucide:shield-check" width="14"></iconify-icon>
                  合规任务
                  <span v-if="taskGroups.compliance.pending > 0">({{ taskGroups.compliance.pending }}项)</span>
                </h3>
                <span class="text-[10px] text-amber-600 font-medium">待完成</span>
              </div>
              <div class="divide-y divide-slate-100">
                <div v-if="taskGroups.compliance.preview.length === 0" class="px-5 py-4 text-xs text-slate-400 text-center">暂无合规任务</div>
                <div
                  v-for="t in taskGroups.compliance.preview"
                  :key="t.id"
                  class="px-4 py-3 hover:bg-slate-50 transition-colors"
                >
                  <div class="flex items-center gap-2 mb-0.5">
                    <span class="px-1.5 py-0.5 bg-amber-100 text-amber-600 text-[9px] rounded font-bold">{{ t.task_sub_type }}</span>
                    <span :class="priorityClass(t.priority)" class="px-1.5 py-0.5 text-[9px] rounded font-bold">{{ t.priority }}优</span>
                    <span class="text-[10px] text-slate-400">截止 {{ t.due_date }}</span>
                  </div>
                  <p class="text-xs font-medium text-slate-800 truncate">
                    {{ t.task_name }}<template v-if="t.cust_name"> · {{ t.cust_name }}</template>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab 2: 成长赋能 -->
        <div v-show="activeTab === 'growth'" class="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <!-- 左侧 2/3: 昨日AI复盘 -->
          <div class="lg:col-span-2 shadcn-card p-6 space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                <iconify-icon class="text-indigo-600" icon="lucide:history" width="18"></iconify-icon>
                昨日工作 AI 复盘
              </h3>
              <span class="text-xs text-slate-400">数据更新于 08:30</span>
            </div>
            <!-- 三项指标 -->
            <div class="grid grid-cols-3 gap-4">
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs text-slate-500 mb-1">目标完成率</p>
                <p class="text-2xl font-bold text-slate-900">78%</p>
                <div class="mt-2 flex items-center gap-1 text-[10px] text-red-500 font-bold">
                  <iconify-icon icon="lucide:trending-down" width="12"></iconify-icon>
                  低于均值 5%
                </div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs text-slate-500 mb-1">转化成功率</p>
                <p class="text-2xl font-bold text-slate-900">+12%</p>
                <div class="mt-2 flex items-center gap-1 text-[10px] text-green-500 font-bold">
                  <iconify-icon icon="lucide:trending-up" width="12"></iconify-icon>
                  环比提升
                </div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs text-slate-500 mb-1">加微成功率</p>
                <p class="text-2xl font-bold text-slate-900">42%</p>
                <div class="mt-2 flex items-center gap-1 text-[10px] text-green-500 font-bold">
                  <iconify-icon icon="lucide:award" width="12"></iconify-icon>
                  超团队均值 15%
                </div>
              </div>
            </div>
            <!-- 亮点与不足 -->
            <div class="space-y-4">
              <div class="flex gap-4">
                <div class="shrink-0 w-9 h-9 bg-green-50 text-green-600 rounded-full flex items-center justify-center">
                  <iconify-icon icon="lucide:thumbs-up" width="16"></iconify-icon>
                </div>
                <div>
                  <p class="text-sm font-bold text-slate-900">核心亮点</p>
                  <p class="text-xs text-slate-500 mt-1 leading-relaxed">加微转化率显著高于团队平均水平，沟通话术亲和力强，客户接受度高。</p>
                </div>
              </div>
              <div class="flex gap-4">
                <div class="shrink-0 w-9 h-9 bg-red-50 text-red-600 rounded-full flex items-center justify-center">
                  <iconify-icon icon="lucide:trending-down" width="16"></iconify-icon>
                </div>
                <div>
                  <p class="text-sm font-bold text-slate-900">核心不足</p>
                  <p class="text-xs text-slate-500 mt-1 leading-relaxed">外呼接通率仅 38%，主要集中在 10:00-11:30 时段，客户接听比例偏低。</p>
                </div>
              </div>
              <!-- AI 智能结论 -->
              <div class="p-4 bg-indigo-50 rounded-xl border border-indigo-100">
                <div class="flex items-start gap-3">
                  <iconify-icon class="text-indigo-600 shrink-0 mt-0.5" icon="lucide:brain-circuit" width="18"></iconify-icon>
                  <div>
                    <p class="text-sm font-bold text-indigo-900">AI 智能结论</p>
                    <p class="text-xs text-indigo-700 mt-1 leading-relaxed">
                      建议优化 <span class="font-bold">14:00-15:30</span> 为核心外呼时段，根据大数据分析，该时段您目标客群接通率最高，可提升约 <span class="font-bold">25%</span> 的触达效率。
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <!-- 操作按钮 -->
            <div class="flex gap-3">
              <button class="flex-1 py-2.5 bg-white border border-slate-200 text-slate-700 text-sm font-bold rounded-xl hover:bg-slate-50 transition-all flex items-center justify-center gap-2">
                <iconify-icon icon="lucide:file-text" width="16"></iconify-icon>
                生成详细报告
              </button>
              <button class="flex-1 py-2.5 bg-blue-600 text-white text-sm font-bold rounded-xl hover:bg-blue-700 shadow-md transition-all flex items-center justify-center gap-2">
                <iconify-icon icon="lucide:message-square" width="16"></iconify-icon>
                AI 答疑
              </button>
            </div>
          </div>

          <!-- 右侧 1/3 -->
          <div class="space-y-4">
            <!-- 月度成长规划 -->
            <div class="shadcn-card p-5 space-y-4">
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-bold text-slate-900">5月 AI 成长规划</h3>
                <button class="text-xs text-blue-600 font-bold hover:underline">调整规划</button>
              </div>
              <div>
                <div class="flex justify-between text-xs mb-2">
                  <span class="text-slate-500">当前进度</span>
                  <span class="font-bold text-indigo-600">45%</span>
                </div>
                <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div class="h-full bg-indigo-500 rounded-full" style="width: 45%"></div>
                </div>
              </div>
              <div class="space-y-3 pt-2">
                <div class="p-3 bg-indigo-50/60 border border-indigo-100 rounded-xl relative">
                  <div class="absolute -left-1 top-3 w-2 h-6 bg-indigo-500 rounded-full"></div>
                  <p class="text-[10px] text-indigo-500 font-bold uppercase mb-1">本周重点 (W2)</p>
                  <p class="text-xs font-bold text-slate-900">强化高净值客户跟进技巧</p>
                </div>
                <div class="p-4 border border-slate-200 rounded-xl space-y-3">
                  <p class="text-xs font-bold text-slate-700">当日成长作业</p>
                  <div class="flex items-center justify-between">
                    <p class="text-xs text-slate-500">学习异议处理话术</p>
                    <button class="px-3 py-1 bg-blue-600 text-white text-[10px] font-bold rounded-lg hover:bg-blue-700 transition-all">去学习</button>
                  </div>
                  <div class="pt-2 border-t border-slate-100 flex items-center gap-2">
                    <iconify-icon class="text-red-500" icon="lucide:circle-x" width="14"></iconify-icon>
                    <span class="text-[10px] text-red-500 font-bold">昨日：客户结案分析 (未完成)</span>
                  </div>
                </div>
              </div>
            </div>
            <!-- 今日精炼建议 -->
            <div class="shadcn-card p-5 bg-gradient-to-br from-slate-900 to-slate-800 text-white">
              <div class="flex items-center gap-2 mb-3">
                <iconify-icon class="text-yellow-400" icon="lucide:sparkles" width="16"></iconify-icon>
                <h3 class="text-sm font-bold">今日精炼建议</h3>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed mb-4">
                今日重点攻关：<span class="text-white font-bold">高净值客户触达话术</span>。昨日 3 位 AUM &gt; 100万客户触达未应答，建议参考「资产配置深度沟通」素材库。
              </p>
              <button class="w-full py-2 bg-white/10 hover:bg-white/20 text-white text-xs font-bold rounded-lg transition-all border border-white/20">
                立即跳转学习
              </button>
            </div>
            <!-- 快捷操作 -->
            <div class="shadcn-card p-5">
              <h3 class="font-bold text-slate-900 mb-4 text-sm">快捷操作</h3>
              <div class="grid grid-cols-3 gap-3">
                <button class="flex flex-col items-center gap-2 group">
                  <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center group-hover:bg-blue-600 group-hover:text-white transition-all">
                    <iconify-icon icon="lucide:phone-call" width="20"></iconify-icon>
                  </div>
                  <span class="text-[10px] font-medium text-slate-600">一键外呼</span>
                </button>
                <button class="flex flex-col items-center gap-2 group">
                  <div class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center group-hover:bg-emerald-600 group-hover:text-white transition-all">
                    <iconify-icon icon="lucide:search" width="20"></iconify-icon>
                  </div>
                  <span class="text-[10px] font-medium text-slate-600">客户查询</span>
                </button>
                <button class="flex flex-col items-center gap-2 group">
                  <div class="w-12 h-12 bg-orange-50 text-orange-600 rounded-2xl flex items-center justify-center group-hover:bg-orange-600 group-hover:text-white transition-all">
                    <iconify-icon icon="lucide:files" width="20"></iconify-icon>
                  </div>
                  <span class="text-[10px] font-medium text-slate-600">素材调用</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 底部合规区 -->
      <footer class="pt-6 pb-8 border-t border-slate-200 mt-2">
        <div class="flex flex-col md:flex-row justify-between gap-6">
          <div class="space-y-2 max-w-md">
            <div class="flex items-center gap-2 text-amber-600">
              <iconify-icon icon="lucide:shield-check" width="14"></iconify-icon>
              <span class="text-xs font-bold">合规安全提示</span>
            </div>
            <p class="text-[11px] text-slate-400 leading-relaxed">
              请严格遵守《2026版展业风险管理办法》，所有外呼话术须经系统合规校验，禁止承诺保本保收益。
            </p>
          </div>
          <div class="flex gap-8">
            <div>
              <p class="text-xs font-bold text-slate-700 mb-2">最新系统公告</p>
              <ul class="space-y-1.5">
                <li class="text-[10px] text-slate-500 hover:text-blue-600 cursor-pointer flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 bg-blue-500 rounded-full shrink-0"></span>
                  关于五月产品费率调整的通知
                </li>
                <li class="text-[10px] text-slate-500 hover:text-blue-600 cursor-pointer flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 bg-slate-300 rounded-full shrink-0"></span>
                  AI辅助外呼 2.0 功能上线培训
                </li>
                <li class="text-[10px] text-slate-500 hover:text-blue-600 cursor-pointer flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 bg-slate-300 rounded-full shrink-0"></span>
                  季度成长培训计划公布
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="mt-6 flex justify-between items-center text-[10px] text-slate-400">
          <p>© 2026 AI展业平台 · 数字化营业中心</p>
          <div class="flex gap-4">
            <a class="hover:text-slate-600" href="#">服务条款</a>
            <a class="hover:text-slate-600" href="#">隐私政策</a>
            <a class="hover:text-slate-600" href="#">技术支持: 400-888-9999</a>
          </div>
        </div>
      </footer>

    </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const LOGIN_ID = 'oa001'
const API_BASE = import.meta.env.VITE_API_BASE ?? ''

let taskChart = null

const activeTab    = ref('tasks')
const router       = useRouter()

// AI 批量任务：统计低优先级未完成任务
const aiTaskStats = computed(() => {
  const all   = allTasks.value.filter(t => ['待处理', '处理中'].includes(t.status))
  const lowPri = all.filter(t => t.priority === '低')
  const total  = all.length
  const ratio  = total > 0 ? Math.round(lowPri.length / total * 100) : 0
  return { count: lowPri.length, total, ratio }
})

function launchAiBatch() {
  router.push({ path: '/business', query: { mode: 'ai-batch', priority: '低' } })
}
const accordion    = reactive({ contact: false, cycle: false, follow: false, marketing: false })

// ── 动态日期 ─────────────────────────────────────────────────────────────────
const todayStr = (() => {
  const d = new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}年${m}月${day}日`
})()

// ── 总览数据 ──────────────────────────────────────────────────────────────────
const overview = reactive({
  aum_card:  null,
  call_card: null,
  task_card: null,
})

async function fetchOverview() {
  try {
    const res  = await fetch(`${API_BASE}/api/staff/overview?login_id=${LOGIN_ID}`)
    const data = await res.json()
    if (data.aum_card)  overview.aum_card  = data.aum_card
    if (data.call_card) overview.call_card = data.call_card
    if (data.task_card) overview.task_card = data.task_card
    // 任务进度图表刷新
    if (taskChart && data.task_card?.done != null && data.task_card?.todo != null) {
      const done = data.task_card.done
      const todo = data.task_card.todo + data.task_card.overdue
      taskChart.setOption({
        series: [{ data: [
          { value: done, itemStyle: { color: '#8b5cf6' } },
          { value: todo, itemStyle: { color: '#f1f5f9' } },
        ] }],
      })
    }
  } catch (e) {
    console.warn('[overview] fetch failed:', e)
  }
}

// ── 每日提醒 ──────────────────────────────────────────────────────────────────
const alertPanelOpen   = ref(false)
const alerts           = ref([])
const newAlertContent  = ref('')
const unreadAlertCount = ref(0)

function toggleAlertPanel() {
  alertPanelOpen.value = !alertPanelOpen.value
}

async function fetchAlerts() {
  try {
    const res  = await fetch(`${API_BASE}/api/manager/alerts?login_id=${LOGIN_ID}`)
    const data = await res.json()
    alerts.value = (data.alerts || []).map(a => ({ id: a.id, content: a.content }))
    unreadAlertCount.value = alerts.value.length
  } catch (e) {
    console.warn('[alerts] fetch failed:', e)
  }
}

async function markAlertDone(id) {
  try {
    await fetch(`${API_BASE}/api/manager/alerts/${id}/done`, { method: 'PATCH' })
    alerts.value = alerts.value.filter(a => a.id !== id)
    unreadAlertCount.value = alerts.value.length
  } catch (e) {
    console.warn('[alerts] mark done failed:', e)
  }
}

async function addAlert() {
  const content = newAlertContent.value.trim()
  if (!content) return
  try {
    const res  = await fetch(`${API_BASE}/api/manager/alerts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ login_id: LOGIN_ID, content }),
    })
    const data = await res.json()
    alerts.value.unshift({ id: data.id, content })
    unreadAlertCount.value = alerts.value.length
    newAlertContent.value = ''
  } catch (e) {
    console.warn('[alerts] add failed:', e)
  }
}

function _onClickOutsideAlert(e) {
  if (!e.target.closest('.alert-panel-wrapper')) {
    alertPanelOpen.value = false
  }
}

// ── 静态数据 ──────────────────────────────────────────────────────────────────

const cycleTasks = [
  { tag: '引客', tagClass: 'bg-blue-100 text-blue-600',   name: '新客专属欢迎',   count: 3 },
  { tag: '养客', tagClass: 'bg-green-100 text-green-600', name: '持仓关怀跟进',   count: 5 },
  { tag: '复投', tagClass: 'bg-purple-100 text-purple-600', name: '到期客户转化', count: 2 },
  { tag: '流失', tagClass: 'bg-red-100 text-red-600',     name: '流失预警处理',   count: 1 },
]

function toggleAccordion(key) {
  accordion[key] = !accordion[key]
}

// ── 任务数据 & 分组 ───────────────────────────────────────────────────────────
const allTasks = ref([])

// 周期子类标签色
const CYCLE_CLASS_MAP = {
  '引客': 'bg-blue-100 text-blue-600',
  '养客': 'bg-green-100 text-green-600',
  '复投': 'bg-purple-100 text-purple-600',
  '流失预警': 'bg-red-100 text-red-600',
}
function cycleSubTypeClass(sub) {
  return CYCLE_CLASS_MAP[sub] ?? 'bg-slate-100 text-slate-600'
}

// 按任务类型聚合，供手风琴和合规卡片使用
const taskGroups = computed(() => {
  const pending = (type) => allTasks.value.filter(
    t => t.task_type === type && ['待处理', '处理中'].includes(t.status)
  )

  const contactTasks = pending('建联类')
  const cycleTasks_  = pending('周期类')
  const complianceTasks = pending('合规类')

  const followTasks    = pending('跟进类')
  const marketingTasks = pending('营销活动类')

  return {
    contact: {
      pending:  contactTasks.length,
      subTypes: [...new Set(contactTasks.map(t => t.task_sub_type))],
      preview:  contactTasks.slice(0, 2),
    },
    cycle: {
      pending:  cycleTasks_.length,
      subTypes: [...new Set(cycleTasks_.map(t => t.task_sub_type))],
      preview:  cycleTasks_.slice(0, 2),
    },
    follow: {
      pending:  followTasks.length,
      subTypes: [...new Set(followTasks.map(t => t.task_sub_type))],
      preview:  followTasks.slice(0, 2),
    },
    marketing: {
      pending:  marketingTasks.length,
      subTypes: [...new Set(marketingTasks.map(t => t.task_sub_type))],
      preview:  marketingTasks.slice(0, 2),
    },
    compliance: {
      pending: complianceTasks.length,
      preview: complianceTasks.slice(0, 3),
    },
  }
})

async function fetchTaskList() {
  try {
    const res  = await fetch(`${API_BASE}/api/staff/tasks?login_id=${LOGIN_ID}&page_size=100`)
    const data = await res.json()
    allTasks.value = data.tasks || []
    // 同步任务进度到圆环图
    const done    = (data.tasks || []).filter(t => t.status === '已完成').length
    const pending = (data.tasks || []).filter(t => ['待处理', '处理中'].includes(t.status)).length
    if (taskChart && (done + pending) > 0) {
      taskChart.setOption({
        series: [{ data: [
          { value: done,    itemStyle: { color: '#8b5cf6' } },
          { value: pending, itemStyle: { color: '#f1f5f9' } },
        ] }],
      })
      // 同步更新 task_card 完成率
      const total = done + pending + (data.tasks || []).filter(t => t.status === '已逾期').length
      if (total > 0 && !overview.task_card) {
        overview.task_card = {
          todo:    pending,
          done:    done,
          overdue: (data.tasks || []).filter(t => t.status === '已逾期').length,
          rate:    Math.round(done / total * 100),
        }
      }
    }
  } catch (e) {
    console.warn('[tasks] list fetch failed:', e)
  }
}

// ── 高优任务紧急程度样式 ──────────────────────────────────────────────────────
// HH:MM → 今日有具体时刻，最紧急（红）
// '今日' → 今日无时刻，次紧急（橙）
// YYYY-MM-DD → 未来日期，不紧急（灰）
function _urgencyLevel(due) {
  if (due && due.length === 5 && due.includes(':')) return 'time'   // HH:MM
  if (due === '今日') return 'today'
  return 'future'
}
// 优先级标签样式
function priorityClass(p) {
  if (p === '高') return 'bg-red-100 text-red-600'
  if (p === '中') return 'bg-amber-100 text-amber-600'
  return 'bg-slate-100 text-slate-500'
}

function urgencyDot(due) {
  const l = _urgencyLevel(due)
  return l === 'time' ? 'bg-red-500' : l === 'today' ? 'bg-orange-400' : 'bg-slate-300'
}
function urgencyTextColor(due) {
  const l = _urgencyLevel(due)
  return l === 'time' ? 'text-red-600' : l === 'today' ? 'text-orange-500' : 'text-slate-500'
}
function urgencyBtn(due) {
  const l = _urgencyLevel(due)
  return l === 'time' ? 'bg-red-600 hover:bg-red-700' : l === 'today' ? 'bg-orange-500 hover:bg-orange-600' : 'bg-slate-700 hover:bg-slate-800'
}

// ── 高优任务聚合 ──────────────────────────────────────────────────────────────
const urgentSummary = reactive({ total: 0, summary: [] })

async function fetchUrgentSummary() {
  try {
    const res  = await fetch(`${API_BASE}/api/staff/tasks/urgent-summary?login_id=${LOGIN_ID}`)
    const data = await res.json()
    urgentSummary.total   = data.total   ?? 0
    urgentSummary.summary = data.summary ?? []
  } catch (e) {
    console.warn('[tasks] urgent-summary fetch failed:', e)
  }
}

// ── 每日资讯 ──────────────────────────────────────────────────────────────────
const todayNews      = ref([])
const newsModalOpen  = ref(false)
const newsList       = ref([])
const newsTotal      = ref(0)
const newsPage       = ref(1)
const newsPageSize   = 20
const newsCategories = ref([])
const newsFilter     = reactive({ title: '', category: '', month: '' })

// 分类色映射
const CAT_CLASS_MAP = {
  '市场': 'bg-blue-100 text-blue-600',
  '政策': 'bg-orange-100 text-orange-600',
  '产品': 'bg-green-100 text-green-600',
  '宏观': 'bg-purple-100 text-purple-600',
  '公司': 'bg-slate-100 text-slate-600',
}
function categoryClass(cat) {
  return CAT_CLASS_MAP[cat] ?? 'bg-slate-100 text-slate-600'
}

async function fetchTodayNews() {
  try {
    const res  = await fetch(`${API_BASE}/api/staff/news/today`)
    const data = await res.json()
    todayNews.value = data.news || []
  } catch (e) {
    console.warn('[news] today fetch failed:', e)
  }
}

async function fetchNewsList(page = 1) {
  newsPage.value = page
  const params = new URLSearchParams({ page, page_size: newsPageSize })
  if (newsFilter.title)    params.set('title',    newsFilter.title)
  if (newsFilter.category) params.set('category', newsFilter.category)
  if (newsFilter.month)    params.set('month',    newsFilter.month)
  try {
    const res  = await fetch(`${API_BASE}/api/staff/news?${params}`)
    const data = await res.json()
    newsList.value       = data.news || []
    newsTotal.value      = data.total || 0
    newsCategories.value = data.categories || []
  } catch (e) {
    console.warn('[news] list fetch failed:', e)
  }
}

// 防抖搜索（标题输入）
let _newsDebounce = null
function debouncedFetchNews() {
  clearTimeout(_newsDebounce)
  _newsDebounce = setTimeout(() => fetchNewsList(1), 350)
}

function openNewsModal() {
  newsModalOpen.value = true
  fetchNewsList(1)
}
function closeNewsModal() {
  newsModalOpen.value = false
}
function resetNewsFilter() {
  newsFilter.title    = ''
  newsFilter.category = ''
  newsFilter.month    = ''
  fetchNewsList(1)
}

function copyNews(title) {
  navigator.clipboard?.writeText(title).catch(() => {})
}
function openLink(url) {
  window.open(url, '_blank', 'noopener')
}

// ── 生命周期 ──────────────────────────────────────────────────────────────────
onMounted(() => {
  const sidebar          = document.getElementById('sidebar')
  const toggleSidebarBtn = document.getElementById('toggleSidebar')
  toggleSidebarBtn?.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed')
  })

  const taskChartDom = document.getElementById('taskProgressChart')
  if (taskChartDom) {
    taskChart = echarts.init(taskChartDom)
    taskChart.setOption({
      series: [{
        type: 'pie',
        radius: ['70%', '90%'],
        label: { show: false },
        data: [
          { value: 0, itemStyle: { color: '#8b5cf6' } },
          { value: 1, itemStyle: { color: '#f1f5f9' } },
        ],
      }],
    })
  }

  window.addEventListener('resize', () => taskChart?.resize())

  fetchOverview()
  fetchAlerts()
  fetchTodayNews()
  fetchUrgentSummary()
  fetchTaskList()
  document.addEventListener('click', _onClickOutsideAlert)
})

onUnmounted(() => {
  taskChart?.dispose()
  window.removeEventListener('resize', () => {})
  document.removeEventListener('click', _onClickOutsideAlert)
})
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');

  :root {
    --primary: #2563eb;
    --sidebar-width: 256px;
    --sidebar-collapsed-width: 80px;
  }

  body {
    font-family: 'Inter', 'Noto Sans SC', sans-serif;
    background-color: #f8fafc;
    color: #1e293b;
  }

  .no-scrollbar::-webkit-scrollbar { display: none; }
  .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

  .shadcn-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    transition: all 0.2s;
  }
  .shadcn-card:hover {
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.06);
  }

  #sidebar { width: var(--sidebar-width); transition: width 0.3s; }
  #sidebar.collapsed { width: var(--sidebar-collapsed-width); }
  #sidebar.collapsed .nav-text,
  #sidebar.collapsed .logo-text,
  #sidebar.collapsed .user-info-text { display: none; }
  #sidebar.collapsed .nav-item { justify-content: center; padding-left: 0; padding-right: 0; }
  #sidebar.collapsed .nav-item iconify-icon { margin-right: 0; }

  .ai-badge {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    color: white;
  }

  /* 弹窗过渡 */
  .modal-fade-enter-active,
  .modal-fade-leave-active { transition: opacity 0.2s ease; }
  .modal-fade-enter-from,
  .modal-fade-leave-to { opacity: 0; }
</style>
