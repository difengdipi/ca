import { defineStore } from 'pinia';
import { UserInfosStates } from './interface';
import { Session } from '/@/utils/storage';
import { request } from '../utils/service';
import Cookies from 'js-cookie';
/**
 * 用户信息
 * @methods setUserInfos 设置用户信息
 */
export const useUserInfo = defineStore('userInfo', {
	state: (): UserInfosStates => ({
		userInfos: {
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
		},
		isSocketOpen: false
	}),
	actions: {
		async updateUserInfos() {
			let userInfos: any = await this.getApiUserInfo();
			this.userInfos.username = userInfos.data.name;
			this.userInfos.avatar = userInfos.data.avatar;
			this.userInfos.name = userInfos.data.name;
			this.userInfos.email = userInfos.data.email;
			this.userInfos.mobile = userInfos.data.mobile;
			this.userInfos.gender = userInfos.data.gender;
			this.userInfos.dept_info = userInfos.data.dept_info;
			this.userInfos.role_info = userInfos.data.role_info;
			Session.set('userInfo', this.userInfos);
		},
		async setUserInfos() {
			// 存储用户信息到浏览器缓存
			// console.log(Session.get('user'))
			const user = JSON.parse(Cookies.get('user'))
			console.log(user)
			if (Session.get('user')) {
				// this.userInfos = Session.get('userInfo');
				let url = 'http://localhost:8000'
				const user = Session.get('user')

				this.userInfos.username = user.yonghuming;
				this.userInfos.avatar = url + user.touxiang;
				this.userInfos.name = user.xingming;
				this.userInfos.email = '';
				this.userInfos.mobile = user.dianhua;
				this.userInfos.gender = user.xingbie;

				console.log(Session.get('user'))
			} else {
				let userInfos: any = await this.getApiUserInfo();
				this.userInfos.username = userInfos.data.name;
				this.userInfos.avatar = userInfos.data.avatar;
				this.userInfos.name = userInfos.data.name;
				this.userInfos.email = userInfos.data.email;
				this.userInfos.mobile = userInfos.data.mobile;
				this.userInfos.gender = userInfos.data.gender;
				this.userInfos.dept_info = userInfos.data.dept_info;
				this.userInfos.role_info = userInfos.data.role_info;
				Session.set('userInfo', this.userInfos);
			}
		},
		async setWebSocketState(socketState: boolean) {
			this.isSocketOpen = socketState;
		},
		// async getApiUserInfo() {
		// 	return request({
		// 		url: '/api/system/user/user_info/',
		// 		method: 'get',
		// 	});


		// },

		getApiUserInfo: async (params?: object) => {
			// console.log(localStorage.getItem('user'))
			Session.get('user')
			console.log(Session.get('user'))
			const url = `/userInfo.json`
			try {
				const response = await fetch(url);
				// const response = await fetch(`/adminmenu.json`);
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
				const contentType = response.headers.get("content-type");
				if (!contentType || !contentType.includes("application/json")) {
					throw new Error("Content type is not application/json");
				}
				const text = await response.text(); // 获取响应的原始文本
				const data = JSON.parse(text); // 手动解析 JSON
				return data; // 返回解析后的数据
			} catch (error) {
				console.error('Error fetching the JSON file:', error);
				throw error; // 重新抛出错误以便调用者处理
			}
		},
	},
});
