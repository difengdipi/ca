<template>
	<el-container class="layout-container flex-center">
		<LayoutHeader />
		<el-container class="layout-mian-height-50">
			<!-- <LayoutAside /> -->
			<div class="flex-center layout-backtop">
				<!-- <LayoutTagsView v-if="isTagsview" /> -->
				<div class="nav-con">
					<div class="nav-list">
						<div
							class="nav-item"
							:class="{ curItem: route.path === item.path }"
							v-for="(item, index) in navDatas"
							:key="index"
							@click="navChange(item.path)"
						>
							{{ item.name }}
						</div>
					</div>
				</div>
				<LayoutMain ref="layoutMainRef" />
			</div>
		</el-container>
	</el-container>
</template>

<script setup lang="ts" name="layoutClassic">
import { defineAsyncComponent, computed, ref, watch, nextTick, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '/@/stores/themeConfig';

// 引入组件
const LayoutAside = defineAsyncComponent(() => import('/@/layout/component/aside.vue'));
const LayoutHeader = defineAsyncComponent(() => import('/@/layout/component/header.vue'));
const LayoutMain = defineAsyncComponent(() => import('/@/layout/component/main.vue'));
const LayoutTagsView = defineAsyncComponent(() => import('/@/layout/navBars/tagsView/tagsView.vue'));
// 自定义nav内容
const navDatas = ref([{ name: '首页', path: '/productList' }]);

// 定义变量内容
const layoutMainRef = ref<InstanceType<typeof LayoutMain>>();
const route = useRoute();
const router = useRouter();
const storesThemeConfig = useThemeConfig();
const { themeConfig } = storeToRefs(storesThemeConfig);
//nav跳转
const navChange = (path: string) => {
	router.push({ path: path });
};

// 判断是否显示 tasgview
const isTagsview = computed(() => {
	return themeConfig.value.isTagsview;
});
// 重置滚动条高度，更新子级 scrollbar
const updateScrollbar = () => {
	layoutMainRef.value?.layoutMainScrollbarRef.update();
};
// 重置滚动条高度，由于组件是异步引入的
const initScrollBarHeight = () => {
	nextTick(() => {
		setTimeout(() => {
			updateScrollbar();
			// '!' not null 断言操作符，不执行运行时检查
			layoutMainRef.value!.layoutMainScrollbarRef.wrapRef.scrollTop = 0;
		}, 500);
	});
};
// 页面加载时
onMounted(() => {
	initScrollBarHeight();
});
// 监听路由的变化，切换界面时，滚动条置顶
watch(
	() => route.path,
	() => {
		initScrollBarHeight();
	}
);
// 监听 themeConfig 配置文件的变化，更新菜单 el-scrollbar 的高度
watch(
	themeConfig,
	() => {
		updateScrollbar();
	},
	{
		deep: true,
	}
);
</script>
<style scoped lang="scss">
.nav-con {
	height: 40px;
	background: #fff;
	line-height: 40px;
	.nav-list {
		max-width: 1600px;
		margin: 0 auto;
		display: flex;
		align-items: center;
		.nav-item {
			padding: 0 20px;
			cursor: pointer;
			&:hover {
				background: var(--el-color-primary);
				color: #fff;
			}
		}
		.curItem {
			background: var(--el-color-primary);
			color: #fff;
		}
	}
}
</style>
