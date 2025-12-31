<template>
	<div class="shop-cart">
		<Shortcut></Shortcut>
		<Header></Header>
		<div class="goods">
			<div class="goods-num">
				全部商品&nbsp;&nbsp;{{cartSumNums}}
			</div>
			<table>
				<tr>
					<th>
						<input type="checkbox" :checked="allChecked" @click="checkedAll">
						全选
					</th>
					<th>商品</th>
					<th></th>
					<th>单价</th>
					<th>数量</th>
					<th>小计</th>
					<th>操作</th>
				</tr>
				<!-- 这里是我们将来写循环的地方 -->
				<tr v-for="(item,key) in cartListData" :key="key">
					<td>
						<input type="checkbox" 
						:checked="item.checked"
						@click="changeChecked(item.sku_id)"
						>
					</td>
					<td>
						<img :src="item.goods.image" alt="">
					</td>
					<td>
						{{item.goods.name}}
					</td>
					<td>
						￥{{item.goods.p_price}}
					</td>
					<td>
						<el-input-number
						    v-model="item.nums"
						    @change="(newValue,oldValue)=>handleChange(newValue,oldValue,item.sku_id)"
						    :min="1"
						    :max="10"
						    label="描述文字"
						  ></el-input-number>
					</td>
					<td>
						￥{{(item.goods.p_price*item.nums).toFixed(2)}}
					</td>
					<td>删除</td>
				</tr>
			</table>
			<div class="bottom-tool">
				<div class="tool-left">
					<input type="checkbox" :checked="allChecked" @click="checkedAll">
					全选
					<span class="delete-selected" @click="deleteGoods(0)">删除选中商品</span>
					<span class="clear-cart"  @click="deleteGoods(1)">清理购物车</span>
				</div>
				<div class="tool-right">
					<span class="selected-goods">已选择 <em>{{selectedGoodsCount}}</em>件商品 </span>
					<span class="price-count">总价: <em>￥{{priceCount.toFixed(2)}}</em></span>
					<a href="#" class="go-order" @click="goOrder">去结算</a>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import Shortcut from "@/components/common/Shortcut";
	import Header from "@/components/home/Header";
	import { getCartDetailData, updateCartGoodsNumData,deleteCartGoods } from "@/network/cart.js";
	import { onMounted, ref, watch } from "vue";
	import {useStore} from "vuex";
	import {createOrderData} from "@/network/order.js";
	import {useRouter} from "vue-router";
	const router = useRouter();
	
	let cartListData=ref([]);
	let cartSumNums=ref(0);
	
	onMounted(()=>{
		getCartDetailData().then(res=>{
			console.log(res.data);
			cartListData.value=res.data;
			// 计算商品总数
			for(let i in res.data){
				cartSumNums.value += res.data[i].nums;
			}
		})
		store.dispatch("updateCart");
		
		
	})
	
	
	// 修改购物车中商品的数量
	const store = useStore()
	const handleChange= (newValue,oldValue,skuId) => {
		console.log(newValue,oldValue,skuId);
		let data=ref({
			sku_id:skuId,
			nums:newValue
		})
		// 需要更新我们的商品数量
		updateCartGoodsNumData(data.value).then(res=>{
			// console.log(res)
			store.dispatch("updateCart");
			// 这种实现方式是有bug
			// cartSumNums.value = store.state.cartCount;
		})
		cartSumNums.value += newValue - oldValue;
	}
	// 全选与取消全选的逻辑
	let allChecked=ref(false);
	const checkedAll= () => {
		// console.log(cartListData.value);
		// 这个是点击了全选
		if(allChecked.value==false){
			for(let i in cartListData.value){
				cartListData.value[i].checked=true;
			}
			allChecked.value=true;
			// todo  更新商品的件数
			selectedGoodsCount.value = cartListData.value.length;
		}else{
			// 取消了全选的逻辑
			for(let i in cartListData.value){
				cartListData.value[i].checked=false;
			}
			allChecked.value=false;
			// todo  更新商品的件数
			selectedGoodsCount.value = 0;
		}
	}
	
	// 计算商品的总件数与总价格
	let selectedGoodsCount = ref(0);
	let priceCount = ref(0);
	
	// 计算商品总价
	watch(()=>cartListData, (newValue,oldValue) => {
		console.log(cartListData);
		priceCount.value = 0;
		cartSumNums.value = 0;
		cartListData.value.forEach( (element) => {
			if(element.checked){
				priceCount.value += element.goods.p_price * element.nums;
			}
			cartSumNums.value += element.nums;
		} )
	},{
		// 加一个深度监听参数，才能监听到ref变量中包含列表，列表中包含json的值的变化
		deep:true,
	} )
	
	// 单个选中与取消商品的逻辑
	const changeChecked = (id) => {
		// console.log(id);
		for(let i in cartListData.value){
			if(cartListData.value[i].sku_id==id){
				cartListData.value[i].checked = !cartListData.value[i].checked
			}
			// 修改选中商品的数量
			selectedGoodsCount.value=0;
			cartListData.value.forEach( (element) => {
				if(element.checked == true){
					selectedGoodsCount.value+=1;
				}
			} )
			// 更新全选那个框的状态
			if(selectedGoodsCount.value == cartListData.value.length){
				allChecked.value = true;
			}else{
				allChecked.value = false;
			}
		}
	}	
	
	// 记录要删除的商品
	let deleteGoodsList = ref([]);
	let noDeleteGoodsList = ref([]);
	const deleteGoods=(deleteStatus) => {
		deleteGoodsList.value = [];
		noDeleteGoodsList.value = [];
		if(deleteStatus==0){
			cartListData.value.forEach( (element) => {
				if(element.checked){
					deleteGoodsList.value.push(element.sku_id);
				}else{
					noDeleteGoodsList.value.push(element);
				}
			} )
			
			if(deleteGoodsList.value.length == 0){
				alert("请先选择要删除的商品")
			}else{
				let res = confirm("此操作将会把商品永久的移除购物车，是否继续?")
				if(res){
					// 请求后端删除接口
					deleteCartGoods(deleteGoodsList.value).then(res=>{
						alert("删除成功");
						// 第一种方法可以手动刷新页面
						// location.reload();
						// 第二种方式，改变cartListData的值，然后动态渲染
						cartListData.value = noDeleteGoodsList.value;
						store.dispatch("updateCart");
						selectedGoodsCount.value = 0;
					})
					
				}else{
					alert("取消删除");
				}
			}
		}else{
			let res = confirm("您将要清空购物车，是否继续?")
			if(res){
				cartListData.value.forEach( (element) => {
					deleteGoodsList.value.push(element.sku_id);

				} )
				// 请求后端删除接口
				deleteCartGoods(deleteGoodsList.value).then(res=>{
					alert("清空购物车成功");
					// 第一种方法可以手动刷新页面
					// location.reload();
					// 第二种方式，改变cartListData的值，然后动态渲染
					cartListData.value = noDeleteGoodsList.value;
					store.dispatch("updateCart");
					selectedGoodsCount.value = 0;
					location.href="/";
				})
				
			}else{
				alert("取消删除")
			}
		}
		

	}

	// 去结算，创建订单功能实现
	let orderGoodsList=ref([]);
	const goOrder=() => {
		for(let i in cartListData.value){
			if(cartListData.value[i].checked==true){
				orderGoodsList.value.push(cartListData.value[i])
			}
		}
		let orderData=ref({
			trade:{
				order_amount:priceCount.value,
			},
			goods:orderGoodsList.value
		})
		// 往后端发送网络请求
		let orderNo=ref("");
		createOrderData(orderData.value).then(res=>{
			orderNo.value = res.data.trade_no;
			router.push("/order/"+orderNo.value)
			store.dispatch("updateCart");
		})
		
	}

</script>

<style lang="less" scoped>
	.shop-cart{
		.goods{
			width: var(--content-width);
			margin: 0 auto;
			.goods-num{
				color:#e2231a;
				font-size: 16px;
				font-weight: 700;
			}
			table{
				border-collapse: collapse;
				tr{
					border-bottom:1px solid #f0f0f0;
					

					th{
						background-color: #f3f3f3;
						height: 45px;
						&:nth-child(1){
							width: 50px;
							padding-left: 10px;
						}
					}
					td{
						padding-top: 10px;
						padding-bottom: 10px;
						img{
							width: 80px;
							height: 80px;
							border:1px solid #eeeeee;
						}
						&:nth-child(1){
							text-align: center;
						}
						&:nth-child(3){
							width: 600px;
							padding-left: 20px;
							padding-right: 50px;
							&:hover{
								color:#e2231a;
								cursor: pointer;
							}
						}
						&:nth-child(4){
							width: 80px;
							text-align: center;
						}
						&:nth-child(5){
							width: 80px;
							text-align: center;
						}
						&:nth-child(6){
							width: 120px;
							text-align: center;
							font-weight: 700;
						}
						&:nth-child(7){
							width: 80px;
							text-align: center;
						}
					}
				}
			}
			.bottom-tool{
				margin-top: 10px;
				border:1px solid #f0f0f0;
				height: 50px;
				line-height: 50px;
				.tool-left{
					float: left;
					padding-left: 20px;
					span {
						padding:0 10px;
						&:hover{
							color:#e2231a;
							cursor: pointer;
						}
					}
					.clear-cart{
						font-size:14px;
						font-weight: 700;
					}
				}
				.tool-right{
					float: right;
					text-align: right;
					span{
						font-weight: 700;
						color:#acacac;
						em{
							color:#e2231a;
							font-weight: 700;
							padding: 0 5px;
						}
					}
					.price-count{
						em{
							font-size: 16px;
						}
					}
					.go-order{
						display: inline-block;
						width: 95px;
						line-height: 50px;
						text-align: center;
						height: 50px;
						background-color: #e2231a;
						color:white;
						font-size: 18px;
						font-weight: 700;
					}
				}
			}
		}
	}
</style>