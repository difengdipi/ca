<template>
	<!-- 登录页面的主容器 -->
	<div class="w3l-signinform">
		<!-- 页面内容的包装容器 -->
		<div class="wrapper">
			<!-- 主要内容区域 -->
			<div class="w3l-form-info">
				<div class="w3_info">
					<!-- 标题和欢迎语 -->
					<h1>欢迎回来</h1>
					<p class="sub-para">欢迎使用我们的服务，请登录您的账户</p>
					<h2>注册</h2>

					<!-- 登录表单 -->
					<form @submit.prevent="register">
						<!-- 邮箱或用户名输入框 -->
						<div class="input-group">
							<span><i class="fa fa-user" aria-hidden="true"></i></span>
							<input v-model="registerForm.username" type="text" placeholder="请输入用户名" required />
						</div>

						<!-- 密码输入框 -->
						<div class="input-group two-groop">
							<span><i class="fa fa-key" aria-hidden="true"></i></span>
							<input v-model="registerForm.password" type="password" placeholder="请输入密码" required />
						</div>

						<div class="input-group three-groop">
							<span><i class="fa fa-key" aria-hidden="true"></i></span>
							<input v-model="registerForm.password2" type="password" placeholder="请输入密码" required />
						</div>

						<!-- 登录按钮 -->
						<button class="btn btn-primary btn-block" type="submit">注册</button>
					</form>

					<!-- 注册提示 -->
					<p class="account"><a @click="toLogin()" style="cursor: pointer">立即登录</a></p>
				</div>
			</div>
		</div>

		<!-- 页脚部分 -->
		<div class="footer">
			<p>
				&copy; 登录页面。保留所有权利 |
				<a target="_blank" href="" title="网页" style="cursor: pointer">网页</a>
			</p>
		</div>
	</div>
</template>
<script setup>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const router = useRouter();

const registerForm = reactive({
	username: '',
	password: '',
	password2: '',
});

const checkUsername = async (username) => {
	const res = await axios.post('/api/check-username/', { username: username });
	return res.data.message;
};

const register = async () => {
	if (registerForm.password !== registerForm.password2) {
		ElMessage.error('两次输入密码不一致');
		return;
	}
	const usernameExists = await checkUsername(registerForm.username);
	if (usernameExists) {
		ElMessage.error('用户名已存在。请选择其他用户名。');
		return;
	}
	const res = await axios.post('/api/register/', {
		username: registerForm.username,
		password: registerForm.password,
	});

	if (res.data.message === '用户注册成功') {
		ElMessage.success('注册成功');
		toLogin();
	} else {
		ElMessage.success('注册失败');
	}
};
// Redirect to login page
const toLogin = () => {
	router.push({ path: '/login' });
};
</script>

<style scoped>
/* 页面基础样式 */
html {
	scroll-behavior: smooth;
}

body,
html {
	margin: 0;
	padding: 0;
	color: #585858;
}

* {
	box-sizing: border-box;
	font-family: 'Kumbh Sans', sans-serif;
}

/*  wrapper */
.wrapper {
	width: 100%;
	padding-right: 15px;
	padding-left: 15px;
	margin-right: auto;
	margin-left: auto;
}

/*  /wrapper */

.d-grid {
	display: grid;
}

button,
input,
select {
	-webkit-appearance: none;
	outline: none;
}

button,
.btn,
select {
	cursor: pointer;
}

a {
	text-decoration: none;
}

h1,
h2,
h3,
h4,
h5,
h6,
p,
ul,
ol {
	margin: 0;
	padding: 0;
}

body {
	background: #f1f1f1;
	margin: 0;
	padding: 0;
}

form,
fieldset {
	border: 0;
	padding: 0;
	margin: 0;
}

img {
	max-width: 100%;
}

/*-- //Reset-Code --*/

/*-- form styling --*/
.w3l-form-info {
	padding-top: 2em;
	height: 80vh;
}

.w3l-signinform {
	padding: 40px 40px;
	min-height: 100vh;
	min-width: 100vw;
	background: url('./bg.jpg') no-repeat center;
	background-size: cover;
	-webkit-background-size: cover;
	-o-background-size: cover;
	-moz-background-size: cover;
	-ms-background-size: cover;
	position: relative;
	z-index: 1;
	align-items: center;
}

.w3l-signinform::before {
	background-color: rgb(0 0 0 / 50%);
	content: '';
	position: absolute;
	top: 0;
	min-height: 100%;
	left: 0;
	right: 0;
	z-index: -1;
}

input[type='text'],
input[type='email'],
input[type='Password'] {
	font-size: 17px;
	font-weight: 500;
	color: #fff;
	text-align: left;
	padding: 18px 18px 20px 42px;
	width: 100%;
	display: inline-block;
	box-sizing: border-box;
	border: none;
	outline: none;
	background: transparent;
	letter-spacing: 0.5px;
}

.input-group {
	/* margin-bottom: 25px; */
	padding: 0px 0px;
	position: relative;
	border: 1px solid #fff;
	border-radius: 6px;
	-webkit-border-radius: 6px;
	-moz-border-radius: 6px;
	-ms-border-radius: 6px;
	-o-border-radius: 6px;
	border-bottom-left-radius: 0px;
	border-bottom-right-radius: 0;
}

.input-group.two-groop {
	border-top: none;
	border-radius: 6px;
	-webkit-border-radius: 6px;
	-moz-border-radius: 6px;
	-ms-border-radius: 6px;
	-o-border-radius: 6px;
	border-top-left-radius: 0px;
	border-top-right-radius: 0;
	border-bottom-left-radius: 0;
}

.input-group.three-groop {
	border-top: none;
	margin-bottom: 30px;
	border-radius: 6px;
	-webkit-border-radius: 6px;
	-moz-border-radius: 6px;
	-ms-border-radius: 6px;
	-o-border-radius: 6px;
	border-top-left-radius: 0px;
	border-top-right-radius: 0;
}

.btn-block {
	display: block;
	width: 50%;
	margin: 0 auto;
}

.btn:active {
	outline: none;
}

.btn-primary {
	color: #232005;
	background-color: #ffd900;
	margin-top: 30px;
	outline: none;
	width: 100%;
	padding: 15px 15px;
	cursor: pointer;
	font-size: 18px;
	font-weight: 600;
	border-radius: 6px;
	-webkit-border-radius: 6px;
	-moz-border-radius: 6px;
	-ms-border-radius: 6px;
	-o-border-radius: 6px;
	border: none;
	text-transform: capitalize;
}

.btn-primary:hover {
	background-color: #eac803;
}

.form-row.bottom {
	display: flex;
	justify-content: space-between;
}

.form-row .form-check input[type='checkbox'] {
	display: none;
}

.form-row .form-check input[type='checkbox'] + label:before {
	border-radius: 3px;
	border: 1px solid #e2e2e2;
	color: transparent;
	content: '\2714';
	display: inline-block;
	height: 18px;
	margin-right: 5px;
	transition: 0.2s;
	vertical-align: inherit;
	width: 18px;
	text-align: center;
	line-height: 20px;
}

.form-row .form-check input[type='checkbox']:checked + label:before {
	background-color: #ffd900;
	border-color: #ffd900;
	color: #232005;
}

.form-row .form-check input[type='checkbox'] + label {
	cursor: pointer;
	color: #fff;
}

.w3_info h2 {
	display: inline-block;
	font-size: 24px;
	line-height: 35px;
	margin-bottom: 20px;
	font-weight: 600;
	color: #fff;
}

.w3_info h4 {
	display: inline-block;
	font-size: 15px;
	padding: 8px 0px;
	color: #444;
	text-transform: capitalize;
}

h1 {
	font-size: 36px;
	font-weight: 600;
	color: #fff;
	margin-bottom: 0.4em;
	line-height: 40px;
}

.w3_info {
	padding: 1em 1em;
	background: transparent;
	max-width: 400px;
	display: grid;
	margin-top: 10vh;
	margin-left: 60vw;
}

.left_grid_info {
	padding: 6em 0;
}

.w3l_form {
	padding: 0px;
	flex-basis: 50%;
	-webkit-flex-basis: 50%;
	background: #dad1f8;
}

.w3_info p {
	padding-bottom: 30px;
	text-align: center;
}

.w3_info p.sub-para {
	padding-bottom: 40px;
	text-align: left;
	color: #fff;
	opacity: 0.9;
	line-height: 28px;
}

p.account,
p.account a {
	text-align: center;
	padding-top: 20px;
	padding-bottom: 0px;
	font-size: 16px;
	color: #fff;
	opacity: 0.9;
}

p.account a {
	color: #ffd900;
}

p.account a:hover {
	text-decoration: underline;
}

a.forgot {
	color: #ffeb3b;
	margin-top: 2px;
	opacity: 0.8;
}

a.forgot:hover {
	text-decoration: underline;
}

h3.w3ls {
	margin: 10px 0px;
	padding-left: 60px;
}

h3.agileits {
	padding-left: 10px;
}

.container {
	max-width: 890px;
	margin: 0 auto;
}

.input-group i {
	font-size: 16px;
	vertical-align: middle;
	box-sizing: border-box;
	float: left;
	width: 8%;
	margin-top: 13px;
	text-align: center;
	color: #fff;
	position: absolute;
	left: 8px;
	top: 6px;
}

h5 {
	text-align: center;
	margin: 10px 0px;
	font-size: 15px;
	font-weight: 600;
	color: #000;
}

.footer {
	padding-top: 3em;
}

.footer p {
	text-align: center;
	font-size: 17px;
	line-height: 28px;
	color: #fff;
	opacity: 0.9;
}

.footer p a {
	color: #ffd900;
}

.footer p a:hover {
	text-decoration: underline;
}

p.continue {
	margin-top: 25px;
	padding: 0;
	margin-bottom: 20px;
	color: #fff;
}

p.continue span {
	position: relative;
}

p.continue span:before {
	position: absolute;
	content: '';
	height: 1px;
	background: #fff;
	width: 89%;
	left: -100%;
	top: 5px;
}

p.continue span:after {
	position: absolute;
	content: '';
	height: 1px;
	background: #fff;
	width: 89%;
	right: -100%;
	top: 5px;
}

::-webkit-input-placeholder {
	/* Edge */
	color: #fff;
}

:-ms-input-placeholder {
	/* Internet Explorer 10-11 */
	color: #fff;
}

::placeholder {
	color: #fff;
}
</style>
