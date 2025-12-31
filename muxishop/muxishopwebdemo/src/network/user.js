import {request} from "./requestConfig.js"


export function loginRequest(data){
	return request({
		url:"/user/login/",
		method:"post",
		data
	})
}