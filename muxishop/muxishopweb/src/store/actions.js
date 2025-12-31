import { getCartCount } from "@/network/cart";

const actions = {
    updateCartCount({commit, state}) {
        getCartCount().then(res => {
            let count = 0;
            // console.log("actions", res.data)
            if (res.data > 0) {
                count = res.data
            }
            window.localStorage.setItem("cartCount", count)
            commit("updateCartCount", {count: count})
        })
    },
}

export default actions