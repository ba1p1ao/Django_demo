<template>
	<!--
	 滚动插件的官网
	 https://doc.wssio.com/opensource/vue3-seamless-scroll/options.html#v-model
	  https://github.com/xfy520/vue3-seamless-scroll
	  -->
	<div class="find-goods">
<!-- 		我是发现好物
		<div v-for="(item,index) in goodsList">
			{{item.name}}
		</div> -->
		<img src="@/assets/images/find-goods.png" alt="">
		  <vue3-seamless-scroll 
		  :list="goodsList" 
		  class="scroll"
		  direction="left"
		  hover="true"
		  step="0.5"
		  singleLine="true"
		  >
			<div class="item" v-for="(item, index) in goodsList" :key="index"
			@click="toGoodsDetail(item.sku_id)"
			>
				<div v-if="index % 2 === 0">
					<span class="dian1">{{item.name}}</span>
					<img :src="item.image" alt="">
				</div>
				<div v-else>
					<img :src="item.image" alt="">
					<span class="dian1">{{item.name}}</span>
				</div>
			  
			</div>
	  </vue3-seamless-scroll>
	</div>
</template>

<script setup>
import {getFindGoods} from "@/network/home.js"
import { onMounted, ref } from "vue";
import {toGoodsDetail} from "@/utils/goods.js"


const goodsList=ref([]);

onMounted(()=>{
	getFindGoods().then(res=>{
		console.log(res.data);
		// for(let i in res.data){
		// 	let jsonData = JSON.parse(res.data[i]);
		// 	goodsList.value.push(jsonData);
		// }
		goodsList.value = res.data;
	})
})

</script>

<style scoped lang="less">
	.find-goods{
		width: var(--content-width);
		margin: 0 auto;
		>img{
			width: 190px;
			height: 260px;
			float: left;
		}
		.scroll {
			height: 260px;
			width: 1000px;
			overflow: hidden;
			margin-left: 200px;
			background-color: #fff;
		  .item {
		    &:hover{
				cursor: pointer;
			}
			height: 260px;
			width: 150px;
			margin-top: 15px;
			padding: 10px;
			span{
				width: 150px;
				font-size: 15px;
				margin: 10px 10px;
			}
			img {
				padding: 10px;
				width: 150px;
				height: 150px;
				border-radius: 20px;
			}
		  }
		}
	}

</style>