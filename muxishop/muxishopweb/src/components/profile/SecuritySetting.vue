<template>
    <div class="main">
        <div class="title">
            <span>修改密码</span>
        </div>
        <div class="security-info">
            <table class="info-table">
                <tbody>
                    <tr>
                        <td class="label">原密码</td>
                        <td class="value">
                            <el-input type="password" v-model="oldpassword" style="width: 300px" placeholder="请输入原密码"
                                show-password />
                        </td>
                    </tr>
                    <tr>
                        <td class="label">密码</td>
                        <td class="value">
                            <el-input type="password" v-model="password1" style="width: 300px" placeholder="请输入新密码"
                                show-password />
                        </td>
                    </tr>
                    <tr>
                        <td class="label">确认密码</td>
                        <td class="value">
                            <el-input type="password" v-model="password2" style="width: 300px" placeholder="再次输入新密码"
                                show-password />
                        </td>
                    </tr>
                    <tr>
                        <td></td>
                        <td class="actions">
                            <el-button type="primary" size="default" @click="handleSave">保存修改</el-button>
                            <el-button size="default" @click="handleReset">取消</el-button>
                        </td>
                    </tr>
                </tbody>

            </table>
        </div>
    </div>
</template>

<script setup>
import { updateUserPassword } from '@/network/user';
import { onActivated, onMounted, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

let oldpassword = ref("")
let password1 = ref("")
let password2 = ref("")

const store = useStore()
const router = useRouter()
const handleSave = () => {
    if (password1.value != password2.value) {
        ElMessage.warning("密码不一致，请重新输入")
        return
    }
    if (password1.value == "" || password2.value == "" || oldpassword.value == "") {
        ElMessage.warning("密码不能为空")
        return
    }

    let data = {
        oldpassword: oldpassword.value,
        password: password1.value
    }
    console.log('asdf')
    updateUserPassword(data).then(res => {
        console.log(res)
        if (res.status == 40000) {
            ElMessage.success(res.data + "，请重新登录")
            window.localStorage.setItem("token", "")
            window.localStorage.setItem("username", "")
            store.commit("setIsLogin", false)
            store.commit("setUsername", "")
            router.push("/")
        } else {
            ElMessage.error(res.data)
        }

    })

}

const handleReset = () => {
    password1.value = ""
    password2.value = ""
}

</script>

<style scoped lang="less">
.main {
    width: 100%;

    .title {
        background-color: #fff;
        height: 60px;
        line-height: 60px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 600;
        padding-left: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        color: #333;
    }

    .security-info {
        background-color: #fff;
        border-radius: 8px;
        padding: 30px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

        .info-table {
            width: 100%;

            tr {
                height: 60px;
                border-bottom: 1px solid #f0f0f0;

                &:last-child {
                    border-bottom: none;
                }
            }

            .label {
                width: 80px;
                padding-right: 20px;
                font-size: 15px;
                color: #666;
                font-weight: 500;
                text-align: right;
            }

            .value {
                padding: 15px 0;

                :deep(.el-input__wrapper) {
                    border-radius: 6px;

                    &.is-focus {
                        box-shadow: 0 0 0 1px #DB2E16;
                    }
                }
            }

            .actions {
                padding-top: 30px;

                .el-button {
                    margin-right: 15px;
                    border-radius: 6px;
                    padding: 10px 24px;

                    &.el-button--primary {
                        background-color: #DB2E16;
                        border-color: #DB2E16;

                        &:hover {
                            background-color: #c02914;
                            border-color: #c02914;
                        }
                    }
                }
            }
        }
    }
}
</style>