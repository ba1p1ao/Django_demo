import {request} from "./requestConfig.js"


export function addAddressData(data){
	return request({
		ul:"/address/",
		method:"post",
		data
	})
}

export function getAllAddressesData(){
	return request({
		url:"/address/",
		method:"get",
	})
}

export function editAddressData(data){
	return request({
		url:"/address/edit/",
		method:"post",
		data
	})
}



