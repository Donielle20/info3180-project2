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
      path: '/register',
      name: 'register',

      component: () => import('../views/AddRegisterForm.vue')
    },
    {
      path: '/login',
      name: 'login',

      component: () => import('../views/AddUserForm.vue')
    },
    {
      path: '/logout',
      name: 'logout',

      component: () => import('../components/Logout.vue')
    },
    {
      path: '/user/profile',
      name: 'user_profile',

      component: () => import('../components/ProfilePage.vue')
    },
    {
      path: '/posts/new',
      name: 'posts_new',

      component: () => import('../components/NewPosts.vue')
    },
    {
      path: '/explore',
      name: 'explore',

      component: () => import('../components/Explore.vue')
    },
    {
      path: '/users/:user_id',
      name: 'others_profile',

      component: () => import('../components/UserProfilePage.vue')
    }
  ]
})

export default router
