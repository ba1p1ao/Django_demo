<template>
	<div class="login">
		<div class="title clearfix">
			<div class="logo fl">
				<Logo></Logo>
			</div>
			<div class="name fl">慕西商城</div>
			<div class="name fl">欢迎登录</div>
		</div>
		<div class="login-info">
			<div class="login-content">
				<div class="login-text">
					<div class="title">
						<img src="@/assets/images/login/warning.png" alt="">
						我不会以任何理由要求你转账，谨防诈骗。
					</div>
					<div class="login-name">
						账户登录
					</div>
					<div class="login-username">
						<label for="username">
							<img src="@/assets/images/login/username.png" alt="">
						</label>
						<input type="text" id="username" placeholder="请输入你的邮箱" v-model="userInfo.username">
					</div>
					<div class="login-password">
						<label for="password">
							<img src="@/assets/images/login/password.png" alt="">
						</label>
						<input type="password" id="password" placeholder="请输入密码" v-model="userInfo.password">
					</div>
					<a href="#" class="forget-password">忘记密码</a>
					<button class="login-commit" @click="login">登录</button>
					<div class="register">
						<a href="#">立即注册</a>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Logo from "@/components/common/Logo";
import {loginRequest} from "@/network/user.js";
import {useStore} from "vuex";
import { reactive } from "vue";
import {useRouter} from "vue-router";
	
	const router = useRouter();

	const store = useStore()
	let userInfo = reactive({
		username:"",
		password:""
	})
	
	const login=()=>{
		console.log(userInfo);
		loginRequest(userInfo).then(res=>{
			if(res.status==40000){
				alert("登录成功");
				window.localStorage.setItem("token",res.data.token);
				window.localStorage.setItem("username",res.data.username);
				store.commit("setIsLogin",true);
				store.commit("setUserName",res.data.username);
				router.push("/");
			}else{
				alert(res.data);
			}
		})
	}
	
</script>

<style lang="less" scoped>
	.login{
		.title{
			width: 1000px;
			margin: 0 auto;
			height: 80px;
			line-height: 80px;
			.logo{
				height: 40px;
			}
			.name{
				font-size: 30px;
				margin-left: 10px;
				margin-top: 30px;
			}
		}
		.login-info{
			margin-top: 30px;
			background-color: #e93854;
			.login-content{
				width: 990px;
				height: 475px;
				margin: 0 auto;
				background-image: url("@/assets/images/login/login-muxi.png");
				.login-text{
					margin-top: 20px;
					width: 350px;
					height: 380px;
					background-color: #fff;
					float: right;
					.title{
						background-color: #fff8f0;
						height: 40px;
						width: 350px;
						line-height: 40px;
						text-align: center;
						color: #999;
						img{
							width: 16px;
							height: 16px;
						}
					}
					.login-name{
						height: 40px;
						width: 350px;
						line-height: 40px;
						text-align: center;
						color: #e93854;
						font-size: 18px;
						font-weight: 700;
						border-bottom: 1px solid #f4f4f4;
					}
					.login-username,.login-password{
						border: 1px solid #bdbdbd;
						width: 310px;
						height: 40px;
						margin: 30px auto 0px;
						line-height: 40px;
						label{
							display: inline-block;
							background-color: #f4f4f4;
							width: 40px;
							text-align: center;
							line-height: 40px;
							border-right: 1px solid #bdbdbd;
							img {
								height: 20px;
								width: 20px;
							}
						}
						input {
							padding-left: 10px;
						}
					}
					
					.forget-password{
						display: block;
						color: #666;
						text-align: right;
						width: 310px;
						margin-top: 20px;
						margin-left: 20px;
						&:hover{
							color:#e93854;
						}
					}
					.login-commit{
						width: 310px;
						height: 35px;
						background-color: #e93854;
						color:white;
						margin-top: 20px;
						font-size: 20px;
						margin-left: 20px;
					}
					.register{
						margin-top: 20px;
						background-color: #fcfcfc;
						height: 50px;
						width: 350px;
						line-height: 50px;
						text-align: right;
						a{
							color: #e93854;
							font-size: 18px;
							margin-right: 20px;
						}
					}
				}
			}
			
			
		}
	}
</style>