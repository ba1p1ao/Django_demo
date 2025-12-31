<template>
    <div class="second">
        <div class="menu-content">
            <span v-for="(item, i) in secondMenuData" :key="i">
                <div class="menu-title">
                    <span v-for="(item, j) in item['channel']" :key="j">

                        <a href="javascript:void(0)" @click="search(item)">
                            {{ item }}
                            <img src="@/assets/images/menu/arrows-white.png" alt="">
                        </a>

                    </span>
                </div>
                <div class="menu-detail">
                    <div class="menu-detail-item clearfix">
                        <span>
                            <div class="menu-detail-title fl">
                                <span v-for="(item, j) in item['dt']" :key="j">
                                    <a href="javascript:void(0)" @click="search(item)">{{ item }}
                                        <img src="@/assets/images/menu/arrows-black.png" alt="">
                                    </a>
                                </span>
                            </div>
                            <div class="menu-detail-data fl">
                                <span v-for="(item, j) in item['dd']" :key="j">
                                    <a href="javascript:void(0)" @click="search(item)">{{ item }}</a>
                                </span>
                            </div>

                        </span>
                    </div>
                </div>
            </span>
        </div>
    </div>
</template>

<script setup>
import { getSecondMenu } from '@/network/home.js';
import { watch, ref } from 'vue';
import { useRouter } from 'vue-router';
const showSecondMenuIndex = defineProps(["showSecondMenuIndex"])

watch(showSecondMenuIndex, (newValue, oldValue) => {
    // getSecondMenu
    // console.log(newValue.showSecondMenuIndex)
    getSecondMenu(newValue.showSecondMenuIndex).then(res => {
        initSecondMenu(res.data)
    })
})
const router = useRouter()
function search(keyword) {
    router.push("/goods_list/" + keyword + "/1/1/")
}
let secondMenuData = ref([])
function initSecondMenu(secondMenu) {
    let result = { "sub_menu_id": "", "channel": [], "dt": [], "dd": [] }
    // 避免重复累加，需要每次设置为空
    secondMenuData.value = []
    // console.log(secondMenu)
    for (let i in secondMenu) {
        // 直接使用对象，不需要 JSON.parse
        let jsonData = secondMenu[i]
        // console.log(jsonData)
        if (result["sub_menu_id"] != null && result["sub_menu_id"] == jsonData.sub_menu_id) {
            if (jsonData.sub_menu_type == "channel") {
                result["channel"].push(jsonData.sub_menu_name)
            } else if (jsonData.sub_menu_type == "dt") {
                result["dt"].push(jsonData.sub_menu_name)
            } else {
                result["dd"].push(jsonData.sub_menu_name)
            }
        } else {
            result = { "sub_menu_id": "", "channel": [], "dt": [], "dd": [] }
            result["sub_menu_id"] = jsonData.sub_menu_id
            if (jsonData.sub_menu_type == "channel") {
                result["channel"].push(jsonData.sub_menu_name)
            } else if (jsonData.sub_menu_type == "dt") {
                result["dt"].push(jsonData.sub_menu_name)
            } else {
                result["dd"].push(jsonData.sub_menu_name)
            }
            secondMenuData.value.push(result)
        }
    }
    // console.log(secondMenuData.value)
}



</script>

<style scoped lang="less">
@red: #e2231a;

.second {
    width: 1000px;
    min-height: 470px;
    border: 2px solid #e9e9e9;
    background-color: #fff;
    padding: 20px;
    margin-left: 5px;

    .menu-content {
        .menu-title {
            a {
                display: inline-block;
                background-color: #000;
                color: #fff;
                padding: 0 10px;
                height: 25px;
                line-height: 25px;
                margin-right: 20px;

                img {
                    height: 18px;
                }

                &:hover {
                    background-color: @red;
                }
            }
        }

        .menu-detail {
            margin-top: 10px;

            .menu-detail-item {
                .menu-detail-title {
                    width: 100px;
                    text-align: right;

                    a {
                        font-weight: 700;
                        align-items: center;

                        img {
                            height: 18px;
                        }

                        &:hover {
                            cursor: pointer;
                            color: @red;
                        }
                    }
                }

                .menu-detail-data {
                    width: 800px;
                    margin-left: 20px;

                    a {
                        margin-right: 20px;
                        line-height: 20px;

                        &:hover {
                            cursor: pointer;
                            color: @red;
                        }
                    }


                }
            }
        }
    }
}
</style>