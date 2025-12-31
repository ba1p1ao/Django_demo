<template>
    <div class="nav">
        <div class="main clearfix">
            <div class="menu fl">
                <LeftMenu></LeftMenu>
            </div>
            <div class="banner fl">
                <Banner></Banner>
            </div>
        </div>

    </div>
</template>

<script setup>
import LeftMenu from './LeftMenu.vue';
import Banner from './Banner.vue';
</script>


<style scoped lang="less">
.nav {
    .main {
        width: var(--content-width);
        margin: 0 auto;
        padding-top: 10px;
        .banner {
            margin-left: 10px;
        }
    }
}
</style>