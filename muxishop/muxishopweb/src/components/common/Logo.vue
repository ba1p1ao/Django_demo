<template>
    <img class="logo" src="../../assets/images/logo/logo-big.png" alt="" @click="home">
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter()

function home() {
    router.push("/")
}

</script>

<style lang="less" scoped>
div {
    .logo {
        width: 100%;
        height: 100%;
    }
}   
</style>