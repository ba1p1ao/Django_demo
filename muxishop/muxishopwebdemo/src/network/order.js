import {request} from "./requestConfig.js"


export function createOrderData(data){
	return request({
		url:"/order/",
		method:"post",
		data
	})
}

export function getAllOrders(data){
	return request({
		url:"/order?pay_status="+data,
		method:"get",
	})
}


export function getAllOrdersByTradeNo(data){
	return request({
		url:"/order/goods/"+data,
		method:"get",
	})
}


export function updateOrderInfoData(data){
	return request({
		url:"/order/update/",
		method:"post",
		data
	})
}

export function toAliPayPage(data){
	return request({
		url:"/pay/alipay",
		method:"post",
		data
	})
}