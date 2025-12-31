<template>
	<div class="second">
		<!-- 我是二级菜单xxxxxxxxxxxxxxxxxxxxxxx {{showSecondMenuIndex}} -->
		<div class="menu-content" v-for="(item,index) in showSubMenuData" :key="index">
			<!-- {{showSubMenuData}} -->
			<div class="menu-title">
				<span v-for="(d,i) in item.data" :key="i">
					<a href="" v-show="d.type==='channel'">{{d.name}}
					<img src="@/assets/images/menu/arrows-white.png" alt="">
					</a>
				</span>
			</div>
			<div class="menu-detail">
				<div class="menu-detail-item">
					<span  v-for="(d,i) in item.data" :key="i">
						<span class="menu-detail-tit" v-if="d.type==='dt'">
							<a :href="'/goods_list/'+d.name+'/1/1'">{{d.name}}
							<img src="@/assets/images/menu/arrows-black.png" alt="">
							</a>
						</span>
						<span class="menu-detail-data" v-else-if="d.type==='dd'">
							<a :href="'/goods_list/'+d.name+'/1/1'">{{d.name}}</a>
						</span>
					</span>
				</div>
			</div>
			
		</div>
	</div>
</template>

<script setup>
import { getSecondMenu } from "@/network/home.js";
import { computed, ref, watch } from "vue";
	const showSecondMenuIndex=defineProps(["showSecondMenuIndex"]);
	watch(showSecondMenuIndex,(newValue,oldValue)=>{
		// console.log(newValue.showSecondMenuIndex);
		getSecondMenu(newValue.showSecondMenuIndex).then(res=>{
			console.log(res);
			initMenuData(res.data);
		})
	});
	let subMenuData=ref([]);
	const initMenuData=(menuData)=>{
		// 这里每次初始化的时候，必须把subMenuData设置为空，
		// 不然的话就会出现数据累加的问题
		subMenuData.value=[];
		for(let i in menuData){
			let jsonData = JSON.parse(menuData[i]);
			subMenuData.value.push(jsonData);
		}
	}
	
	const showSubMenuData=computed(()=>{
		let resultList=[];
		let result={"index":"","data":[]};
		for(let i in subMenuData.value){
			let id = subMenuData.value[i].sub_menu_id;
			let data={
				"name":subMenuData.value[i].sub_menu_name,
				"type":subMenuData.value[i].sub_menu_type
			}
			if(result["index"]!=null && id==result["index"]){
				result["data"].push(data);
			}else{
				result={"index":"","data":[]};
				result["index"]=id;
				result["data"].push(data);
				resultList.push(result)
			}
		}
		return resultList;
	})
	
</script>

<style lang="less" scoped>
@red:#e2231a;
	.second{
		width: 1000px;
		background-color: #fff;
		border: 2px solid #e9e9e9;
		padding:20px;
		.menu-content {
			.menu-title {
				a {
					display:inline-block;
					background-color: black;
					color:white;
					margin-right: 10px;
					height:25px;
					line-height: 25px;
					padding:0 10px;
					img {
						height: 18px;
					}
					&:hover{
						background-color: @red;
					}
				}
				
				
			}
		
		.menu-detail{
			margin-top: 15px;
			.menu-detail-item {
				.menu-detail-tit{
					a{
						font-weight:700;
						img{
							height: 18px;
						}
						&:hover{
							color:@red;
						}
					}
				}
				.menu-detail-data{
					a{
						margin-left: 20px;
						&:hover{
							color:@red;
						}
					}
				}
			}
		}
		}
	}
</style>