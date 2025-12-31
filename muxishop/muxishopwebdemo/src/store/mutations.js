const mutations = {
	setIsLogin(state,payload){
		state.user.isLogin = payload;
	},
	setUserName(state,payload){
		state.user.name = payload;
	},
	updateCartCount(state,payload){
		state.cartCount=payload.count;
	}
}

export default mutations;