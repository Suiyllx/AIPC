<template>
    <div class="business-hall">
        <!-- 侧边导航 (与展业大厅完全一致) -->
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
                        <p class="text-xs text-slate-500 truncate">最后登录: {{ todayStr }}</p>
                    </div>
                </div>
            </div>
        </aside>

        <!-- 主体内容 -->
        <main class="flex-1 flex flex-col min-w-0 bg-[#F8FAFC]">
            <!-- 顶部导航栏 (与展业大厅完全一致) -->
            <header class="h-16 bg-white backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-6 shrink-0 sticky top-0 z-40">
                <div class="flex items-center gap-4">
                    <button class="p-2 hover:bg-slate-100 rounded-lg transition-colors" @click="toggleSidebar">
                        <iconify-icon class="text-xl text-slate-600" icon="lucide:menu"></iconify-icon>
                    </button>
                    <div class="h-6 w-px bg-slate-200"></div>
                    <span class="text-sm font-medium text-slate-500">今天是 {{ todayStr }}</span>
                </div>
                <div class="flex items-center gap-3">
                    <div class="flex items-center gap-1 bg-slate-100 rounded-lg p-1 text-xs font-medium">
                        <span class="px-2.5 py-1 bg-white text-slate-900 rounded-md shadow-sm">营销人员</span>
                        <router-link class="px-2.5 py-1 text-slate-500 hover:text-slate-700 rounded-md transition-all" to="/manager">管理人员</router-link>
                    </div>
                    <!-- 每日提醒铃铛 -->
                    <div class="relative alert-panel-wrapper">
                        <button @click="toggleAlertPanel"
                                class="p-2 hover:bg-slate-100 rounded-lg relative transition-colors">
                            <iconify-icon class="text-xl text-slate-600" icon="lucide:bell"></iconify-icon>
                            <span v-if="unreadAlertCount > 0"
                                  class="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
                        </button>
                        <div v-if="alertPanelOpen"
                             class="absolute right-0 top-12 w-96 bg-white border border-gray-200 rounded-xl shadow-2xl z-50 flex flex-col"
                             style="max-height: 520px;">
                            <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
                                <span class="text-sm font-semibold text-gray-800">每日提醒</span>
                                <span class="text-xs text-gray-400">近30天未完成（{{ unreadAlertCount }} 条）</span>
                            </div>
                            <div class="flex-1 overflow-y-auto divide-y divide-gray-100">
                                <div v-if="alerts.length === 0" class="py-10 text-center text-gray-400 text-sm">暂无未完成提醒</div>
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
                            <div class="px-4 py-3 border-t border-gray-100">
                                <div class="flex gap-2">
                                    <input v-model="newAlertContent" @keydown.enter="addAlert"
                                           placeholder="新增提醒…"
                                           class="flex-1 bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-lg px-3 py-2 outline-none placeholder-gray-400 focus:ring-1 focus:ring-blue-500" />
                                    <button @click="addAlert" :disabled="!newAlertContent.trim()"
                                            class="px-3 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white text-sm rounded-lg transition-colors">添加</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <div class="flex-1 overflow-y-auto">
      <div class="p-8 space-y-6">
        <!-- AI 任务执行状态条 -->
        <div
          v-if="aiLogStats.running > 0 || aiLogStats.doneToday > 0"
          class="flex items-center gap-4 bg-blue-50 border border-blue-100 rounded-2xl px-5 py-3 cursor-pointer hover:bg-blue-100 transition-colors"
          @click="toggleProgressModal"
        >
          <!-- 执行中 -->
          <template v-if="aiLogStats.running > 0">
            <span class="relative flex h-2.5 w-2.5 shrink-0">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-600"></span>
            </span>
            <span class="text-blue-700 text-sm font-medium">
              AI 正在执行 <span class="font-bold">{{ aiLogStats.running }}</span> 个任务
            </span>
            <span class="text-blue-300 text-sm">|</span>
          </template>
          <!-- 今日已完成 -->
          <template v-if="aiLogStats.doneToday > 0">
            <iconify-icon icon="lucide:check-circle-2" width="15" class="text-emerald-500 shrink-0"></iconify-icon>
            <span class="text-slate-600 text-sm">
              今日已完成 <span class="font-bold text-emerald-600">{{ aiLogStats.doneToday }}</span> 个 AI 任务
            </span>
          </template>
          <!-- 失败提醒 -->
          <template v-if="aiLogStats.failedToday > 0">
            <span class="text-blue-300 text-sm">|</span>
            <iconify-icon icon="lucide:alert-circle" width="15" class="text-red-400 shrink-0"></iconify-icon>
            <span class="text-red-500 text-sm font-medium">{{ aiLogStats.failedToday }} 个失败</span>
          </template>
          <span class="ml-auto text-xs text-blue-500 font-medium flex items-center gap-1 shrink-0">
            点击查看详情 <iconify-icon icon="lucide:chevron-right" width="13"></iconify-icon>
          </span>
        </div>
        <!-- 1. 顶部数据概览 -->
        <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <!-- 今日待办 -->
          <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
            <p class="text-xs font-medium text-gray-500 mb-1">今日待办任务</p>
            <div class="flex items-end justify-between">
              <h3 class="text-2xl font-bold text-gray-900">{{ todoCount }}</h3>
              <span class="text-xs text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">
                {{ doneRate }}% 完成
              </span>
            </div>
          </div>
          <!-- 今日已完成 -->
          <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
            <p class="text-xs font-medium text-gray-500 mb-1">今日已完成</p>
            <div class="flex items-end justify-between">
              <h3 class="text-2xl font-bold text-gray-900">{{ doneCount }}</h3>
              <div class="w-12 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div class="bg-green-500 h-full transition-all duration-500" :style="{ width: doneRate + '%' }"></div>
              </div>
            </div>
          </div>
          <!-- AI代劳完成 -->
          <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
            <p class="text-xs font-medium text-gray-500 mb-1">AI代劳完成</p>
            <div class="flex items-end justify-between">
              <h3 class="text-2xl font-bold text-purple-600">{{ aiLogStats.doneToday }}</h3>
              <iconify-icon class="text-purple-200 text-xl" icon="solar:magic-stick-3-bold"></iconify-icon>
            </div>
          </div>
          <!-- 外呼接通数 -->
          <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
            <p class="text-xs font-medium text-gray-500 mb-1">外呼接通数</p>
            <div class="flex items-end justify-between">
              <h3 class="text-2xl font-bold text-gray-900">{{ connected }}</h3>
              <span class="text-[10px] text-gray-400">接通率 {{ connectRate }}%</span>
            </div>
          </div>
          <!-- 今日逾期任务 -->
          <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm"
               :class="overdueCount > 0 ? 'border-red-100' : ''">
            <p class="text-xs font-medium text-gray-500 mb-1">今日逾期任务</p>
            <div class="flex items-end justify-between">
              <h3 class="text-2xl font-bold" :class="overdueCount > 0 ? 'text-red-500' : 'text-gray-900'">
                {{ overdueCount }}
              </h3>
              <iconify-icon
                :icon="overdueCount > 0 ? 'lucide:alarm-clock' : 'lucide:check-circle-2'"
                width="18"
                :class="overdueCount > 0 ? 'text-red-300' : 'text-slate-200'"
              ></iconify-icon>
            </div>
          </div>
          <!-- 高优未处理 -->
          <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm"
               :class="highPriCount > 0 ? 'border-orange-100' : ''">
            <p class="text-xs font-medium text-gray-500 mb-1">高优未处理</p>
            <div class="flex items-end justify-between">
              <h3 class="text-2xl font-bold" :class="highPriCount > 0 ? 'text-orange-500' : 'text-gray-900'">
                {{ highPriCount }}
              </h3>
              <span class="text-[10px]" :class="highPriCount > 0 ? 'text-orange-400' : 'text-gray-300'">
                {{ highPriCount > 0 ? '需立即处理' : '全部完成' }}
              </span>
            </div>
          </div>
        </div>
        <!-- 2. 任务分类Tab -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          <div class="flex border-b border-gray-100 px-6 overflow-x-auto scrollbar-hide">
            <button v-for="tab in tabDefs" :key="tab.key"
              class="px-5 py-4 text-sm whitespace-nowrap transition-colors flex items-center gap-1.5 shrink-0 border-b-2"
              :class="activeTab === tab.key
                ? 'font-semibold text-blue-600 border-blue-600'
                : tab.key === 'ai_center'
                  ? 'font-medium text-purple-500 hover:text-purple-700 border-transparent'
                  : 'font-medium text-gray-500 hover:text-gray-700 border-transparent'"
              @click="activeTab = tab.key">
              <iconify-icon v-if="tab.key === 'ai_center'" icon="solar:bolt-bold"></iconify-icon>
              {{ tab.label }}
              <span v-if="tab.key !== 'ai_center' && tabCount(tab.key) > 0"
                class="text-[10px] font-bold px-1.5 py-0.5 rounded-full"
                :class="activeTab === tab.key ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-500'">
                {{ tabCount(tab.key) }}
              </span>
            </button>
          </div>
          <!-- 3. 筛选与搜索区域 -->
          <div class="p-6 bg-gray-50 flex flex-wrap gap-3 items-center">
            <div class="flex-1 min-w-[220px] relative">
              <iconify-icon class="search-icon text-gray-400" icon="solar:magnifer-linear"></iconify-icon>
              <input v-model="filterSearch" class="w-full pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-200" placeholder="搜索客户手机号/姓名..." type="text"/>
            </div>
            <select v-model="filterPriority" class="bg-white border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-200">
              <option value="">优先级: 全部</option>
              <option value="高">高</option>
              <option value="中">中</option>
              <option value="低">低</option>
            </select>
            <select v-model="filterContactStatus" class="bg-white border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-200">
              <option value="">建联状态: 全部</option>
              <option value="已认证">已认证</option>
              <option value="未添加或未绑定">未添加或未绑定</option>
            </select>
            <select v-model="filterSource" class="bg-white border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-200">
              <option value="">任务来源: 全部</option>
              <option value="系统触发">系统触发</option>
              <option value="模型预警">模型预警</option>
              <option value="主管分配">主管分配</option>
              <option value="手动创建">手动创建</option>
            </select>
            <div class="flex items-center gap-2">
              <label class="inline-flex items-center cursor-pointer">
                <input v-model="filterAIOnly" class="sr-only peer" type="checkbox"/>
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600 relative"></div>
                <span class="ms-3 text-sm font-medium text-gray-600">可AI代劳</span>
              </label>
            </div>
            <button @click="resetTaskFilters" class="px-4 py-2 border border-gray-200 text-gray-500 text-xs font-bold rounded-xl hover:bg-gray-50 transition-all flex items-center gap-1.5">
              <iconify-icon icon="solar:restart-bold" width="13"></iconify-icon>
              重置
            </button>
          </div>
          <!-- 4. 批量操作栏 -->
          <div class="px-6 py-3 border-b border-gray-100 bg-white flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <label class="flex items-center space-x-2 text-sm font-medium text-gray-600 bg-gray-100 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer">
                <input class="rounded text-blue-600" type="checkbox"
                  :checked="allRowsSelected"
                  :indeterminate.prop="someRowsSelected"
                  @change="toggleAllRows"/>
                <span>全选</span>
              </label>
              <div class="h-4 w-px bg-gray-200"></div>
              <button class="flex items-center space-x-1 text-sm font-bold text-purple-700 bg-purple-50 px-4 py-2 rounded-lg hover:bg-purple-100 transition-colors" @click="openBatchAI">
                <iconify-icon icon="solar:magic-stick-3-bold"></iconify-icon>
                <span>AI批量处理</span>
              </button>
              <button class="flex items-center space-x-1 text-sm font-medium text-blue-700 bg-blue-50 px-4 py-2 rounded-lg hover:bg-blue-100 transition-colors" @click="showDoubleCallWip">
                <iconify-icon icon="solar:phone-calling-bold"></iconify-icon>
                <span>批量双呼外呼</span>
              </button>
              <button class="flex items-center space-x-1 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-200 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors">
                <iconify-icon icon="solar:tag-bold"></iconify-icon>
                <span>批量标记结果</span>
              </button>
            </div>
            <div class="text-xs text-gray-400">
              已选择 <span class="font-bold text-blue-600">{{ selectedRows.length }}</span> 项任务
            </div>
          </div>
          <!-- 5. 任务列表区域 -->
          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead class="bg-gray-50 text-xs text-gray-500 uppercase font-semibold">
                <tr>
                  <th class="px-6 py-4 w-10"></th>
                  <th class="px-6 py-4">客户基本信息</th>
                  <th class="px-6 py-4">建联状态</th>
                  <th class="px-6 py-4">任务名称</th>
                  <th class="px-6 py-4">任务类型</th>
                  <th class="px-6 py-4">任务来源</th>
                  <th class="px-6 py-4">优先级</th>
                  <th class="px-6 py-4">截止时间</th>
                  <th class="px-6 py-4 text-right">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="row in filteredTaskRows" :key="row.id"
                    class="table-row-hover transition-colors"
                    :class="selectedRows.includes(row.id) ? 'bg-blue-50' : ''">
                  <td class="px-6 py-4">
                    <input class="rounded text-blue-600" type="checkbox"
                      :checked="selectedRows.includes(row.id)"
                      @change="toggleRow(row.id)"/>
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-full bg-blue-100 flex items-center justify-center shrink-0 text-blue-600 font-bold text-sm">
                        {{ row.custName?.[0] ?? '?' }}
                      </div>
                      <div class="min-w-0">
                        <p class="text-sm font-bold text-gray-800 truncate mb-0.5">{{ row.custName }}</p>
                        <p class="text-[10px] text-gray-400 truncate">{{ row.phone }} · {{ row.riskLevel }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-center">
                    <span class="inline-flex items-center justify-center px-2.5 py-1 text-[10px] font-bold rounded-lg whitespace-nowrap"
                          :class="row.contactStatus === '已认证' ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' : 'bg-zinc-100 text-zinc-500'">
                      {{ row.contactStatus || '—' }}
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <span class="text-sm text-gray-700">{{ row.taskName }}</span>
                  </td>
                  <td class="px-6 py-4">
                    <span class="text-xs font-medium text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-lg">{{ row.taskType }}</span>
                  </td>
                  <td class="px-6 py-4">
                    <span class="text-xs text-gray-500">{{ row.source }}</span>
                  </td>
                  <td class="px-6 py-4">
                    <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium"
                          :class="row.priorityCls">{{ row.priority }}</span>
                  </td>
                  <td class="px-6 py-4">
                    <span class="text-xs text-gray-500">{{ row.dueDate }}</span>
                  </td>
                  <td class="px-6 py-4 text-right">
                    <div class="flex items-center justify-end space-x-2">
                      <button class="text-xs font-bold text-gray-500 hover:text-blue-600" @click="openDetail(row)">详情</button>
                      <button class="text-xs font-bold transition-colors"
                        :class="row.priority === '低' ? 'text-purple-600 hover:text-purple-700' : 'text-gray-300 cursor-not-allowed'"
                        :disabled="row.priority !== '低'"
                        :title="row.priority !== '低' ? '仅低优先级任务可由AI代劳' : ''"
                        @click="row.priority === '低' && openBatchAI()">AI处理</button>
                      <button class="text-xs font-bold text-blue-600 hover:text-blue-700" @click="openAIPanel(row)">去处理</button>
                      <button class="p-1 text-gray-400 hover:text-blue-600 transition-colors"><iconify-icon class="text-lg" icon="solar:phone-bold"></iconify-icon></button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <!-- 列表底部分页 -->
          <div class="px-6 py-4 bg-gray-50 flex items-center justify-between">
            <span class="text-xs text-gray-500">共 {{ filteredTaskRows.length }} 条记录</span>
            <div class="flex items-center space-x-2">
              <button class="p-2 border border-gray-200 rounded-lg hover:bg-white transition-colors disabled:opacity-50" disabled><iconify-icon icon="solar:alt-arrow-left-linear"></iconify-icon></button>
              <button class="w-8 h-8 bg-blue-600 text-white text-xs font-bold rounded-lg shadow-md shadow-blue-100">1</button>
              <button class="w-8 h-8 text-xs font-medium text-gray-500 hover:bg-white rounded-lg transition-colors">2</button>
              <button class="w-8 h-8 text-xs font-medium text-gray-500 hover:bg-white rounded-lg transition-colors">3</button>
              <button class="p-2 border border-gray-200 rounded-lg hover:bg-white transition-colors"><iconify-icon icon="solar:alt-arrow-right-linear"></iconify-icon></button>
            </div>
          </div>
        </div>
      </div>
            </div><!-- /flex-1 overflow-y-auto -->
        </main>
    <!-- AI 面板遮罩（点击关闭） -->
    <div v-if="aiPanelOpen" class="panel-overlay" @click="closeAIPanel"></div>
    <!-- 6. AI 辅助面板 (Slide-over) -->
    <div class="fixed top-16 bottom-0 right-0 w-[450px] bg-white shadow-2xl z-30 transform transition-transform duration-300 ease-in-out border-l border-gray-100 flex flex-col"
         :class="aiPanelOpen ? 'translate-x-0' : 'translate-x-full'" id="aiAuxPanel">
      <div class="p-6 border-b border-gray-100 flex items-center justify-between bg-gradient-to-r from-blue-50 to-white">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-md">
            <iconify-icon class="text-white" icon="solar:magic-stick-3-bold"></iconify-icon>
          </div>
          <div>
            <h2 class="text-lg font-bold text-gray-800">AI 展业助手</h2>
            <p class="text-xs text-blue-600 font-medium">正在辅助处理: {{ activeTask?.custName ?? '--' }}</p>
          </div>
        </div>
        <button class="p-2 hover:bg-gray-100 rounded-full text-gray-400" @click="closeAIPanel">
          <iconify-icon class="text-2xl" icon="solar:close-circle-linear"></iconify-icon>
        </button>
      </div>
      <div class="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide">
        <!-- 客户一句话摘要 -->
        <div class="bg-blue-50 rounded-2xl p-4 border border-blue-100">
          <h3 class="text-xs font-bold text-blue-800 uppercase tracking-wider mb-2 flex items-center gap-1">
            <iconify-icon icon="solar:user-speak-bold"></iconify-icon> AI 客户摘要
          </h3>
          <p class="text-sm text-gray-700 leading-relaxed">
            该客户为<span class="font-bold text-blue-600">稳健型高净值客户</span>，偏好定期理财，当前有一笔20万理财即将在下周到期。近期浏览过"权益类基金"页面3次，显示出潜在的<span class="font-bold text-orange-600">资产增值需求</span>。
          </p>
        </div>
        <!-- 关键信息 -->
        <div class="grid grid-cols-2 gap-3">
          <div class="bg-gray-50 rounded-xl p-3">
            <p class="text-[10px] text-gray-400 font-medium uppercase mb-1">风险等级</p>
            <p class="text-sm font-bold text-gray-800">R2 稳健型</p>
          </div>
          <div class="bg-gray-50 rounded-xl p-3">
            <p class="text-[10px] text-gray-400 font-medium uppercase mb-1">关注偏好</p>
            <p class="text-sm font-bold text-gray-800">定期/权益</p>
          </div>
        </div>
        <!-- 智能话术 -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-gray-800">实时智能话术</h3>
            <div class="flex gap-2">
              <button class="text-[10px] bg-white border border-gray-200 px-2 py-1 rounded text-gray-500 hover:border-blue-500 hover:text-blue-600 transition-colors">专业</button>
              <button class="text-[10px] bg-blue-600 px-2 py-1 rounded text-white font-medium">亲切</button>
            </div>
          </div>
          <div class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm relative group">
            <p class="text-sm text-gray-600 italic mb-4 leading-relaxed">
              "张先生您好，我是您的专属财富顾问王小明。注意到您有一笔理财快到期了，最近市场波动较大，我为您准备了一份针对性的资产接续方案，结合了您最近关注的权益类产品动态，方便给您介绍下吗？"
            </p>
            <div class="flex justify-end gap-2">
              <button class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all" title="复制">
                <iconify-icon icon="solar:copy-bold"></iconify-icon>
              </button>
              <button class="px-4 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg shadow-md hover:bg-blue-700 transition-all flex items-center gap-1">
                <iconify-icon icon="solar:plain-2-bold"></iconify-icon>
                一键发送企微
              </button>
            </div>
          </div>
        </div>
        <!-- 快捷结果按钮 -->
        <div class="space-y-3">
          <h3 class="text-sm font-bold text-gray-800">快捷结果标记</h3>
          <div class="grid grid-cols-3 gap-2">
            <button class="py-2 px-1 text-[10px] font-medium border border-gray-200 rounded-lg text-gray-600 hover:bg-green-50 hover:border-green-200 hover:text-green-600 transition-all">意向强烈</button>
            <button class="py-2 px-1 text-[10px] font-medium border border-gray-200 rounded-lg text-gray-600 hover:bg-blue-50 hover:border-blue-200 hover:text-blue-600 transition-all">后续跟进</button>
            <button class="py-2 px-1 text-[10px] font-medium border border-gray-200 rounded-lg text-gray-600 hover:bg-red-50 hover:border-red-200 hover:text-red-600 transition-all">无意向/拒绝</button>
          </div>
        </div>
        <!-- 合规提示 -->
        <div class="p-4 bg-orange-50 rounded-2xl border border-orange-100 flex gap-3">
          <iconify-icon class="text-orange-500 text-xl shrink-0" icon="solar:shield-warning-bold"></iconify-icon>
          <div>
            <h4 class="text-xs font-bold text-orange-800 mb-1">合规提示</h4>
            <p class="text-[10px] text-orange-700 leading-normal">
              触达内容中请勿包含具体的收益承诺表述。当前话术已通过系统自动审核，可安全使用。
            </p>
          </div>
        </div>
      </div>
    </div>
    <!-- 7. 任务执行进度弹窗 (Modal) -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="progressModalOpen" class="fixed inset-0 z-[200] flex items-center justify-center p-4">
          <div class="modal-overlay" @click="closeProgressModal"></div>
          <div class="bg-white rounded-3xl w-full max-w-2xl shadow-2xl relative z-10 overflow-hidden flex flex-col max-h-[85vh]">
            <!-- 头部 -->
            <div class="p-6 border-b border-gray-100 flex items-center justify-between shrink-0">
              <div>
                <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
                  AI 任务执行进度
                  <span v-if="aiLogStats.running > 0" class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-blue-600"></span>
                  </span>
                </h2>
                <p class="text-xs text-gray-400 mt-0.5">
                  {{ aiLogStats.running > 0 ? '正在异步执行批量任务，请勿关闭页面' : '本批次任务已全部处理完毕' }}
                </p>
              </div>
              <button class="p-2 hover:bg-gray-100 rounded-full text-gray-400 transition-colors" @click="closeProgressModal">
                <iconify-icon class="text-2xl" icon="solar:close-circle-linear"></iconify-icon>
              </button>
            </div>

            <div class="p-6 overflow-y-auto space-y-6">
              <!-- 四格统计 -->
              <div class="grid grid-cols-4 gap-4">
                <div class="bg-gray-50 p-3 rounded-2xl text-center">
                  <p class="text-[10px] text-gray-400 font-medium uppercase mb-1">总任务</p>
                  <p class="text-xl font-bold text-gray-800">{{ progressStats.total }}</p>
                </div>
                <div class="bg-blue-50 p-3 rounded-2xl text-center">
                  <p class="text-[10px] text-blue-400 font-medium uppercase mb-1">执行中</p>
                  <p class="text-xl font-bold text-blue-600">{{ progressStats.running }}</p>
                </div>
                <div class="bg-green-50 p-3 rounded-2xl text-center">
                  <p class="text-[10px] text-green-400 font-medium uppercase mb-1">已完成</p>
                  <p class="text-xl font-bold text-green-600">{{ progressStats.done }}</p>
                </div>
                <div class="bg-red-50 p-3 rounded-2xl text-center">
                  <p class="text-[10px] text-red-400 font-medium uppercase mb-1">失败</p>
                  <p class="text-xl font-bold text-red-600">{{ progressStats.failed }}</p>
                </div>
              </div>

              <!-- 进度条 -->
              <div class="space-y-2">
                <div class="flex justify-between items-end">
                  <span class="text-sm font-bold text-gray-700">整体进度</span>
                  <span class="text-sm font-bold text-blue-600">{{ progressStats.pct }}%</span>
                </div>
                <div class="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                  <div class="bg-blue-600 h-full transition-all duration-700 rounded-full"
                       :style="{ width: progressStats.pct + '%' }"></div>
                </div>
              </div>

              <!-- 执行日志 -->
              <div class="space-y-3">
                <h3 class="text-sm font-bold text-gray-800 flex items-center gap-2">
                  <iconify-icon class="text-blue-500" icon="solar:document-text-bold"></iconify-icon>
                  执行日志
                </h3>
                <div class="bg-slate-900 rounded-xl p-4 font-mono text-[10px] text-slate-300 h-52 overflow-y-auto space-y-1" ref="logBoxRef">
                  <p v-for="(log, i) in progressLogs" :key="i">
                    <span class="text-slate-500">[{{ log.time }}]</span>
                    <span v-if="log.type === 'success'" class="text-emerald-400"> SUCCESS: </span>
                    <span v-else-if="log.type === 'error'" class="text-red-400"> ERROR: </span>
                    <span v-else> </span>
                    {{ log.msg }}
                  </p>
                  <p v-if="aiLogStats.running > 0" class="animate-pulse text-blue-400">正在处理剩余 {{ progressStats.running }} 个任务...</p>
                </div>
              </div>

              <!-- 失败清单（有失败才显示） -->
              <div v-if="progressStats.failed > 0" class="bg-red-50 border border-red-100 rounded-2xl p-4">
                <div class="flex items-center justify-between mb-3">
                  <h4 class="text-xs font-bold text-red-800">失败清单 ({{ progressStats.failed }})</h4>
                  <button class="text-[10px] text-red-600 font-bold hover:underline">重试全部失败</button>
                </div>
                <div class="space-y-2">
                  <div v-for="f in failedLogs" :key="f.id" class="flex justify-between text-[10px]">
                    <span class="text-gray-600 font-medium">{{ f.task_name }}<template v-if="f.cust_name"> · {{ f.cust_name }}</template></span>
                    <span class="text-red-500">{{ f.fail_reason }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 底部操作 -->
            <div class="p-5 border-t border-gray-100 bg-gray-50 flex items-center justify-between shrink-0">
              <div class="flex gap-2">
                <button @click="fetchAiLogStats" class="px-4 py-2 border border-gray-200 bg-white text-gray-600 text-xs font-bold rounded-xl hover:bg-gray-50 transition-all flex items-center gap-1.5">
                  <iconify-icon icon="solar:refresh-bold"></iconify-icon> 刷新
                </button>
                <button class="px-4 py-2 border border-gray-200 bg-white text-gray-600 text-xs font-bold rounded-xl hover:bg-gray-50 transition-all flex items-center gap-1.5">
                  <iconify-icon icon="solar:export-bold"></iconify-icon> 导出清单
                </button>
              </div>
              <button class="px-6 py-2 bg-red-50 text-red-600 text-xs font-bold rounded-xl hover:bg-red-100 transition-all">撤销全部</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
    <!-- WIP Toast -->
    <Teleport to="body">
      <Transition name="toast-slide">
        <div v-if="wipToastVisible" style="position:fixed;bottom:2rem;left:50%;transform:translateX(-50%);z-index:300;" class="bg-slate-800 text-white text-sm font-medium px-5 py-3 rounded-2xl shadow-xl flex items-center gap-2">
          <iconify-icon icon="lucide:wrench" width="15" class="text-amber-400"></iconify-icon>
          功能开发中，敬请期待
        </div>
      </Transition>
    </Teleport>

    <!-- AI 批量处理弹窗 (与展业大厅对齐) -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="batchAIModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div class="modal-overlay" @click="closeBatchAI"></div>
          <div class="bg-white rounded-3xl w-full max-w-2xl shadow-2xl relative z-10 overflow-hidden flex flex-col max-h-[85vh]">
            <!-- 头部 -->
            <div class="p-6 border-b border-gray-100 flex items-center justify-between shrink-0">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg">
                  <iconify-icon class="text-white text-xl" icon="solar:cpu-bolt-bold-duotone"></iconify-icon>
                </div>
                <div>
                  <h2 class="text-xl font-bold text-gray-800">AI 批量处理</h2>
                  <p class="text-xs text-gray-400 mt-0.5">以下为系统自动筛选的低优先级任务，可交由 AI 代为执行，执行结果将自动留痕</p>
                </div>
              </div>
              <button class="px-5 py-2 bg-indigo-600 text-white text-sm font-bold rounded-xl shadow-lg shadow-indigo-100 hover:bg-indigo-700 transition-all disabled:opacity-40 flex items-center gap-2"
                      :disabled="noBatchSelected"
                      @click="startBatchAI">
                <iconify-icon icon="lucide:play-circle" width="16"></iconify-icon>
                确认执行 {{ batchSelectedLabel }}
              </button>
            </div>

            <div class="p-6 overflow-y-auto space-y-5">
              <!-- 统计卡 -->
              <div class="grid grid-cols-3 gap-4">
                <div class="bg-white border border-slate-200 rounded-2xl p-4 flex items-center gap-3">
                  <div class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center shrink-0">
                    <iconify-icon icon="lucide:list-checks" width="20"></iconify-icon>
                  </div>
                  <div>
                    <p class="text-2xl font-bold text-slate-900">{{ batchAITasks.length }}</p>
                    <p class="text-xs text-slate-400">低优任务总数</p>
                  </div>
                </div>
                <div class="bg-white border border-slate-200 rounded-2xl p-4 flex items-center gap-3">
                  <div class="w-10 h-10 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center shrink-0">
                    <iconify-icon icon="lucide:check-square" width="20"></iconify-icon>
                  </div>
                  <div>
                    <p class="text-2xl font-bold text-emerald-600">{{ batchAISelected.length }}</p>
                    <p class="text-xs text-slate-400">已选中</p>
                  </div>
                </div>
                <div class="bg-white border border-slate-200 rounded-2xl p-4 flex items-center gap-3">
                  <div class="w-10 h-10 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center shrink-0">
                    <iconify-icon icon="lucide:clock" width="20"></iconify-icon>
                  </div>
                  <div>
                    <p class="text-2xl font-bold text-slate-900">≈ {{ batchAITasks.length * 3 }}min</p>
                    <p class="text-xs text-slate-400">预计节省时间</p>
                  </div>
                </div>
              </div>

              <!-- 全选操作栏 -->
              <div class="flex items-center justify-between bg-indigo-50 border border-indigo-100 rounded-xl px-4 py-2.5">
                <label class="flex items-center gap-2 cursor-pointer select-none">
                  <input type="checkbox" class="w-4 h-4 rounded text-indigo-600 focus:ring-0"
                    :checked="allBatchSelected"
                    @change="toggleBatchAISelectAll"/>
                  <span class="text-sm font-medium text-indigo-700">全选 / 取消全选</span>
                </label>
                <span class="text-xs text-indigo-500">共 {{ batchAITasks.length }} 项低优先级任务</span>
              </div>

              <!-- 任务列表 -->
              <div class="space-y-3">
                <div v-if="batchAITasks.length === 0" class="text-center text-slate-400 py-16">
                  <iconify-icon icon="lucide:check-circle-2" width="36" class="mb-3 opacity-30"></iconify-icon>
                  <p class="text-sm">暂无低优先级任务</p>
                </div>
                <div v-for="t in batchAITasks" :key="t.id"
                     class="bg-white border rounded-xl px-5 py-4 flex items-center gap-4 cursor-pointer transition-all"
                     :class="batchAISelected.includes(t.id) ? 'border-indigo-300 shadow-sm shadow-indigo-50' : 'border-slate-200 hover:border-slate-300'"
                     @click="toggleBatchAIItem(t.id)">
                  <input type="checkbox" class="w-4 h-4 rounded text-indigo-600 focus:ring-0 shrink-0"
                    :checked="batchAISelected.includes(t.id)" @click.stop @change="toggleBatchAIItem(t.id)"/>
                  <div class="w-9 h-9 rounded-lg bg-indigo-50 flex items-center justify-center shrink-0">
                    <iconify-icon icon="solar:magic-stick-3-bold" width="16" class="text-indigo-600"></iconify-icon>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-bold text-slate-900 flex items-center gap-1.5 flex-wrap">
                      {{ t.taskName }}<template v-if="t.custName"> · {{ t.custName }}</template>
                      <span class="px-1.5 py-0.5 bg-slate-100 text-slate-500 text-[9px] rounded font-bold">低优</span>
                    </p>
                    <p class="text-[10px] text-slate-400 mt-0.5">{{ t.taskType }} · {{ t.contactStatus || '—' }} · 截止 {{ t.dueDate }}</p>
                  </div>
                  <span class="text-[10px] px-2 py-1 bg-slate-100 text-slate-500 rounded-lg font-medium shrink-0">待处理</span>
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
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- 任务详情弹窗 -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="taskDetailOpen" class="fixed inset-0 z-[150] flex items-center justify-center p-4">
          <div class="modal-overlay" @click="closeTaskDetail"></div>
          <div class="bg-white rounded-3xl w-full max-w-2xl shadow-2xl relative z-10 overflow-hidden flex flex-col max-h-[90vh]">
            <!-- 头部 -->
            <div class="p-6 border-b border-gray-100 flex items-center justify-between shrink-0 bg-gradient-to-r from-blue-50 to-white">
              <div class="flex items-center gap-4">
                <div class="w-11 h-11 bg-blue-600 rounded-xl flex items-center justify-center shadow-md">
                  <iconify-icon class="text-white text-xl" icon="solar:clipboard-list-bold"></iconify-icon>
                </div>
                <div>
                  <h2 class="text-lg font-bold text-gray-800">{{ detailTask?.taskName }}</h2>
                  <div class="flex items-center gap-2 mt-0.5">
                    <span class="text-xs px-2 py-0.5 rounded-full font-medium"
                          :class="detailTask?.priorityCls">{{ detailTask?.priority }}优先级</span>
                    <span class="text-xs text-gray-400">{{ detailTask?.source }}</span>
                  </div>
                </div>
              </div>
              <button class="p-2 hover:bg-gray-100 rounded-full text-gray-400 transition-colors" @click="closeTaskDetail">
                <iconify-icon class="text-2xl" icon="solar:close-circle-linear"></iconify-icon>
              </button>
            </div>

            <div class="flex-1 overflow-y-auto p-6 space-y-5">
              <!-- 客户信息 -->
              <div class="bg-gray-50 rounded-2xl p-4">
                <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">客户信息</h3>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <p class="text-[10px] text-gray-400 mb-1">客户姓名</p>
                    <p class="text-sm font-bold text-gray-800">{{ detailTask?.custName }}</p>
                  </div>
                  <div>
                    <p class="text-[10px] text-gray-400 mb-1">联系电话</p>
                    <p class="text-sm font-medium text-gray-700">{{ detailTask?.phone }}</p>
                  </div>
                  <div>
                    <p class="text-[10px] text-gray-400 mb-1">风险等级</p>
                    <p class="text-sm font-medium text-gray-700">{{ detailTask?.riskLevel }}</p>
                  </div>
                  <div>
                    <p class="text-[10px] text-gray-400 mb-1">建联状态</p>
                    <span class="inline-flex items-center justify-center px-2.5 py-1 text-[10px] font-bold rounded-lg whitespace-nowrap"
                          :class="detailTask?.contactStatus === '已认证' ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' : 'bg-zinc-100 text-zinc-500'">
                      {{ detailTask?.contactStatus || '—' }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- 任务信息 -->
              <div class="bg-gray-50 rounded-2xl p-4">
                <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">任务信息</h3>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <p class="text-[10px] text-gray-400 mb-1">任务类型</p>
                    <p class="text-sm font-medium text-gray-700">{{ detailTask?.taskType }}</p>
                  </div>
                  <div>
                    <p class="text-[10px] text-gray-400 mb-1">任务来源</p>
                    <p class="text-sm font-medium text-gray-700">{{ detailTask?.source }}</p>
                  </div>
                  <div>
                    <p class="text-[10px] text-gray-400 mb-1">截止时间</p>
                    <p class="text-sm font-medium text-gray-700">{{ detailTask?.dueDate }}</p>
                  </div>
                  <div>
                    <p class="text-[10px] text-gray-400 mb-1">当前状态</p>
                    <span class="text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-600 font-medium">待处理</span>
                  </div>
                </div>
              </div>

              <!-- AI 客户摘要 -->
              <div class="bg-blue-50 rounded-2xl p-4 border border-blue-100">
                <h3 class="text-xs font-bold text-blue-800 uppercase tracking-wider mb-2 flex items-center gap-1">
                  <iconify-icon icon="solar:magic-stick-3-bold" class="text-blue-600"></iconify-icon> AI 客户摘要
                </h3>
                <p class="text-sm text-gray-700 leading-relaxed">{{ detailTask?.aiSummary }}</p>
              </div>

              <!-- 智能话术建议 -->
              <div class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm">
                <h3 class="text-xs font-bold text-gray-700 mb-2">推荐话术</h3>
                <p class="text-sm text-gray-600 italic leading-relaxed">{{ detailTask?.suggestedScript }}</p>
                <div class="flex justify-end gap-2 mt-3">
                  <button class="px-3 py-1.5 text-xs border border-gray-200 rounded-lg text-gray-500 hover:border-blue-300 hover:text-blue-600 transition-colors flex items-center gap-1">
                    <iconify-icon icon="solar:copy-bold"></iconify-icon> 复制
                  </button>
                  <button class="px-3 py-1.5 text-xs bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all flex items-center gap-1">
                    <iconify-icon icon="solar:plain-2-bold"></iconify-icon> 一键发送企微
                  </button>
                </div>
              </div>

              <!-- 合规提示 -->
              <div class="p-4 bg-orange-50 rounded-2xl border border-orange-100 flex gap-3">
                <iconify-icon class="text-orange-500 text-xl shrink-0" icon="solar:shield-warning-bold"></iconify-icon>
                <div>
                  <h4 class="text-xs font-bold text-orange-800 mb-1">合规提示</h4>
                  <p class="text-[10px] text-orange-700 leading-normal">触达内容中请勿包含具体的收益承诺表述。当前话术已通过系统自动审核，可安全使用。</p>
                </div>
              </div>
            </div>

            <!-- 底部操作 -->
            <div class="p-5 border-t border-gray-100 bg-gray-50 flex items-center justify-between shrink-0">
              <div class="flex gap-2">
                <button class="px-4 py-2 border border-gray-200 bg-white text-gray-600 text-xs font-bold rounded-xl hover:bg-gray-50 transition-all flex items-center gap-1.5">
                  <iconify-icon icon="solar:phone-bold"></iconify-icon> 立即外呼
                </button>
                <button class="px-4 py-2 border border-gray-200 bg-white text-gray-600 text-xs font-bold rounded-xl hover:bg-gray-50 transition-all flex items-center gap-1.5">
                  <iconify-icon icon="solar:tag-bold"></iconify-icon> 标记结果
                </button>
              </div>
              <button @click="openAIFromDetail"
                      class="px-6 py-2 bg-blue-600 text-white text-xs font-bold rounded-xl shadow-md hover:bg-blue-700 transition-all flex items-center gap-1.5">
                <iconify-icon icon="solar:magic-stick-3-bold"></iconify-icon> 去处理
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    </div><!-- /.business-hall -->
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

const todayStr = (() => {
    const d = new Date()
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}年${m}月${day}日`
})()

// ── 侧边栏折叠 ────────────────────────────────────────────────
const sidebarCollapsed = ref(false)

// ── 每日提醒 ──────────────────────────────────────────────────
const STAFF_LOGIN_ID   = 'oa001'
const alertPanelOpen   = ref(false)
const alerts           = ref([])
const newAlertContent  = ref('')
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
    } catch (e) { console.error('markAlertDone error', e) } finally { alert._marking = false }
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

// ── 顶部 6 卡片数据 ───────────────────────────────────────────
const taskList   = ref([])   // 全量任务（用于今日待办/已完成统计）
const callCard   = ref({})   // 外呼/加微/绑定数据（来自 overview）

const todoCount     = computed(() => taskList.value.filter(t => ['待处理','处理中'].includes(t.status)).length)
const doneCount     = computed(() => taskList.value.filter(t => t.status === '已完成').length)
const doneRate      = computed(() => {
    const total = taskList.value.length
    return total > 0 ? Math.round(doneCount.value / total * 100) : 0
})
const connected     = computed(() => callCard.value.connected ?? '--')
const callTotal     = computed(() => callCard.value.total ?? 0)
const connectRate   = computed(() => callTotal.value > 0 ? Math.round(connected.value / callTotal.value * 100) : '--')
// 今日逾期任务
const overdueCount  = computed(() => taskList.value.filter(t => t.status === '已逾期').length)
// 高优未处理
const highPriCount  = computed(() => taskList.value.filter(t =>
    t.priority === '高' && ['待处理', '处理中'].includes(t.status)
).length)

async function fetchTasksSummary() {
    try {
        const res  = await fetch(`/api/staff/tasks?login_id=${STAFF_LOGIN_ID}&page_size=200`)
        const data = await res.json()
        taskList.value = data.tasks || []
    } catch (e) { console.warn('[tasks-summary] fetch failed', e) }
}

async function fetchOverviewCard() {
    try {
        const res  = await fetch(`/api/staff/overview?login_id=${STAFF_LOGIN_ID}`)
        const data = await res.json()
        // 只取外呼数据（connected / total），其他字段任务大厅不用
        callCard.value = data.call_card || {}
    } catch (e) { console.warn('[overview-card] fetch failed', e) }
}

// ── AI 任务执行进度弹窗 ───────────────────────────────────────
const progressModalOpen = ref(false)
const logBoxRef         = ref(null)

// ── AI 任务执行状态（AIPC_AI_TASKS_LOG） ──────────────────────
const aiLogStats = ref({ running: 0, doneToday: 0, failedToday: 0 })

// MOCK 数据：模拟 2 个执行中、5 个今日已完成、1 个失败
// 真实模式下替换为 GET /api/staff/ai-tasks/stats?login_id=xxx
async function fetchAiLogStats() {
    try {
        const res  = await fetch(`/api/staff/ai-tasks/stats?login_id=${STAFF_LOGIN_ID}`)
        const json = await res.json()
        aiLogStats.value = {
            running:     json.running      ?? 0,
            doneToday:   json.done_today   ?? 0,
            failedToday: json.failed_today ?? 0,
        }
    } catch {
        // 接口未就绪时使用 mock 数据（基于 staff_tasks.py 的低优任务）
        // mock: 3个低优任务中 2个执行中、5个已完成（含历史）、1个失败
        aiLogStats.value = { running: 2, doneToday: 5, failedToday: 1 }
    }
}

// ── 进度弹窗：基于 aiLogStats mock 数据构建展示 ───────────────
const progressStats = computed(() => {
    const { running, doneToday, failedToday } = aiLogStats.value
    const done  = doneToday
    const total = running + done + failedToday
    const pct   = total > 0 ? Math.round((done + failedToday) / total * 100) : 0
    return { total, running, done, failed: failedToday, pct }
})

// 基于 staff_tasks mock 低优任务生成执行日志
const progressLogs = computed(() => {
    const now = new Date()
    const fmt = (d) => `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}:${String(d.getSeconds()).padStart(2,'0')}`
    const base = new Date(now.getTime() - 8 * 60 * 1000)  // 8分钟前开始
    const tick = (sec) => { const d = new Date(base.getTime() + sec * 1000); return fmt(d) }

    // 对应 staff_tasks.py 低优任务（id 13:引客-程*雪, id 15:培训作业）
    return [
        { time: tick(0),   type: 'info',    msg: `初始化 AI 批量处理任务，共 ${progressStats.value.total} 项...` },
        { time: tick(3),   type: 'info',    msg: '正在验证任务合规性...' },
        { time: tick(8),   type: 'info',    msg: '合规检查通过，开始执行' },
        { time: tick(15),  type: 'success', msg: '新客欢迎触达 · 程*雪 — 欢迎短信已发送' },
        { time: tick(28),  type: 'success', msg: '培训作业完成 — 作业已提交至培训平台' },
        { time: tick(42),  type: 'success', msg: '持仓关怀 · 冯*梅 — 关怀信息已推送' },
        { time: tick(58),  type: 'success', msg: '到期产品复投 · 韩*东 — 复投提醒已发送' },
        { time: tick(75),  type: 'error',   msg: '外呼录音复盘 — 系统繁忙，跳过处理' },
        { time: tick(90),  type: 'info',    msg: '正在进行合规留痕写入...' },
        { time: tick(100), type: 'info',    msg: `已完成 ${progressStats.value.done} 项，${progressStats.value.running} 项处理中` },
    ]
})

// 失败任务列表（与 mock 日志保持一致）
const failedLogs = computed(() => [
    { id: 1, task_name: '外呼录音复盘', cust_name: null,  fail_reason: '系统繁忙，稍后重试' },
])

// 声明所有用到的事件方法（避免全局onclick导致的冲突）
const toggleProgressModal = () => {
  progressModalOpen.value = !progressModalOpen.value
  if (progressModalOpen.value) {
    fetchAiLogStats()
    nextTick(() => {
      if (logBoxRef.value) logBoxRef.value.scrollTop = logBoxRef.value.scrollHeight
    })
  }
}

// ── Tab 定义 ──────────────────────────────────────────────────
const activeTab = ref('todo')

const tabDefs = [
  { key: 'todo',       label: '我的待办' },
  { key: 'connect',    label: '建联类' },
  { key: 'follow',     label: '跟进类' },
  { key: 'cycle',      label: '周期类' },
  { key: 'activity',   label: '营销活动类' },
  { key: 'compliance', label: '合规类' },
  { key: 'closed',     label: '已完成/已关闭' },
  { key: 'ai_center',  label: 'AI批量任务中心' },
]

// tab key → taskType 映射（todo 和 closed 特殊处理）
const tabTypeMap = {
  connect:    '建联类',
  follow:     '跟进类',
  cycle:      '周期类',
  activity:   '营销活动类',
  compliance: '合规类',
}

// ── 任务行 mock 数据 ──────────────────────────────────────────
const mockTaskRows = ref([
  // ── 建联类
  {
    id: 1, custName: '李华', phone: '13512346677',
    contactStatus: '未添加或未绑定',
    taskName: '潜在流失客户二次唤醒', taskType: '建联类', source: '模型预警', status: 'open',
    priority: '高', priorityCls: 'bg-red-50 text-red-600', dueDate: '2026-06-09 12:00',
    riskLevel: 'R3 平衡型',
    aiSummary: '该客户近90天无交易记录，资产有所缩水，模型判定流失风险高。历史沟通记录显示客户对基金定投有一定了解，近期有税收优惠类产品问询。',
    suggestedScript: '"李女士您好，最近市场有一些比较好的投资机会，结合您之前关注过的产品，我想给您做个简单的介绍，请问现在方便吗？"',
  },
  {
    id: 2, custName: '王强', phone: '18811111234',
    contactStatus: '未添加或未绑定',
    taskName: '新客开户24h未加微跟进', taskType: '建联类', source: '系统触发', status: 'open',
    priority: '低', priorityCls: 'bg-slate-100 text-slate-500', dueDate: '2026-06-08 20:00',
    riskLevel: 'R1 保守型',
    aiSummary: '新客户，刚完成开户但尚未添加企业微信，开户资金量较小。属于新客转化关键节点，建议通过短信+企微邀请双触达，提升首次服务体验。',
    suggestedScript: '"王先生您好，恭喜您成功开户！为了给您提供更便捷的账户服务，请添加我的企业微信，后续我可以为您推送个性化行情资讯和投资建议，方便您随时查看。"',
  },
  // ── 跟进类
  {
    id: 3, custName: '赵梅', phone: '13912345521',
    contactStatus: '已认证',
    taskName: '高价值客户月度回访', taskType: '跟进类', source: '系统触发', status: 'open',
    priority: '高', priorityCls: 'bg-red-50 text-red-600', dueDate: '2026-06-10 15:00',
    riskLevel: 'R2 稳健型',
    aiSummary: '该客户资产规模超50万，近期无异常操作，但距上次主动联系已超30天，属于高价值沉默客户，需定期维护。',
    suggestedScript: '"赵女士您好，本月我们有几款稳健型产品想给您介绍，同时也想了解一下您最近的资产配置需求，方便聊几分钟吗？"',
  },
  {
    id: 4, custName: '陈国', phone: '15612348843',
    contactStatus: '已认证',
    taskName: '产品到期客户跟进', taskType: '跟进类', source: '模型预警', status: 'open',
    priority: '中', priorityCls: 'bg-amber-50 text-amber-600', dueDate: '2026-06-11 18:00',
    riskLevel: 'R4 进取型',
    aiSummary: '客户有一笔基金定投将于本月到期，历史上对权益类产品接受度较高，当前市场行情适合沟通续投或切换方向。',
    suggestedScript: '"陈先生您好，您的定投计划本月即将到期，我这边整理了几个接续方向，是否方便花几分钟了解一下？"',
  },
  // ── 周期类
  {
    id: 5, custName: '张民', phone: '13812348888',
    contactStatus: '已认证',
    taskName: '产品到期前7天续接建议', taskType: '周期类', source: '系统触发', status: 'open',
    priority: '高', priorityCls: 'bg-red-50 text-red-600', dueDate: '2026-06-08 18:00',
    riskLevel: 'R2 稳健型',
    aiSummary: '该客户为稳健型高净值客户，偏好定期理财，当前有一笔20万理财即将在下周到期。近期浏览过"权益类基金"页面3次，显示出潜在的资产增值需求。',
    suggestedScript: '"张先生您好，我是您的专属财富顾问。注意到您有一笔理财快到期了，最近市场波动较大，我为您准备了一份针对性的资产接续方案，结合了您最近关注的权益类产品动态，方便给您介绍下吗？"',
  },
  {
    id: 6, custName: '孙丽', phone: '18612343310',
    contactStatus: '已认证',
    taskName: '季度资产配置复盘', taskType: '周期类', source: '系统触发', status: 'open',
    priority: '中', priorityCls: 'bg-amber-50 text-amber-600', dueDate: '2026-06-15 10:00',
    riskLevel: 'R3 平衡型',
    aiSummary: '每季度定期复盘任务，该客户配置以固收为主，近期有增配意愿，可趁此次复盘推荐平衡型组合。',
    suggestedScript: '"孙女士您好，本季度到了咱们定期复盘的时间，我整理了您的资产配置情况和一些调整建议，方便现在聊一下吗？"',
  },
  // ── 营销活动类
  {
    id: 7, custName: '刘波', phone: '17712346629',
    contactStatus: '未添加或未绑定',
    taskName: '基金节专属活动邀约', taskType: '营销活动类', source: '手动创建', status: 'open',
    priority: '中', priorityCls: 'bg-amber-50 text-amber-600', dueDate: '2026-06-12 18:00',
    riskLevel: 'R3 平衡型',
    aiSummary: '该客户历史参与过线下活动，对新产品有较强兴趣，本次基金节活动与其风险偏好匹配，邀约成功率较高。',
    suggestedScript: '"刘先生您好，本周我们举办基金节专属活动，有限量席位名额，结合您的投资偏好我专门为您保留了一个名额，方便参加吗？"',
  },
  {
    id: 8, custName: '周芳', phone: '15012342287',
    contactStatus: '已认证',
    taskName: '新产品发售优先认购通知', taskType: '营销活动类', source: '系统触发', status: 'open',
    priority: '低', priorityCls: 'bg-slate-100 text-slate-500', dueDate: '2026-06-14 12:00',
    riskLevel: 'R2 稳健型',
    aiSummary: '新发稳健型产品，客户历史持仓中有类似品种，风险匹配，属优先推荐名单。',
    suggestedScript: '"周女士您好，有一款新发的稳健型产品刚好在您的配置偏好范围内，是否需要我给您发一份产品说明书？"',
  },
  // ── 合规类
  {
    id: 9, custName: '吴峰', phone: '13212349901',
    contactStatus: '已认证',
    taskName: '投资者适当性年度确认', taskType: '合规类', source: '系统触发', status: 'open',
    priority: '高', priorityCls: 'bg-red-50 text-red-600', dueDate: '2026-06-09 18:00',
    riskLevel: 'R4 进取型',
    aiSummary: '客户风险测评已超1年未更新，按监管要求需在持仓交易前完成年度适当性确认，逾期将影响其交易权限。',
    suggestedScript: '"吴先生您好，您的投资者适当性年度确认即将到期，麻烦您通过App完成更新，以免影响正常交易，需要我帮您发送操作指引吗？"',
  },
  {
    id: 10, custName: '郑云', phone: '15812344432',
    contactStatus: '已认证',
    taskName: '大额交易异常提醒确认', taskType: '合规类', source: '模型预警', status: 'open',
    priority: '高', priorityCls: 'bg-red-50 text-red-600', dueDate: '2026-06-08 16:00',
    riskLevel: 'R3 平衡型',
    aiSummary: '系统检测到该客户近期有一笔大额赎回，触发合规预警，需及时联系客户确认是否属于本人操作并了解资金去向。',
    suggestedScript: '"郑女士您好，我们系统检测到您账户近期有一笔较大金额的操作，按规定需要跟您确认一下，请问这笔操作是您本人发起的吗？"',
  },
  // ── 已完成
  {
    id: 11, custName: '马军', phone: '13712346654',
    contactStatus: '已认证',
    taskName: '存量客户季度回访', taskType: '跟进类', source: '系统触发', status: 'closed',
    priority: '中', priorityCls: 'bg-amber-50 text-amber-600', dueDate: '2026-06-01 18:00',
    riskLevel: 'R2 稳健型',
    aiSummary: '已完成回访，客户表示满意，暂无新增需求。',
    suggestedScript: '',
  },
])

// ── 筛选状态 ──────────────────────────────────────────────────
const filterSearch        = ref('')
const filterPriority      = ref('')
const filterContactStatus = ref('')
const filterSource        = ref('')
const filterAIOnly        = ref(false)

const PRIORITY_ORDER = { '高': 0, '中': 1, '低': 2 }

const resetTaskFilters = () => {
  filterSearch.value        = ''
  filterPriority.value      = ''
  filterContactStatus.value = ''
  filterSource.value        = ''
  filterAIOnly.value        = false
}

const filteredTaskRows = computed(() => {
  const rows = mockTaskRows.value.filter(r => {
    // Tab 过滤
    if (activeTab.value === 'ai_center') return false
    if (activeTab.value === 'closed') {
      if (r.status !== 'closed') return false
    } else if (activeTab.value !== 'todo') {
      const targetType = tabTypeMap[activeTab.value]
      if (r.taskType !== targetType) return false
    } else {
      if (r.status === 'closed') return false
    }
    // 筛选条件
    if (filterAIOnly.value && r.priority !== '低') return false
    if (filterSearch.value) {
      const q = filterSearch.value.toLowerCase()
      if (!r.custName.toLowerCase().includes(q) && !r.phone.includes(q)) return false
    }
    if (filterPriority.value && r.priority !== filterPriority.value) return false
    if (filterContactStatus.value && r.contactStatus !== filterContactStatus.value) return false
    if (filterSource.value && r.source !== filterSource.value) return false
    return true
  })
  // 排序：优先级（高→中→低）再按截止时间升序
  return rows.slice().sort((a, b) => {
    const pd = (PRIORITY_ORDER[a.priority] ?? 9) - (PRIORITY_ORDER[b.priority] ?? 9)
    if (pd !== 0) return pd
    return new Date(a.dueDate) - new Date(b.dueDate)
  })
})

const tabCount = (key) => {
  if (key === 'todo') return mockTaskRows.value.filter(r => r.status !== 'closed').length
  if (key === 'closed') return mockTaskRows.value.filter(r => r.status === 'closed').length
  const targetType = tabTypeMap[key]
  if (!targetType) return 0
  return mockTaskRows.value.filter(r => r.taskType === targetType && r.status !== 'closed').length
}

// ── 复选框状态 ─────────────────────────────────────────────────
const selectedRows = ref([])

const toggleAllRows = () => {
  if (selectedRows.value.length === filteredTaskRows.value.length) {
    selectedRows.value = []
  } else {
    selectedRows.value = filteredTaskRows.value.map(r => r.id)
  }
}

const toggleRow = (id) => {
  const idx = selectedRows.value.indexOf(id)
  if (idx === -1) selectedRows.value.push(id)
  else selectedRows.value.splice(idx, 1)
}

// ── 任务详情弹窗 ───────────────────────────────────────────────
const taskDetailOpen = ref(false)
const detailTask     = ref(null)

const openDetail = (row) => {
  detailTask.value  = row
  taskDetailOpen.value = true
}

// ── AI 批量处理弹窗（与展业大厅对齐） ─────────────────────────
const batchAIModalOpen = ref(false)
const batchAITasks     = computed(() => mockTaskRows.value.filter(r => r.priority === '低'))
const batchAISelected  = ref([])

const openBatchAI = () => {
  batchAISelected.value = batchAITasks.value.map(t => t.id)  // 默认全选
  batchAIModalOpen.value = true
}

const toggleBatchAISelectAll = () => {
  if (batchAISelected.value.length === batchAITasks.value.length) {
    batchAISelected.value = []
  } else {
    batchAISelected.value = batchAITasks.value.map(t => t.id)
  }
}

const toggleBatchAIItem = (id) => {
  const idx = batchAISelected.value.indexOf(id)
  if (idx === -1) batchAISelected.value.push(id)
  else batchAISelected.value.splice(idx, 1)
}

const startBatchAI = () => {
  batchAIModalOpen.value = false
  toggleProgressModal()
}

// ── AI 辅助面板 ───────────────────────────────────────────────
const aiPanelOpen = ref(false)
const activeTask  = ref(null)

const openAIPanel = (row) => {
  activeTask.value = row ?? null
  aiPanelOpen.value = true
}

const closeAIPanel = () => { aiPanelOpen.value = false }

// ── computed：取代模板内的复杂表达式（兼容严格 Vue 模板解析器）──────────────
const allRowsSelected   = computed(() => filteredTaskRows.value.length > 0 && filteredTaskRows.value.every(r => selectedRows.value.includes(r.id)))
const someRowsSelected  = computed(() => filteredTaskRows.value.some(r => selectedRows.value.includes(r.id)) && !allRowsSelected.value)
const noBatchSelected   = computed(() => batchAISelected.value.length === 0)
const allBatchSelected  = computed(() => batchAISelected.value.length === batchAITasks.value.length && batchAITasks.value.length > 0)
const batchSelectedLabel = computed(() => batchAISelected.value.length > 0 ? '(' + batchAISelected.value.length + '项)' : '')

// ── 方法：取代模板内的赋值表达式（兼容严格 Vue 模板解析器）────────────────
const toggleSidebar      = () => { sidebarCollapsed.value = !sidebarCollapsed.value }
const toggleAlertPanel   = () => { alertPanelOpen.value  = !alertPanelOpen.value }
const closeProgressModal = () => { progressModalOpen.value = false }
const closeBatchAI       = () => { batchAIModalOpen.value  = false }
const closeTaskDetail    = () => { taskDetailOpen.value    = false }
const openAIFromDetail   = () => { openAIPanel(detailTask.value); taskDetailOpen.value = false }

// ── 批量双呼 WIP toast ─────────────────────────────────────────
const wipToastVisible = ref(false)
let wipToastTimer = null

const showDoubleCallWip = () => {
  wipToastVisible.value = true
  clearTimeout(wipToastTimer)
  wipToastTimer = setTimeout(() => { wipToastVisible.value = false }, 2500)
}

onMounted(() => {
    fetchAlerts()
    fetchAiLogStats()
    fetchTasksSummary()
    fetchOverviewCard()
    document.addEventListener('click', _onClickOutsideAlert)
})

onUnmounted(() => {
    document.removeEventListener('click', _onClickOutsideAlert)
    clearTimeout(wipToastTimer)
})
</script>

<style scoped>
/* ── 整体布局 ─────────────────────────────────────── */
.business-hall {
    display: flex;
    height: 100vh;
    overflow: hidden;
}

:root {
  --sidebar-width: 256px;
  --sidebar-collapsed-width: 80px;
}
#sidebar {
  width: var(--sidebar-width);
  transition: width 0.3s;
}
#sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}
#sidebar.collapsed .nav-text,
#sidebar.collapsed .logo-text,
#sidebar.collapsed .user-info-text {
  display: none;
}
#sidebar.collapsed .nav-item {
  justify-content: center;
  padding-left: 0;
  padding-right: 0;
}
#sidebar.collapsed .nav-item iconify-icon {
  margin-right: 0;
}
.no-scrollbar::-webkit-scrollbar { 
  display: none; 
}
/* 补充缺失的样式 */
.table-row-hover:hover {
  background-color: #f9fafb;
}
.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
.toast-slide-enter-active, .toast-slide-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.toast-slide-enter-from, .toast-slide-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(8px);
}
.modal-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
}
.panel-overlay {
  position: fixed;
  top: 4rem;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 20;
  background-color: rgba(0, 0, 0, 0.1);
}
.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
}
</style>