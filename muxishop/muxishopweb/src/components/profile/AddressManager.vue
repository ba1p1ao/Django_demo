<template>
    <div class="main">
        <div class="title">
            <el-button plain @click="isCreateAddress">新增收货地址</el-button>
            <span>当前地址数量为&nbsp;{{ addressList.length }}&nbsp;个最多可以设置&nbsp;25&nbsp;个</span>
        </div>
        <div class="addresslist" v-for="(item, index) in addressList" :key="index">
            <div class="addressinfo">
                <div class="address-title clearfix">
                    <span class="name fl">{{ item.signer_name }}</span>
                    <span class="district fl">&nbsp;&nbsp;{{ item.district }}&nbsp;&nbsp;</span>
                    <div :class="item.default == 1 ? 'isdefaultaddresss fl' : 'fl'">
                        <span>{{ item.default == 1 ? "&nbsp;默认地址&nbsp;" : "" }}</span>
                    </div>
                    <div class="close fr" @click="deleteAddress(item.id)"><img src="@/assets/images/profile/deletex.png"
                            alt=""></div>
                </div>
                <div class="address-table">
                    <table>
                        <tbody>
                            <tr>
                                <td class="label">收货人：</td>
                                <td>
                                    {{ item.signer_name }}
                                </td>
                            </tr>

                            <tr>
                                <td class="label">所在地区：</td>
                                <td>{{ item.district }}</td>
                            </tr>
                            <tr>
                                <td class="label">收货地：</td>
                                <td>
                                    {{ item.signer_address }}
                                </td>
                            </tr>
                            <tr>
                                <td class="label">手机号：</td>
                                <td>{{ item.telphone }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="botton-tools clearfix">
                    <div class="edit fr" @click="edit(item)"><span>编辑</span></div>
                    <div class="set-default fr" v-if="!item.default" @click="setDefault(item.id)"><span>设为默认</span>
                    </div>

                </div>
            </div>
        </div>
    </div>

    <!-- 新增收货地址弹出框 -->
    <el-dialog v-model="createAddressDialogFormVisible" title="新增收货地址" width="500">
        <el-form :model="form">
            <el-form-item label="收货人：" :label-width="formLabelWidth">
                <el-input v-model="form.signer_name" autocomplete="off" />
            </el-form-item>
            <el-form-item label="所在地区：" :label-width="formLabelWidth">
                <el-input v-model="form.district" autocomplete="off" />
            </el-form-item>
            <el-form-item label="收货地：" :label-width="formLabelWidth">
                <el-input v-model="form.signer_address" autocomplete="off" />
            </el-form-item>
            <el-form-item label="手机号：" :label-width="formLabelWidth">
                <el-input v-model="form.telphone" autocomplete="off" />
            </el-form-item>
            <el-form-item label="是否为默认地址：" :label-width="formLabelWidth">
                <el-switch v-model="form.default" inline-prompt active-text="是" inactive-text="否" />
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="createAddressDialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="createAddress">
                    提交
                </el-button>
            </div>
        </template>
    </el-dialog>


    <!-- 修改收货地址弹出框 -->
    <el-dialog v-model="updateAddressDialogFormVisible" title="修改收货地址" width="500">
        <el-form :model="form">
            <el-form-item label="收货人：" :label-width="formLabelWidth">
                <el-input v-model="form.signer_name" autocomplete="off" />
            </el-form-item>
            <el-form-item label="所在地区：" :label-width="formLabelWidth">
                <el-input v-model="form.district" autocomplete="off" />
            </el-form-item>
            <el-form-item label="收货地：" :label-width="formLabelWidth">
                <el-input v-model="form.signer_address" autocomplete="off" />
            </el-form-item>
            <el-form-item label="手机号：" :label-width="formLabelWidth">
                <el-input v-model="form.telphone" autocomplete="off" />
            </el-form-item>
            <el-form-item label="是否为默认地址：" :label-width="formLabelWidth">
                <el-switch v-model="form.default" inline-prompt active-text="是" inactive-text="否" />
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="updateAddressDialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="updateAddress">
                    提交
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script setup>
import { getUserAddress, createUserAddress, setDefaultAddress, deleteUserAddress, updateUserAddress } from '@/network/useraddress';
import { onMounted, reactive, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';

const createAddressDialogFormVisible = ref(false)
const updateAddressDialogFormVisible = ref(false)
const formLabelWidth = '140px'
const router = useRouter()


let form = reactive({
    signer_name: '',
    district: '',
    signer_address: '',
    telphone: '',
    default: false,
})

let addressList = ref([])
onMounted(() => {
    addressList.value = []
    getUserAddress().then(res => {
        // console.log(res)
        if (res.status == 70000) {
            addressList.value = res.data
        }
    })
})

const isCreateAddress = () => {
    if (addressList.value.length + 1 > 25) {
        ElMessage.warning("最多只能设置 25 个地址")
        return
    }
    createAddressDialogFormVisible.value = true
}

const createAddress = () => {
    createUserAddress(form).then(res => {
        if (res.status == 70000) {
            ElMessage.success(res.data)
            createAddressDialogFormVisible.value = false
            location.href = "/profile/?component_index=2"
        } else {
            ElMessage.error(res.data + "，请重新输入")
        }
    })
}

const deleteAddress = (id) => {
    deleteUserAddress(id).then(res => {
        if (res.status == 70000) {
            ElMessage.success(res.data)
            // addressList.value = addressList.value.filter(item => item.id !== id)
            location.href = "/profile/?component_index=2"
        } else {
            ElMessage.error(res.data)
        }
    })
}

const setDefault = (id) => {
    // console.log(id)
    setDefaultAddress(id).then(res => {
        if (res.status == 70000) {
            addressList.value.forEach((item) => {
                if (item.id == id) {
                    item.default = 1
                } else {
                    item.default = 0
                }
            })
            addressList.value.sort((a, b) => b.default - a.default)

            ElMessage.success(res.data)
        } else {
            ElMessage.error(res.data)
        }
    })
}

const edit = (item) => {
    form = reactive({
        signer_name: item.signer_name,
        district: item.district,
        signer_address: item.signer_address,
        telphone: item.telphone,
        default: item.default ? true : false,
        id: item.id
    })
    updateAddressDialogFormVisible.value = true
    console.log(form)
}

const updateAddress = () => {
    updateUserAddress(form).then(res => {
        if (res.status == 70000) {
            ElMessage.success(res.data)
            location.href = "/profile/?component_index=2"
        } else {
            ElMessage.error(res.data)
        }
    })
}




</script>

<style scoped lang="less">
.main {
    width: 100%;
    background-color: #fff !important;
    padding: 20px;

    .title {
        height: 40px;
        line-height: 40px;

        // #EFF8E6
        .el-button {
            background-color: #EFF8E6
        }

        span {
            display: inline-block;
            margin-left: 20px;
            color: #939A96;
        }
    }

    .addresslist {
        margin-top: 10px;

        .addressinfo {
            border: 2px solid #E9E9E9;
            margin: 10px 0;
            padding: 10px;

            .address-title {
                height: 20px;
                line-height: 20px;

                .name {
                    font-size: 15px;
                    font-weight: 700;
                }

                .district {
                    font-size: 15px;
                    font-weight: 700;
                }

                .isdefaultaddresss {
                    background-color: #FFAF37;
                    color: #fff;
                }

                .close {
                    img {
                        width: 20px;
                        height: 20px;
                    }

                    &:hover {
                        cursor: pointer;
                    }

                }
            }

            .address-table {
                padding: 20px;

                td {
                    padding: 2px 0;
                    font-size: 14px;
                }

                .label {
                    width: 80px;
                    text-align: right;
                    color: #9E9CA4;
                }
            }

            .botton-tools {
                color: #446070;

                .edit {
                    margin: 0 10px;

                    &:hover {
                        font-weight: 700;
                        cursor: pointer;
                        color: #9c1d1d;
                    }
                }

                .set-default {
                    margin: 0 10px;

                    &:hover {
                        font-weight: 700;
                        cursor: pointer;
                        color: #9c1d1d;
                    }
                }
            }
        }
    }
}
</style>
