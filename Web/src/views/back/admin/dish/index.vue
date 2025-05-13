
<template>
  <div style="margin: 20px">

    <el-input
        v-model="searchQuery.name"
        placeholder="请输入名称"
        style="width: 300px; margin-right: 10px;"
        clearable>
    </el-input>

    <el-input
        v-model="searchQuery.description"
        placeholder="请输入描述"
        style="width: 300px; margin-right: 10px;"
        clearable>
    </el-input>

    <el-button type="primary" @click="searchData">搜索</el-button>
    <el-button type="primary" @click="openForm(null)">新增数据</el-button>
    <el-table :data="data" style="width: 100%; margin-top: 20px;" stripe border>
      <el-table-column prop='window.name' label='窗口'></el-table-column>
      <el-table-column prop='name' label='名称'></el-table-column>
      <el-table-column prop='description' label='描述'>
        <template #default="scope">
          <div style="max-height: 100px;overflow-y:auto; word-break: break-all;">
            {{scope.row.description}}
          </div>
        </template></el-table-column>
      <el-table-column prop='price' label='价格'></el-table-column>
      <el-table-column label='图片'>
        <template v-slot='{ row }'>
          <img v-if='row.image' :src='row.image' alt='图片' style='width:50px; height:50px;' />
        </template>
      </el-table-column>
      <el-table-column prop='stock_quantity' label='库存数量'></el-table-column>
      <el-table-column prop='score' label='评分'></el-table-column>
      <el-table-column prop='time' label='上架时间'></el-table-column>
      <el-table-column prop="like_count" label="点赞数"></el-table-column>
      <el-table-column prop="favorite_count" label="收藏数"></el-table-column>
      <el-table-column prop="comment_count" label="评论数"></el-table-column>
      <el-table-column prop="order_count" label="订单数"></el-table-column>

      <el-table-column label="操作" fixed="right" width="180">
        <template #default="scope">
          <el-button type="warning" @click="openForm(scope.row)">编辑</el-button>
          <el-button type="danger" @click="deleteData(scope.row.id)">删除</el-button>
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
        <el-form-item label='窗口'>

          <el-select v-model="form.window_id" placeholder="请选择窗口">
            <el-option v-for="(item,index) in Window_Datas" :key="index" :label="item.name" :value="item.id"/>
          </el-select>
        </el-form-item>
        <el-form-item label='名称'>
          <el-input v-model='form.name'></el-input>
        </el-form-item>

        <el-form-item label='描述'>
          <el-input type='textarea' v-model='form.description'></el-input>
        </el-form-item>
        <el-form-item label='价格'>
          <el-input v-model='form.price'></el-input>
        </el-form-item>
        <el-form-item label='图片'>

          <el-upload
              class="upload-image"
              action=""
              :show-file-list="false"
              :on-change="handleimageChange"
          >
            <img
                v-if="form.imagePreview"
                :src="form.imagePreview"
                class="image-preview"
            />
            <el-icon v-else><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label='库存数量'>
          <el-input v-model='form.stock_quantity'></el-input>
        </el-form-item>
        <el-form-item label='评分'>
          <el-input v-model='form.score'></el-input>
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
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import Cookies from "js-cookie";

const pagination = reactive({
  page: 1,
  page_size: 8,
  count: 0,
});
const userInfo = ref({})
const data = ref([])
const dialogVisible = ref(false)
const API_URL = '/api/dish/'
const form = ref({})
const searchQuery = ref({name:'',description:'',})

onMounted(() => {
  userInfo.value = JSON.parse(Cookies.get('user'));
  fetchData()
  get_Window_Datas()

})

const decodeFileName = (filePath) => {
  return decodeURIComponent(filePath.split('/').pop()); // 解码文件名并返回
};

const downloadFile = (filePath) => {
  const url = `${filePath}`;
  window.open(url, '_blank');
};

const handleCurrentChange = async (val) => {
  pagination.page = val
  const hasSearchCondition = Object.values(searchQuery.value).some((item) => item.trim() !== '');

  if (hasSearchCondition) {
    await searchData();
  } else {
    await fetchData();
  }
}
const searchData = async () => {
  try {
    const params =
        {
          page: pagination.page,
          page_size: pagination.page_size,
        };
    const response = await axios.post('/api/search/dish/', searchQuery.value, {params});
    data.value = response.data.results;
    pagination.count = response.data.count; // 假设后端返回了分页总数
  } catch (error) {
    ElMessage.error('搜索失败');
  }
}

const Window_Datas = ref([])
const get_Window_Datas = async () => {
  const res = await axios.get('/api/window/',{page: 1, page_size: 999 })
  Window_Datas.value = res.data.results
}


const fetchData = async () => {
  try {
    const params =
        {
          page: pagination.page,
          page_size: pagination.page_size,
        };
    const response = await axios.get(API_URL, {params})
    data.value = response.data.results
    pagination.count = response.data.count;

  } catch (error) {
    ElMessage.error('数据加载失败')
  }
}

const saveData = async () => {
  try {
    const formData = new FormData();
    for (const key in form.value) {
      formData.append(key, form.value[key]);

      if (key === 'image') {
        if (form.value[key] instanceof File) {
          formData.append(key, form.value[key]);
        }
        else{
          formData.delete(key)
        }
      }
      if (key === 'imagePreview') {
        formData.delete(key)
      }

    }
    if (form.value.id) {
      await axios.put(`${API_URL}${form.value.id}/ `, formData)
      ElMessage.success('数据更新成功')
    } else {
      await axios.post(API_URL, formData)
      ElMessage.success('数据添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('数据保存失败')
  }
}

const deleteData = async (id) => {
  ElMessageBox.confirm(
      '此操作将永久删除该记录, 是否继续?',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
  ).then(async () => {

    try {
      await axios.delete(`${API_URL}${id} / `);
      ElMessage.success('数据删除成功');
      fetchData();
    } catch (error) {
      ElMessage.error('数据删除失败');
    }

  }).catch(() => {
    ElMessage({
      type: 'info',
      message: '已取消删除',
    });
  });
}


const openForm = (item) => {
  if (item) {
    form.value =
        {...item,imagePreview: item.image,} } else {
    form.value = {} }
  dialogVisible.value = true
}

const handleimageChange = (file) => {
  const reader = new FileReader();
  reader.onload = (e) => {
    form.value.imagePreview =
        e.target.result; // 预览
  };
  reader.readAsDataURL(file.raw);
  form.value.image = file.raw; // 存储文件
};

</script>
<style scoped>
/* 你可以在这里添加一些样式 */
</style>
