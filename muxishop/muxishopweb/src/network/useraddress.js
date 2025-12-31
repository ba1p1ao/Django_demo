import { request } from "./requestConfig";


export function getUserAddress() {
    return request({
        url: "/address/",
        method: "get"
    })
}


export function createUserAddress(data) {
    return request({
        url: "/address/",
        method: "post",
        data
    })
}

export function setDefaultAddress(id) {
    let data = {id: id}
    return request({
        url: "/address/default/",
        method: "post",
        data
    })
}

export function deleteUserAddress(id) {
    let data = {id: id}
    return request({
        url: "/address/",
        method: "delete",
        data
    })
}

export function updateUserAddress(data) {
    return request({
        url: "/address/edit/",
        method: "post",
        data
    })
}