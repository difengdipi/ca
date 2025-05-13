<template>
	<div style="height: 80vh; margin: 20px">
		<div v-if="loading" style="text-align: center; margin-top: 20px">
			<el-spinner />
		</div>
		<div v-else>
			<el-card shadow="hover" style="border-radius: 8px">
				<div style="display: flex; gap: 20px">
					<div style="flex: 1; max-width: 50%">
						<img :src="detail.image" controls style="width: 100%; max-height: 400px; border-radius: 6px" />
					</div>
					<div style="flex: 1">
						<h1 style="font-size: 24px; margin-bottom: 20px">{{ detail.name }}</h1>

						<div style="font-size: 16px; line-height: 1.6; color: #333">
							<p>窗口：{{ detail.window.name }}</p>
						</div>

						<div style="font-size: 16px; line-height: 1.6; color: #333">
							<p>名称：{{ detail.name }}</p>
						</div>
            <div style="font-size: 16px; line-height: 1.6; color: #333">
              <p>评分：{{ detail.score }}</p>
            </div>

						<div style="font-size: 16px; line-height: 1.6; color: #333">
							<p>地址：{{ detail.description }}</p>
						</div>

						<div style="font-size: 16px; line-height: 1.6; color: #333">
							<p>价格：{{ detail.price }}</p>
						</div>

<!--						<div style="font-size: 16px; line-height: 1.6; color: #333">-->
<!--							<p>图片：{{ detail.image }}</p>-->
<!--						</div>-->

						<div style="font-size: 16px; line-height: 1.6; color: #333">
							<p>库存数量：{{ detail.stock_quantity }}</p>
						</div>

						<div style="font-size: 16px; line-height: 1.6; color: #333">
							<p>上架时间：{{ detail.time }}</p>
						</div>
						<div style="display: flex; margin-top: 20px">
							<LikeButton></LikeButton>
							<FavoriteButton></FavoriteButton>
							<PurchaseButton :dish-detail="detail" />
						</div>
					</div>
				</div>
			</el-card>

			<el-card shadow="hover" style="border-radius: 8px; margin-top: 10px">
				<el-tabs v-model="activeTab">
					<el-tab-pane label="评论" name="comments">
						<Comment></Comment>
					</el-tab-pane>
				</el-tabs>
			</el-card>
		</div>
	</div>
</template>

<script setup>
import LikeButton from '/@/views/front/main/main_dish/LikeButton.vue';
import FavoriteButton from '/@/views/front/main/main_dish/FavoriteButton.vue';
import Comment from '/@/views/front/main/main_dish/Comment.vue';
import PurchaseButton from '/@/views/front/main/main_dish/PurchaseButton.vue';

import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const router = useRouter();
const detail = ref({});
const loading = ref(true);

const activeTab = ref('comments');

const fetchDetail = async () => {
	const dish_id = localStorage.getItem('dish_id');
	if (!dish_id) {
		ElMessage.error('未找到详情');
		router.push('/main_dish_list');
		return;
	}

	try {
		const response = await axios.get(`/api/dish/${dish_id}/`);
		detail.value = response.data;
	} catch (error) {
		ElMessage.error('数据加载失败');
	} finally {
		loading.value = false;
	}
};

onMounted(() => {
	fetchDetail();
});
</script>

<style scoped>
/* 你可以在这里添加一些样式 */
</style>
