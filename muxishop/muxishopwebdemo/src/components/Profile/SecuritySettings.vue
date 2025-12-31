<template>
	<div class="basic-info">
		<table>
			<tr>
				<td class="table-key">
					<span>旧密码:</span>
				</td>
				<td class="table-value">
					<el-input type="password" v-model="oldPassword" placeholder="请输入密码"></el-input>
				</td>
			</tr>
			<tr>
				<td class="table-key">
					<span>新密码:</span>
				</td>
				<td class="table-value">
					<el-input type="password" v-model="newPassword" placeholder="请输入密码"></el-input>
				</td>
			</tr>
			<tr>
				<td class="table-key">
					<span>请再次输入新密码:</span>
				</td>
				<td class="table-value">
					<el-input type="password" v-model="secNewPassword" placeholder="请输入密码"></el-input>
				</td>
			</tr>
			<tr>
				<td class="table-key">
					
				</td>
				<td class="submit">
					<el-button type="success">提交</el-button>
				</td>
				
			</tr>
		</table>
		
	</div>
</template>

<script setup>
import { ref } from 'vue';
	let oldPassword=ref("");
	let newPassword=ref("");
	let secNewPassword=ref("");
</script>

<style lang="less" scoped>
	.basic-info{
		background-color: #fff;
		width: 800px;
		height: 300px;
		table{
			margin-top:20px;
			tr{
				.table-key{
					padding-left: 20px;
					font-weight: 700;
				}
				.table-value{
					padding-left: 20px;
				}
				.submit{
					padding-top: 20px;
					padding-left: 150px;
				}
			}
			
		}

	}
</style>