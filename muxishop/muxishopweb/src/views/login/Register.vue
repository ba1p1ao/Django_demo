<!-- <template>
    <div class="main">
        <div class="header clearfix">
            <div class="title fl">
                <div class="logo fl">
                    <Logo></Logo>
                </div>
                <span class="welcome fl">欢迎注册</span>
            </div>
            <div class="exist fr">
                <span>已有账号？</span>
                <a href="/login">请登录&gt;</a>
            </div>
        </div>
        <div class="line"></div>
        <div class="content">
            <div class="form-body">
                <div class="progress-bar clearfix">
                    <div class="step step-1 fl" :class="invalidEmailForm ? 'cur-step' : ''">
                        <span>1</span>
                        <p>验证手机号</p>
                    </div>
                    <div class="step-line step-line-1">
                        <span>-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;&gt;</span>
                    </div>
                    <div class="step step-2 fl" :class="invalidProfileForm ? 'cur-step' : ''">
                        <span>2</span>
                        <p>填写基本信息</p>
                    </div>
                    <div class="step-line step-line-2">
                        <span>-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;&gt;</span>
                    </div>
                    <div class="step step-3 fl" :class="invalidUserForm ? 'cur-step' : ''">
                        <span>3</span>
                        <p>注册成功</p>
                    </div>
                </div>

                <div class="invalid-email-body" v-show="invalidEmailForm">
                    <div class="item-email-wrap">
                        <el-input v-model="email" style="width: 240px;" placeholder="请输入邮箱" />
                    </div>
                    <div class="invalid-email-wrap">
                        <el-button style="width: 240px;" @click="handelInvalidEmail">验证邮箱</el-button>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import Logo from '@/components/common/Logo.vue';
import { ElMessage } from 'element-plus';
import { ref } from 'vue';

let email = ref("")
let invalidEmailForm = ref(true)
let invalidProfileForm = ref(false)
let invalidUserForm = ref(false)
const handelInvalidEmail = () => {
    invalidEmailForm.value = !invalidEmailForm.value
    invalidProfileForm.value = !invalidProfileForm.value
}
</script>

<style scoped lang="less">
.main {
    width: 100%;

    .header {
        width: var(--content-width);
        height: 110px;
        margin: 0 auto;

        .title {
            margin-top: 20px;

            .welcome {
                margin-top: 20px;
                font-size: 24px;
            }
        }

        .exist {
            margin-top: 60px;
            font-size: 16px;

            a {
                color: #e22;
                text-decoration: underline !important;
            }
        }
    }

    .line {
        border-top: 2px solid #e3e3e3;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .content {
        width: var(--content-width);
        margin: 0 auto;

        .form-body {
            margin: 80px auto 0;
            width: 400px;

            .progress-bar {
                position: relative;

                .step {
                    text-align: center;

                    span {
                        width: 24px;
                        height: 24px;
                        line-height: 24px;
                        display: inline-block;
                        border: 1px solid #ccc;
                        border-radius: 24px;
                    }

                    p {
                        display: block;
                        margin-top: 10px;
                    }
                }

                .step-2,
                .step-3 {
                    margin-left: 109px;
                }

                .cur-step {
                    color: #2FBC42;

                    span {
                        border: 1px solid #2FBC42;
                    }
                }

                .step-line {
                    position: absolute;
                    top: 5px;
                }

                .step-line-1 {
                    left: 65px;
                }

                .step-line-2 {
                    left: 235px;
                }

            }

            .invalid-email-body {
                margin-top: 50px;
                width: 400px;

                .item-email-wrap {
                    margin-top: 10px;
                    text-align: center;

                    el-input {
                        text-align: center;
                    }
                }

                .invalid-email-wrap {
                    margin-top: 10px;
                    text-align: center;
                }
            }

        }
    }

}
</style> -->



<template>
    <div class="main">
        <div class="header clearfix">
            <div class="title fl">
                <div class="logo fl">
                    <Logo></Logo>
                </div>
                <span class="welcome fl">欢迎注册</span>
            </div>
            <div class="exist fr">
                <span>已有账号？</span>
                <a href="/login">请登录&gt;</a>
            </div>
        </div>
        <div class="line"></div>
        <div class="content">
            <div class="form-body">
                <div class="progress-bar clearfix">
                    <div class="step step-1 fl" :class="invalidEmailForm ? 'cur-step' : ''">
                        <span>1</span>
                        <p>验证邮箱</p>
                    </div>
                    <div class="step-line step-line-1">
                        <span>-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;&gt;</span>
                    </div>
                    <div class="step step-2 fl" :class="invalidProfileForm ? 'cur-step' : ''">
                        <span>2</span>
                        <p>填写基本信息</p>
                    </div>
                    <div class="step-line step-line-2">
                        <span>-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;-&nbsp;&gt;</span>
                    </div>
                    <div class="step step-3 fl" :class="invalidUserForm ? 'cur-step' : ''">
                        <span>3</span>
                        <p>注册成功</p>
                    </div>
                </div>

                <!-- 第一步：验证邮箱 -->
                <div class="invalid-email-body" v-if="invalidEmailForm">
                    <div class="item-email-wrap">
                        <el-input 
                            v-model="email" 
                            style="width: 240px;" 
                            placeholder="请输入邮箱" 
                            :disabled="isSendingCode"
                        />
                    </div>
                    <div class="item-code-wrap">
                        <el-input 
                            v-model="verificationCode" 
                            style="width: 120px; margin-top: 15px; " 
                            placeholder="请输入验证码"
                            maxlength="6"
                            :disabled="isVerifyingCode"
                        />
                        <img :src="captchaImageBase64" alt="" @click="resendCode">
                    </div>
                    <div class="resend-code" v-if="countdown > 0">
                        <span class="countdown-text">{{ countdown }}秒后可重新发送</span>
                    </div>
                    <div class="resend-code" v-if="countdown === 0">
                        <el-button type="text" @click="resendCode" :disabled="isSendingCode">重新获取验证码</el-button>
                    </div>
                    <div class="invalid-email-wrap">
                        <el-button 
                            type="primary" 
                            style="width: 240px; margin-top: 20px;" 
                            @click="handleEmailStep"
                            :disabled="isSendingCode || isVerifyingCode || !email"
                            :loading="isSendingCode || isVerifyingCode"
                        >
                            {{ '完成验证' }}
                        </el-button>
                    </div>
                    
                </div>

                <!-- 第二步：填写基本信息 -->
                <div class="profile-form-body" v-else-if="invalidProfileForm">
                    <div class="form-item">
                        <el-input 
                            v-model="userForm.username" 
                            placeholder="请输入用户名"
                            clearable
                            maxlength="20"
                        >
                            <template #prefix>
                                <el-icon><User /></el-icon>
                            </template>
                        </el-input>
                        <div class="form-error" v-if="formErrors.username">{{ formErrors.username }}</div>
                    </div>
                    <div class="form-item">
                        <el-date-picker
                            style="width: 100%;"
                            v-model="userForm.birthday"
                            type="date"
                            value-format="YYYY-MM-DD"
                            placeholder="请选择生日"
                            clearable
                            :disabled-date="disabledDate"
                        />
                        <div class="form-error" v-if="formErrors.birthday">{{ formErrors.birthday }}</div>
                    </div>
                    <div class="form-item">
                        <el-input 
                            v-model="userForm.password" 
                            type="password" 
                            placeholder="请输入密码"
                            show-password
                            clearable
                            @blur="validatePassword"
                        >
                            <template #prefix>
                                <el-icon><Lock /></el-icon>
                            </template>
                        </el-input>
                        <div class="form-error" v-if="formErrors.password">{{ formErrors.password }}</div>
                    </div>
                    <div class="form-item">
                        <el-input 
                            v-model="userForm.confirmPassword" 
                            type="password" 
                            placeholder="请确认密码"
                            show-password
                            clearable
                            @blur="validateConfirmPassword"
                        >
                            <template #prefix>
                                <el-icon><Lock /></el-icon>
                            </template>
                        </el-input>
                        <div class="form-error" v-if="formErrors.confirmPassword">{{ formErrors.confirmPassword }}</div>
                    </div>
                    <div class="form-item">
                        <el-input 
                            v-model="userForm.mobile" 
                            placeholder="请输入手机号"
                            clearable
                            maxlength="20"
                            @blur="validateMobile"
                        >
                            <template #prefix>
                                <el-icon><Iphone /></el-icon>
                            </template>
                        </el-input>
                        <div class="form-error" v-if="formErrors.mobile">{{ formErrors.mobile }}</div>
                    </div>
                    <div class="form-item">
                        <el-select 
                            v-model="userForm.gender" 
                            placeholder="请选择性别"
                            style="width: 100%"
                        >
                            <el-option label="男" value="1" />
                            <el-option label="女" value="0" />
                            <el-option label="保密" value="3" />
                        </el-select>
                        <div class="form-error" v-if="formErrors.gender">{{ formErrors.gender }}</div>
                    </div>
                    <div class="form-item terms">
                        <el-checkbox v-model="agreeTerms">
                            我已阅读并同意
                            <el-link type="primary" :underline="false">《用户协议》</el-link>
                            和
                            <el-link type="primary" :underline="false">《隐私政策》</el-link>
                        </el-checkbox>
                        <div class="form-error" v-if="formErrors.terms">{{ formErrors.terms }}</div>
                    </div>
                    <div class="form-buttons">
                        <el-button 
                            type="primary" 
                            @click="handleRegister"
                            :disabled="isRegistering"
                            :loading="isRegistering"
                            style="width: 100%; margin-top: 20px; margin-left: 0;"
                        >
                            {{ isRegistering ? '注册中...' : '注册' }}
                        </el-button>
                        <el-button 
                            @click="goBackToEmail"
                            :disabled="isRegistering"
                            style="width: 100%; margin-top: 10px; margin-left: 0;"
                        >
                            返回上一步
                        </el-button>
                    </div>
                </div>

                <!-- 第三步：注册成功 -->
                <div class="success-body" v-else-if="invalidUserForm">
                    <div class="success-icon">
                        <el-icon style="font-size: 80px; color: #67C23A;">
                            <CircleCheck />
                        </el-icon>
                    </div>
                    <div class="success-message">
                        <h3>注册成功！</h3>
                        <p>恭喜您，账号 {{ email }} 注册成功</p>
                        <p>系统已向您的邮箱发送了激活链接，请及时查收</p>
                    </div>
                    <div class="success-buttons">
                        <el-button 
                            type="primary" 
                            @click="goToLogin"
                            style="width: 240px; margin-top: 30px; margin-left: 0px;"
                        >
                            立即登录
                        </el-button>
                        <el-button 
                            @click="goToHome"
                            style="width: 240px; margin-top: 10px; margin-left: 0px;"
                        >
                            返回首页
                        </el-button>
                    </div>
                    <div class="success-tips">
                        <p><el-icon><Warning /></el-icon> 温馨提示：</p>
                        <ul>
                            <li>请妥善保管您的账号密码</li>
                            <li>建议您尽快完善个人信息</li>
                            <li>如遇到问题，请联系客服</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Logo from '@/components/common/Logo.vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { ref, computed, watch, onUnmounted, onMounted } from 'vue';
import { 
    User, 
    Lock, 
    Avatar, 
    CircleCheck,
    Warning,
    Iphone
} from '@element-plus/icons-vue';
import { getCaptchaCode, verityCaptchaCode, isExistUser, registerRequest } from '@/network/user';
import { useRouter } from 'vue-router';

const router = useRouter();

// 响应式数据
const email = ref("")
const verificationCode = ref("")
// const showVerificationCode = ref(true)
const countdown = ref(0)
const countdownTimer = ref(null)

const invalidEmailForm = ref(true)
const invalidProfileForm = ref(false)
const invalidUserForm = ref(false)

// 加载状态
const isSendingCode = ref(false)
const isVerifyingCode = ref(false)
const isRegistering = ref(false)

// 验证码图片 
const captchaImageBase64 = ref("")
const captchaImageUUID = ref("")
// 用户表单数据
const userForm = ref({
    username: '',
    birthday: '',
    password: '',
    confirmPassword: '',
    mobile: '',
    gender: ''
})

// 表单错误信息
const formErrors = ref({
    username: '',
    birthday: '',
    password: '',
    confirmPassword: '',
    gender: '',
    mobile: '',
    terms: ''
})

const agreeTerms = ref(false)

// 页面加载时执行
onMounted(() => {
    getImageBase64()
})


// 计算属性：检查表单是否有效
const isFormValid = computed(() => {
    const form = userForm.value;
    return form.username && 
           form.password && 
           form.confirmPassword && 
           form.nickname && 
           form.gender &&
           form.password === form.confirmPassword &&
           agreeTerms.value;
})

// 邮箱格式验证
const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

const validateEmailExsit = (email) => {
    let request_data = {
        "email": email
    }
    let isExist = true
    isExistUser(request_data).then(res => {       
        return isExist = res.status === 40000        
    })
    return isExist
}

// 用户名验证
const validateUsername = () => {
    const username = userForm.value.username;
    if (!username) {
        formErrors.value.username = '用户名不能为空';
        return false;
    }
    if (username.length < 3 || username.length > 20) {
        formErrors.value.username = '用户名长度为3-20个字符';
        return false;
    }
    formErrors.value.username = '';
    return true;
}

// 日期禁止选择未来日期
const disabledDate = (time) => {
  return time.getTime() > Date.now()
}

// 密码验证
const validatePassword = () => {
    const password = userForm.value.password;
    if (!password) {
        formErrors.value.password = '密码不能为空';
        return false;
    }
    if (password.length < 6 || password.length > 20) {
        formErrors.value.password = '密码长度为6-20个字符';
        return false;
    }
    // 密码强度验证（可选）
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    if (!(hasUpperCase && hasLowerCase && hasNumbers)) {
        formErrors.value.password = '密码需包含大小写字母和数字';
        return false;
    }
    
    formErrors.value.password = '';
    return true;
}

// 确认密码验证
const validateConfirmPassword = () => {
    if (userForm.value.password !== userForm.value.confirmPassword) {
        formErrors.value.confirmPassword = '两次输入的密码不一致';
        return false;
    }
    formErrors.value.confirmPassword = '';
    return true;
}

// 手机号验证
const validateMobile = () => {
    const mobileRegex = /^[1](([3][0-9])|([4][0,1,4-9])|([5][0-3,5-9])|([6][2,5-7])|([7][0-8])|([8][0-9])|([9][0-3,5-9]))[0-9]{8}$/;
    if (!mobileRegex.test(userForm.value.mobile)) {
        formErrors.value.mobile = '手机号格式不正确'
        return false
    }
    formErrors.value.mobile = ''
    return true
}

const getImageBase64 = () => {
    getCaptchaCode().then(res => {
        if (res.status == 90000) {
            captchaImageBase64.value = res.data["image"]
            captchaImageUUID.value = res.data["uuid"]
            return true
        } else {
            return false
        }
    })
}

// 邮箱验证步骤处理
const handleEmailStep = async () => {
    if (!email.value) {
        ElMessage.warning('请输入邮箱地址');
        return;
    }

    // 邮箱格式验证
    if (!validateEmail(email.value)) {
        ElMessage.warning('请输入有效的邮箱地址');
        return;
    }

    // 验证验证码
    if (!verificationCode.value) {
        ElMessage.warning('请输入验证码');
        return;
    }

    if (!validateEmailExsit(email.value)) {
        ElMessage.error("邮箱已存在")
        getImageBase64()
        return;
    }

    isVerifyingCode.value = true;
    try {
        // 这里应该是验证验证码的API调用
        
        let request_data = {
            "captcha_id": captchaImageUUID.value,
            "captcha_text": verificationCode.value,
        }
        verityCaptchaCode(request_data).then(res => {
            if (res.status == 90000) {
                // 验证成功，进入下一步
                invalidEmailForm.value = false;
                invalidProfileForm.value = true;
                clearCountdown();
                ElMessage.success('邮箱验证成功');
            }
        })
        
    } catch (error) {
        ElMessage.error('验证码错误，请重试');
    } finally {
        isVerifyingCode.value = false;
    }
}

// 开始倒计时
const startCountdown = () => {
    countdown.value = 5;
    clearCountdown(); // 清除之前的定时器
    countdownTimer.value = setInterval(() => {
        if (countdown.value > 0) {
            countdown.value--;
        } else {
            clearCountdown();
        }
    }, 1000);
}

// 清除倒计时
const clearCountdown = () => {
    if (countdownTimer.value) {
        clearInterval(countdownTimer.value);
        countdownTimer.value = null;
    }
}

// 重新发送验证码
const resendCode = async () => {
    if (countdown.value > 0) return;
    
    isSendingCode.value = true;
    try {
        // 重新发送验证码的API调用
        // await resendVerificationCode(email.value);
        getImageBase64();

        startCountdown();
        // ElMessage.success('验证码已重新发送');
    } catch (error) {
        ElMessage.error('发送失败，请重试');
    } finally {
        isSendingCode.value = false;
    }
}

// 返回上一步（邮箱验证）
const goBackToEmail = () => {
    invalidProfileForm.value = false;
    invalidEmailForm.value = true;
    verificationCode.value = "";
    clearCountdown();
}

// 注册处理
const handleRegister = async () => {
    // 验证所有字段
    const validations = [
        validateUsername(),
        validatePassword(),
        validateConfirmPassword(),
        validateMobile()
    ];
    console.log(userForm.value)
    console.log(validations)
    
    if (!userForm.value.gender) {
        formErrors.value.gender = '请选择性别';
        validations.push(false);
    } else {
        formErrors.value.gender = '';
    }
    
    if (!agreeTerms.value) {
        formErrors.value.terms = '请阅读并同意用户协议和隐私政策';
        validations.push(false);
    } else {
        formErrors.value.terms = '';
    }
    
    if (validations.includes(false)) {
        ElMessage.warning('请正确填写所有信息');
        return;
    }

    let requestData = {
        email: email.value,
        name: userForm.value.username,
        birthday: userForm.value.birthday,
        mobile: userForm.value.mobile,
        gender: userForm.value.gender,
        password: userForm.value.password
    }

    isRegistering.value = true;
    try {
        // 这里应该是注册的API调用
        // await register({
        //     email: email.value,
        //     ...userForm.value
        // });
        registerRequest(requestData).then(res => {
            if (res.status == 40000) {
                ElMessage.success("注册成功")
                // 注册成功，进入第三步
                invalidProfileForm.value = false;
                invalidUserForm.value = true;
            } else {
                isRegistering.value = false
                ElMessage.error(res.data)
                return
            }
        })
        
    } catch (error) {
        ElMessage.error('注册失败，请重试');
    } finally {
        isRegistering.value = false;
    }
}

// 跳转到登录页
const goToLogin = () => {
    router.push('/login');
}

// 跳转到首页
const goToHome = () => {
    router.push('/');
}

// 监听邮箱变化
watch(email, (newVal) => {
    clearCountdown();
    verificationCode.value = "";
})

// 监听表单字段变化，清除对应的错误信息
watch(() => userForm.value.username, () => {
    if (formErrors.value.username) validateUsername();
});

watch(() => userForm.value.password, () => {
    if (formErrors.value.password) validatePassword();
    if (formErrors.value.confirmPassword) validateConfirmPassword();
});

watch(() => userForm.value.confirmPassword, () => {
    if (formErrors.value.confirmPassword) validateConfirmPassword();
});

watch(() => userForm.value.nickname, () => {
    if (formErrors.value.nickname) validateNickname();
});

watch(() => userForm.value.gender, () => {
    if (formErrors.value.gender) formErrors.value.gender = '';
});

watch(() => agreeTerms.value, () => {
    if (formErrors.value.terms) formErrors.value.terms = '';
});

// 组件卸载时清除定时器
onUnmounted(() => {
    clearCountdown();
})
</script>

<style scoped lang="less">
.main {
    width: 100%;
    min-height: 100vh;
    background-color: #f5f5f5;

    .header {
        width: var(--content-width);
        height: 110px;
        margin: 0 auto;

        .title {
            margin-top: 20px;

            .welcome {
                margin-top: 20px;
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }
        }

        .exist {
            margin-top: 60px;
            font-size: 16px;
            color: #666;

            a {
                color: #e22;
                text-decoration: underline !important;
                margin-left: 5px;

                &:hover {
                    color: #c11;
                }
            }
        }
    }

    .line {
        border-top: 2px solid #e3e3e3;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .content {
        width: var(--content-width);
        margin: 0 auto;

        .form-body {
            margin: 80px auto 0;
            width: 400px;
            background: white;
            border-radius: 8px;
            padding: 40px;
            box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

            .progress-bar {
                position: relative;
                margin-bottom: 40px;

                .step {
                    text-align: center;
                    z-index: 2;
                    position: relative;

                    span {
                        width: 30px;
                        height: 30px;
                        line-height: 30px;
                        display: inline-block;
                        border: 2px solid #ccc;
                        border-radius: 50%;
                        background: white;
                        font-size: 14px;
                        transition: all 0.3s;
                    }

                    p {
                        display: block;
                        margin-top: 10px;
                        font-size: 14px;
                        color: #666;
                        transition: all 0.3s;
                    }
                }

                .step-2,
                .step-3 {
                    margin-left: 102px;
                }

                .cur-step {
                    span {
                        border-color: #2FBC42;
                        background-color: #2FBC42;
                        color: white;
                    }

                    p {
                        color: #2FBC42;
                        font-weight: bold;
                    }
                }

                .step-line {
                    position: absolute;
                    top: 10px;
                    color: #ccc;
                    font-size: 12px;
                    z-index: 1;
                }

                .step-line-1 {
                    left: 60px;
                }

                .step-line-2 {
                    left: 230px;
                }
            }

            .invalid-email-body,
            .profile-form-body,
            .success-body {
                text-align: center;
            }

            .invalid-email-body {
                // .item-email-wrap,
                // .item-code-wrap {
                //     // margin-bottom: 15px;
                    
                // }
                .item-code-wrap {
                    text-align: left;
                    padding-left: 80px;
                   img {
                        margin-top: 15px;
                        margin-left: 20px;
                        width: 100px;
                        height: 30px;
                    }
                }

                .resend-code {
                    height: 25px;
                    margin-top: 10px;
                    text-align: right;
                    padding-right: 85px;
                    font-size: 12px;
                    
                    .countdown-text {
                        line-height: 25px;
                        color: #999;
                    }

                    :deep(.el-button) {
                        font-size: 12px;
                        padding: 0;
                    }
                }
            }

            .profile-form-body {
                .form-item {
                    margin-bottom: 15px;

                    &:deep(.el-input__wrapper) {
                        padding: 0 10px;
                    }

                    &:deep(.el-select) {
                        width: 100%;
                    }

                }

                .form-error {
                    color: #f56c6c;
                    font-size: 12px;
                    text-align: left;
                    margin-top: 4px;
                    min-height: 18px;
                }

                .terms {
                    text-align: left;
                    margin-top: 20px;
                    font-size: 13px;

                    &:deep(.el-checkbox) {
                        width: 100%;
                    }

                    &:deep(.el-link) {
                        margin: 0 2px;
                    }
                }

                .form-buttons {
                    margin-top: 10px;
                }
            }

            .success-body {
                .success-icon {
                    margin-bottom: 30px;
                }

                .success-message {
                    h3 {
                        color: #2FBC42;
                        font-size: 24px;
                        margin-bottom: 15px;
                    }

                    p {
                        color: #666;
                        margin: 8px 0;
                        font-size: 14px;
                    }
                }

                .success-tips {
                    margin-top: 30px;
                    padding: 15px;
                    background-color: #f8f9fa;
                    border-radius: 6px;
                    text-align: left;
                    font-size: 13px;

                    p {
                        color: #333;
                        margin-bottom: 10px;
                        font-weight: bold;

                        .el-icon {
                            color: #E6A23C;
                            margin-right: 5px;
                        }
                    }

                    ul {
                        margin: 0;
                        padding-left: 20px;
                        color: #666;

                        li {
                            margin: 5px 0;
                        }
                    }
                }
            }
        }
    }
}

</style>    