<template>
    <div class="category-main clearfix">
        <div class="goods fl" v-for="(item, index) in goods" :key="index" @click="toGoodsDetail(item.sku_id)">
            <div class="first-row">
                <img :src="item.image" alt="">
            </div>
            <div class="second-row dian2">
                <span>{{ item.name }}</span>
            </div>
            <div class="third-row">
                <small>￥</small>
                <span>{{ item.p_price }}</span>
            </div>
        </div>

    </div>

</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { getCategoryGoods } from '@/network/home';
import { toGoodsDetail } from '@/utils/goods';

let categoryId = defineProps(["categoryId"])
let goods = ref([])
let page = ref(1)
onMounted(() => {
    getCategoryGoodsData(1, 1)
})

function getCategoryGoodsData(categoryId, page) {
    getCategoryGoods(categoryId, page).then(res => {
        goods.value = res.data
        // console.log(goods.value)
    })

}
watch(categoryId, (newValue, oldValue) => {
    getCategoryGoodsData(newValue.categoryId, page.value)
    page.value = 1
})
function windosScroll() {
    // 可视区域的度，就是我们用眼睛能看见的内容的高度
    let clientHeight = document.documentElement.clientHeight
    // 滚动条在文档中的高度的位置(滚出可见区域的高度)
    let scrollTop = document.documentElement.scrollTop
    // 所有内容的高度
    let scrollHeight = document.documentElement.scrollHeight

    if (clientHeight + scrollTop >= scrollHeight) {
        // console.log(categoryId.categoryId, page.value)
        page.value += 1
        getCategoryGoods(categoryId.categoryId, page.value).then(res => {
            for (let i in res.data) {
                goods.value.push(res.data[i])
            }
        })

    }
}
window.addEventListener("scroll", windosScroll)
</script>

<style scoped lang="less">
.category-main {
    width: var(--content-width);
    margin: 10px auto;
    margin-bottom: 0;

    .goods {
        &:not(:nth-child(5n)) {
            margin-right: 12px;
        }

        margin-bottom: 12px;
        background-color: #fff;
        width: 230px;
        height: 320px;

        &:hover {
            cursor: pointer;
        }

        .first-row {
            text-align: center;
            margin: 40px 0;

            img {
                margin: 0 auto;
                width: 150px;
                height: 150px;
            }
        }

        .second-row {
            margin: 0 auto;
            font-size: 14px;
            color: #666;
            width: 190px;
            height: 40px;

            &:hover {
                color: #c81623;
            }
        }

        .third-row {
            width: 190px;
            color: #c81623;

            span {
                font-size: 20px;
                font-weight: 700;
            }

            margin: 0 auto;
            margin-top: 15px;
        }
    }
}
</style>