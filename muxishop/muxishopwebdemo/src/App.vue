<template>
	<!-- 我们不要在app.vue中写代码，如果在这里写了，因为这里是入口就意味着
	 所有的页面都会包含这里的内容
	 除非你真的有所有的页面都需要公共的内容才需要写在这里
	 -->
	
  <router-view/>
</template>
<script setup>
	// import {getMainMenu} from "@/network/home"
	// getMainMenu().then(res=>{
	// 	console.log(res)
	// })
</script>
<style lang="less">

</style>
