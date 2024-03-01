import { createRouter, createWebHistory } from 'vue-router'
import WordsSubmit from '@/views/WordsSubmit.vue'
import Review from '@/views/Review.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/word',
      name: 'word',
      component: WordsSubmit,
    },
    {
      path: '/review',
      name: 'review',
      component: Review,
    },
    {
      path: '/',
      redirect: '/word'
    }
  ]
})

export default router
