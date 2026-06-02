import { createRouter, createWebHistory } from 'vue-router'
import Index from '@/views/Index.vue'
import Tasks from '@/views/Tasks.vue'
import Business from '../views/Business.vue'
import Performance from '../views/Performance.vue'
import ManagerDashboard from '../views/ManagerDashboard.vue'
import ManagerCustomers from '../views/ManagerCustomers.vue'

const routes = [
  { path: '/', name: 'index', component: Index },
  { path: '/tasks', name: 'tasks', component: Tasks },
  { path: '/business', name: 'business', component: Business },
  { path: '/performance', name: 'performance', component: Performance },
  { path: '/manager', name: 'manager', component: ManagerDashboard },
  { path: '/manager/customers', name: 'manager-customers', component: ManagerCustomers },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router