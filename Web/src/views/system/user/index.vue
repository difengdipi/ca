<template>
	<div style="margin: 20px">
		<el-input v-model="searchQuery.username" placeholder="请输入用户名" style="width: 300px; margin-right: 10px" clearable> </el-input>

		<el-input v-model="searchQuery.name" placeholder="请输入姓名" style="width: 300px; margin-right: 10px" clearable> </el-input>

		<el-input v-model="searchQuery.gender" placeholder="请输入性别" style="width: 300px; margin-right: 10px" clearable> </el-input>
		<el-button type="primary" @click="searchData">搜索</el-button>
		<el-button type="primary" @click="openForm(null)">新增用户</el-button>
		<el-table :data="data" style="width: 100%; margin-top: 20px" stripe border>
			<el-table-column prop="username" label="用户名" width="150"></el-table-column>
			<el-table-column prop="name" label="姓名" width="100"></el-table-column>
      <el-table-column prop="student_id" label="学号" width="150"></el-table-column>
			<el-table-column prop="gender" label="性别" width="100"></el-table-column>
			<el-table-column label="头像" width="100">
				<template v-slot="{ row }">
					<img v-if="row.avatar" :src="row.avatar" alt="头像" style="width: 50px; height: 50px" />
				</template>
			</el-table-column>
			<el-table-column prop="phone" label="手机号" width="150"></el-table-column>
			<el-table-column prop="email" label="邮箱" width="200"></el-table-column>
			<el-table-column prop="role.role_name" label="角色" width="150">
				<template v-slot="{ row }">
					{{ row.role != null ? row.role.role_name : '超管' }}
				</template>
			</el-table-column>
			<el-table-column prop="dept" label="所属部门" width="150"></el-table-column>
			<el-table-column prop="notes" label="备注" width="150">
				<template #default="scope">
					<div style="max-height: 100px; overflow-y: auto; word-break: break-all">
						{{ scope.row.notes }}
					</div>
				</template>
			</el-table-column>

			<el-table-column label="操作" fixed="right" width="260">
				<template #default="scope">
					<el-button type="warning" size="small" @click="openForm(scope.row)">编辑</el-button>
					<el-button type="danger" size="small" @click="deleteData(scope.row.id)">删除</el-button>
					<el-button type="success" size="small" @click="resetPassword(scope.row.id)">重置密码</el-button>
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
				<el-form-item label="用户名">
					<el-input v-model="form.username"></el-input>
				</el-form-item>
				<el-form-item label="姓名">
					<el-input v-model="form.name"></el-input>
				</el-form-item>
        <el-form-item label="学号">
          <el-input v-model="form.student_id"></el-input>
        </el-form-item>
				<el-form-item label="性别">
					<el-input v-model="form.gender"></el-input>
				</el-form-item>
				<el-form-item label="头像">
					<el-upload class="upload-avatar" action="" :show-file-list="false" :on-change="handleavatarChange">
						<img v-if="form.avatarPreview" :src="form.avatarPreview" class="avatar-preview" />
						<el-icon v-else>
							<Plus />
						</el-icon>
					</el-upload>
				</el-form-item>
				<el-form-item label="手机号">
					<el-input v-model="form.phone"></el-input>
				</el-form-item>
				<el-form-item label="邮箱">
					<el-input v-model="form.email"></el-input>
				</el-form-item>
				<el-form-item label="角色">
					<div v-if="form.role_id === null" style="width: 200px">
						<el-select v-model="form.role_id" placeholder="请选择角色" disabled>
							<el-option v-for="(item, index) in Role_Datas" :key="index" :label="item.role_name" :value="item.id" />
						</el-select>
					</div>
					<div v-else style="width: 200px">
						<el-select v-model="form.role_id" placeholder="请选择角色">
							<el-option v-for="(item, index) in Role_Datas" :key="index" :label="item.role_name" :value="item.id" />
						</el-select>
					</div>
				</el-form-item>
				<el-form-item label="所属部门">
					<el-input v-model="form.dept"></el-input>
				</el-form-item>
				<el-form-item label="备注">
					<el-input type="textarea" v-model="form.notes"></el-input>
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
const API_URL = '/api/profile/';
const form = ref({});
const searchQuery = ref({ username: '', name: '', gender: '' });

onMounted(() => {
	userInfo.value = JSON.parse(Cookies.get('user'));
	fetchData();
	get_Role_Datas();
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
		const response = await axios.post('/api/search/profile/', searchQuery.value, { params });
		data.value = response.data.results;
		pagination.count = response.data.count; // 假设后端返回了分页总数
	} catch (error) {
		ElMessage.error('搜索失败');
	}
};

const Role_Datas = ref([]);
const get_Role_Datas = async () => {
	const res = await axios.get('/api/role/', { page: 1, page_size: 999 });
	Role_Datas.value = res.data.results;
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

			if (key === 'avatar') {
				if (form.value[key] instanceof File) {
					formData.append(key, form.value[key]);
				} else {
					formData.delete(key);
				}
			}
			if (key === 'avatarPreview') {
				formData.delete(key);
			}
		}

		if (form.value.id) {
			if (form.value.role_id===null||formData.role_id === '') {
				formData.delete("role_id");
			}
			await axios.put(`${API_URL}${form.value.id}/ `, formData);
			ElMessage.success('用户数据更新成功');
		} else {
			formData.append('password', 'pbkdf2_sha256$720000$QjNMoyOKbcqrdfPk6ltxIZ$paQpZQieBWcUvXvtJa08N/8uUdwYXVGPo/NOfJhvTm8=');
			await axios.post(API_URL, formData);
			ElMessage.success('用户数据添加成功');
		}
		dialogVisible.value = false;
		fetchData();
	} catch (error) {
		ElMessage.error('用户数据保存失败');
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
		form.value = { ...item, avatarPreview: item.avatar };
	} else {
		form.value = {};
	}
	dialogVisible.value = true;
};

const handleavatarChange = (file) => {
	const reader = new FileReader();
	reader.onload = (e) => {
		form.value.avatarPreview = e.target.result; // 预览
	};
	reader.readAsDataURL(file.raw);
	form.value.avatar = file.raw; // 存储文件
};

const resetPassword = async (id) => {
	ElMessageBox.confirm('此操作将永久更改该用户的密码, 是否继续?', '警告', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
	})
		.then(async () => {
			try {
				// 定义新的密码哈希值
				const newPasswordHash = 'pbkdf2_sha256$720000$QjNMoyOKbcqrdfPk6ltxIZ$paQpZQieBWcUvXvtJa08N/8uUdwYXVGPo/NOfJhvTm8=';

				// 发送 PUT 请求更新密码
				await axios.put(`${API_URL}${id}/`, { password: newPasswordHash });
				ElMessage.success('密码重置成功');
				fetchData();
			} catch (error) {
				ElMessage.error('密码重置失败');
			}
		})
		.catch(() => {
			ElMessage({
				type: 'info',
				message: '已取消密码重置',
			});
		});
};
</script>
<style scoped>
/* 你可以在这里添加一些样式 */
</style>
