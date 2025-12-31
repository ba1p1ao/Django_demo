import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
// const GoodsList = () => import("../views/GoodsList/GoodsList.vue")

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: "幕西商城首页"
    }
  },
  {
    // 这个 问号 ？ 的意思是这个参数可以传也可以不传
    path: '/goods_list/:keyword/:page/:order?',
    name: "GoodsList",
    component: () => import("@/views/goods/GoodsList.vue"),
    meta: {
      title: "商品列表页"
    }
  },
  {
    path: "/detail/:sku_id",
    name: "GoodsDetail",
    component: () => import("@/views/goods/GoodsDetail.vue"),
    meta: {
      title: "商品详情",
      isAuthRequired: true
    }
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/login/Login.vue"),
    meta: {
      title: "欢迎登录"
    }
  },
    {
    path: "/register",
    name: "Register",
    component: () => import("@/views/login/Register.vue"),
    meta: {
      title: "欢迎注册"
    }
  },
  {
    path: "/cart/detail",
    name: "Cart",
    component: () => import("@/views/cart/Cart.vue"),
    meta: {
      title: "购物车",
      isAuthRequired: true
    }
  },
  {
    path: "/order/:trade_no",
    name: "Order",
    component: () => import("@/views/order/Order.vue"),
    meta: {
      title: "订单",
      isAuthRequired: true
    }
  },
  {
    path: "/order/pay",
    name: "OrderPay",
    component: () => import("@/views/order/OrderPay.vue"),
    meta: {
      title: "收银台",
      isAuthRequired: true
    }
  },
  {
    path: "/profile",
    name: "Profile",
    component: () => import("@/views/profile/Profile.vue"),
    meta: {
      title: "个人中心",
      isAuthRequired: true
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

import store from "@/store"
router.beforeEach((to, from) => {
  document.title = to.meta.title;
  if (to.meta.isAuthRequired == true && store.state.user.isLogin == false) {
    router.push("/login")
  }
})

export default router
