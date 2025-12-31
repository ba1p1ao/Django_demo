<template>
    <div class="main">
        <div class="title">
            <span>修改个人信息</span>
        </div>
        <div class="basic-info">
            <table class="info-table">
                <tbody>
                    <tr>
                        <td class="label">昵称</td>
                        <td class="value">
                            <el-input v-model="userInfo.name" style="width: 300px" placeholder="请输入昵称" />
                            <div class="form-error" v-if="userInfoError.name">{{ userInfoError.name}}</div>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="label">邮箱</td>
                        <td class="value">
                            <el-input v-model="userInfo.email" style="width: 300px" placeholder="请输入邮箱" />
                            <div class="form-error" v-if="userInfoError.email">{{ userInfoError.email}}</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="label">手机号</td>
                        <td class="value">
                            <el-input v-model="userInfo.mobile" style="width: 300px" placeholder="请输入手机号" />
                            <div class="form-error" v-if="userInfoError.mobile">{{ userInfoError.mobile}}</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="label">性别</td>
                        <td class="value">
                            <el-radio-group v-model="userInfo.gender">
                                <el-radio label="0">女</el-radio>
                                <el-radio label="1">男</el-radio>
                                <el-radio label="3">保密</el-radio>
                            </el-radio-group>
                        </td>
                    </tr>
                    <tr>
                        <td class="label">生日</td>
                        <td class="value">
                            <el-date-picker v-model="userInfo.birthday" type="date" placeholder="选择生日"
                                :disabled-date="disabledDate" style="width: 300px" />
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
import { getUserInfo, updateUserInfo } from '@/network/user';
import { onMounted, ref, watch } from 'vue';
import { ElMessage } from 'element-plus';
import dayjs from 'dayjs'


// 表单数据
const userInfo = ref({
    name: '',
    email: '',
    mobile: '',
    gender: '0',
    birthday: ''
})

// 错误表单数据
const userInfoError = ref({
    name: '',
    email: '',
    mobile: '',
    gender: '0',
    birthday: ''
})

// 用于重置的数据
const originalData = ref({})
// 用于显示的数据
onMounted(() => {
    getUserInfo().then(res => {
        if (res.status == 40000) {
            originalData.value = res.data

            let birthdayDate = null
            if (res.data.birthday) {
                // 去除时间部分，只保留日期
                const dateStr = res.data.birthday.split(' ')[0]
                birthdayDate = dateStr
            }
            originalData.value.birthday = birthdayDate
            userInfo.value = {
                name: res.data.name || '',
                email: res.data.email || '',
                mobile: res.data.mobile || '',
                gender: res.data.gender || '0',
                birthday: birthdayDate
            }
        } else {
            ElMessage.error('获取用户信息失败')
        }
    })
})

// 禁止选择未来的日期
const disabledDate = (time) => {
    return time.getTime() > Date.now()
}
// 表单验证
const validateForm = () => {
    if (!userInfo.value.name?.trim()) {
        ElMessage.warning('请输入昵称')
        return false
    }

    if (!userInfo.value.email?.trim()) {
        ElMessage.warning('请输入邮箱')
        return false
    }

    // 简单的邮箱格式验证
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(userInfo.value.email)) {
        ElMessage.warning('请输入正确的邮箱格式')
        return false
    }

    if (!userInfo.value.mobile?.trim()) {
        ElMessage.warning('请输入手机号')
        return false
    }

    // 手机号格式验证
    const mobileRegex = /^1[3-9]\d{9}$/
    if (!mobileRegex.test(userInfo.value.mobile)) {
        ElMessage.warning('请输入正确的手机号格式')
        return false
    }

    return true
}
const handleReset = () => {
    let birthdayDate = null
    if (originalData.value.birthday) {
        const dateStr = originalData.value.birthday.split(' ')[0]
        birthdayDate = dateStr
    }

    userInfo.value = {
        name: originalData.value.name || '',
        email: originalData.value.email || '',
        mobile: originalData.value.mobile || '',
        gender: originalData.value.gender || '0',
        birthday: birthdayDate
    }
}
const hasDataChanged = () => {
    if (userInfo.value.birthday != originalData.value.birthday ||
        userInfo.value.email != originalData.value.email ||
        userInfo.value.gender != originalData.value.gender ||
        userInfo.value.mobile != originalData.value.mobile ||
        userInfo.value.name != originalData.value.name
    ) {
        return true
    }
    return false
}

const handleSave = () => {
    if (!validateForm() || !hasDataChanged()) return

    // 准备提交的数据
    const submitData = {
        name: userInfo.value.name,
        email: userInfo.value.email,
        mobile: userInfo.value.mobile,
        gender: userInfo.value.gender,
        birthday: userInfo.value.birthday ? dayjs(userInfo.value.birthday).format('YYYY-MM-DD') : ''
    }

    // console.log('提交数据:', submitData);

    updateUserInfo(submitData).then(res => {
        if (res.status == 40000) {
            ElMessage.success(res.data)
            // 更新原始数据
            originalData.value = { ...originalData.value, ...submitData }
        } else {
            ElMessage.error(res.data)
        }
    })
}

const validatename = () => {
    const username = userInfo.value.name;
    // 定义需要检测的特殊字符集合
    const specialChars = '!@#$%^&*()_+=[]{}|;:,.<>?`~-';
    // 1. 非空校验
    if (!username) {
        userInfoError.value.name = '用户名不能为空';
        return false;
    }
    // 2. 可选：用户名长度校验（比如2-20位，可根据需求调整）
    if (username.length < 2 || username.length > 20) {
        userInfoError.value.name = '用户名长度需在2-20位之间';
        return false;
    }
    // 3. 特殊字符检测
    // 转义正则特殊字符（如^、$、\等），避免正则语法错误
    const escapedChars = specialChars.replace(/[\\^$.*+?|()\[\]{}]/g, '\\$&');
    const specialCharReg = new RegExp(`[${escapedChars}]`);
    if (specialCharReg.test(username)) {
        userInfoError.value.name = `用户名不能包含${specialChars}等特殊字符`;
        return false;
    }

    // 4. 所有验证通过：清空错误提示，返回true
    userInfoError.value.name = '';
    return true;
}

const validateemail = () => {
    const email = userInfo.value.email

    if (!email) {
        userInfoError.value.email = '邮箱不能为空'
        return false
    }

    // 简单的邮箱格式验证
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
        userInfoError.value.email = '邮箱格式有误'
        return false
    }
    userInfoError.value.email = ''
    return true
}

const validatemobile = () => {
    const mobile = userInfo.value.mobile
    if (!mobile) {
        userInfoError.value.mobile = '手机号信息不能为空'
        return false
    }
    const mobileRegex = /^1[3-9]\d{9}$/
    if (!mobileRegex.test(mobile)) {
        userInfoError.value.mobile = '手机号格式有误'
        return false
    }
    userInfoError.value.mobile = ''
    return true
}

watch(() => userInfo.value.name, () => {
    validatename()
})

watch(() => userInfo.value.email, () => {
    validateemail()
})

watch(() => userInfo.value.mobile, () => {
    validatemobile()
})

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

    .basic-info {
        background-color: #fff;
        border-radius: 8px;
        padding: 30px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

        .info-table {
            width: 100%;
            position: relative;
            .form-error {
                position: absolute;
                margin-top: 5px;
                color: red;
            }
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