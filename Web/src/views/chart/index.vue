<template>
	<div class="dashboard">
		<!-- 标题 -->
		<h1 class="title">数据可视化大屏</h1>
		<el-row :gutter="20" style="margin: 15px">
			<el-col :span="12">
				<v-chart v-if="dataLoaded" class="chart" :option="dish_window_pie_Option(dish_dataAnalysis_Datas)" autoresize />
			</el-col>
		</el-row>
	</div>
</template>
<script setup>
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart, BarChart, LineChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components';
import VChart from 'vue-echarts';
import { ref, onMounted } from 'vue';
import axios from 'axios';
const dataLoaded = ref(false);
// 注册 ECharts 模块
use([CanvasRenderer, PieChart, BarChart, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent]);
onMounted(() => {
	get_dish_dataAnalysis_Datas();
});

const dish_dataAnalysis_Datas = ref();
const get_dish_dataAnalysis_Datas = async () => {
	const res = await axios.get('/api/dataAnalysis/dish/');
	dish_dataAnalysis_Datas.value = res.data;
	dataLoaded.value = true;
};

const dish_window_pie_Option = (data) => {
	const seriesData = data.dish_window_pie_Data.map((item) => ({
		name: item.window,
		value: item.count,
	}));
	const legendData = seriesData.map((item) => item.name);
	return {
		title: {
			text: '菜品的各window数量统计',
			left: 'center',
		},
		tooltip: {
			trigger: 'item',
			formatter: '{a} <br/>{b}: {c} ({d}%)',
		},
		legend: {
			orient: 'vertical',
			left: 'left',
			data: legendData,
		},
		series: [
			{
				name: 'window数量统计',
				type: 'pie',
				radius: '50%',
				data: seriesData,
				smooth: true,
				emphasis: {
					itemStyle: {
						shadowBlur: 10,
						shadowOffsetX: 0,
						shadowColor: 'rgba(0, 0, 0, 0.5)',
					},
				},
			},
		],
	};
};
</script>
<style scoped>
/* 你可以在这里添加一些样式 */
.title {
	text-align: center;
	font-size: xx-large;
}
.chart {
	height: 400px;
	background-color: #fff;
	border-radius: 8px;
	box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
