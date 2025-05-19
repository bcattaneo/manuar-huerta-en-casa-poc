import { createRouter, createWebHistory } from 'vue-router'
import HomeScreen from '../components/HomeScreen.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeScreen
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router