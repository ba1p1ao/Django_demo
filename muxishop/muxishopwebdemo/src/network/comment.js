import {request} from "./requestConfig.js"


export function getCommentCountData(skuId){
	return request({
		url:"/comment/count?sku_id="+skuId,
	})
}

export function getGoodsCommentData(skuId,page){
	return request({
		url:"/comment/detail?sku_id="+skuId +"&page=" + page,
	})
}
