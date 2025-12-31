<template>
    <div class="main">
        <div class="content">
            <input type="text" placeholder="搜索..." ref="searchWord" @keydown.enter="search($event.target.value)"></input>
            <span class="iconfont icon-fangdajing" @click="search(this.$refs.searchWord.value)"></span>
            <div class="hotword">
                <a href="javascript:void(0)" v-for="(item, key) in hotWords" :key="key" :class="item.active ? 'active' : ''"
                    @click="search(item.word)">{{ item.word }}</a>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router";

const router = useRouter()
let hotWords = ref([
    { "word": "电脑", "active": true },
    { "word": "手机", "active": false },
    { "word": "裙子", "active": false },
    { "word": "空调", "active": false },
    { "word": "裤子", "active": false },
])

function search(keyword) {
    for (let i in hotWords.value) {
        if (hotWords.value[i]["word"] == keyword) {
            hotWords.value[i]["active"] = true
        } else {
            hotWords.value[i]["active"] = false
        }
    }
    router.push("/goods_list/" + keyword + "/1/1/")
}
</script>

<style scoped lang="less">
@red: #e2231a;

.main {
    margin-top: 45px;

    .content {
        .hotword {
            margin-top: 10px;

            a {
                margin-right: 10px;
                font-size: 15px;

                &:hover {
                    color: @red;
                }
            }

            .active {
                color: @red;
            }

        }

        width: 550px;
        height: 35px;
        border: 2px solid @red;
        margin-left: 80px;

        input {
            width: 490px;
            height: 100%;
            line-height: 35px;
            padding-left: 10px;
            font-size: 15px;
        }

        span {
            display: inline-block;
            background-color: @red;
            width: 50px;
            height: 35px;
            line-height: 35px;
            text-align: center;
            color: #fff;
            font-weight: 700;

            &:hover {
                cursor: pointer;
                background-color: #c81623;
            }
        }

    }


}
</style>