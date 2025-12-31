import {request} from "./requestConfig.js"


export function getMainMenu(){
	return request({
		url:"/menu/mainmenu/",
	})
}


export function getSecondMenu(mainMenuId){
	return request({
		url:"/menu/submenu/?main_menu_id="+mainMenuId,
	})
}

export function getFindGoods(){
	return request({
		url:"/goods/find/",
	})
}



export function getCategoryGoods(categoryId,page){
	return request({
		url:"/goods/category/"+categoryId+"/"+page,
	})
}
