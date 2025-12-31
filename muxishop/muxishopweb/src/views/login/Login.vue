<template>
    <div class="main">
        <div class="title clearfix">
            <div class="log fl">
                <Logo></Logo>
            </div>
            <div class="welcome fl">欢迎登录</div>
        </div>
        <div class="login-info">
            <div class="login-content clearfix">
                <div class="login-image fl">
                    <img src="@/assets/images/login/login-muxi.png" alt="">
                </div>
                <div class="login-text fl">
                    <div class="login-title">
                        <img src="@/assets/images/login/warning.png" alt="">
                        我不会以任何理由要求你转账，谨防诈骗。
                    </div>
                    <div class="login-name">账户登录</div>
                    <div class="login-username clearfix">
                        <label for="username">
                            <div class="user-image fl">
                                <img src="@/assets/images/login/username.png" alt=""></img>
                            </div>

                            <input type="text" id="username" placeholder="请输入邮箱" v-model="userInfo.username">
                        </label>
                    </div>
                    <div class="login-password clearfix">
                        <label for="password">
                            <div class="password-image fl">
                                <img src="@/assets/images/login/password.png" alt="">
                            </div>
                            <input type="password" id="password" placeholder="请输入密码" v-model="userInfo.password">
                        </label>
                    </div>
                    <div class="forget-passwrod">
                        <a href="javascript:void(0)">忘记密码</a>
                    </div>

                    <button class="login-commint" @click="login">登&nbsp;&nbsp;&nbsp;&nbsp;录</button>
                    <div class="register">
                        <a href="/register" @click="register">
                            <span>&nbsp;&gt;&nbsp;</span>
                            立即注册
                        </a>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import Logo from '@/components/common/Logo.vue';
import { reactive } from 'vue';
import { loginRequest } from '@/network/user';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore()
const router = useRouter()
let userInfo = reactive({
    username: "",
    password: "",
})
function login() {
    console.log(userInfo)
    loginRequest(userInfo).then(res => {
        console.log(res.data)
        console.log(res.status)
        if (res.status == 40000) {
            alert("登录成功")
            window.localStorage.setItem("token", res.data.token)
            window.localStorage.setItem("username", res.data.username)
            store.commit("setIsLogin", true)
            store.commit("setUsername", res.data.username)
            router.push("/")
        } else {
            alert(res.data)
        }
    })
}
function register() {

}
</script>


<style scoped lang="less">
.main {
    .title {
        width: var(--content-width);
        margin: 0 auto;

        img {
            margin-left: 100px;
            width: 100px;
            height: 100px;
        }

        .welcome {
            margin-left: 50px;
            height: 100px;
            line-height: 100px;
            font-size: 30px;
        }
    }

    .login-info {
        height: 500px;
        background-color: #EA3553;

        .login-content {
            position: relative;
            margin: 0 auto;
            width: var(--content-width);

            .login-image {
                img {
                    width: 1000px;
                    height: 500px;
                }

            }

            .login-text {
                margin-top: 30px;
                position: absolute;
                left: 800px;
                width: 350px;
                height: 400px;
                background-color: #fff;

                .login-title {
                    height: 40px;
                    line-height: 40px;
                    text-align: center;
                    background-color: #FFF8EE;
                    color: #9E9993;

                    img {
                        width: 20px;
                        height: 20px;
                    }

                    font-size: 12px;
                }

                .login-name {
                    height: 60px;
                    line-height: 60px;
                    text-align: center;
                    color: #EF958B;
                    font-size: 18px;
                    font-weight: 700;

                    &:hover {
                        cursor: pointer;
                    }
                }

                .login-username {
                    border: 1px solid #cacaca;
                    margin: 20px auto;
                    width: 310px;
                    height: 40px;
                    line-height: 40px;

                    .user-image {
                        width: 40px;
                        background-color: #F3F3F3;
                        text-align: center;
                        border-right: 1px solid #cacaca;

                        img {
                            width: 17px;
                            height: 17px;
                        }
                    }

                    input {
                        margin-left: 10px;
                    }

                }

                .login-password {
                    border: 1px solid #cacaca;
                    margin: 20px auto;
                    width: 310px;
                    height: 40px;
                    line-height: 40px;

                    .password-image {
                        width: 40px;
                        background-color: #F3F3F3;
                        text-align: center;
                        border-right: 1px solid #cacaca;

                        img {
                            width: 17px;
                            height: 17px;
                        }
                    }

                    input {
                        margin-left: 10px;
                    }
                }

                .forget-passwrod {
                    margin: 0 auto;
                    width: 310px;
                    text-align: right;
                }

                .login-commint {
                    margin: 25px 25px;
                    width: 300px;
                    height: 35px;
                    background-color: #F3473C;
                    color: #fff;
                    font-size: 20px;
                    border: 1px solid #9E9993;

                    &:hover {
                        background-color: #d61d3c;
                    }

                    &:active {
                        background-color: #C81030;
                    }
                }

                .register {
                    width: 350px;
                    height: 54px;
                    background-color: #FBFBFB;
                    text-align: right;

                    a {
                        display: inline-block;
                        margin-right: 25px;
                        line-height: 54px;
                        color: #7E403A;
                        font-size: 14px;

                        span {
                            // display: inline-block;
                            background-color: #F14B3F;
                            color: #fff;
                            width: 15px;
                            height: 15px;
                            border-radius: 15px;
                            align-items: center;
                        }
                    }

                }
            }
        }
    }
}
</style>