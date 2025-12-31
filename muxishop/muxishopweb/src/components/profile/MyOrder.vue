<template>
    <div class="main">
        <div class="title">
            <span>我的订单</span>
        </div>
        <div class="myorder-info">

            <div class="select clearfix">
                <a href="javascript:void(0)" v-for="(item, index) in orderStatusDict" :key="index"
                    @click="changeOrderStatus(item.payStatus)" :class="item.isActive ? 'active fl' : 'fl'">
                    {{ item.payName }}
                </a>
            </div>
            <div class="order-table">
                <table>
                    <thead>
                        <tr class="table-header">
                            <th>订单详细</th>
                            <th>收货人</th>
                            <th>金额</th>
                            <th>全部状态</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody class="order-info" v-for="(orderItem, orderIndex) in orderList" :key="orderIndex">
                        <tr class="blank"></tr>
                        <tr class="order-header">
                            <td class="createtime">
                                <span>{{ orderItem.create_time }}</span>
                                <span>订单号：</span>
                                <b>{{ orderItem.trade_no }}</b>
                            </td>

                            <td colspan="4" class="del-img">
                                <el-popconfirm width="200" title="确认要删除这个订单吗？">
                                    <template #reference>
                                        <img src="@/assets/images/profile/delete.png" alt="">
                                    </template>
                                    <template #actions="{ confirm, cancel }">
                                        <el-button size="small" @click="cancel">取消</el-button>
                                        <el-button type="danger" size="small"
                                            @click="handlerDeleteOrder(orderItem.trade_no, confirm)">
                                            确认
                                        </el-button>
                                    </template>
                                </el-popconfirm>
                            </td>
                        </tr>
                        <tr class="order-detail" v-for="(goods, goodsIndex) in orderItem.order_goods" :key="goodsIndex">
                            <td class="goods-detail">
                                <a :href="'/detail/' + goods.sku_id" target="_blank" class="goods-img">
                                    <img :src="goods.image" alt="">
                                </a>
                                <a :href="'/detail/' + goods.sku_id" target="_blank" class="goods-name">
                                    <span>{{ goods.name }}</span>
                                </a>
                                <span class="goods-nums">×{{ goods.goods_num }}</span>
                            </td>
                            <td :rowspan="orderItem.order_goods.length" v-if="goodsIndex < 1">
                                <span>{{ $store.state.user.name }}</span>
                            </td>
                            <td :rowspan="orderItem.order_goods.length" v-if="goodsIndex < 1">
                                <span>{{ orderItem.order_amount }}</span>
                            </td>
                            <td :rowspan="orderItem.order_goods.length" v-if="goodsIndex < 1">
                                <span>{{ switchPayStatus(orderItem.pay_status)[0] }}</span>
                            </td>
                            <td :rowspan="orderItem.order_goods.length" v-if="goodsIndex < 1" class="order-action"
                                @click="toAction(orderItem.pay_status, orderItem.trade_no, orderItem.order_amount, orderItem.order_goods)">
                                <span>{{ switchPayStatus(orderItem.pay_status)[1] }}</span>
                            </td>
                        </tr>
                    </tbody>

                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { getOrderData, updateOrderData, createOrderData, deleteOrderData } from '@/network/order';
import { InfoFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';


const router = useRouter()

let orderList = ref([])
let payStatus = ref("-1")

let orderStatusDict = ref([
    {
        payStatus: -1,
        payName: "全部订单",
        isActive: true,
    },
    {
        payStatus: 0,
        payName: "待确认",
        isActive: false,
    },
    {
        payStatus: 1,
        payName: "待付款",
        isActive: false,
    },
    {
        payStatus: 2,
        payName: "待收货",
        isActive: false,
    },
    {
        payStatus: 3,
        payName: "已完成",
        isActive: false,
    },
])

const changeOrderStatus = (payStatus) => {
    console.log(payStatus)
    orderStatusDict.value.forEach(item => {
        if (item.payStatus == payStatus) {
            getAllOrderInfo(payStatus)
            item.isActive = true
        } else {
            item.isActive = false
        }
    })
}

const switchPayStatus = (payStatus) => {
    const orderStatus = reactive({
        0: ["待确认", "确认订单"],
        1: ["待付款", "支付订单"],
        2: ["待收货", "确认收货"],
        3: ["已完成", "再次购买"],
    })
    return orderStatus[payStatus]
}

const getAllOrderInfo = (pay_status) => {

    getOrderData(pay_status).then(res => {
        if (res.status == 60000) {
            orderList.value = res.data
        }
    })
}
onMounted(() => {
    getAllOrderInfo(payStatus.value)
})


function handlerDeleteOrder(orderNo, confirm) {
    console.log(orderNo)
    let data = {
        trade_no: orderNo
    }
    confirm()
    deleteOrderData(data).then(res => {
        if (res.status == 60000) {
            ElMessage.success(res.data)
            window.location.reload()
        } else {
            ElMessage.error(res.data)
        }
    })
}    

function toAction(pay_status, trade_no, order_amount, order_goods) {
    if (pay_status == 0) {
        // 0 待确认
        // 跳转到订单页面
        router.push("/order/" + trade_no)
    } else if (pay_status == 1) {
        // 1 待付款
        // 跳转到支付页面
        router.push({
            name: "OrderPay",
            query: {
                tradeNo: trade_no,
                orderAmount: order_amount
            }
        })
    } else if (pay_status == 2) {
        // 2 待收货
        // 调用更新订单接口
        let data = {
            trade_no: trade_no,
            pay_status: 3,
        }
        updateOrderData(data).then(res => {
            if (res.status == 60000) {
                ElMessage.success("更新收货成功")
            }
        })
        window.location.reload()
    } else if (pay_status == 3) {
        // 3 再次购买
        // 调用创建订单接口
        for (let i in order_goods) {
            order_goods[i].nums = order_goods[i].goods_num
        }
        let request_data = {
            trade: {
                order_amount: order_amount,
            },
            goods_list: order_goods
        }
        console.log(request_data)
        createOrderData(request_data).then(res => {
            if (res.status == 60000) {
                ElMessage.success("已成功提交订单")
                router.push("/order/" + res.data.trade_no)
            } else {
                ElMessage.error("提交订单失败")
            }

        })
    }
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

    .myorder-info {
        background-color: #fff;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-radius: 8px;

        .select {
            a {
                display: inline-block;
                margin-right: 20px;
                border-bottom: 1px solid #fff;

                &:hover {
                    color: #DB2E16;
                }
            }

            .active {
                color: #DB2E16;
                font-weight: 700;
                border-bottom: 1px solid #DB2E16;
            }
        }

        .order-table {
            margin-top: 20px;

            table {
                border-collapse: collapse;
                width: 100%;
            }

            .table-header {
                height: 35px;
                background-color: #f5f5f5;
                border: 1px solid #e5e5e5;

                th:not(:first-child) {
                    width: 100px;
                }
            }

            .order-info {
                .blank {
                    height: 20px;
                }

                .order-header {
                    border: 1px solid #e5e5e5;
                    background-color: #f5f5f5;
                    height: 30px;

                    .createtime {
                        span {
                            font-size: 12px;
                            color: #aaa;
                            margin-left: 30px;
                        }

                    }

                    .del-img {
                        text-align: right;

                        img {
                            margin-right: 40px;
                            width: 20px;
                            height: 20px;

                            &:hover {
                                cursor: pointer;
                                content: url("@/assets/images/profile/delete-red.png");
                            }
                        }

                    }
                }

                .order-detail {
                    border: 1px solid #e5e5e5;

                    td {
                        border: 1px solid #e5e5e5;
                    }

                    td:not(:first-child) {
                        text-align: center;
                    }

                    .goods-detail {
                        padding: 5px;

                        a {
                            display: inline-block;
                        }

                        .goods-img {
                            img {
                                width: 60px;
                                height: 60px;
                                border: 1px solid #f5f5f5;
                                padding: 10px;
                            }
                        }

                        .goods-name {
                            height: 100%;
                            width: 400px;
                            margin-left: 20px;

                            &:hover {
                                color: #DB2E16
                            }
                        }

                        .goods-nums {
                            margin-left: 20px;
                        }
                    }

                    .order-action {
                        span {
                            padding: 5px;
                            border: 1px solid #ddd;
                            background-color: #f5f5f5;

                            &:hover {
                                cursor: pointer;
                                color: #DB2E16;
                                border: 1px solid #DB2E16;
                            }
                        }

                    }


                }

            }
        }
    }
}
</style>