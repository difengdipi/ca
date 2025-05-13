<template>
  <div style="height: 80vh; margin: 20px">
    <!-- 添加排序按钮 -->
    <div style="margin: 20px 0; display: flex; justify-content: flex-end;">
      <el-button
          type="primary"
          @click="toggleSort"
          :icon="sortAscending ? 'SortUp' : 'SortDown'"
      >
        {{ sortAscending ? '评分升序' : '评分降序' }}
      </el-button>
    </div>

    <div style="margin-top: 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px">
      <div
          v-for="item in sortedData"
          :key="item.id"
          style="border: 1px solid #eee; border-radius: 8px; padding: 0; padding-bottom: 5px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); cursor: pointer"
          @click="go_main_dish_detail(item)"
      >
        <img :src="item.image" alt="图片" style="width: 100%; height: 200px; object-fit: cover; border-radius: 6px" />
        <div
            style="
                        display: flex;
                        justify-content: space-between;
                        width: 100%;
                        padding-top: 5px;
                        padding-left: 8px;
                        padding-right: 8px;
                        font-weight: bold;
                        font-size: large;
                    "
        >
          <span>{{ item.name }}</span>
          <span style="color: red">￥{{ item.price }}</span>
        </div>
        <div style="display: flex; justify-content: space-between; width: 100%; padding-left: 8px; padding-right: 8px">
          <span style="color: gray">{{ item.time }}</span>
          <!-- 添加评分显示 -->
          <span style="color: #e6a23c">评分: {{ item.score || '未评分' }}</span>
        </div>
      </div>
    </div>
    <el-pagination
        style="margin: 20px"
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        layout="total, prev, pager, next, jumper"
        :total="pagination.count"
        @current-change="handleCurrentChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useRouter } from 'vue-router';
const router = useRouter();

const pagination = reactive({
  page: 1,
  page_size: 30,
  count: 0,
});
const userInfo = ref({});
const data = ref([]);
// 添加排序状态
const sortAscending = ref(false);

const API_URL = '/api/dish/';
const searchQuery = ref({ name: '', description: '' });

// 计算属性来处理排序
const sortedData = computed(() => {
  const sortedArray = [...data.value];
  sortedArray.sort((a, b) => {
    // 如果score不存在，默认值为0
    const scoreA = a.score || 0;
    const scoreB = b.score || 0;
    return sortAscending.value ? scoreA - scoreB : scoreB - scoreA;
  });
  return sortedArray;
});

onMounted(() => {
  userInfo.value = JSON.parse(Cookies.get('user'));
  fetchData();
  get_Window_Datas();
});

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
    const response = await axios.post('/api/search/dish/', searchQuery.value, { params });
    data.value = response.data.results;
    pagination.count = response.data.count;
  } catch (error) {
    ElMessage.error('搜索失败');
  }
};

const Window_Datas = ref([]);
const get_Window_Datas = async () => {
  const res = await axios.get('/api/window/', { page: 1, page_size: 999 });
  Window_Datas.value = res.data.results;
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

const go_main_dish_detail = async (item) => {
  localStorage.setItem('dish_id', item.id);
  router.push('/main_dish_detail');
};

// 切换排序方式
const toggleSort = () => {
  sortAscending.value = !sortAscending.value;
};
</script>

<style scoped>
/* 你可以在这里添加一些样式 */
</style>