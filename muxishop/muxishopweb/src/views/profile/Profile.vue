<template>
    <div class="main">
        <Shutcut></Shutcut>
        <div class="profile">
            <div class="header">
                <div class="title clearfix">
                    <div class="log fl">
                        <Logo></Logo>
                    </div>
                    <div class="welcome fl">欢迎来到个人中心</div>
                    <div class="cart fr">
                        <ShopCart></ShopCart>
                    </div>
                </div>

            </div>

            <div class="content clearfix">
                <div class="left-menu fl">

                    <div v-for="(item, index) in componentList" :key="index" @click="currentComponent = item.component"
                        :class="[currentComponent == item.component ? 'active' : 'noactive']">
                        <a href="javascript:void(0)">{{ item.name }}</a>
                    </div>
                </div>
                <div class="right-content fl">
                    <component :is="components[currentComponent]"></component>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Shutcut from '@/components/common/Shutcut.vue';
import Logo from '@/components/common/Logo.vue';
import ShopCart from '@/components/home/ShopCart.vue';
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import BasicInfo from '@/components/profile/BasicInfo.vue';
import AddressManager from '@/components/profile/AddressManager.vue';
import MyOrder from '@/components/profile/MyOrder.vue';
import SecuritySetting from '@/components/profile/SecuritySetting.vue';


const router = useRouter()
const route = useRoute()

const componentList = ref([
    { component: "BasicInfo", name: "基本信息" },
    { component: "AddressManager", name: "地址管理" },
    { component: "MyOrder", name: "我的订单" },
    { component: "SecuritySetting", name: "安全设置" },
])
const componentIndex = route.query.component_index || 1
const currentComponent = ref(componentList.value[componentIndex - 1].component)
const components = {
    BasicInfo, AddressManager, MyOrder, SecuritySetting
}
console.log(route.query.component_index)


</script>


<style scoped lang="less">
.main {
    background-color: #f5f5f5;
    height: 100%;
}

.profile {

    .header {
        background-color: #DB2E16;

        .title {

            width: var(--content-width);
            margin: 0 auto;
            height: 80px;
            line-height: 80px;


            img {
                width: 80px;
                height: 80px;
            }

            .welcome {
                margin-left: 50px;
                font-size: 30px;
                font-weight: 700;
                color: #fff;
            }

            .cart {
                margin: 20px 0;
            }
        }
    }


    .content {
        width: var(--content-width);
        margin: 0 auto;
        margin-top: 20px;
        height: 100%;
        .left-menu {
            width: 150px;
            font-size: 14px;

            .active {
                margin: 20px 0;

                a {
                    cursor: pointer;
                    color: #DB2E16;
                    font-weight: 700;
                }
            }

            .noactive {
                margin: 20px 0;

                a {
                    color: #333;

                    &:hover {
                        cursor: pointer;
                        color: #DB2E16;
                        text-decoration: underline !important;
                        text-decoration-color: #DB2E16;
                    }
                }
            }

        }

        .right-content {
            width: 1050px;
            margin: 20px 0;
        }
    }
}
</style>
