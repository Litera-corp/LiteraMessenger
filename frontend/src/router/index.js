import {createRouter, createWebHistory} from 'vue-router'

import HelloWorld from '@/components/HelloWorld.vue'
import Signup from '@/components/auth/Signup.vue'

const routes = [
    {
        path: '/', // Главная страница
        name: 'home',
        component: HelloWorld,
    },
    {
        path: '/auth/signup', // Страница авторизации
        name: 'signup',
        component: Signup,
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})

export default router