// src/utils/register.js

import { ElMessage } from 'element-plus';
import { reactive } from 'vue';
import api from '/@/api';
import { useRouter } from 'vue-router';

export default {
	setup() {
		const router = useRouter();
		const registerform = reactive({
			username: '',
			password: '',
			password2: '',
		});

		function verify() {
			if (registerform.username === '') {
				ElMessage({
					message: '用户名不能为空',
					type: 'warning',
				});
				return Promise.resolve(false);
			}

			if (registerform.password === '') {
				ElMessage({
					message: '密码不能为空',
					type: 'warning',
				});
				return Promise.resolve(false);
			}

			if (registerform.password !== registerform.password2) {
				ElMessage({
					message: '两次密码不一致',
					type: 'warning',
				});
				return Promise.resolve(false);
			}

			const formData = new FormData();
			formData.append('yonghuming', registerform.username);
			formData.append('mima', registerform.password);

			return api
				.post('/find/yonghu/', formData)
				.then((res) => {
					if (res.data.code === '0') {
						return true;
					} else {
						ElMessage({
							message: res.data.msg,
							type: 'warning',
						});
						return false;
					}
				})
				.catch((error) => {
					ElMessage({
						message: error.message || error,
						type: 'warning',
					});
					return false;
				});
		}

		const register = async () => {
			const isVerified = await verify();
			if (isVerified) {
				const formData = new FormData();
				formData.append('yonghuming', registerform.username);
				formData.append('mima', registerform.password);

				api
					.post('/yonghu/', formData)
					.then((res) => {
						if (res.data != '') {
							ElMessage({
								message: '注册成功',
								type: 'success',
							});
						} else {
							ElMessage({
								message: '注册失败',
								type: 'warning',
							});
						}
					})
					.catch((error) => {
						ElMessage({
							message: error.message || error,
							type: 'warning',
						});
					});
			}
		};

		function tologin(page) {
			router.push({ name: 'login' });
		}

		return {
			registerform,
			register,
			tologin,
		};
	},
};
