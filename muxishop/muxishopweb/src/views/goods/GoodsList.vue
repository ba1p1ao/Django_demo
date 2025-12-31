<template>
    <div class="home">
        <Shutcut></Shutcut>
        <Header></Header>
        <div class="all-goods">
            <div>
                <span>全部商品分类</span>
            </div>
        </div>
        <div class="all-goods-list">
            <div class="result-keyword">
                <span class="all-result-keyword">
                    全部结果&nbsp;&nbsp;>&nbsp;&nbsp;
                </span>
                <span class="search-word">
                    "{{ keyword }}"
                </span>
            </div>
            <div class="goods-list">
                <div class="search-condition">
                    <a href="javascript:void(0)" v-for="(item, index) in orderTypes" :key="index"
                        @click="changeOrder(item.order, item.index)"
                        :class="item.active ? 'current-condition' : 'not-current-condition'">
                        <span>{{ item.name }}</span>
                        <img src="" alt="">
                    </a>
                </div>

                <div class="list-detail clearfix">
                    <div class="every-good fl" v-for="(item, index) in goodsList" :key="index" @click="toGoodsDetail(item.sku_id)">
                        <div class="image-box">
                            <img :src="item.image" alt="" class="good-img">
                        </div>
                        <div class="price">
                            <small>￥</small>
                            <span>{{ item.p_price }}</span>
                        </div>
                        <div class="name cs dian2">
                            <span>{{ item.name }}</span>
                        </div>
                        <div class="comment-count">
                            <span class="count">{{ item.comment_count ? item.comment_count : 0 }}</span>
                            <span class="comment">条评价</span>
                        </div>
                        <div class="shop-name dian1">
                            <span>{{ item.shop_name }}</span>
                        </div>
                        <div class="add-card cs">
                            <img src="@/assets/images/cart/add-cart1.png" alt="">
                            加入购物车
                        </div>
                    </div>
                </div>
                <div class="page-box clearfix">
                    <div class="page-btn-list">
                        <button class="prev-btn" @click="prevPage"><span><</span></button>
                        <button :class="item != -1 ? 'page-btn' : 'not-page-btn'" v-for="(item, index) in pagebtnlist" :key="index"
                        @click="changePage(item)">
                            <span v-if="item != -1">{{ item }}</span>
                            <span v-else>...</span>
                        </button>
                        <button class="next-btn" @click="nextPage"><span>></span></button>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Shutcut from '@/components/common/Shutcut.vue';
import Header from '@/components/home/Header.vue';
import { onMounted, ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { getGoodsListData } from '@/network/goods';
import { getKeywordGoodsCountData } from '@/network/goods';
import { toGoodsDetail } from '@/utils/goods';
import { addCartData } from '@/network/cart';

const router = useRouter() // 全局路由
const route = useRoute()   // 当前路由
let orderTypes = ref([
    { index: 1, order: 1, name: "综合", active: true },
    { index: 2, order: 1, name: "评论数", active: false },
    { index: 3, order: 2, name: "价格", active: false },
])

const keyword = computed(() => {
    return route.params.keyword
})
const page = computed(() => {
    return route.params.page
})
const order = computed(() => {
    return route.params.order
})
watch(keyword, (newValue, oldValue) => {
    getSearchData(newValue, page.value, order.value)
})
watch(page, (newValue, oldValue) => {
    getSearchData(keyword.value, newValue, order.value)
})
watch(order, (newValue, oldValue) => {
    getSearchData(keyword.value, page.value, newValue)
})

const goodsList = ref([])
function getSearchData(keyword, page, order) {
    getKeywordDataCount(keyword)
    getGoodsListData(keyword, page, order).then(res => {
        goodsList.value = res.data
    })
}

onMounted(() => {
    getSearchData(route.params.keyword, route.params.page, route.params.order)
})

const goodsKeywordCount = ref(0)
const pagebtnlist = ref([])
const pageTotal = ref(1)
const currentPage = ref(parseInt(route.params.page, 10))
function getKeywordDataCount(keyword) {

    getKeywordGoodsCountData(keyword).then(res => {
        pagebtnlist.value = []
        pageTotal.value = 1
        currentPage.value = parseInt(route.params.page, 10)
        pageTotal.value = Math.ceil(res.data / 15)
        if (pageTotal.value <= 3) {
            for (let i = 1; i < pageTotal.value; i++) {
                pagebtnlist.value.push(i)
            }
        } else {
            for (let i = 1; i <= pageTotal.value; i++) {
                if (i <= Math.ceil(pageTotal.value / 3 + 1)) {
                    pagebtnlist.value.push(i)
                } else {
                    pagebtnlist.value.push(-1)
                    break
                }
            }
        }
        pagebtnlist.value.push(pageTotal.value)
        // console.log(pagebtnlist.value)
    })
}

function changePage(page) {
    if (page <= 0) {
        return null
    }
    currentPage.value = page
    // console.log(currentPage.value, pageTotal.value)
    router.push("/goods_list/" + route.params.keyword + "/" + currentPage.value + "/" + route.params.order)
}

function prevPage() {
    console.log(currentPage.value - 1, pageTotal.value)
    if (currentPage.value - 1 > 0) {
        currentPage.value--
        router.push("/goods_list/" + route.params.keyword + "/" + currentPage.value + "/" + route.params.order)
    }
}

function nextPage() {
    console.log(currentPage.value + 1, pageTotal.value)
    if (currentPage.value + 1 <= pageTotal.value) {
        currentPage.value++
        router.push("/goods_list/" + route.params.keyword + "/" + currentPage.value + "/" + route.params.order)
    }
}



function changeOrder(order, index) {
    // 全页面重新加载
    // goodsList.value = []
    // getSearchData(route.params.keyword, 1, order)
    router.push("/goods_list/" + route.params.keyword + "/" + 1 + "/" + order)
    for (let i in orderTypes.value) {
        if (index == orderTypes.value[i].index) {
            orderTypes.value[i].active = true
        } else {
            orderTypes.value[i].active = false
        }
    }
}

</script>

<style scoped lang="less">
.home {
    .all-goods {
        border-bottom: 2px solid #f30213;

        >div {
            width: var(--content-width);
            margin: 0 auto;

            span {
                display: block;
                background-color: #f30213;
                color: #fff;
                padding: 0 20px;
                font-size: 14px;
                font-weight: 700;
                height: 33px;
                line-height: 33px;
                width: 190px;
                text-align: center;
            }
        }

    }

    .all-goods-list {
        width: var(--content-width);
        margin: 0 auto;

        .result-keyword {
            margin-top: 20px;
            margin-bottom: 10px;

            .all-result-keyword {
                color: #666;
                font-size: 12px;
            }

            .search-word {
                color: #666;
                font-weight: 700;
            }
        }

        .goods-list {
            .search-condition {
                padding-left: 10px;
                height: 40px;
                line-height: 40px;
                background-color: #f1f1f1;

                .current-condition {
                    background-color: #e4393c;
                    color: #fff;
                    border: 1px solid #e4393c;

                    img {
                        content: url("@/assets/images/goods-list/down3.png")
                    }
                }

                .not-current-condition {
                    background-color: #fff;

                    img {
                        content: url("@/assets/images/goods-list/down1.png")
                    }

                    &:hover {
                        color: #e4393c;
                        border: 1px solid #e4393c;

                        img {
                            content: url("@/assets/images/goods-list/down2.png")
                        }
                    }
                }

                a {
                    height: 25px;
                    line-height: 25px;
                    display: inline-block;
                    text-align: center;
                    width: 80px;
                    font-size: 14px;
                    border: 1px solid #ddd;

                    img {
                        height: 14px;
                        width: 14px;
                    }
                }



            }

            .list-detail {
                margin-top: 10px;

                .every-good {
                    width: 238px;
                    height: 420px;
                    border: 1px solid #fff;

                    &:hover {
                        border: 1px solid #ddd;
                    }

                    // &:not(:last-child) {
                    //     margin-right: 5px;
                    // }
                    .image-box {
                        text-align: center;
                        margin-top: 10px;

                        .good-img {
                            width: 220px;
                            height: 220px;

                        }
                    }


                    .price {
                        margin-left: 10px;
                        margin-top: 10px;
                        color: #e4393c;
                        font-size: 20px;
                    }

                    .name {
                        margin-left: 10px;
                        margin-top: 10px;
                        font-size: 12px;
                        height: 35px;
                        color: #666;

                        &:hover {
                            color: #e4393c;
                        }
                    }

                    .comment-count {
                        margin-left: 10px;
                        margin-top: 10px;

                        .count {
                            color: #646fb0;
                            font-weight: 700;
                        }

                        .comment {
                            color: #a7a7a7;
                        }
                    }

                    .shop-name {
                        margin-top: 10px;
                        margin-left: 10px;
                        color: #999;
                    }

                    .add-card {
                        margin: 0 auto;
                        margin-top: 20px;
                        width: 120px;
                        border: 1px solid #e4393c;
                        border-radius: 15px;
                        text-align: center;

                        img {
                            width: 20px;
                            height: 20px;
                        }

                        &:hover {
                            color: #e4393c;
                        }
                    }
                }
            }

            .page-box {
                margin-top: 20px;
                text-align: center;

                .page-btn {
                    width: 40px;
                    height: 40px;
                    background-color: #ececec;
                    margin: 0 5px;
                    &:hover {
                        color: #fff;
                        background-color: #cd6767;
                    }
                    &:active {
                        color: #fff;
                        background-color: #cd6767;
                    }
                    &:focus {
                        color: #fff;
                        background-color: #cd6767;
                    }
                }
                .not-page-btn {
                    width: 40px;
                    height: 40px;
                    &:hover {
                        color: #fff;
                        background-color: #cd6767;
                    }
                }
                .prev-btn {
                    width: 40px;
                    height: 40px;
                    &:hover {
                        color: #fff;
                        background-color: #cd6767;
                    }
                }
                .next-btn {
                    width: 40px;
                    height: 40px;
                    &:hover {
                        color: #fff;
                        background-color: #cd6767;
                    }
                }
            }
        }
    }
}
</style>