<template>
  <div>
    <h1>支付成功</h1>
    <p>订单号：{{ orderId }}</p>
    <p>支付金额：{{ totalAmount }} 元</p>
    <el-button type="primary" @click="goToHome">返回首页</el-button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const orderId = ref('');
const totalAmount = ref('');

// 从 URL 中获取订单信息
onMounted(() => {
  const query = new URLSearchParams(window.location.search);
  orderId.value = query.get('out_trade_no');
  totalAmount.value = query.get('total_amount');

  // 向后端确认支付状态
  confirmPaymentStatus();
});

// 确认支付状态
const confirmPaymentStatus = async () => {
  try {
    const response = await axios.get('/api/confirm_payment/', {
      params: {order_id: orderId.value},
    });
    if (response.data.success) {
      console.log('支付状态确认成功');
    } else {
      console.error('支付状态确认失败');
    }
  } catch (error) {
    console.error('支付状态确认失败', error);
  }
};

// 返回首页
const goToHome = () => {
  router.push('/main_dish_detail');
};
</script>

<style scoped>
/* 你可以在这里添加一些样式 */
</style>