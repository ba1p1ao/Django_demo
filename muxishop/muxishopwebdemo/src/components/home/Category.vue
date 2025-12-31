<template>
	<div class="main">
		<div class="category clearfix">
			<!-- {{goods}} -->
			<div class="goods fl" v-for="(item,index) in goods" :key="index"
			@click="toGoodsDetail(item.sku_id)"
			>
				<div class="first-row">
					<img :src="item.image" alt="">
				</div>
				<div class="second-row dian2">
					{{item.name}}
				</div>
				<div class="third-row">
					<small>￥</small>
					<span>{{item.jd_price}}</span>
				</div>
			</div>
		</div>
	</div>

</template>

<script setup>
import {ref, onMounted, watch} from 'vue';
import {getCategoryGoods} from "@/network/home.js";
import {toGoodsDetail} from "@/utils/goods.js";
	let categoryId = defineProps(["categoryId"])
	let goods = ref([]);
	// 用来存储现在是多少页
	let page=ref(1);
	onMounted(()=>{
		getCategoryGoodsData(1,1);
	})
	const getCategoryGoodsData=(categoryId,page)=>{
		getCategoryGoods(categoryId,page).then(res=>{
			let serverData = res.data;
			console.log(serverData);
			for(let i in serverData){
				let jsonData=JSON.parse(serverData[i]);
				goods.value.push(jsonData);
			}
			
		})
	}
	
	watch(categoryId,(newValue,oldValue)=>{
		console.log(newValue.categoryId);
		goods.value=[];
		getCategoryGoodsData(newValue.categoryId,1);
		page.value=1;
	})
	
	const windowScroll=()=>{
		// 可视区域的高度，就是我们用眼睛能看见的内容的高度
		let clientHeight=document.documentElement.clientHeight;
		// 滚动条在文档中的高度的位置（滚出可见区域的高度）
		let scrollTop=document.documentElement.scrollTop;
		// 所有内容的高度
		let scrollHeight=document.body.scrollHeight;
		
		if(clientHeight+scrollTop>=scrollHeight){
			// console.log(categoryId.categoryId);
			page.value+=1;
			getCategoryGoodsData(categoryId.categoryId,page.value);
		}
		
	}
		
	window.addEventListener("scroll",windowScroll);
		
</script>

<style lang="less" scoped>
	.main{
		margin-top: 10px;
		.category{
			width: var(--content-width);
			margin: 0 auto;
			.goods{
				background-color: #fff;
				width: 232px;
				height: 320px;
				margin-bottom: 10px;
				&:hover{
					cursor: pointer;
				}
				// margin-right: 10px;
				&:not(:nth-child(5n)){
					margin-right: 10px;
				}
				.first-row{
					height: 210px;
					line-height: 210px;
					text-align: center;
					img {
						width: 150px;
						height: 150px;
					}
				}
				.second-row{
					font-size: 12px;
					color: #666;
					width: 190px;
					height: 40px;
					line-height: 20px;
					margin: 0 auto;
					&:hover{
						color: #c81623;
					}
					
				}
				.third-row{
					color: #c81623;
					width: 190px;
					margin: 0 auto;
					margin-top: 20px;
					span{
						font-weight: 700;
						font-size: 20px;
					}
				}
			}
		}
	}
	
</style>