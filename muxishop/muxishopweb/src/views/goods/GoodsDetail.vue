<template>
    <div>
        <Shutcut></Shutcut>
        <Header></Header>
        <div class="goods">
            <div class="detail clearfix">
                <div class="goods-img fl">
                    <img :src="goodsDetailData.image" alt="">
                </div>
                <div class="goods-content fl">
                    <div class="desc"> {{ goodsDetailData.name }}</div>
                    <div class="price">{{ goodsDetailData.p_price }}</div>
                    <div class="count">
                        <el-input-number v-model="num" :min="1" :max="999" @change="handleChange" />
                    </div>
                    <div class="add-card">
                        <a href="javascript:void(0)" @click="addCart">添加购物车</a>
                    </div>
                </div>
            </div>

            <div class="comment">
                <Comment :skuId="route.params.sku_id"></Comment>
            </div>
        </div>
    </div>
</template>

<script setup>
import Shutcut from '@/components/common/Shutcut.vue';
import Header from '@/components/home/Header.vue';
import Comment from '@/components/goods/Comment.vue';
import { getGoodsDetail } from '@/network/goods';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { addCartData, getCartCount } from '@/network/cart';
import { ElMessage } from 'element-plus'


let skuId = ref("")
const route = useRoute()
let goodsDetailData = ref({})
onMounted(() => {
    skuId.value = route.params.sku_id
    getGoodsDetail(skuId.value).then(res => {
        // console.log(res)
        goodsDetailData.value = res.data
    })
})

let num = ref(1)
const handleChange = (value) => {
    num.value = value
}

function addCart() {
    const data = {
        sku_id: goodsDetailData.value.sku_id,
        nums: num.value
    }
    addCartData(data)

}


</script>


<style scoped lang="less">
.goods {
    width: var(--content-width);
    margin: 0 auto;

    .detail {
        margin-top: 30px;

        img {
            width: 350px;
            height: 350px;
        }

        .goods-content {
            width: 800px;
            margin-left: 20px;
            margin-top: 30px;

            .desc {
                font-size: 20px;
                color: #666;
            }

            .price {
                margin: 10px 0;
                font-size: 22px;
                color: #e4393c;
            }

            .add-card {
                a {
                    margin-top: 10px;
                    display: inline-block;
                    width: 150px;
                    height: 45px;
                    background-color: #e4393c;
                    font-size: 18px;
                    color: #fff;
                    text-align: center;
                    line-height: 45px;
                    font-weight: 700;
                }


            }
        }
    }

    .comment {
        margin-top: 50px;
    }
}
</style>
