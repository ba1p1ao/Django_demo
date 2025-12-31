<template>
    <div class="main">
        <div class="content" @click="toCart">
            <el-badge :value="$store.state.cartCount" class="item">
                <span class="iconfont icon-gouwuche"></span>
            </el-badge>
            <span>我的购物车</span>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { onMounted, ref, watch } from 'vue';
import { getCartCount } from '@/network/cart';
import { useStore } from 'vuex';
import store from '@/store';
// const usestore = useStore()
onMounted(() => {
    // getCartCount().then(res => {
    //     let count = res.data || 0
    //     window.localStorage.setItem("cartCount", count)
    //     store.state.cartCount = count

    // })
    store.dispatch("updateCartCount")
})

const router = useRouter()

function toCart() {
    if (store.state.cartCount == 0) {
        alert("购物车里面没有商品，请添加商品")
    } else {
        router.push("/cart/detail")
    }

    // if (store.state.user.isLogin == true) {
    //     router.push("/cart/detail")
    // } else {

    // }

}
</script>

<style scoped lang="less">
@red: #e2231a;

.main {
    // height: 140px;
    // margin-top: 45px;
    // margin-left: 25px;

    .content {
        border: 1px solid #e3e4e5;
        width: 130px;
        height: 35px;
        line-height: 35px;
        text-align: center;
        padding-top: 5px;

        &:hover {
            cursor: pointer;
            border: 1px solid @red
        }

        .item {
            height: 25px;
            line-height: 20px;

            >span {
                font-size: 25px;
                color: @red;
                font-weight: 700;
            }
        }

        >span {
            margin-left: 20px;
            color: @red;
            font-size: 14px;
        }
    }
}
</style>