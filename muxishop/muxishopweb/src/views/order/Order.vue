<template>
    <div class="main">
        <Shutcut></Shutcut>
        <div class="order">
            <div class="header">
                <div class="title clearfix">
                    <div class="log fl">
                        <Logo></Logo>
                    </div>
                    <div class="name fl">订单结算</div>
                </div>

            </div>
            <div class="content">

                <div class="order-info-title">
                    填写并核对订单信息
                </div>

                <div class="order-info-content">
                    <div class="signer-info">
                        <div class="signer-info-title clearfix">
                            <h3 class="fl">收货人信息</h3>
                            <a href="javascript:void(0)" class="fr">新增收货地址</a>
                        </div>
                        <div class="address-info">

                            <div class="address-div" v-show="!showAddressList">
                                <span :class="selectedAddress.selected == 1 ? 'signer-name selected' : 'signer-name'">
                                    {{ selectedAddress.signer_name }}&nbsp;&nbsp;{{ selectedAddress.district }}
                                </span>
                                <span class="address-signer-name">{{ selectedAddress.signer_name }}</span>
                                <span class="address-signer-address">{{ selectedAddress.signer_address }}</span>
                                <span class="address-district">{{ selectedAddress.district }}</span>
                                <span class="address-telphone">{{ selectedAddress.telphone }}</span>
                                <span class="address-default" v-show="selectedAddress.default == 1">
                                    &nbsp;默认地址&nbsp;
                                </span>
                            </div>
                            <el-scrollbar height="150px" v-show="showAddressList">
                                <div class="address-div" v-for="(addressItem, index) in allAddress" :key="index">
                                    <span :class="addressItem.selected == 1 ? 'signer-name selected' : 'signer-name'"
                                        @click="changeselectedAddress(addressItem.id)">
                                        {{ addressItem.signer_name }}&nbsp;&nbsp;{{ addressItem.district }}
                                    </span>
                                    <span class="address-signer-name">{{ addressItem.signer_name }}</span>
                                    <span class="address-signer-address">{{ addressItem.signer_address }}</span>
                                    <span class="address-district">{{ addressItem.district }}</span>
                                    <span class="address-telphone">{{ addressItem.telphone }}</span>
                                    <span class="address-default" v-show="addressItem.default == 1">
                                        &nbsp;默认地址&nbsp;
                                    </span>
                                </div>
                            </el-scrollbar>
                            <span class="show-address-list" @click="showAddressList = !showAddressList">{{
                                !showAddressList ? "显示其他地址↓" : "收起地址↑"
                            }}</span>
                        </div>
                    </div>
                    <hr>
                    <div class="pay-mode">
                        <div class="step-title">
                            <h3>支付方式</h3>
                        </div>
                        <div class="pay-mode-content">
                            <div class="pay-mode-info selected">
                                <a href="javascript:void(0)">支付宝支付</a>
                            </div>
                        </div>

                    </div>
                    <hr>
                    <div class="goods-info">
                        <div class="goods-info-title">
                            <h3>送货清单</h3>
                        </div>
                        <div class="goods-detail clearfix" v-for="(goodsItem, goodsIndex) in goodsList"
                            :key="goodsIndex">
                            <div class="left fl">
                                <h3>配送方式</h3>
                                <div class="selected">
                                    <span>京东快递</span>
                                </div>
                                <div>
                                    <i>标&nbsp;&nbsp;准&nbsp;&nbsp;达:</i>
                                    <i>&nbsp;预计&nbsp;{{ getGoodsTime(orderInfo.create_time) }}&nbsp;送达&nbsp;</i>
                                </div>

                            </div>

                            <div class="right fl">
                                <h3>商家：{{ goodsItem.shop_name }}</h3>
                                <div>
                                    <span class="goods-img"><img :src="goodsItem.image" alt=""></span>
                                    <span class="goods-name dian3">{{ goodsItem.name }}</span>
                                    <span class="goods-price">￥{{ goodsItem.p_price }}</span>
                                    <span class="goods-num">×{{ goodsItem.goods_num }}</span>
                                </div>
                            </div>
                        </div>

                    </div>

                </div>

            </div>
            <div class="bottom">
                <div class="order-amount"><span>应付总额：<b>￥{{ orderInfo.order_amount }}</b></span></div>
                <div class="address">
                    <span class="qisongdi">寄送地: {{ selectedAddress.district }} {{ selectedAddress.signer_address }}
                    </span>
                    <span class="shouhuoren">收货人: {{ selectedAddress.signer_name }} {{ selectedAddress.telphone
                        }}</span>
                </div>

            </div>
            <div class="submit fr" @click="submitOrder">
                <span>提交订单</span>
            </div>
        </div>
    </div>
</template>

<script setup>
import Shutcut from '@/components/common/Shutcut.vue';
import Logo from '@/components/common/Logo.vue';
import ShopCart from '@/components/home/ShopCart.vue';
import { onMounted, ref } from 'vue';
import { getUserAddress } from '@/network/useraddress';
import { getOrderByTradeNoData } from '@/network/order';
import { useRoute, useRouter } from 'vue-router';
import { updateOrderData } from '@/network/order';
import OrderPay from './OrderPay.vue';


const route = useRoute()
const router = useRouter()

let allAddress = ref([])
let orderInfo = ref({})
let goodsList = ref([])
let tradeNo = ref()
let selectedAddress = ref({})
let showAddressList = ref(false)

onMounted(() => {
    tradeNo.value = route.params.trade_no
    getUserAddress().then(res => {
        allAddress.value = res.data
        console.log(allAddress.value)
        getselectedAddress(allAddress)
    })

    getOrderByTradeNoData(tradeNo.value).then(res => {
        orderInfo.value = res.data
        goodsList.value = orderInfo.value["order_goods"]
        console.log(orderInfo.value)
    })
})
const getselectedAddress = (allAddress) => {
    for (let i in allAddress.value) {
        if (allAddress.value[i].default == 1) {
            selectedAddress.value = allAddress.value[i]
            selectedAddress.value.selected = 1
            break
        }
    }
}

const changeselectedAddress = (id) => {
    for (let i in allAddress.value) {

        if (allAddress.value[i].id == id) {
            selectedAddress.value = allAddress.value[i]
            allAddress.value[i].selected = 1
        } else {
            allAddress.value[i].selected = 0
        }
    }
}


const getGoodsTime = (createTime) => {
    let date = createTime.split(" ")[0].split("-")
    // 获取物流时间，假设6天
    let year = parseInt(date[0], 10)
    let month = parseInt(date[1], 10)
    let day = parseInt(date[2], 10)
    day += 6
    return month + "月" + day + "日"
}

const submitOrder = () => {
    let data = {
        trade_no: tradeNo.value,
        address_id: selectedAddress.value.id,
        pay_status: 1,
    }
    updateOrderData(data).then(res => {
        if (res.status == 60000) {
            router.push({
                name: "OrderPay",
                query: {
                    tradeNo: tradeNo.value,
                    orderAmount: orderInfo.value["order_amount"]
                }
            })
        }
    })
}



</script>

<style scoped lang="less">
.main {
    height: 100%;
}

.order {
    width: 1000px;
    margin: 0 auto;

    .header {
        .title {
            height: 80px;
            line-height: 80px;


            img {
                width: 80px;
                height: 80px;
            }

            .name {
                margin-left: 50px;
                font-size: 30px;
                font-weight: 700;
                color: #000;
            }
        }
    }

    .content {

        margin-top: 10px;

        .order-info-title {
            text-align: left;
            font-size: 16px;
        }

        .order-info-content {

            hr {
                width: 980px;
                margin: 10px 0;
            }

            padding: 10px;
            margin-top: 10px;
            border: 1px solid #f0f0f0;
            border-radius: 5px;

            .signer-info {
                .signer-info-title {
                    h3 {
                        font-size: 14px;
                        font-weight: 700;
                    }

                    a {
                        color: #005ea7;

                        &:hover {
                            cursor: pointer;
                            color: #F14A3C;
                        }
                    }
                }


                .address-info {

                    .address-div {
                        margin: 5px 0;

                        .selected {
                            cursor: pointer;
                            border: 2px solid #F14A3C;
                            border-radius: 5px;
                            background-image: url("@/assets/images/order/address-selected.png");
                            background-position: 103%;
                            background-repeat: no-repeat;
                            background-size: 35px;
                        }
                    }

                    .show-address-list {
                        margin-top: 20px;

                        &:hover {
                            cursor: pointer;
                        }
                    }

                    padding: 10px;

                    .signer-name {
                        border: 2px solid #ddd;
                        border-radius: 5px;
                        text-align: center;
                        width: 100px;
                        height: 30px;
                        line-height: 30px;

                        &:hover {
                            cursor: pointer;
                        }
                    }

                    .selected {
                        border: 2px solid #F14A3C;
                        border-radius: 5px;
                        text-align: center;
                        width: 100px;
                    }


                    span {
                        display: inline-block;
                        height: 30px;
                        line-height: 30px;
                        margin: 5px 10px;
                    }

                    .address-default {
                        background-color: #989898;
                        color: #fff;
                    }
                }
            }

            .pay-mode {

                h3 {
                    font-size: 14px;
                    font-weight: 700;
                }


                .pay-mode-content {
                    padding: 10px;

                    .pay-mode-info {
                        margin: 5px 10px;
                        width: 100px;
                        height: 30px;
                        line-height: 30px;
                        text-align: center;
                        border: 2px solid #d4d4d4;
                        border-radius: 5px;

                        &:hover {
                            cursor: pointer;
                            border: 2px solid #F14A3C;
                            border-radius: 5px;
                        }
                    }

                    .selected {
                        cursor: pointer;
                        border: 2px solid #F14A3C;
                        border-radius: 5px;
                        background-image: url("@/assets/images/order/address-selected.png");
                        background-position: 103%;
                        background-repeat: no-repeat;
                        background-size: 35px;
                    }
                }



            }

            .goods-info {
                h3 {
                    font-size: 14px;
                    font-weight: 700;
                }

                .goods-detail {
                    padding: 10px;
                    height: 150px;

                    .left {
                        width: 300px;
                        height: 100%;
                        background-color: #f7f7f7;

                        h3,
                        div {
                            margin-top: 10px;
                            margin-left: 10px;
                        }

                        .selected {
                            font-weight: 700;
                            width: 100px;
                            height: 30px;
                            line-height: 30px;
                            text-align: center;
                            cursor: pointer;
                            border: 2px solid #F14A3C;
                            border-radius: 5px;
                            background-image: url("@/assets/images/order/address-selected.png");
                            background-position: 103%;
                            background-repeat: no-repeat;
                            background-size: 35px;

                        }
                    }

                    .right {
                        width: 657px;
                        height: 100%;
                        background-color: #F4FAFD;

                        h3,
                        div {
                            margin-top: 10px;
                            margin-left: 10px;
                        }

                        img {
                            width: 85px;
                            height: 85px;
                        }

                        span {
                            display: inline-block;
                        }

                        .goods-img {
                            border: 1px solid #a8a8a8;
                            border-radius: 5px;
                            padding: 5px;
                            background-color: #fff;
                        }

                        .goods-name {
                            width: 400px;
                            margin-left: 10px;
                        }

                        .goods-price {
                            color: #E4393C;
                            font-weight: 700;
                            margin-left: 10px;
                            font-size: 15px;
                        }

                        .goods-num {
                            margin-left: 10px;
                            font-size: 15px;
                        }
                    }
                }
            }
        }

    }

    .bottom {
        margin-top: 10px;
        background-color: #F4F4F4;
        text-align: right;
        padding: 10px;

        .order-amount {
            b {
                font-size: 18px;
                font-weight: 700;
                color: #F14A3C;
            }
        }

        .address {
            span {
                margin-left: 20px;
            }
        }
    }

    .submit {
        margin-top: 10px;
        width: 140px;
        height: 40px;
        line-height: 40px;
        text-align: center;
        background-color: #F14A3C;
        color: #fff;
        font-size: 18px;
        font-weight: 700;
        border-radius: 5px;

        &:hover {
            cursor: pointer;
        }
    }
}
</style>