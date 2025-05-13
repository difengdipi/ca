<!--这段代码定义了一个 Vue 3 组件，
它使用了 Element Plus UI 库来创建一个数据表格界面，
允许用户进行搜索、分页、新增、编辑和删除操作-->
<template>
	<div style="margin: 20px">
		<el-input v-model="searchQuery.address" placeholder="请输入地址" style="width: 300px; margin-right: 10px" clearable> </el-input>

		<el-button type="primary" @click="searchData">搜索</el-button>
		<el-button type="primary" @click="openForm(null)">新增数据</el-button>
		<el-table :data="data" style="width: 100%; margin-top: 20px" stripe border>
			<el-table-column prop="user.name" label="用户"></el-table-column>
			<el-table-column prop="address" label="地址">
				<template #default="scope">
					<div style="max-height: 100px; overflow-y: auto; word-break: break-all">
						{{ scope.row.address }}
					</div>
				</template></el-table-column
			>
			<el-table-column prop="phone" label="联系电话"></el-table-column>
			<el-table-column prop="is_default" label="默认地址"></el-table-column>
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
				<el-form-item label="用户">
					<el-select v-model="form.user_id" placeholder="请选择用户">
						<el-option v-for="(item, index) in Profile_Datas" :key="index" :label="item.name" :value="item.id" />
					</el-select>
				</el-form-item>
				<el-form-item label="地址">
					<el-input type="textarea" v-model="form.address"></el-input>
				</el-form-item>
				<el-form-item label="联系电话">
					<el-input v-model="form.phone"></el-input>
				</el-form-item>
				<el-form-item label="默认地址">
					<el-select v-model="form.is_default" placeholder="请选择默认地址" clearable>
						<el-option label="是" value="是"></el-option>
						<el-option label="否" value="否"></el-option>
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
const API_URL = '/api/address/';
const form = ref({});
const searchQuery = ref({ address: '' });

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
		const response = await axios.post('/api/search/address/', searchQuery.value, { params });
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
