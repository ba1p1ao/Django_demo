<template>
    <div class="find-goods">
        <img src="@/assets/images/find-goods.png" alt="">
        <!-- 使用大写的组件名，并传入必要的参数 -->
        <Vue3SeamlessScroll :list="goodsFindList" class="scroll" direction="left" :hover="true" :singleLine="true">
            <div class="item" v-for="(item, index) in goodsFindList" :key="index" @click="toGoodsDetail(item.sku_id)">
                <div v-if="index % 2 == 0">
                    <span class="dian1">{{ item.name }}</span>
                    <img :src="item.image" alt="">
                </div>
                <div v-else>
                    <img :src="item.image" alt="">
                    <span class="dian1">{{ item.name }}</span>

                </div>
            </div>
        </Vue3SeamlessScroll>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
// 1. 正确导入组件
import { Vue3SeamlessScroll } from 'vue3-seamless-scroll';
import { getFindGoods } from '@/network/home';
import { toGoodsDetail } from '@/utils/goods';


let goodsFindList = ref([])
onMounted(() => {
    getFindGoods().then(res => {
        goodsFindList.value = res.data
    })
})
</script>

<style scoped lang="less">
.find-goods {
    width: var(--content-width);
    margin: 15px auto;
    >img {
        width: 190px;
        height: 260px;
        float: left;
    }

    .scroll {
        background-color: #fff;
        height: 260px;
        width: 1000px;
        overflow: hidden;
        margin-left: 200px;
        .item {
            height: 260px;
            width: 150px;
            margin: 20px 10px;
            span {
                width: 150px;
                font-size: 14px;
                margin: 10px 10px;
                // padding: 10px;
            }
            img {
                padding: 10px;
                width: 150px;
                height: 150px;
                border-radius: 20px;
            }
            &:hover {
                cursor: pointer;
            }
        }
    }


}
</style>