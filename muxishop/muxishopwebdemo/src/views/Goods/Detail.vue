<template>
	<div>
		<Shortcut></Shortcut>
		<Header></Header>
		<div class="goods">
			<div class="good clearfix">
				<!-- {{goodsList}} -->
				<div class="fl">
					<img :src="goodsList.data.image" alt="">
				</div>
				<div class="good-content fl">
					<div class="desc">{{goodsList.data.name}}</div>
					<div class="price">{{goodsList.data.p_price}}</div>
					<div class="count">
						<el-input-number
						    v-model="num"
						    @change="handleChange"
						    :min="1"
						    :max="10"
						    label="描述文字"
						  ></el-input-number>
					</div>
					<a href="#" class="add-cart" 
					@click="addCartData(goodsList.data.sku_id,num,0)">加入购物车</a>
				</div>
			</div>
			<div class="comment">
				<Comment :skuId="$route.params.sku_id"></Comment>
			</div>
		</div>
	</div>
</template>


<script setup>
import Shortcut from "@/components/common/Shortcut";
import Header from "@/components/home/Header";
import Comment from "@/components/GoodsDetail/Comment";

import {addCartData} from "@/utils/goods.js";
import {getGoodsDetail} from "@/network/goods.js"
import {onMounted, ref, reactive} from "vue";
import {useRoute} from "vue-router";
let skuId = ref("");
const route = useRoute();
let goodsList=reactive({
	data:{}
})
onMounted(()=>{
	skuId.value = route.params.sku_id;
	getGoodsDetail(skuId.value).then(res=>{
		goodsList.data=res.data;
	})
})
let num = ref(1);
const handleChange=(value)=>{
	num.value=value;
}


</script>

<style lang="less" scoped>
.goods{
	width: var(--content-width);
	margin: 0 auto;
	.good{
		
		img{
			width: 350px;
			height: 350px;
		}
		.good-content{
			margin-top: 70px;
			margin-left: 20px;
			width: 600px;
			.desc{
				font-size: 16px;
				color: #666;
			}
			.price{
				margin-top: 10px;
				font-size: 22px;
				color:#e4393c;
			}
			.count{
				margin-top: 10px;
			}
			.add-cart{
				margin-top: 10px;
				display: block;
				width: 150px;
				height: 45px;
				background-color: #df3033;
				font-size: 18px;
				color: white;
				font-weight: 700;
				text-align: center;
				line-height: 45px;
			}
		}
	}
	.comment{
		margin-top: 20px;
	}
}

</style>