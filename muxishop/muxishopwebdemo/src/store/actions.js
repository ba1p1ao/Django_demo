import {getCartCounts} from "@/network/cart.js"

const actions = {
	updateCart({commit,state}){
		getCartCounts().then(res=>{
			let count=0;
			console.log(res.data)
			if(res.data.nums__sum>0){
				count = res.data.nums__sum;
			}
			window.localStorage.setItem("count",count);
			commit("updateCartCount",{count:count})
		})
	}
}

export default actions;