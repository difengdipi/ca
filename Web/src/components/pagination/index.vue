<template>
	<el-pagination background layout="prev, pager, next" :total="total" :page-size="pageSizes" @change="pageChange" />
</template>
<script setup>
const props = defineProps({
	total: {
		type: Number,
		default: 0,
	},
	pageSizes: {
		type: Number,
		default: 10,
	},
});
const emit = defineEmits(['pageChange']);
const pageChange = (e) => {
	emit('pageChange', e);
};
</script>
