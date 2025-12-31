import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, getUserInfo as getUserInfoApi } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  // 登录
  const login = async (loginForm) => {
    const res = await loginApi(loginForm)
    token.value = res.data.token
    localStorage.setItem('token', res.data.token)
    await getUserInfo()
    return res
  }

  // 获取用户信息
  const getUserInfo = async () => {
    const res = await getUserInfoApi()
    userInfo.value = res.data
    localStorage.setItem('userInfo', JSON.stringify(res.data))
    return res
  }

  // 登出
  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  return {
    token,
    userInfo,
    login,
    getUserInfo,
    logout
  }
})