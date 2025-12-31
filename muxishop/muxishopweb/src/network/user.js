import { request } from "./requestConfig.js"


export function isExistUser(data) {
    return request({
        url: "/user/register/",
        method: "post", 
        data,
    })
}
export function registerRequest(data) {
    return request({
        url: "/user/",
        method: "post",
        data,
    })
}
export function loginRequest(data) {
    return request({
        url: "/user/login/",
        method: "post",
        data,
    })
}

export function getUserInfo() {
    return request({
        url: "/user/info/",
        method: "get"
    })
}

export function updateUserInfo(data) {
    return request({
        url: "/user/info/",
        method: "post",
        data
    })
}

export function updateUserPassword(data) {
    return request({
        url: "/user/password/",
        method: "post",
        data
    })
}

export function getCaptchaCode() {
    return request({
        url: "/tools/captcha/",
        method: "get"
    })
}

export function verityCaptchaCode(data) {
    return request({
        url: "/tools/captcha/verify/",
        method: "post",
        data
    })
}