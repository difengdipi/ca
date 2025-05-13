

<!--发布系统反馈：包含了一个表单，允许用户输入反馈的主题和信息，并可以上传图片和视频。
     反馈列表：展示所有已发布的反馈，包括发布者的头像、名字、反馈主题、内容、配图或视频以及发布时间。
-->
<template>
	<div style="display: flex; flex-direction: column; align-items: center; justify-content: center">
		<el-card style="margin-bottom: 20px; width: 80%; border-radius: 10px">
			<div style="font-size: 25px; padding: 10px">发布系统反馈</div>
			<el-form :model="form" label-width="80px">
				<el-form-item label="反馈主题">
					<el-input v-model="form.subject"></el-input>
				</el-form-item>
				<el-form-item label="反馈信息">
					<el-input type="textarea" v-model="form.message"></el-input>
				</el-form-item>
				<el-form-item label="配图">
					<el-upload class="upload-image" action="" :show-file-list="false" :on-change="handleimageChange">
						<img v-if="form.imagePreview" :src="form.imagePreview" class="image-preview" style="width: 100px; height: 100px" />
						<el-icon v-else><Plus /></el-icon>
					</el-upload>
				</el-form-item>
				<el-form-item label="视频">
					<el-upload class="upload-video" action="" :show-file-list="false" :on-change="handlevideoChange">
						<div v-if="form.videoPreview">已选择文件: {{ form.videoPreview }}<el-button size="small" type="warning">修改文件</el-button></div>
						<div v-else-if="form.video">
							{{ form.video.split('/').pop() }}
							<el-button size="small" type="warning">修改文件</el-button>
						</div>
						<el-button v-else size="small" type="primary">上传文件</el-button>
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
				<div style="font-size: medium; font-weight: bold">{{ item.subject }}</div>
				<div style="margin-top: 10px"><span></span>{{ item.message }}</div>
				<div style="display: flex; margin: 10px">
					<img v-if="item.image" :src="item.image" alt="" style="width: 200px; height: 200px; border-radius: 20px" />
					<video v-if="item.video" :src="item.video" alt="" style="width: 200px; height: 200px; border-radius: 20px"></video>
				</div>
				<div style="color: gray; margin-top: 10px; font-weight: normal">{{ item.created_at }}</div>
			</div>
		</el-card>
	</div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useRouter } from 'vue-router';
const router = useRouter();

const pagination = reactive({
	page: 1,
	page_size: 30,
	count: 0,
});
const userInfo = ref({});
const data = ref([]);
const dialogVisible = ref(false);
const API_URL = '/api/feedback/';
const form = ref({});
const searchQuery = ref({});

onMounted(() => {
	userInfo.value = JSON.parse(Cookies.get('user'));
	fetchData();
	get_Profile_Datas();
});

const decodeFileName = (filePath) => {
	return decodeURIComponent(filePath.split('/').pop()); // 解码文件名并返回
};

const downloadFile = (filePath) => {
	const url = `${filePath}`;
	window.open(url, '_blank');
};

const handleCurrentChange = async (val) => {
	pagination.page = val;
	const hasSearchCondition = Object.values(searchQuery.value).some((item) => item.trim() !== '');

	if (hasSearchCondition) {
		await searchData();
	} else {
		await fetchData();
	}
};
const searchData = async () => {
	try {
		const params = {
			page: pagination.page,
			page_size: pagination.page_size,
		};
		const response = await axios.post('/api/search/feedback/', searchQuery.value, { params });
		data.value = response.data.results;
		pagination.count = response.data.count; // 假设后端返回了分页总数
	} catch (error) {
		ElMessage.error('搜索失败');
	}
};

const Profile_Datas = ref([]);
const get_Profile_Datas = async () => {
	const res = await axios.get('/api/profile/', { page: 1, page_size: 999 });
	Profile_Datas.value = res.data.results;
};

const fetchData = async () => {
	try {
		const params = {
			page: pagination.page,
			page_size: pagination.page_size,
		};
		const response = await axios.get(API_URL, { params });
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

			if (key === 'video') {
				if (form.value[key] instanceof File) {
					formData.append(key, form.value[key]);
				} else {
					formData.delete(key);
				}
			}
			if (key === 'videoPreview') {
				formData.delete(key);
			}
		}
		if (form.value.id) {
			await axios.put(`${API_URL}${form.value.id}/ `, formData);
			ElMessage.success('数据更新成功');
		} else {
			formData.append('user_id', userInfo.value.id);
			await axios.post(API_URL, formData);
			ElMessage.success('数据添加成功');
		}
		dialogVisible.value = false;
		fetchData();
	} catch (error) {
		ElMessage.error('数据保存失败');
	}
};

const deleteData = async (id) => {
	ElMessageBox.confirm('此操作将永久删除该记录, 是否继续?', '警告', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
	})
		.then(async () => {
			try {
				await axios.delete(`${API_URL}${id} / `);
				ElMessage.success('数据删除成功');
				fetchData();
			} catch (error) {
				ElMessage.error('数据删除失败');
			}
		})
		.catch(() => {
			ElMessage({
				type: 'info',
				message: '已取消删除',
			});
		});
};

const openForm = (item) => {
	if (item) {
		form.value = { ...item, imagePreview: item.image };
	} else {
		form.value = {};
	}
	dialogVisible.value = true;
};

const handleimageChange = (file) => {
	const reader = new FileReader();
	reader.onload = (e) => {
		form.value.imagePreview = e.target.result; // 预览
	};
	reader.readAsDataURL(file.raw);
	form.value.image = file.raw; // 存储文件
};

const handlevideoChange = (file) => {
	form.value.video = file.raw; // 存储文件
	form.value.videoPreview = file.raw.name;
};
</script>
<style scoped>
/* 你可以在这里添加一些样式 */
</style>
