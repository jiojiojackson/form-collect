// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginCom from '../components/LoginCom.vue';
import SignaturePad from '../components/SignaturePad.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginCom },
  { path: '/form', component: SignaturePad, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('authToken'); // 假设使用本地存储来保存登录状态
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ path: '/login' });
  } else {
    next();
  }
});

export default router;
