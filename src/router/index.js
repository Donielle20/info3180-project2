import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/register/user',
      name: 'register_user',

      component: () => import('../views/AddRegisterForm.vue')
    },
    {
      path: '/user/login',
      name: 'user_login',

      component: () => import('../views/AddUserForm.vue')
    },
    {
      path: '/user/logout',
      name: 'user_logout',

      component: () => import('../components/Logout.vue')
    },
    {
      path: '/user/profile',
      name: 'user_profile',

      component: () => import('../components/ProfilePage.vue')
    }
  ]
})

export default router
