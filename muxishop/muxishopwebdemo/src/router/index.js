import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
const GoodsList=()=>import("../views/GoodsList/GoodsList")
const Detail=()=>import("../views/Goods/Detail")
const Login=()=>import("../views/Login/Login")
const Cart=()=>import("../views/Cart/Cart")
const Order=()=>import("../views/Order/Order")
const OrderPay=()=>import("../views/Order/OrderPay")
const Profile=()=>import("../views/Profile/Profile")
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
	meta: {
		title:"慕西商城首页"
	}
  },
  {
	  // 这个问号?的意思是这个参数你可以传也可以不传
    path: '/goods_list/:keyword/:page/:order?',
    name: 'GoodsList',
    component: GoodsList,
  	meta: {
  		title:"商品列表页"
  	}
  },
  {
  	  // 这个问号?的意思是这个参数你可以传也可以不传
    path: '/detail/:sku_id',
    name: 'Detail',
    component: Detail,
  	meta: {
  		title:"商品详情页",
		// isAuthRequired:true
  	}
  },
  {
  	  // 这个问号?的意思是这个参数你可以传也可以不传
    path: '/login',
    name: 'Login',
    component: Login,
  	meta: {
  		title:"欢迎登录"
  	}
  },
  {
    path: '/cart/detail',
    name: 'Cart',
    component: Cart,
  	meta: {
  		title:"购物车",
  		// isAuthRequired:true
  	}
  },
  {
    path: '/Order/:trade_no',
    name: 'Order',
    component: Order,
  	meta: {
  		title:"订单页面",
  		// isAuthRequired:true
  	}
  },
  {
  path: '/Order/Pay',
    name: 'OrderPay',
    component: OrderPay,
  	meta: {
  		title:"收银台",
  		// isAuthRequired:true
  	}
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
  	meta: {
  		title:"个人中心",
  		// isAuthRequired:true
  	}
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

import store from "../store"

router.beforeEach((to,from)=>{
	document.title = to.meta.title;
	if(to.meta.isAuthRequired==true && store.state.user.isLogin==false){
		router.push("/login")
	}
})


export default router
