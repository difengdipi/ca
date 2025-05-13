<template>
	<div class="personal layout-pd">
		<el-row>
			<!-- 个人信息 -->
			<el-col :xs="24" :sm="16">
				<el-card shadow="hover" header="个人信息">
					<div class="personal-user">
						<div class="personal-user-left">
							<avatarSelector v-model="selectImgVisible" @uploadImg="uploadImg" ref="avatarSelectorRef"></avatarSelector>
						</div>
						<div class="personal-user-right">
							<el-row>
								<el-col :span="24" class="personal-title mb18"> {{ state.personalForm.username }}，即使生活再糟糕，也阻挡不了我变得更好！ </el-col>
								<el-col :span="24">
									<el-row>
										<el-col :xs="24" :sm="8" class="personal-item mb6">
											<div class="personal-item-label">昵称：</div>
											<div class="personal-item-value">{{ state.personalForm.name }}</div>
										</el-col>
									</el-row>
								</el-col>
								<el-col :span="24">
									<el-row>
										<el-col :xs="24" :sm="8" class="personal-item mb6">
											<div class="personal-item-label">角色：</div>
											<div class="personal-item-value">
												<el-tag v-for="(item, index) in state.personalForm.role_info" :key="index">
													<div v-if="item.name.role_name == null">超级管理员</div>
													<div v-else>
														{{ item.name.role_name }}
													</div>
												</el-tag>
											</div>
										</el-col>
									</el-row>
								</el-col>
							</el-row>
						</div>
					</div>
				</el-card>
			</el-col>

			<!-- 通知 -->
			<!--      <el-col :xs="24" :sm="8" class="pl15 personal-info">-->
			<!--        <el-card shadow="hover">-->
			<!--          <template #header>-->
			<!--            <span>通知</span>-->
			<!--            <span class="personal-info-more" @click="msgMore">更多</span>-->
			<!--          </template>-->
			<!--          <div class="personal-info-box">-->
			<!--            <ul class="personal-info-ul">-->
			<!--              <li v-for="(v, k) in state.newsInfoList" :key="k" class="personal-info-li">-->
			<!--                <div class="personal-info-li-title">[{{ v.creator_name }}，{{ v.create_datetime }}] {{ v.title }}</div>-->
			<!--              </li>-->
			<!--            </ul>-->
			<!--          </div>-->
			<!--        </el-card>-->
			<!--      </el-col>-->

			<!-- 更新信息 -->
			<el-col :span="24">
				<el-card shadow="hover" class="mt15 personal-edit" header="更新信息">
					<div class="personal-edit-title">基本信息</div>
					<el-form :model="state.personalForm" ref="userInfoFormRef" :rules="rules" size="default" label-width="50px" class="mt35 mb35">
						<el-row :gutter="35">
							<el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" class="mb20">
								<el-form-item label="昵称" prop="name">
									<el-input v-model="state.personalForm.name" placeholder="请输入昵称" clearable></el-input>
								</el-form-item>
							</el-col>
							<el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" class="mb20">
								<el-form-item label="邮箱">
									<el-input v-model="state.personalForm.email" placeholder="请输入邮箱" clearable></el-input>
								</el-form-item>
							</el-col>
							<el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" class="mb20">
								<el-form-item label="电话" prop="mobile">
									<el-input v-model="state.personalForm.mobile" placeholder="请输入电话号码" clearable></el-input>
								</el-form-item>
							</el-col>
							<el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" class="mb20">
								<el-form-item label="性别">
									<el-select v-model="state.personalForm.gender" placeholder="请选择性别" clearable class="w100">
										<el-option label="男" value="男"></el-option>
										<el-option label="女" value="女"></el-option>
									</el-select>
								</el-form-item>
							</el-col>
							<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
								<el-form-item>
									<el-button type="primary" @click="submitForm">
										<el-icon>
											<ele-Position />
										</el-icon>
										更新个人信息
									</el-button>
								</el-form-item>
							</el-col>
						</el-row>
					</el-form>
					<div class="personal-edit-title mb15">账号安全</div>
					<div class="personal-edit-safe-box">
						<div class="personal-edit-safe-item">
							<div class="personal-edit-safe-item-left">
								<div class="personal-edit-safe-item-left-label">账号密码</div>
							</div>
							<div class="personal-edit-safe-item-right">
								<el-button text type="primary" @click="passwordFormShow = true">立即修改</el-button>
							</div>
						</div>
					</div>
					<div class="personal-edit-safe-box">
						<div class="personal-edit-safe-item">
							<div class="personal-edit-safe-item-left">
								<div class="personal-edit-safe-item-left-label">手机绑定</div>
								<div class="personal-edit-safe-item-left-value">已绑定手机：{{ state.personalForm.mobile }}</div>
							</div>
						</div>
					</div>
					<div class="personal-edit-safe-box">
						<div class="personal-edit-safe-item">
							<div class="personal-edit-safe-item-left">
								<div class="personal-edit-safe-item-left-label">邮箱绑定</div>
								<div class="personal-edit-safe-item-left-value">已绑定邮箱：{{ state.personalForm.email }}</div>
							</div>
						</div>
					</div>
				</el-card>
			</el-col>
		</el-row>
		<!-- 密码修改 -->
		<el-dialog v-model="passwordFormShow" title="修改密码">
			<el-form
				ref="userPasswordFormRef"
				:model="userPasswordInfo"
				required-asterisk
				label-width="100px"
				label-position="left"
				:rules="passwordRules"
				center
			>
				<el-form-item label="旧密码" required prop="oldPassword">
					<el-input type="password" v-model="userPasswordInfo.oldPassword" placeholder="请输入旧密码" show-password clearable></el-input>
				</el-form-item>
				<el-form-item required prop="newPassword" label="新密码">
					<el-input type="password" v-model="userPasswordInfo.newPassword" placeholder="请输入新密码" show-password clearable></el-input>
				</el-form-item>
				<el-form-item required prop="newPassword2" label="确认密码">
					<el-input type="password" v-model="userPasswordInfo.newPassword2" placeholder="请确认新密码" show-password clearable></el-input>
				</el-form-item>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button type="primary" @click="settingPassword"> <i class="fa fa-check"></i>提交 </el-button>
				</span>
			</template>
		</el-dialog>
	</div>
</template>

<script setup lang="ts" name="personal">
import { reactive, computed, onMounted, ref, defineAsyncComponent } from 'vue';
import { formatAxis } from '/@/utils/formatTime';
import * as api from './api';
import { ElMessage } from 'element-plus';
import { getBaseURL } from '/@/utils/baseUrl';
import { Session } from '/@/utils/storage';
import { useRouter } from 'vue-router';
import { useUserInfo } from '/@/stores/userInfo';
import { successMessage } from '/@/utils/message';
import { dictionary } from '/@/utils/dictionary';
import { Md5 } from 'ts-md5';
import Cookies from 'js-cookie';
const router = useRouter();
import axios from 'axios';

// 头像裁剪组件
const avatarSelector = defineAsyncComponent(() => import('/@/components/avatarSelector/index.vue'));
const avatarSelectorRef = ref(null);
// 当前时间提示语
const currentTime = computed(() => {
	return formatAxis(new Date());
});
const userInfoFormRef = ref({
	name: '',
	email: '',
	mobile: '',
	gender: '',
});
const rules = reactive({
	name: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
	mobile: [{ pattern: /^1[3-9]\d{9}$/, message: '请输入正确手机号' }],
});

let selectImgVisible = ref(false);

const state = reactive({
	newsInfoList: [],
	personalForm: {
		avatar: '',
		username: '',
		name: '',
		email: '',
		mobile: '',
		gender: '',
		dept_info: {
			dept_id: 0,
			dept_name: '',
		},
		role_info: [
			{
				id: 0,
				name: '',
			},
		],
		permission: '',
	},
});

/**
 * 跳转消息中心
 */
const route = useRouter();
const msgMore = () => {
	route.push({ path: '/messageCenter' });
};

const genderList = ref();
/**
 * 获取用户个人信息
 */
const getUserInfo = async function () {
	const user_id = JSON.parse(Cookies.get('user')).id;
	const response = await axios.get('/api/profile/' + user_id + '/');
	console.log(response.data);
	state.personalForm.avatar = response.data.avatar || '';
	state.personalForm.username = response.data.username || '';
	state.personalForm.name = response.data.name || '';
	state.personalForm.email = response.data.email || '';
	state.personalForm.mobile = response.data.phone || '';
	state.personalForm.gender = response.data.gender;
	state.personalForm.dept_info.dept_name = response.data.dept || '';
	state.personalForm.role_info[0].name = response.data.role || [];
	state.personalForm.permission = response.data.permission || '';
};

// const submitForm = async () => {
//   if (!userInfoFormRef.value) return;
//   await userInfoFormRef.value.validate((valid, fields) => {
//     if (valid) {
//       api.updateUserInfo(state.personalForm).then((res: any) => {
//         ElMessage.success('更新成功');
//         getUserInfo();
//       });
//     } else {
//       ElMessage.error('表单验证失败,请检查~');
//     }
//   });
// };
const API_URL = '/api/profile/';
const submitForm = async () => {
	const user_id = JSON.parse(Cookies.get('user')).id;
	userInfoFormRef.value.name = state.personalForm.name;
	userInfoFormRef.value.email = state.personalForm.email;
	userInfoFormRef.value.phone = state.personalForm.mobile;
	userInfoFormRef.value.gender = state.personalForm.gender;
	await axios.put(`${API_URL}${user_id}/`, userInfoFormRef.value);
	ElMessage.success('数据更新成功');
};

/**
 * 获取消息通知
 */
const getMsg = () => {
	api.GetSelfReceive({}).then((res: any) => {
		const { data } = res;
		state.newsInfoList = data || [];
	});
};
onMounted(() => {
	getUserInfo();
	// getMsg();
});

/**************************密码修改部分************************/
const passwordFormShow = ref(false);
const userPasswordFormRef = ref();
const userPasswordInfo = reactive({
	id: '',
	oldPassword: '',
	newPassword: '',
	newPassword2: '',
});

const validatePass = (rule, value, callback) => {
	const pwdRegex = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z]).{8,30}');
	if (value === '') {
		callback(new Error('请输入密码'));
	} else if (value === userPasswordInfo.oldPassword) {
		callback(new Error('原密码与新密码一致'));
	} else if (!pwdRegex.test(value)) {
		callback(new Error('您的密码复杂度太低(密码中必须包含字母、数字)'));
	} else {
		if (userPasswordInfo.newPassword2 !== '') {
			userPasswordFormRef.value.validateField('newPassword2');
		}
		callback();
	}
};
const validatePass2 = (rule, value, callback) => {
	if (value === '') {
		callback(new Error('请再次输入密码'));
	} else if (value !== userPasswordInfo.newPassword) {
		callback(new Error('两次输入密码不一致!'));
	} else {
		callback();
	}
};

const passwordRules = reactive({
	oldPassword: [
		{
			required: true,
			message: '请输入原密码',
			trigger: 'blur',
		},
	],
	newPassword: [{ validator: validatePass, trigger: 'blur' }],
	newPassword2: [{ validator: validatePass2, trigger: 'blur' }],
});

/**
 * 重新设置密码
 */

const settingPassword = async () => {
	// 表单校验
	userPasswordFormRef.value.validate(async (valid) => {
		if (valid) {
			try {
				// 获取用户 ID
				const userCookie = Cookies.get('user');
				if (!userCookie) {
					ElMessage.error('用户信息未找到，请重新登录');
					router.push('/login');
					return;
				}
				const user = JSON.parse(userCookie);
				userPasswordInfo.id = user.id;

				// 发送修改密码请求
				const response = await axios.post(`/api/setting-password/`, userPasswordInfo);

				// 根据响应结果进行处理
				if (response.data.message === '修改成功') {
					ElMessage.success('修改密码成功，请重新登录');

					// 清除所有 Cookies
					document.cookie.split(';').forEach((cookie) => {
						const name = cookie.split('=')[0].trim();
						document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
					});

					// 跳转到登录页
					router.push('/login');
				} else {
					ElMessage.error('旧密码有误！');
				}
			} catch (error) {
				// 捕获错误
				ElMessage.error(`修改密码失败：${error.response?.data?.message || error.message}`);
			}
		} else {
			// 表单校验失败
			ElMessage.error('表单校验失败，请检查');
		}
	});
};

const uploadImg = (data: any) => {
	let formdata = new FormData();
	formdata.append('file', data);
	api.uploadAvatar(formdata).then((res: any) => {
		if (res.code === 2000) {
			selectImgVisible.value = false;
			// state.personalForm.avatar = getBaseURL() + res.data.url;
			state.personalForm.avatar = res.data.url;
			api.updateUserInfo(state.personalForm).then((res: any) => {
				successMessage('更新成功');
				getUserInfo();
				useUserInfo().updateUserInfos();
				// @ts-ignore
				avatarSelectorRef.value.updateAvatar(state.personalForm.avatar);
			});
		}
	});
};
</script>

<style scoped lang="scss">
@import '/@/theme/mixins/index.scss';
.personal {
	.personal-user {
		height: 130px;
		display: flex;
		align-items: center;
		.personal-user-left {
			width: 100px;
			height: 130px;
			border-radius: 3px;
			:deep(.el-upload) {
				height: 100%;
			}
			.personal-user-left-upload {
				img {
					width: 100%;
					height: 100%;
					border-radius: 3px;
				}
				&:hover {
					img {
						animation: logoAnimation 0.3s ease-in-out;
					}
				}
			}
		}
		.personal-user-right {
			flex: 1;
			padding: 0 15px;
			.personal-title {
				font-size: 18px;
				@include text-ellipsis(1);
			}
			.personal-item {
				display: flex;
				align-items: center;
				font-size: 13px;
				.personal-item-label {
					color: var(--el-text-color-secondary);
					@include text-ellipsis(1);
				}
				.personal-item-value {
					@include text-ellipsis(1);
				}
			}
		}
	}
	.personal-info {
		.personal-info-more {
			float: right;
			color: var(--el-text-color-secondary);
			font-size: 13px;
			&:hover {
				color: var(--el-color-primary);
				cursor: pointer;
			}
		}
		.personal-info-box {
			height: 130px;
			overflow: hidden;
			.personal-info-ul {
				list-style: none;
				.personal-info-li {
					font-size: 13px;
					padding-bottom: 10px;
					.personal-info-li-title {
						display: inline-block;
						@include text-ellipsis(1);
						color: var(--el-text-color-secondary);
						text-decoration: none;
					}
					& a:hover {
						color: var(--el-color-primary);
						cursor: pointer;
					}
				}
			}
		}
	}
	.personal-recommend-row {
		.personal-recommend-col {
			.personal-recommend {
				position: relative;
				height: 100px;
				border-radius: 3px;
				overflow: hidden;
				cursor: pointer;
				&:hover {
					i {
						right: 0px !important;
						bottom: 0px !important;
						transition: all ease 0.3s;
					}
				}
				i {
					position: absolute;
					right: -10px;
					bottom: -10px;
					font-size: 70px;
					transform: rotate(-30deg);
					transition: all ease 0.3s;
				}
				.personal-recommend-auto {
					padding: 15px;
					position: absolute;
					left: 0;
					top: 5%;
					color: var(--next-color-white);
					.personal-recommend-msg {
						font-size: 12px;
						margin-top: 10px;
					}
				}
			}
		}
	}
	.personal-edit {
		.personal-edit-title {
			position: relative;
			padding-left: 10px;
			color: var(--el-text-color-regular);
			&::after {
				content: '';
				width: 2px;
				height: 10px;
				position: absolute;
				left: 0;
				top: 50%;
				transform: translateY(-50%);
				background: var(--el-color-primary);
			}
		}
		.personal-edit-safe-box {
			border-bottom: 1px solid var(--el-border-color-light, #ebeef5);
			padding: 15px 0;
			.personal-edit-safe-item {
				width: 100%;
				display: flex;
				align-items: center;
				justify-content: space-between;
				.personal-edit-safe-item-left {
					flex: 1;
					overflow: hidden;
					.personal-edit-safe-item-left-label {
						color: var(--el-text-color-regular);
						margin-bottom: 5px;
					}
					.personal-edit-safe-item-left-value {
						color: var(--el-text-color-secondary);
						@include text-ellipsis(1);
						margin-right: 15px;
					}
				}
			}
			&:last-of-type {
				padding-bottom: 0;
				border-bottom: none;
			}
		}
	}
}
</style>
