<template>
  <div>
    <el-button type="danger" @click="handleBuyClick" size="large">立即购买</el-button>

    <!-- 确认订单弹窗 -->
    <el-dialog v-model="dialogVisible" title="确认订单" width="30%">
      <div>
        <p style="font-size: 20px; font-weight: bold; margin-bottom: 5px">名称: {{ dishDetail.name }}</p>
        <p style="font-size: 15px; font-weight: bold; margin-bottom: 5px">
          价格: <span style="color: red">{{ dishDetail.price }}</span>
        </p>
        <p style="font-size: 15px; font-weight: bold; margin-bottom: 5px">
          购买数量：<el-input-number v-model="quantity" :min="1" :max="dishDetail.stock_quantity" label="购买数量"></el-input-number>
        </p>
        <p style="font-size: 15px; font-weight: bold; margin-bottom: 5px">
          总价：<span style="color: red">{{ parseFloat((dishDetail.price * quantity).toFixed(2)) }}</span>
        </p>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmOrder">支付</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import Cookies from 'js-cookie';

const userInfo = ref({});
const props = defineProps({
  dishDetail: {
    type: Object,
    required: true,
  },
});

const dialogVisible = ref(false);
const quantity = ref(1);

// 点击“立即购买”按钮
const handleBuyClick = () => {
  dialogVisible.value = true;
};

// 确认订单并支付
const confirmOrder = async () => {
  try {
    // 构造订单数据
    const orderData = {
      dish_id: props.dishDetail.id,
      user_id: userInfo.value.id,
      quantity: quantity.value,
      total_price: parseFloat((props.dishDetail.price * quantity.value).toFixed(2)),
      status: '支付成功',
    };

    console.log('订单数据:', orderData);

    // 1. 创建订单
    const orderResponse = await axios.post('/api/dish-order/', orderData);
    console.log('订单创建响应:', orderResponse.data);

    if (orderResponse.status !== 201) {
      throw new Error('订单创建失败');
    }

    // 2. 获取支付宝支付链接
    const paymentResponse = await axios.post('/api/payment/', {
      order_id: orderResponse.data.id,
      total_amount: orderData.total_price,
      subject: props.dishDetail.name,
    });
    console.log('支付链接响应:', paymentResponse.data);

    const payUrl = paymentResponse.data.pay_url;
    if (!payUrl) {
      throw new Error('支付链接生成失败');
    }

    console.log('支付链接:', payUrl);

    // 3. 跳转到支付宝支付页面
    window.location.href = payUrl;
  } catch (error) {
    console.error('支付失败:', error);
    ElMessage.error('支付失败: ' + error.message);
  }
};

// 初始化用户信息
onMounted(() => {
  userInfo.value = JSON.parse(Cookies.get('user'));
});
</script>

<style scoped>
/* 你可以在这里添加一些样式 */
</style>