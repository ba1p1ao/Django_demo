import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'


import "@/assets/css/config.css"
// 引入iconfont
import "./assets/iconfont/iconfont.css"
// 引入 elementplus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 引入 滚动插件
import vue3SeamlessScroll from "vue3-seamless-scroll";
createApp(App)
    .use(store)
    .use(router)
    .use(ElementPlus)
    .use(vue3SeamlessScroll)
    .mount('#app')
