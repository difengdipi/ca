<template>
	<div style="display: flex; flex-direction: column; align-items: center; justify-content: center">
		<el-card style="margin-bottom: 20px; width: 80%; border-radius: 10px">
			<div style="font-size: 25px; padding: 10px">发表你的评论</div>
			<el-form :model="form" label-width="80px">
				<el-form-item label="评分">
					<div class="rating">
						<!-- 手动编写 5 个星星 -->
						<input type="radio" id="star-1" name="star-radio" value="5" v-model="form.score" />
						<label for="star-1">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
								<path
									pathLength="360"
									d="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z"
								></path>
							</svg>
						</label>

						<input type="radio" id="star-2" name="star-radio" value="4" v-model="form.score" />
						<label for="star-2">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
								<path
									pathLength="360"
									d="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z"
								></path>
							</svg>
						</label>

						<input type="radio" id="star-3" name="star-radio" value="3" v-model="form.score" />
						<label for="star-3">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
								<path
									pathLength="360"
									d="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z"
								></path>
							</svg>
						</label>

						<input type="radio" id="star-4" name="star-radio" value="2" v-model="form.score" />
						<label for="star-4">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
								<path
									pathLength="360"
									d="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z"
								></path>
							</svg>
						</label>

						<input type="radio" id="star-5" name="star-radio" value="1" v-model="form.score" />
						<label for="star-5">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
								<path
									pathLength="360"
									d="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z"
								></path>
							</svg>
						</label>
					</div>
				</el-form-item>
				<el-form-item label="评论内容">
					<el-input type="textarea" v-model="form.content"></el-input>
				</el-form-item>
				<el-form-item label="配图">
					<el-upload class="upload-image" action="" :show-file-list="false" :on-change="handleimageChange">
						<img v-if="form.imagePreview" :src="form.imagePreview" class="image-preview" style="width: 100px; height: 100px" />
						<el-icon v-else>
							<Plus />
						</el-icon>
					</el-upload>
				</el-form-item>
			</el-form>
			<div style="text-align: right">
				<el-button type="primary" @click="saveData">发布</el-button>
			</div>
		</el-card>
		<el-card v-for="(item, index) in data" :key="index" style="margin-top: 20px; width: 80%; cursor: pointer; border-radius: 10px">
			<div style="display: flex; height: 50px">
				<img :src="item.user.avatar" alt="" style="border-radius: 50%; width: 50px; height: 50px" />
				<span style="display: flex; align-items: center; height: 100%; margin-left: 10px; font-size: large">
					{{ item.user.name }}
				</span>
			</div>
			<div style="margin: 10px">
				<div style="margin-top: 10px"><span></span>{{ item.content }}</div>
				<div style="display: flex; margin: 10px">
					<img v-if="item.image" :src="item.image" alt="" style="width: 200px; height: 200px; border-radius: 20px" />
				</div>
				<div style="margin-top: 10px"><span></span>评分：{{ item.score }}</div>
				<div style="color: gray; margin-top: 10px; font-weight: normal">{{ item.created_at }}</div>
			</div>
		</el-card>
	</div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useRouter } from 'vue-router';

const pagination = reactive({
	page: 1,
	page_size: 30,
	count: 0,
});
const userInfo = ref({});
const data = ref([]);
const dialogVisible = ref(false);
const API_URL = '/api/dish-comment/';
const API_COMMENT_URL = '/api/dish-comment-frontend/';
const form = ref({});

onMounted(() => {
	userInfo.value = JSON.parse(Cookies.get('user'));
	fetchData();
});

const fetchData = async () => {
	try {
		const params = {
			page: pagination.page,
			page_size: pagination.page_size,
      dish_id: localStorage.getItem('dish_id')
		};
		const response = await axios.get(API_COMMENT_URL, { params });
		data.value = response.data.results;
		pagination.count = response.data.count;
	} catch (error) {
		ElMessage.error('数据加载失败');
	}
};

const saveData = async () => {
	try {
		const formData = new FormData();
		for (const key in form.value) {
			formData.append(key, form.value[key]);

			if (key === 'image') {
				if (form.value[key] instanceof File) {
					formData.append(key, form.value[key]);
				} else {
					formData.delete(key);
				}
			}
			if (key === 'imagePreview') {
				formData.delete(key);
			}
		}
		if (form.value.id) {
			await axios.put(`${API_URL}${form.value.id}/ `, formData);
			ElMessage.success('数据更新成功');
		} else {
			formData.append('user_id', userInfo.value.id);
			formData.append('dish_id', localStorage.getItem('dish_id'));
			await axios.post(API_URL, formData);
			ElMessage.success('发表评论成功');
		}
		dialogVisible.value = false;
		fetchData();
	} catch (error) {
		ElMessage.error('发表评论失败');
	}
};

const handleimageChange = (file) => {
	const reader = new FileReader();
	reader.onload = (e) => {
		form.value.imagePreview = e.target.result; // 预览
	};
	reader.readAsDataURL(file.raw);
	form.value.image = file.raw;
};
</script>
<style scoped>
.rating {
	display: flex;
	flex-direction: row-reverse;
	gap: 0.3rem;
	--stroke: #666;
	--fill: #ffc73a;
}

.rating input {
	appearance: unset;
}

.rating label {
	cursor: pointer;
}

.rating svg {
	width: 2rem;
	height: 2rem;
	overflow: visible;
	fill: transparent;
	stroke: var(--stroke);
	stroke-linejoin: bevel;
	stroke-dasharray: 12;
	animation: idle 4s linear infinite;
	transition:
		stroke 0.2s,
		fill 0.5s;
}

@keyframes idle {
	from {
		stroke-dashoffset: 24;
	}
}

.rating label:hover svg {
	stroke: var(--fill);
}

.rating input:checked ~ label svg {
	transition: 0s;
	animation:
		idle 4s linear infinite,
		yippee 0.75s backwards;
	fill: var(--fill);
	stroke: var(--fill);
	stroke-opacity: 0;
	stroke-dasharray: 0;
	stroke-linejoin: miter;
	stroke-width: 8px;
}

@keyframes yippee {
	0% {
		transform: scale(1);
		fill: var(--fill);
		fill-opacity: 0;
		stroke-opacity: 1;
		stroke: var(--stroke);
		stroke-dasharray: 10;
		stroke-width: 1px;
		stroke-linejoin: bevel;
	}

	30% {
		transform: scale(0);
		fill: var(--fill);
		fill-opacity: 0;
		stroke-opacity: 1;
		stroke: var(--stroke);
		stroke-dasharray: 10;
		stroke-width: 1px;
		stroke-linejoin: bevel;
	}

	30.1% {
		stroke: var(--fill);
		stroke-dasharray: 0;
		stroke-linejoin: miter;
		stroke-width: 8px;
	}

	60% {
		transform: scale(1.2);
		fill: var(--fill);
	}
}
</style>
