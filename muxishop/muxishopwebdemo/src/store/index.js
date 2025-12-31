import { createStore } from 'vuex'
import mutations from "./mutations.js"
import actions from "./actions.js"
const state = {
	user:{
		isLogin:window.localStorage.getItem("token")?true:false,
		name:window.localStorage.getItem("username")?window.localStorage.getItem("username"):"",
	},
	cartCount:window.localStorage.getItem("count") || 0,
}

export default createStore({
  state,
  getters: {
  },
  mutations,
  actions,
  modules: {
  }
})
