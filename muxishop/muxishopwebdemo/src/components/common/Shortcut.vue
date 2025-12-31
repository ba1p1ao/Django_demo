<template>
	<div class="warpper">
		<div class="header">
			<span v-if="isLogin == false">
				<a href="/login">你好,请登录</a>
				<a href="#" class="reg">免费注册</a> &nbsp;&nbsp;|
			</span>
			<span v-else>
				<a href="/profile?activeIndex=1">{{ username }},欢迎进入慕西商城</a>
				<a href="#" @click="logout">退出</a> &nbsp;&nbsp;|
			</span>
			<a href="/profile?activeIndex=3">我的订单</a>

		</div>

	</div>
</template>

<script setup>
import { useStore } from "vuex";
import { reactive } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useStore();
const isLogin = store.state.user.isLogin;
const username = store.state.user.name;
const logout = () => {
	window.localStorage.setItem("token", "");
	store.commit("setIsLogin", false);
	router.push("/");
}
</script>

<style lang="less" scoped>
.warpper {
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

			margin-left: 10px;
		}

		.reg {
			color: var(--font-red);
		}
	}
}
</style>