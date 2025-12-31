import { request } from "./requestConfig";

export function createOrderData(data) {
    return request({
        url: "/order/",
        method: "post",
        data
    })
}

export function getOrderData(pay_status) {
    return request({
        url: "/order/?pay_status=" + pay_status,
        method: "get",
    })
}

export function deleteOrderData(data) {
    return request({
        url: "/order/",
        method: "delete",
        data
    })
}

export function updateOrderData(data) {
    return request({
        url: "/order/",
        method: "put",
        data
    })
}


export function getOrderByTradeNoData(tradeNo) {
    return request({
        url: "/order/" + tradeNo,
        method: "get"
    })
}

export function toAliPayPage(data) {
    return request({
        url: "/pay/alipay/",
        method: "post",
        data
    })
}