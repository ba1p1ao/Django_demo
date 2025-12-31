<template>
    <div class="main">
        <div class="content">
            <div class="logo fl">
                <Logo></Logo>
            </div>
            <div class="search-box fl">
                <div class="input-search fl">
                    <SearchBox></SearchBox>
                </div>
                <div class="shopcart fl">
                    <ShopCart></ShopCart>
                </div>
            </div>
            <div class="right fr">
                <img src="../../assets/images/header-right.png" alt="">
            </div>
        </div>
    </div>
</template>

<script setup>
import Logo from '../common/Logo.vue';
import SearchBox from './SearchBox.vue';
import ShopCart from './ShopCart.vue';
</script>


<style lang="less" scoped>
.main {
    .content {
        width: var(--content-width);
        margin: 0 auto;
        height: 140px;
        //border: 1px solid red;

        .logo {
            line-height: 140px;
            width: 140px;
            height: 140px;
        }

        .search-box {
            width: 800px;
            height: 140px;

            .shopcart {
                margin-top: 45px;
                margin-left: 25px;
            }
        }

        .right {
            img {
                width: 200px;

            }

            line-height: 140px;

        }
    }
}
</style>