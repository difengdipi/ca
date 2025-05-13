import { ElMessage } from 'element-plus';
import { ref, reactive, onMounted } from 'vue';
import api from '/@/api';
import { useRouter, useRoute } from 'vue-router';

export default {
	setup() {
		const router = useRouter();
		const loginform = reactive({
			username: '',
			password: '',
		});
		const rememberMe = ref(false);

		onMounted(() => {
			const savedRememberMe = localStorage.getItem('rememberMe');
			if (savedRememberMe) {
				rememberMe.value = JSON.parse(savedRememberMe);
				loginform.username = localStorage.getItem('username');
				loginform.password = localStorage.getItem('password');
			}
		});

		function verify() {
			if (loginform.username === '') {
				ElMessage({
					message: '用户名不能为空',
					type: 'warning',
				});
				return Promise.resolve(false);
			}

			if (loginform.password === '') {
				ElMessage({
					message: '密码不能为空',
					type: 'warning',
				});
				return Promise.resolve(false);
			}

			const formData = new FormData();
			formData.append('yonghuming', loginform.username);
			formData.append('mima', loginform.password);

			return api
				.post('/find/yonghu/', formData)
				.then((res) => {
					if (res.data.code === '1') {
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

		const login = async () => {
			const isVerified = await verify();
			if (isVerified) {
				const formData = new FormData();
				formData.append('yonghuming', loginform.username);
				formData.append('mima', loginform.password);

				api
					.post('/login/yonghu/', formData)
					.then((res) => {
						if (res.data.code === '0') {
							ElMessage({
								message: res.data.msg,
								type: 'success',
							});
							localStorage.setItem('user', res.data.data);
							localStorage.setItem('role', 'user');
							if (rememberMe.value) {
								localStorage.setItem('rememberMe', true);
								localStorage.setItem('username', loginform.username);
								localStorage.setItem('password', loginform.password);
							} else {
								localStorage.setItem('rememberMe', false);
								localStorage.removeItem('username');
								localStorage.removeItem('password');
							}
							router.push({ name: 'main' });
						} else {
							ElMessage({
								message: res.data.msg,
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

		function toregister(page) {
			console.log(page);
			router.push({ name: 'register' });
		}

		return {
			loginform,
			rememberMe,
			login,
			toregister,
		};
	},
};
