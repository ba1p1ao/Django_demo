<template>
    <div class="block" style="width: 1000px;">
        <div class="block text-center" m="t-4">
            <span class="demonstration"></span>
            <el-carousel trigger="click" height="470px">
                <el-carousel-item v-for="item in images" :key="item">
                    <img :src="item" alt="">
                </el-carousel-item>
            </el-carousel>
        </div>
    </div>
</template>

<script setup>
import banner1 from '@/assets/images/banner/banner1.png'
import banner2 from '@/assets/images/banner/banner2.png'
import banner3 from '@/assets/images/banner/banner3.png'
import banner4 from '@/assets/images/banner/banner4.png'
import banner5 from '@/assets/images/banner/banner5.png'
import { ref } from 'vue'
const images = ref([
    banner1, banner2, banner3, banner4, banner5
])


</script>

<style scoped>
.demonstration {
    color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
    color: #475669;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
    text-align: center;
}

.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
    background-color: #d3dce6;
}
</style>