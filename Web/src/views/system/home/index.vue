<template>
	<div class="huanying">
		<!-- <img src=""> -->
		<div class="huanying-text">
			<h1>欢迎使用</h1>
			<h2>django的校园食堂点餐</h2>
		</div>
	</div>
</template>
<style scoped lang="scss">
.huanying {
	background: url('./bg.jpg') no-repeat;
	background-size: cover;
	height: 100%;
	.huanying-text {
		color: #ffffff;
		position: relative;
		top: 48%;
		transform: translateY(-50%);
		padding-left: 10%;
		letter-spacing: 6px;
		h1 {
			font-size: 56px;
		}
		h2 {
			font-size: 50px;
		}
	}
}
</style>
