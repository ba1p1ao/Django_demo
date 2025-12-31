<template>
  <div class="home">
    <Shutcut></Shutcut>
    <Header></Header>
    <div class="inner">
      <Navigation></Navigation>
      <div class="find-goods">
        <FindGoods></FindGoods>
      </div>
      <div class="category clearfix">
        <div class="content fl" v-for="(item, index) in categoryList" :key="index">
          <div @click="toCategory(item.typeId)">
            <div class="category-title" :class="{ selected_title: item.selected }">
              <span> {{ item.title }}</span>

            </div>
            <div class="category-content" :class="{ selected_content: item.selected }">
              <span> {{ item.content }}</span>
            </div>
          </div>
        </div>
      </div>
      <Category :categoryId="categoryId"></Category>
    </div>
    <el-backtop :right="100" :bottom="100" />
    <div>
      我是主页
    </div>
  </div>
</template>

<script setup>
import Shutcut from '@/components/common/Shutcut.vue';
import Header from '@/components/home/Header.vue';
import Navigation from '@/components/home/Navigation.vue';
import FindGoods from '@/components/home/FindGoods.vue';
import Category from '@/components/home/Category.vue';
import { ref } from 'vue';

let categoryList = ref([
  { typeId: 1, title: "精选", content: "猜你喜欢", selected: true },
  { typeId: 2, title: "智能先锋", content: "大电器城", selected: false },
  { typeId: 3, title: "居家优品", content: "品质生活", selected: false },
  { typeId: 4, title: "超市百货", content: "百货生鲜", selected: false },
  { typeId: 5, title: "时尚达人", content: "美妆穿搭", selected: false },
  { typeId: 6, title: "进口好物", content: "京东国际", selected: false },
])
let categoryId = ref(1)
function toCategory(id) {
  for (let i in categoryList.value) {
    if (categoryList.value[i].typeId != id) {
      categoryList.value[i].selected = false
    } else {
      categoryList.value[i].selected = true
    }
  }
  categoryId.value = id

}

</script>

<style scoped lang="less">
.inner {
  background-color: #f4f4f4;

  .category {
    width: var(--content-width);
    margin: 0 auto;
    background-color: #fff;
    height: 60px;
    text-align: center;

    .content {
      width: 196px;
      margin: 5px 0;

      &:first-child {
        padding-left: 10px;
      }

      &:not(:last-child) {
        border-right: 1px solid #e8e8e8;
      }

      .category-title {
        margin-bottom: 5px;
        font-size: 16px;
        font-weight: 700;
      }

      .category-content {
        font-size: 14px;
        color: #999;
      }

      &:hover div:last-child {
        cursor: pointer;
        color: #e1251b;
      }

      .selected_title {
        span {
          background-color: #e1251b;
          border-radius: 15px;
          padding: 5px 15px;
          color: #fff;
        }

      }
    }
  }

}
</style>