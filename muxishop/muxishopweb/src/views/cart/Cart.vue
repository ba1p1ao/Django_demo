<template>
    <div class="main">
        <Shutcut></Shutcut>
        <Header></Header>
        <div class="content">
            <div class="goods-num">
                全部商品&nbsp;&nbsp;{{ cartTotalNum }}
            </div>
            <div class="goods-table">
                <table>
                    <thead>
                        <tr>
                            <th class="th-all-selete">
                                <div>
                                    <input type="checkbox" :checked="allChecked" @click="checkedAll">
                                    <span>&nbsp;&nbsp;全选</span>
                                </div>

                            </th>
                            <th class="th-goods">商品</th>
                            <th class="th-price">单价</th>
                            <th class="th-nums">数量</th>
                            <th class="th-total">小计</th>
                            <th class="th-doing">操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="goods-detail" v-for="(item, index) in cartList" :key="index">
                            <td class="td-goods-select">
                                <div>
                                    <input type="checkbox" :checked="item.checked" @click="checkedOne(index)">
                                    <img :src="item.goods.image" alt="">
                                </div>

                            </td>
                            <td class="td-goods-info">
                                <div>
                                    <span>{{ item.goods.name }}</span>
                                </div>

                            </td>
                            <td class="goods-price">￥{{ item.goods.p_price }}</td>
                            <td class="goods-num"><el-input-number v-model="item.nums" :min="1" :max="999"
                                    @change="(newValue, oldValue) => handleChange(newValue, oldValue, item.sku_id)" />
                            </td>
                            <td class="goods-total-price">￥{{ (item.goods.p_price * item.nums).toFixed(2) }}</td>
                            <td class="goods-detele"><button @click="delOneGoods(item.sku_id, item.nums)">删除商品</button>
                            </td>
                        </tr>
                    </tbody>

                </table>
            </div>

        </div>
        <div class="bottom">
            <div class="bottom-tool clearfix">
                <div class="tool-left fl">
                    <input type="checkbox" :checked="allChecked" @click="checkedAll"><span
                        class="all-selected">全选</span>
                    <span class="delete-seleted" @click="delSelectGoods">删除选中商品</span>
                    <span class="clear-cart" @click="clearCart">清空购物车</span>
                </div>
                <div class="tool-right fr">
                    <span class="selected-num">已选择 <em>{{ checkedGoodsNum }}</em> 件商品</span>
                    <span class="total-price">总价：<em>￥&nbsp;{{ goodsTotalPrice.toFixed(2) }}</em></span>
                    <a href="javascript:void(0)" @click="goOrder">去结算 </a>
                </div>
            </div>
        </div>

    </div>

</template>

<script setup>
import Shutcut from '@/components/common/Shutcut.vue';
import Header from '@/components/home/Header.vue';
import { ref, onMounted, watch } from 'vue';
import { getCartDetailData, updateCartNumber, delCartData } from '@/network/cart';
import { createOrderData } from '@/network/order';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';

const router = useRouter()

let cartList = ref([])
let cartTotalNum = ref(0)
onMounted(() => {
    getCartDetailData().then(res => {
        cartList.value = res.data
        // console.log(cartList.value)

        // 计算购物车商品总数
        for (let i in cartList.value) {
            cartTotalNum.value += cartList.value[i].nums
        }
    })

})

const store = useStore()


const handleChange = (newValue, oldValue, skuId) => {
    // console.log(newValue, oldValue, skuId)
    const data = {
        sku_id: skuId,
        num: newValue
    }
    updateCartNumber(data).then(res => {
        // console.log(res)
        if (res.status == 30001) {
            alert(res.data)
            router.push("/login")
        }
        store.dispatch("updateCartCount")
        // cartTotalNum.value = store.state.cartCount
    })
    cartTotalNum.value += newValue - oldValue
}


// 全选 与 取消全选
let allChecked = ref(false)
let checkedGoodsNum = ref(0)
let goodsTotalPrice = ref(0)
// 
function getCheckedGoodsNum() {
    checkedGoodsNum.value = 0
    goodsTotalPrice.value = 0
    for (let i in cartList.value) {
        if (cartList.value[i].checked == true) {
            checkedGoodsNum.value++
            goodsTotalPrice.value += parseFloat((cartList.value[i].goods.p_price * cartList.value[i].nums).toFixed(2))
        }
    }
}

// 全选的逻辑
function checkedAll() {
    const targetChecked = !allChecked.value;
    allChecked.value = targetChecked;
    cartList.value.forEach(item => {
        item.checked = targetChecked;
    });
}


function checkedOne(index) {
    // 边界兜底：避免 cartList 未初始化、索引越界导致报错
    const cartListVal = cartList.value;
    if (!cartListVal?.length || index < 0 || index >= cartListVal.length) return;

    // 1. 切换当前商品选中状态（兼容 checked 属性缺失的情况：缺失视为 false，取反后为 true）
    const targetItem = cartListVal[index];
    const newCheckedState = !(targetItem.checked ?? false); // 核心兼容逻辑：?? false 处理属性缺失

    // 2. Vue 响应式优化：直接修改数组项属性可能丢失响应式，用 map 生成新数组（触发一次更新）
    cartList.value = cartListVal.map((item, idx) =>
        idx === index ? { ...item, checked: newCheckedState } : item
    );

    // 3. 同步全选状态：判断所有商品是否都选中（兼容 checked 属性缺失）
    allChecked.value = cartList.value.every(item => item.checked ?? false);
}

watch(() => cartList, (newValue, oldValue) => {
    // console.log(cartList)
    getCheckedGoodsNum()
}, {
    // 通过深度监听，来监听 cartList 中的 json 对象的值变化，如果变化就执行
    deep: true,
})



function delCarts(goods) {
    let skuIds = []
    goods.value.forEach((item) => {
        skuIds.push(item.sku_id)
    })
    const data = {
        sku_id: skuIds,
    }
    delCartData(data)
}

function delOneGoods(skuId, nums) {
    const data = {
        sku_id: [skuId],
    }
    delCartData(data)
    cartTotalNum.value -= nums
    for (let i in cartList.value) {
        if (skuId == cartList.value[i].sku_id) {
            cartList.value.splice(i, 1)
        }
    }
}

let delSelectedGoodsList = ref([])
let noDelGoodsList = ref([])
function delSelectGoods() {
    delSelectedGoodsList.value = []
    noDelGoodsList.value = []
    cartList.value.forEach((item) => {
        if (item.checked) {
            delSelectedGoodsList.value.push(item)
        } else {
            noDelGoodsList.value.push(item)
        }
    })

    console.log(delSelectedGoodsList.value)
    if (delSelectedGoodsList.value.length == 0) {
        alert("请选择商品")
    } else {
        let flag = confirm("是否要删除选择的商品？")
        if (flag) {
            delCarts(delSelectedGoodsList)
            delSelectedGoodsList.value.forEach((item) => {
                cartTotalNum.value -= item.nums
            })
            cartList.value = noDelGoodsList.value
        }
    }
}

function clearCart() {
    if (cartList.value.length == 0) {
        alert("购物车为空")
    } else {
        let flag = confirm("是否要清空购物车？")
        if (flag) {
            delCarts(cartList)
            cartList.value = []
            cartTotalNum.value = 0
        }
        location.href = "/"
    }

}

function goOrder() {
    let orderGoodsList = []
    noDelGoodsList.value = []
    cartList.value.forEach((item) => {
        if (item.checked) {
            orderGoodsList.push(item)
        } else {
            noDelGoodsList.value.push(item)
        }
    })
    if (orderGoodsList.length == 0) {
        alert("请选择结算的商品")
        return
    }
    let request_data = {
        trade: {
            order_amount: goodsTotalPrice.value,
        },
        goods_list: orderGoodsList
    }
    createOrderData(request_data).then(res => {
        if (res.status == 60000) {
            ElMessage.success("已成功提交订单")
            cartList.value = noDelGoodsList.value
            store.dispatch("updateCartCount")
            router.push("/order/" + res.data.trade_no)
        } else {
            ElMessage.error("提交订单失败")
        }

    })

}

</script>

<style scoped lang="less">
.content {
    width: var(--content-width);
    margin: 0 auto;

    .goods-num {
        font-size: 16px;

        font-weight: 700;
        color: #e2231a;
    }

    .goods-table {
        table {
            border-collapse: separate;
            border-spacing: 0 20px;
            width: var(--content-width);

            thead {
                padding-left: 10px;
                text-align: center;
                background-color: #f3f3f3;
                height: 45px;

                .th-all-selete {
                    text-align: left;
                    width: 150px;

                    div {
                        margin-left: 15px;
                    }
                }

                .th-total {
                    width: 150px;
                }

                .th-goods {
                    text-align: left;
                    width: 480px;
                }

            }

            tbody {
                .goods-detail {
                    text-align: center;

                    td {
                        border-bottom: 2px solid #ddd;
                        padding: 12px 0;
                    }

                    .td-goods-select {
                        text-align: left;

                        div {
                            margin-left: 15px;
                        }

                        img {
                            width: 80px;
                            height: 80px;
                            border: 1px solid #eee;
                            margin: 0 10px;
                        }
                    }

                    .td-goods-info {
                        text-align: left;
                    }

                    .goods-total-price {
                        font-weight: 700;
                        font-size: 15px;
                    }

                    .goods-detele {
                        button {
                            cursor: pointer;
                            background-color: #fff;
                        }
                    }
                }

            }
        }



    }


}

.bottom {
    border-top: 4px solid #F9F9F9;
    border-bottom: 2px solid #F9F9F9;

    .bottom-tool {
        width: var(--content-width);
        margin: 0 auto;
        height: 55px;
        line-height: 55px;
        text-align: center;

        z-index: 999;

        .tool-left {
            margin-left: 15px;

            span {
                margin-left: 15px;

            }

            .delete-seleted {
                cursor: pointer;

                &:hover {
                    color: #e2231a;
                }
            }

            .clear-cart {
                cursor: pointer;

                &:hover {
                    color: #e2231a;
                }
            }

        }

        .tool-right {
            span {
                margin-right: 15px;
            }

            .selected-num {
                em {
                    color: #E43822;
                    font-size: 12px;
                }
            }

            .total-price {
                em {
                    font-weight: 700;
                    color: #E43822;
                    font-size: 18px;
                }
            }

            a {
                display: inline-block;
                width: 95px;
                height: 55px;
                background-color: #F65147;
                color: #fff;
                font-size: 18px;
                font-weight: 700;
            }
        }
    }
}
</style>