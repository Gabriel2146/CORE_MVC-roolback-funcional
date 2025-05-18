import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Admin from '../components/Admin.vue'
import Trainer from '../components/Trainer.vue'
import Athlete from '../components/Athlete.vue'
import Guest from '../components/Guest.vue'
import TrainingPlanList from '../components/TrainingPlanList.vue'
import TrainingPlanCreate from '../components/TrainingPlanCreate.vue'

const routes = [
  {
    path: '/',
    name: 'LoginRedirect',
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('access_token')
      if (token) {
        next({ name: 'Login' })
      } else {
        next({ name: 'Home' })
      }
    }
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/trainer',
    name: 'Trainer',
    component: Trainer,
    meta: { requiresAuth: true, role: 'trainer' }
  },
  {
    path: '/athlete',
    name: 'Athlete',
    component: Athlete,
    meta: { requiresAuth: true, role: 'athlete' }
  },
  {
    path: '/guest',
    name: 'Guest',
    component: Guest,
    meta: { requiresAuth: true, role: 'guest' }
  },
  {
    path: '/training-plans',
    name: 'TrainingPlanList',
    component: TrainingPlanList,
    meta: { requiresAuth: true }
  },
  {
    path: '/training-plan/create',
    name: 'TrainingPlanCreate',
    component: TrainingPlanCreate,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userRole = localStorage.getItem('user_role') // You need to set this on login

  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login' })
  } else if (to.meta.role && to.meta.role !== userRole) {
    next({ name: 'Home' }) // Redirect if role does not match
  } else {
    next()
  }
})

export default router
