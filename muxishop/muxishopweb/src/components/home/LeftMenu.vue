<template>
    <div class="main-menu" @mouseleave="noItem()">
        <ul>
            <li 
            v-for="(item, i) in leftMenuData" 
            :key="i"
            @mouseenter="showItem(item, i)"
            >
                <span v-for="(name, j) in item['data']" :key="j">
                    <a href="javascript:void(0)" @click="search(name)">{{ name }}</a>
                    <span v-if="item['data'].length - j - 1">&nbsp;/&nbsp;</span>
                </span>
            </li>
        </ul>

        <div class="second-menu" v-show="isShowItem">
            
            <SecondMenu :showSecondMenuIndex="showSecondMenuIndex"></SecondMenu>
        </div>
    </div>

</template>


<script setup>
import { computed, onMounted, ref } from "vue";
import { getMainMenu } from '@/network/home.js';
import SecondMenu from "./SecondMenu.vue";
import { useRouter } from "vue-router";

onMounted(() => {
    getMainMenu().then(res => {
        initMenuData(res.data)
    })
})

let leftMenuData = ref([])
const initMenuData = (menuData) => {
    var result = { "index": "", "data": [] }
    for (let i in menuData) {
        // 直接使用对象，不需要 JSON.parse
        let jsonData = menuData[i]
        let id = jsonData.main_menu_id
        if (result["index"] != null && id == result["index"]) {
            result["data"].push(jsonData.main_menu_name)
        } else {
            result = { "index": "", "data": [] };
            result["index"] = id
            result["data"].push(jsonData.main_menu_name)
            leftMenuData.value.push(result)
        }
    }
}

let isShowItem = ref(false)
let showSecondMenuIndex = ref()
function showItem(item, i) {
    isShowItem.value = true
    showSecondMenuIndex.value = i + 1
}
function noItem() {
    isShowItem.value = false
}

const router = useRouter()
function search(keyword) {
    router.push("/goods_list/" + keyword + "/1/1/")
}
</script>

<style scoped lang="less">
@red: #e2231a;

.main-menu {
    width: 190px;
    height: 470px;
    background-color: #fff;
    position: relative;

    ul {
        padding-top: 10px;

        li {
            padding-left: 15px;
            line-height: 25px;
            height: 25px;

            &:hover {
                cursor: pointer;
                background-color: #d9d9d9;
            }

            a {
                font-size: 12px;
                color: #333;

                &:hover {
                    cursor: pointer;
                    color: @red;
                }
            }
        }
    }

    .second-menu {
        position: absolute;
        left: 190px;
        top: 0px;
        z-index: 999;
    }
}
</style>