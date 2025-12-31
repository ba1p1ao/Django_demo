<template>
    <div class="main">
        <Shutcut></Shutcut>
        <div class="order-pay">
            <div class="header">
                <div class="title clearfix">
                    <div class="log fl">
                        <Logo></Logo>
                    </div>
                    <div class="name fl">收银台</div>
                </div>
            </div>

            <div class="order-info clearfix">
                <div class="order-num fl">
                    <span>订单提交成功，请尽快付款!</span>
                    <span>订单号: <b>{{ tradeNo }}</b> </span>
                </div>

                <div class="order-amount fr">
                    <span>应付金额：<b>{{ orderAmount }}</b> 元 </span>
                </div>
            </div>

            <div class="pay-mod">
                <div class="pay-mod-title">
                    <span>支付方式</span>
                </div>
                <div class="pay-mod-content">
                    <table>
                        <tbody>
                            <tr>
                                <td class="tdcheckbox">
                                    <input type="checkbox" class="checkbox" :checked="payMod[0].checked"
                                        @click="changePayMod(0)">
                                </td>
                                <td class="tdalipay">
                                    <div class="alipay">
                                        <img src="@/assets/images/order/alipay.png" alt="">
                                        <span>支付宝支付</span>
                                    </div>
                                </td>

                            </tr>
                        </tbody>
                    </table>


                </div>

                <div class="pay-submit fr">
                    <button class="noactive" :class="payMod[payModIndex].checked ? 'isactive' : ''" @click="submit">立即支付</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Shutcut from '@/components/common/Shutcut.vue';
import Logo from '@/components/common/Logo.vue';
import { useRoute, useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { toAliPayPage } from '@/network/order';


const route = useRoute()
const router = useRouter()
let payModIndex = ref(0)
let payMod = ref([
    { mod: "alipay", checked: 0 },
])
let tradeNo = ref("")
let orderAmount = ref(0)
onMounted(() => {
    tradeNo.value = route.query.tradeNo
    orderAmount.value = route.query.orderAmount
})
const changePayMod = (index) => {
    for (let i in payMod.value) {
        if (i == index) {
            payMod.value[i].checked = !payMod.value[i].checked
        } else {
            payMod.value[i].checked = 0
        }

    }
}

const submit = () => {
    if (!payMod.value[payModIndex.value].checked) return 
    let data = {
        tradeNo: tradeNo.value,
        orderAmount: orderAmount.value,
    }

    toAliPayPage(data).then(res => {
        if (res.status == 80000) {
            let re_url = res.data['alipay']
            window.location.href = re_url
        }
    })
}

</script>

<style scoped lang="less">
.main {
    height: 100%;
}

.order-pay {
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

    .order-info {
        margin-top: 10px;

        .order-num {
            font-size: 18px;
        }

        .order-amount {
            font-size: 18px;

            b {
                color: #F00C0C;
            }
        }

    }

    .pay-mod {
        width: 100%;
        padding: 20px;

        .pay-mod-title {
            font-size: 20px;
            font-weight: 600;
        }

        .pay-mod-content {
            border: 1px solid #f4f4f4;
            border-radius: 5px;
            padding: 10px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

            table {

                margin-left: 20px;
            }

            margin-top: 20px;

            .tdcheckbox {
                width: 60px;

                .checkbox {
                    width: 20px;
                    height: 20px;
                }
            }

            .tdalipay {
                .alipay {
                    height: 48px;
                    line-height: 48px;
                    span {
                        font-size: 18px;
                    }
                }
            }
        }

        .pay-submit {
            margin-top: 10px;
            margin-right: 10px;

            .noactive {
                border-radius: 5px;
                width: 100px;
                height: 40px;
                font-size: 18px;
                font-weight: 700;
                text-align: center;
                color: #fff;
                background-color: #9d9d9d;
            }

            .isactive {
                background-color: #F00C0C;
            }
        }
    }
}
</style>
