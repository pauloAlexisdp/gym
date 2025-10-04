import { createRouter, createWebHistory } from 'vue-router'
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
      path: '/iniciar-sesion',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/registrarse',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
  ],
})

export default router
