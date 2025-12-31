<template>
	<div class="main">
		<div class="shopcart" @click="toShopCartPage">
			<el-badge :value="cartCount" class="item">
			    <span class="iconfont icon-gouwuche"></span>
			</el-badge>
			
			<span>我的购物车</span>
		</div>
	</div>
</template>

<script setup>
	import {useRouter} from "vue-router";
	import {useStore} from "vuex";
	const store = useStore();
	const cartCount = store.state.cartCount;
	const router = useRouter()
	
	const toShopCartPage = ()=>{
		router.push("/cart/detail")
	}
</script>

<style lang="less" scoped>
@red:#e2231a;
	.main {
		height: 140px;
		margin-top: 45px;
		margin-left: 20px;
		.shopcart {
			border:1px solid #e3e4e5;
			width: 130px;
			height: 35px;
			line-height: 35px;
			text-align: center;
			padding-top: 4px;
			.item {
				height: 25px;
				line-height: 25px;
				>span{
					color: @red;
					font-weight: 700;
				}
			
			}
			&:hover{
				cursor: pointer;
				border:1px solid @red;
			}
			>span{
				margin-left: 20px;
				color: @red;
			}
		}
	}
	
</style>