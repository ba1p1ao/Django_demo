import {addCart} from "@/network/cart.js"
import store from "@/store";

export function toGoodsDetail(skuId){
	window.open("/detail/"+skuId)
}


export function addCartData(skuId,nums,isDelete=0){
	let requestData = {
		sku_id:skuId,
		nums:nums,
		is_delete:isDelete
	}
	addCart(requestData).then(res=>{
		if(res.status==3000){
			alert(res.data);
		}else{
			alert(res.data);
		}
		store.dispatch("updateCart");
	})
}