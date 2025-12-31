<template>
	<div class="main">
		<div class="content">
			<input type="text" placeholder="大周老师的秘密" ref="searchWord">
			<span class="iconfont icon-fangdajing" @click="search(this.$refs.searchWord.value)"></span>
		</div>
		<div class="hotword">
			<a v-for="(item, key) in hotWords" :key="key" :class="item.active === true ? 'active' : ''"
				@click="search(item.word)" href="#">{{ item.word }}</a>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const hotWords = ref([
	{ "word": "电脑", "active": true },
	{ "word": "手机", "active": false },
	{ "word": "裙子", "active": false },
	{ "word": "空调", "active": false },
	{ "word": "裤子", "active": false },
])
const search = (keyword) => {
	router.push("/goods_list/" + keyword + "/1/1");
	hotWords.value.forEach((d) => {
		if (d.word == keyword) {
			d.active = true;
		} else {
			d.active = false;
		}
	})
}
</script>

<style lang="less" scoped>
@red: #e2231a;

.main {
	height: 140px;
	margin-top: 45px;

	.content {
		width: 550px;
		height: 35px;
		border: 2px solid @red;
		margin-left: 80px;

		input {
			width: 485px;
			line-height: 35px;
			height: 35px;
			padding-left: 15px;
		}

		span {
			display: inline-block;
			background-color: @red;
			width: 50px;
			height: 35px;
			line-height: 35px;
			text-align: center;
			color: white;
			font-weight: 700;

			&:hover {
				cursor: pointer;
				background-color: #c81623;
			}
		}

		.hotword {
			margin-left: 80px;
			margin-top: 10px;

			a {
				color: #999;
				margin-right: 10px;

				&:hover {
					color: @red;
				}
			}

			.active {
				color: @red;
			}

		}
	}
}
</style>