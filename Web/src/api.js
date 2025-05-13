import axios from 'axios';

// 创建一个 Axios 实例
const instance = axios.create({
	baseURL: 'http://10.18.1.48:8001/', // Django API 的基础 URL
	withCredentials: false, // 如果不需要携带 cookie，设为 false
	headers: {
		'Content-Type': 'application/json',
	},
});

// 请求拦截器
instance.interceptors.request.use(
	(config) => {
		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);

// 响应拦截器
instance.interceptors.response.use(
	(response) => {
		return response;
	},
	(error) => {
		return Promise.reject(error);
	}
);

export default instance;
