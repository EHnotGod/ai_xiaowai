import { createWebHashHistory, createRouter } from 'vue-router'

const routes = [{
    path:"/",
    component:()=>import("@/LayoutMenu/Layout.vue"),
    children:[
        {
            //聊天界面
            path:"",
            name:"home",
            component:()=>import("@/page/home/home.vue")
        },
        {
            //地图界面
            path:"/map",
            name:"map",
            component:()=>import("@/page/map/index.vue")
        },
        {
            //信息界面
            path:"/message",
            name:"message",
            component:()=>import("@/page/message/message.vue")
        },
        {
            //关于我们
            path:"/we",
            name:"we",
            component:()=>import("@/page/we/we.vue")
        },
    ]
}, { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})
export default router;
