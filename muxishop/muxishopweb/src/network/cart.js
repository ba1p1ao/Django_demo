import { ElMessage } from "element-plus";
import { request } from "./requestConfig";
import store from "@/store";


export function getCartDetailData() {
    return request({
        url: "/cart/detail/",
        method: "post",
        // data
    })
}
export function getCartCount() {
    return request({
        url: "/cart/count/",
        method: "get",
    })
}
export function updateCartNumber(data) {
    return request({
        url: "/cart/num/",
        method: "post",
        data
    })
}

export function addCart(data) {
    return request({
        url: "/cart/",
        method: "post",
        data
    })
}


export function addCartData(data) {
    addCart(data).then(res => {
        if (res.status == 30000) {
            ElMessage({
                message: res.data,
                type: 'success',
            })
        } else {
            ElMessage({
                message: res.data,
                type: 'error',
            })
        }
        store.dispatch("updateCartCount")
    })
}

export function delCart(data) {
    return request({
        url: "/cart/",
        method: "delete",
        data
    })
}
export function delCartData(data) {
    delCart(data).then(res => {
        if (res.status == 30000) {
            ElMessage({
                message: res.data,
                type: 'success',
            })
        } else {
            ElMessage({
                message: res.data,
                type: 'error',
            })
        }
        store.dispatch("updateCartCount")
    })
}
