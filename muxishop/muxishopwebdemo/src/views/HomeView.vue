<template>
	<div>
		<Shortcut></Shortcut>
		<Header></Header>
		<div class="inner">
			<Navigation></Navigation>
			<div class="find-goods">
				<FindGoods></FindGoods>
			</div>
			<div class="category clearfix">
				<div class="content fl" v-for="(item,index) in category" :key="index">
					<div @click="toCategory(item.typeId)">
						<div class="category-title" :class="{selected_title: item.selected}">{{item.title}}</div>
						<div class="category-content" :class="{selected_content: item.selected}">{{item.content}}</div>
					</div>

				</div>
			</div>
			<Category :categoryId="categoryId"></Category>
		</div>
		<el-backtop right="200" bottom="200"></el-backtop>
		<div>我是主页</div>
		
	</div>
</template>

<script setup>
import Shortcut from "@/components/common/Shortcut"
import Header from "@/components/home/Header"
import Navigation from "@/components/home/Navigation"
import FindGoods from "@/components/home/FindGoods"
import Category from "@/components/home/Category"


import { ref } from "vue";

let category = ref([
	{typeId:1,title:"精选",content:"猜你喜欢",selected:true},
	{typeId:2,title:"智能先锋",content:"大电器城",selected:false},
	{typeId:3,title:"居家优品",content:"品质生活",selected:false},
	{typeId:4,title:"超市百货",content:"百货生鲜",selected:false},
	{typeId:5,title:"时尚达人",content:"美妆穿搭",selected:false},
	{typeId:6,title:"进口好物",content:"京东国际",selected:false},
])
let categoryId=ref(1);
const toCategory=(typeId)=>{
	categoryId.value = typeId;
	for(let i in category.value){
		category.value[i].selected=false;
		if(typeId==(parseInt(i)+1)){
			category.value[i].selected=true;
		}
	}
}

</script>

<style lang="less" scoped>
	.inner {
		background-color: #f4f4f4;
		.find-goods {
			padding-top: 15px;
			padding-bottom: 15px;
		}
		.category{
			width: var(--content-width);
			margin: 0 auto;
			background-color: #fff;
			height: 70px;
			text-align: center;
			.content{
				width: 198px;
				margin-top: 10px;
				&:not(:last-child){
					border-right: 1px solid #e8e8e8;
				}
				.category-title{
					font-size: 16px;
					font-weight: 700;
					height: 30px;
					line-height: 30px;
				}
				.category-content{
					font-size: 14px;
					color:#999;
				}
				&:hover{
					cursor: pointer;
					color:#e1251b;
				}
				&:hover div:last-child{
					cursor: pointer;
					color:#e1251b;
				}
				>div{
					width: 80px;
					margin: 0 auto;
					
				}
				.selected_title{
					background-color: #e1251b;
					color: #fff;
					border-radius: 15px;
				}
				.selected_content{
					color:#e1251b;
				}
			}
		}
	}
	
</style>