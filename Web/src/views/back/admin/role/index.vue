<template>
	<div style="margin: 20px">
		<el-button type="primary" @click="searchData">搜索</el-button>
		<el-button type="primary" @click="openForm(null)">新增数据</el-button>
		<el-table :data="data" style="width: 100%; margin-top: 20px" stripe border>
			<el-table-column prop="role_name" label="角色名称"></el-table-column>
			<el-table-column prop="description" label="角色描述">
				<template #default="scope">
					<div style="max-height: 100px; overflow-y: auto; word-break: break-all">
						{{ scope.row.description }}
					</div>
				</template></el-table-column
			>
			<el-table-column prop="created_at" label="创建时间"></el-table-column>

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
				<el-form-item label="角色名称">
					<el-input v-model="form.role_name"></el-input>
				</el-form-item>
				<el-form-item label="角色描述">
					<el-input type="textarea" v-model="form.description"></el-input>
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
import { ref, onMounted, reactive } from 'vue';
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
const API_URL = '/api/role/';
const form = ref({});
const searchQuery = ref({});

onMounted(() => {
	userInfo.value = JSON.parse(Cookies.get('user'));
	fetchData();
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
		const response = await axios.post('/api/search/role/', searchQuery.value, { params });
		data.value = response.data.results;
		pagination.count = response.data.count; // 假设后端返回了分页总数
	} catch (error) {
		ElMessage.error('搜索失败');
	}
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
