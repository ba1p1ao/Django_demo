<template>
	<div class="main clearfix">
		<div class="content">
			<div class="logo fl">
				<Logo></Logo>
			</div>
			<div class="serach-box fl">
				<div class="input-search fl">
					<SearchBox></SearchBox>
				</div>
				<div class="shopcart fl">
					<ShopCart></ShopCart>
				</div>
			</div>
			<div class="right fr">
				<img src="@/assets/images/header-right.png" alt="">
			</div>
		</div>
	</div>
</template>

<script setup>
import Logo from "@/components/common/Logo"
import SearchBox from "@/components/home/SearchBox"
import ShopCart from "@/components/home/ShopCart"
</script>

<style lang="less" scoped>
.main {
	.content {
		width: var(--content-width);
		margin: 0 auto;
		height: 140px;
		// border: 1px solid red;
	}

	.serach-box {
		width: 800px;
		height: 70px;
	}

	.right {
		img {
			width: 200px;
		}

		line-height: 140px;
	}
}
</style>