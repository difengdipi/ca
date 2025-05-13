<template>
	<div class="heart-container" :title="title">
		<input type="checkbox" class="checkbox" v-model="isLiked" @click="Like" />
		<div class="svg-container">
			<svg viewBox="0 0 24 24" class="svg-outline" xmlns="http://www.w3.org/2000/svg">
				<path
					d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Zm-3.585,18.4a2.973,2.973,0,0,1-3.83,0C4.947,16.006,2,11.87,2,8.967a4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,11,8.967a1,1,0,0,0,2,0,4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,22,8.967C22,11.87,19.053,16.006,13.915,20.313Z"
				></path>
			</svg>
			<svg viewBox="0 0 24 24" class="svg-filled" xmlns="http://www.w3.org/2000/svg">
				<path
					d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Z"
				></path>
			</svg>
			<svg class="svg-celebrate" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
				<polygon points="10,10 20,20"></polygon>
				<polygon points="10,50 20,50"></polygon>
				<polygon points="20,80 30,70"></polygon>
				<polygon points="90,10 80,20"></polygon>
				<polygon points="90,50 80,50"></polygon>
				<polygon points="80,80 70,70"></polygon>
			</svg>
		</div>
		<span class="like-text">{{ isLiked ? '取消点赞' : '点赞' }}</span>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const API_URL = '/api/dish-like/';

const isLiked = ref(false);
const userInfo = ref({});
const data = ref([]);

const fetchData = async () => {
	try {
		const response = await axios.get(API_URL + `?user_id=${userInfo.value.id}&dish_id=${localStorage.getItem('dish_id')}`);
		data.value = response.data.results;
		isLiked.value = data.value.length !== 0;
		console.log(isLiked.value);
	} catch (error) {
		ElMessage.error('失败', error);
	}
};

const Like = async () => {
	if (isLiked.value) {
		try {
			const response = await axios.delete(API_URL + `${data.value[0].id}/`);
			data.value = response.data.results;
			await fetchData();
		} catch (error) {
			ElMessage.error('失败', error);
		}
	} else {
		try {
			const response = await axios.post(API_URL, {
				user_id: userInfo.value.id,
				dish_id: localStorage.getItem('dish_id'),
			});
			data.value = response.data.results;
			await fetchData();
		} catch (error) {
			ElMessage.error('失败', error);
		}
	}
};

onMounted(() => {
	userInfo.value = JSON.parse(Cookies.get('user'));
	fetchData();
});
</script>

<style scoped>
.heart-container {
	--heart-color: rgb(255, 91, 137);
	position: relative;
	display: flex;
	width: 180px;
	height: 50px;
	transition: 0.3s;
}

.heart-container .checkbox {
	position: absolute;
	width: 100%;
	height: 100%;
	opacity: 0;
	z-index: 20;
	cursor: pointer;
}

.heart-container .svg-container {
	width: 80px;
	height: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
}

.heart-container .svg-outline,
.heart-container .svg-filled {
	fill: var(--heart-color);
	position: absolute;
}

.heart-container .svg-filled {
	animation: keyframes-svg-filled 1s;
	display: none;
}

.heart-container .svg-celebrate {
	position: absolute;
	animation: keyframes-svg-celebrate 0.5s;
	animation-fill-mode: forwards;
	display: none;
	stroke: var(--heart-color);
	fill: var(--heart-color);
	stroke-width: 2px;
}

.heart-container .checkbox:checked ~ .svg-container .svg-filled {
	display: block;
}

.heart-container .checkbox:checked ~ .svg-container .svg-celebrate {
	display: block;
}

@keyframes keyframes-svg-filled {
	0% {
		transform: scale(0);
	}

	25% {
		transform: scale(1.2);
	}

	50% {
		transform: scale(1);
		filter: brightness(1.5);
	}
}

@keyframes keyframes-svg-celebrate {
	0% {
		transform: scale(0);
	}

	50% {
		opacity: 1;
		filter: brightness(1.5);
	}

	100% {
		transform: scale(1.4);
		opacity: 0;
		display: none;
	}
}
.like-text {
	width: 200px;
	margin-left: 0.5em;
	padding: 0.5em;
	color: #000000;
	font-size: 15px;
	font-family: Arial, sans-serif;
	font-weight: bold;
}
</style>
