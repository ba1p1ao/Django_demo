<template>
    <div class="main">
        <div class="comment clearfix" v-for="(item, index) in commentList" :key="index">
            <div class="left fl">
                <div class="header-content">
                    <img :src="'https://' + item.user_image_url" alt="">
                    <span class="nickname">{{ item.nickname }}</span>
                </div>
            </div>

            <div class="right fl">
                <div class="star">

                    <img src="@/assets/images/goods/star.png" alt="" v-for="(index) in item.score">
                    <img src="@/assets/images/goods/star1.png" alt="" v-for="(index) in 5 - item.score">
                </div>

                <div class="text">
                    {{ item.content }}
                </div>
                <div class="time">
                    {{ item.create_time }}
                </div>
            </div>
        </div>
        <div class="page">
            <el-pagination background layout="prev, pager, next" :total="commentTotal" :page-size="15"
                @current-change="handleChangePage"> </el-pagination>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getCommentCount, getGoodsCommentData } from '@/network/comment';


let skuId = defineProps(["skuId"])
let commentTotal = ref(0)
let commentList = ref([])


onMounted(() => {
    getCommentCount(skuId.skuId).then(res => {
        commentTotal.value = res.data
    })

    getGoodsCommentData(skuId.skuId, 1).then(res => {
        commentList.value = res.data.results || []
        // console.log(commentList.value)
    })

})
const handleChangePage = (page) => {
    getGoodsCommentData(skuId.skuId, page).then(res => {
        commentList.value = res.data.results || []
        console.log(commentList.value)
        // console.log(commentList.value)
    })
}

</script>


<style scoped lang="less">
.main {
    width: var(--content-width);
    margin: 0 auto;

    .comment {
        margin: 20px 0;
        border-bottom: 2px solid #dcdcdc;

        .left {
            width: 200px;

            .header-content {
                img {
                    width: 25px;
                    height: 25px;
                    border-radius: 25px;
                }

                .nickname {
                    margin-left: 10px;
                }
            }
        }

        .right {
            width: 1000px;

            .star {
                img {
                    height: 14px;
                    width: 14px;
                }
            }

            .text {
                margin: 20px 0;
                color: #333;
                font-size: 14px;
            }

            .time {
                margin: 10px 0;
                font-size: 14px;
            }
        }
    }

    .page {
        margin: 20px 0;
        text-align: center;

        .el-pagination {
            position: relative;
            float: none !important;
            display: inline-flex !important;
        }
    }

}
</style>
