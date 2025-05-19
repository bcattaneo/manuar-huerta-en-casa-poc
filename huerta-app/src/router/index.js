import { createRouter, createWebHistory } from 'vue-router'
import HomeScreen from '../components/HomeScreen.vue'
import ChatScreen from '../components/ChatScreen.vue'
import IdentifyPlantScreen from '../components/IdentifyPlantScreen.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeScreen
  },
  {
    path: '/chat',
    name: 'chat',
    component: ChatScreen,
    props: route => ({ plantContext: route.query.plant })
  },
  {
    path: '/identify',
    name: 'identify',
    component: IdentifyPlantScreen
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router