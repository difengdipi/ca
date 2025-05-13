<template>
	<div style="margin: 20px">
		<el-button type="primary" @click="searchData">搜索</el-button>
<!--		<el-button type="primary" @click="openForm(null)">新增数据</el-button>-->
		<el-table :data="data" style="width: 100%; margin-top: 20px" stripe border>
			<el-table-column prop="dish.name" label="菜品"></el-table-column>
			<el-table-column prop="user.name" label="用户"></el-table-column>
			<el-table-column prop="created_at" label="收藏时间"></el-table-column>

			<el-table-column label="操作" fixed="right" width="180">
				<template #default="scope">
					<el-button type="warning" @click="openForm(scope.row)">编辑</el-button>
					<el-button type="danger" @click="deleteData(scope.row.id)">删除</el-button>
				</template>
			</el-table-column>
		</el-table>
		<el-pagination
			v-model:current-page="pagination.page"
			v-model:page-size="pagination.page_size"
			layout="total,  prev, pager, next, jumper"
			:total="pagination.count"
			@current-change="handleCurrentChange"
		/>
		<el-dialog v-model="dialogVisible" title="数据表单" width="30%">
			<el-form :model="form" label-width="100px">
				<el-form-item label="菜品">
					<el-select v-model="form.dish_id" placeholder="请选择菜品">
						<el-option v-for="(item, index) in dish_Datas" :key="index" :label="item.name" :value="item.id" />
					</el-select>
				</el-form-item>
				<el-form-item label="用户">
					<el-select v-model="form.user_id" placeholder="请选择用户">
						<el-option v-for="(item, index) in Profile_Datas" :key="index" :label="item.name" :value="item.id" />
					</el-select>
				</el-form-item>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button type="warning" @click="dialogVisible = false">取 消</el-button>
					<el-button type="primary" @click="saveData">确 定</el-button>
				</span>
			</template>
		</el-dialog>
	</div>
</template>
<script setup>
import { onMounted, reactive, ref } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from 'axios';
import Cookies from 'js-cookie';

const pagination = reactive({
	page: 1,
	page_size: 8,
	count: 0,
});
const userInfo = ref({});
const data = ref([]);
const dialogVisible = ref(false);
const API_URL = '/api/dish-favorite/';
const form = ref({});
const searchQuery = ref({});

onMounted(() => {
	userInfo.value = JSON.parse(Cookies.get('user'));
	fetchData();
	get_dish_Datas();
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
		const response = await axios.post('/api/search/dish-favorite/', searchQuery.value, { params });
		data.value = response.data.results;
		pagination.count = response.data.count; // 假设后端返回了分页总数
	} catch (error) {
		ElMessage.error('搜索失败');
	}
};

const dish_Datas = ref([]);
const get_dish_Datas = async () => {
	const res = await axios.get('/api/dish/', { page: 1, page_size: 999 });
	dish_Datas.value = res.data.results;
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
		}
		if (form.value.id) {
			formData.delete('user');
			await axios.put(`${API_URL}${form.value.id}/ `, formData);
			ElMessage.success('数据更新成功');
		} else {
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
		form.value = { ...item };
	} else {
		form.value = {};
	}
	dialogVisible.value = true;
};
</script>
<style scoped>
/* 你可以在这里添加一些样式 */
</style>
