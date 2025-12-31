import { createStore } from 'vuex'
import { getCartCount } from '@/network/cart'
// import mutations from './mutations.js'
import actions from './actions'

const state = {
    // 初始化 存储应用的全局状态数据，类似 Vue 组件的 data
    user: {
        isLogin: window.localStorage.getItem("token") ? true : false,
        name: window.localStorage.getItem("username") ? window.localStorage.getItem("username") : ""
    },
    cartCount: window.localStorage.getItem("cartCount") || 0,
}
const mutations = {
    // 更改 Vuex 的 store 中的状态的唯一方法
    setIsLogin(state, payload) {
        state.user.isLogin = payload
    },
    setUsername(state, payload) {
        state.user.name = payload
    },
    updateCartCount(state, payload) {
        state.cartCount = payload.count
    }
}

// const actions = {
//     updateCartCount({commit, state}) {
//         getCartCount().then(res => {
//             console.log("actions", res.data)
//         })
//     },
// }


export default createStore({
    state,
    getters: {
    },
    mutations,
    actions,
    modules: {
    }
})
