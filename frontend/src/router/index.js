import { createRouter, createWebHistory } from 'vue-router'

import HelloWorld from '@/components/HelloWorld.vue'
import Signup from '@/components/auth/Signup.vue'
import Signin from '@/components/auth/Signin.vue'

const routes = [
  {
    path: '/', // Главная страница
    name: 'home',
    component: HelloWorld,
  },
  {
    path: '/auth/signup', // Страница регистрации
    name: 'signup',
    component: Signup,
  },
  {
    path: '/auth/signin', // Страница авторизации
    name: 'signin',
    component: Signin,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
