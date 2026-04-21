import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/inicio',
      name: 'inicio',
      component: () => import('../views/HomeUserView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/home-user',
      redirect: '/inicio',
    },
    {
      path: '/rutinas',
      name: 'rutinas',
      component: () => import('../views/RoutinesView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/planes',
      name: 'planes',
      component: () => import('../views/PlansView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/contactenos',
      name: 'contactenos',
      component: () => import('../views/ContactView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/exercises/:muscleGroup',
      name: 'exercise-list',
      component: () => import('../views/ExerciseListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('../views/ResetPasswordView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { name: 'home' }
  }
})

export default router
