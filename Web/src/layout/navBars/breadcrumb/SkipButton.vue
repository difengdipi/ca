<template>
	<!--  <div v-if="userInfos.role === '顾客'||userInfos.role === '用户'" class="" style="margin-right: 30px" @click="tiaozhan">-->
	<div class="" style="margin-right: 30px" @click="tiaozhan">
		<el-button type="text">{{ buttonText }}</el-button>
	</div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
const router = useRouter();
const route = useRoute();
// 定义 props
const props = defineProps({
	userInfos: {
		type: Object,
		required: true,
	},
	route: {
		type: Object,
		required: true,
	},
});

const buttonText = computed(() => {
	return props.route.meta.isReception ? '后台管理' : '主页';
});

const tiaozhan = () => {
	if (route.meta.isReception) {
		router.push('/home');
	} else {
		router.push('/main');
	}
};
</script>
<style scoped>
/* 你可以在这里添加组件的样式 */
</style>
