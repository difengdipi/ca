<!--这段代码是一个使用 Vue 3 和 Element Plus UI 库构建的单文件组件（SFC），
用于创建一个具有导航、轮播图展示和动态内容区域的网页布局。以下是对其主要部分的解释：-->
<template>
	<div class="app-container">
		<header class="app-header">
			<div class="logo">
				<div class="logo-link" style="font-weight: bold">{{ themeConfig.globalTitle }}</div>
			</div>
			<nav class="navigation">
				<ul class="nav-list">
					<li v-for="item in navItems" :key="item.name" class="nav-item">
						<router-link :to="item.path" :class="{ active: isActive(item) }" class="nav-link">{{ item.meta.title }}</router-link>
					</li>
				</ul>
			</nav>
			<div class="admin-link">
				<router-link to="/home" class="admin-link-text">后台管理</router-link>
			</div>
		</header>
		<main class="content-area">
			<div class="carousel-container">
				<el-carousel height="600px" motion-blur>
					<el-carousel-item v-for="item in swiperData" :key="item">
						<div class="image-container">
							<img :src="item.image" alt="图片" class="full-image" />
						</div>
					</el-carousel-item>
				</el-carousel>
			</div>

			<!-- 路由出口 -->
			<router-view style="margin: 20px" />
		</main>

		<!-- 页脚部分 -->
		<footer class="footer bg-light text-center py-3" style="height: 100px; display: flex; align-items: flex-start; justify-content: center">
			<div class="container">
				<p class="mb-0">
					<a>食品监管局举报电话:</a>
					<a target="_blank" href="https://www.samr.gov.cn/">12345</a>
				</p>
			</div>
		</footer>
	</div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '/@/stores/themeConfig';
import { ElMessage } from 'element-plus';
import axios from 'axios';

const storesThemeConfig = useThemeConfig();
const { themeConfig } = storeToRefs(storesThemeConfig);

// 定义导航项
const navItems = [
	{ path: '/main-algorithm', name: 'list', meta: { title: '菜品推荐' } },
	// { path: '/main-detail', name: 'detail', meta: {title: '详细' } },

	{ path: '/main_dish_list', name: 'list', meta: { title: '菜品列表' } },
	{ path: '/main-feedback', name: 'feedback', meta: { title: '系统反馈' } },
	// { path: '/chart', name: 'chart', meta: { title: '图表' } },
];

// 获取当前路由对象
const route = useRoute();

// 计算属性来判断是否为激活状态
const isActive = computed(() => (item) => {
	return route.path.startsWith(item.path);
});

const swiperData = ref([]);
const fetchData = async () => {
	try {
		const response = await axios.get('/api/swiper/');
		swiperData.value = response.data.results;
	} catch (error) {
		ElMessage.error('数据加载失败');
	}
};

onMounted(() => {
	fetchData();
});
</script>

<style scoped>
.app-container {
	display: flex;
	flex-direction: column;
	min-height: 90vh; /* 确保整个视口高度 */
}

.app-header {
	height: 70px;
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 0 20px;
	background-color: rgba(233, 254, 255, 0.65);
	color: black;
	font-size: x-large;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

.logo-link,
.nav-link {
	text-decoration: none;
}

.nav-list {
	list-style-type: none;
	padding: 0;
	margin: 0;
	display: flex;
	font-size: large;
	font-weight: normal;
}

.nav-item {
	margin-right: 15px;
}

.nav-link.active {
	font-weight: bold;
}

.admin-link {
	display: flex;
	align-items: center;
}

.admin-link-text {
	color: orange;
	font-size: large;
	font-weight: bold;
	text-decoration: none;
}

.content-area {
	flex-grow: 1;
	background-color: #f9f9f9;
	height: 85vh;
	overflow-y: scroll;
}

.carousel-container {
	width: 100%;
}

.image-container {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100%;
	width: 100%;
	overflow: hidden; /* 防止图片超出容器 */
}

.full-image {
	width: 100%;
	height: 100%;
	object-fit: cover; /* 让图片完全覆盖容器，可能会裁剪图片 */
}

/* 页脚样式 */
.footer {
	background-color: #f8f9fa;
	color: #6c757d;
	padding: 2rem 0;
	margin-top: auto; /* 确保页脚在页面底部 */
}
</style>
