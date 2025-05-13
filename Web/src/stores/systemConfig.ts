import { defineStore } from 'pinia';
import { ConfigStates } from './interface';
import { request } from '../utils/service';
import { cookie } from 'xe-utils';
export const urlPrefix = '/api/init/settings/';

/**
 * 系统配置数据
 * @methods getSystemConfig 获取系统配置数据
 */
export const SystemConfigStore = defineStore('SystemConfig', {
	state: (): ConfigStates => ({
		systemConfig: {},
	}),
	actions: {
		// async getSystemConfigs() {
		// 	request({
		// 		url: urlPrefix,
		// 		method: 'get',
		// 	}).then((ret: { data: [] }) => {
		// 		// 转换数据格式并保存到pinia
		// 		this.systemConfig = JSON.parse(JSON.stringify(ret.data));
		// 	});
			
		// },
		async getSystemConfigs(){

			const url = '/setting.json'
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
			  this.systemConfig = JSON.parse(JSON.stringify(data.data));
			} catch (error) {
			  console.error('Error fetching the JSON file:', error);
			  throw error; // 重新抛出错误以便调用者处理
			}
		  },
	},
	persist: {
		enabled: true,
	},
});
