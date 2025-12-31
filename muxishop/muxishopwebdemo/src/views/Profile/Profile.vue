<template>
	<div>
		<Shortcut></Shortcut>
		<div class="profile">
			<div class="header">
				<div class="title clearfix">
					<div class="logo fl">
						<Logo></Logo>
					</div>
					<div class="shop-name fl">慕西商城</div>
					<div class="name fl">个人中心</div>
					<div class="cart fr">
						<ShopCart></ShopCart>
					</div>
				</div>
			</div>
			<div class="main clearfix">
				<div class="content">
					<div class="left-menu fl">
						<div class="basic" 
						:class="activeIndex==1?'active-menu':false"
						@click="changeComponent(1)"
						>基本信息</div>
						<div class="address"
						:class="activeIndex==2?'active-menu':false"
						@click="changeComponent(2)"
						>地址管理</div>
						<div class="order"
						:class="activeIndex==3?'active-menu':false"
						@click="changeComponent(3)"
						>我的订单</div>
						<div class="security"
						:class="activeIndex==4?'active-menu':false"
						@click="changeComponent(4)"
						>安全设置</div>
					</div>
					<div class="right-content fl">
						<component :is="activeComponentName"></component>
					</div>
				</div>

			</div>
		</div>
		
	</div>
</template>

<script>
	import Shortcut from "@/components/common/Shortcut";
	import Logo from "@/components/common/Logo";
	import ShopCart from "@/components/home/ShopCart";
	import {useRouter, useRoute} from "vue-router";
	import {ref, onMounted} from 'vue';
	import BasicInfo from  "@/components/Profile/BasicInfo";
	import AddressManager from  "@/components/Profile/AddressManager";
	import MyOrder from  "@/components/Profile/MyOrder";
	import SecuritySettings from  "@/components/Profile/SecuritySettings";
	
	export default {
		name:"Profile",
		setup(){
			const router = useRouter();
			const route = useRoute();
			let activeComponentName = ref("BasicInfo");
			let activeIndex = ref(1);
			let activeComponent = ref([
				{index:1,componentName:'BasicInfo'},
				{index:2,componentName:'AddressManager'},
				{index:3,componentName:'MyOrder'},
				{index:4,componentName:'SecuritySettings'},
			])
			const changeComponent=(index) => {
				activeIndex.value=index;
				activeComponent.value.forEach( (element) => {
					if(element.index==activeIndex.value){
						activeComponentName.value=element.componentName;
					}
				} )
				router.push("profile?activeIndex="+index)
				
			}
			
			onMounted( () => {
				activeIndex.value = route.query.activeIndex;
				activeComponent.value.forEach( (element) => {
					if(element.index==activeIndex.value){
						activeComponentName.value=element.componentName;
					}
				} )
			} )
			return {
				activeComponentName,
				activeIndex,
				activeComponent,
				changeComponent
			}
		},
		components:{
			BasicInfo,
			AddressManager,
			MyOrder,
			SecuritySettings,
			Shortcut,
			Logo,
			ShopCart
		}
		
		
	}
	
	
	
	
</script>

<style lang="less" scoped>
	.profile {
		.header{
			border-bottom: 2px solid #f00c0c;
			height: 130px;
			line-height: 130px;
		}
		.title{
			width: var(--content-width);
			margin: 0 auto;
			height: 80px;
			line-height: 80px;
			.logo{
				height: 40px;
			}
			.shop-name{
				font-size: 40px;
				margin-left: 10px;
				margin-top: 30px;
				font-weight: 700;
				color:#f00c0c;
			}
			.name{
				font-size: 25px;
				margin-left: 10px;
				margin-top: 30px;
			}
			.cart{
				margin-top: 30px;
			}
		}
		>.main{
			background-color: #f5f5f5;
			.content{
				width: var(--content-width);
				margin: 0 auto;
				.left-menu{
					margin-top: 20px;
					color:#333;
					font-size: 14px;
					height: 800px;
					div{
						margin-top: 20px;
						border-bottom: 1px solid #f5f5f5;
						&:hover{
							cursor: pointer;
							color: #f00c0c;
							border-bottom: 1px solid #f00c0c;
						}
					}
					.active-menu{
						color: #f00c0c;
					}
					
				}
				.right-content{
					margin-top: 40px;
					margin-left: 50px;
					background-color: #fff;
				}
			}

		}
	
	}
</style>