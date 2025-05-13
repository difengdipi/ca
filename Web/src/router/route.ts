
import { RouteRecordRaw } from 'vue-router';
export const dynamicRoutes: Array<RouteRecordRaw> = [
{
    path: '/',
    name: '/',
    component: () => import('/@/layout/index.vue'),
    meta: {
    isKeepAlive: true,
    },
    children: [],
},
{
    path: '/personal',
    name: 'personal',
    component: () => import('/@/views/system/personal/index.vue'),
    meta: {
    title: 'message.router.personal',
        isLink: '',
        isHide: false,
        isKeepAlive: true,
        isAffix: false,
        isIframe: false,
        icon: 'iconfont icon-gerenzhongxin',
    },
}
];

export const notFoundAndNoPower = [
];

export const staticRoutes: Array<RouteRecordRaw> = [
{
    path: '/',
    redirect: '/login',
},
{
    path: '/login',
    name: 'login',
    component: () => import('/@/views/front/login/login.vue'),
    meta: {
    title: '登录',
    }
},
{
    path: '/main',
    name: 'main',
    component: () => import('/@/views/front/main/main.vue'),
    meta: {
    title: '主页',
    },
    children: [

         {
            path: '/main-feedback',
            name: 'main-feedback',
            component: () => import('/@/views/front/main/feedback/index.vue'),
            meta: {
            title: '系统反馈',
            }
        },

        {
            path:'/main',
            redirect:"/main_dish_list",
        },
        {
            path: '/main_dish_list',
            name: 'main_dish_list',
            component: () => import('/@/views/front/main/main_dish/list.vue'),
            meta: {
            title: '菜品列表',
                isReception:true,
            }
        },
        {
            path: '/main_dish_detail',
            name: 'main_dish_detail',
            component: () => import('/@/views/front/main/main_dish/detail.vue'),
            meta: {
            title: '菜品详情',
                isReception:true,
            }
        },
        {
            path: '/main-algorithm',
            name: 'main-algorithm',
            component: () => import('/@/views/front/main/main_algorithm/index.vue'),
            meta: {
                title: '推荐界面',
                isReception:true,
            }
        },
    ],
},
{
    path: '/register',
    name: 'register',
    component: () => import('/@/views/front/register/register.vue'),
    meta: {
    title: '注册',
    }
},
{
    path: '/chart',
    name: 'chart',
    component: () => import('/@/views/chart/index.vue'),
    meta: {
    title: '图表',
        isReception:true,
    }
},
];
