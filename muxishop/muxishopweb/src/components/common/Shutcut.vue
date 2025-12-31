<template>

    <div class="wapper">
        <div class="header">
            <span v-if="$store.state.user.isLogin == false">
                <a href="/login">你好，请登录</a> <span>|</span>
                <a href="/register" class="reg" @click=register>注册</a> |
            </span>
            <span v-else>
                <a href="javascript:void(0)" @click=toProfile(1)>{{ $store.state.user.name }}， 欢迎进入幕西商城</a> <span>|</span>
                <a href="javascript:void(0)" @click=logout>退出</a> |
            </span>
            <a href="javascript:void(0)" @click=toProfile(3)>我的订单</a>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const store = useStore()
const router = useRouter()
const logout = () => {
    window.localStorage.setItem("token", "")
    window.localStorage.setItem("username", "")
    store.commit("setIsLogin", false)
    store.commit("setUsername", "")
    router.push("/")

}
const register = () => {

}

const toProfile = (index) => {
    // router.push("/profile/?component_index=" + index)
    location.href = "/profile/?component_index=" + index
}
</script>

<style lang="less" scoped>
.wapper {
    background-color: #e3e4e5;
    height: 30px;

    .header {
        width: var(--content-width);
        margin: 0 auto;
        text-align: right;
        line-height: 30px;

        a {
            color: var(--font-gray);

            &:hover {
                color: var(--font-red);
            }

            margin: 0 10px;
        }

        .reg {
            color: var(--font-red);
        }

    }
}
</style>