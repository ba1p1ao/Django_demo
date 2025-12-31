<template>
	<div class="basic-info">
		<table>
			<tr>
				<td class="table-key">
					<span>昵称:</span>
				</td>
				<td class="table-value">
					<el-input v-model="input" placeholder="请输入昵称"></el-input>
				</td>
			</tr>
			<tr>
				<td class="table-key">
					<span>性别:</span>
				</td>
				<td class="table-value">
					 <el-radio v-model="gender" label="男" size="medium">男</el-radio>
					<el-radio v-model="gender" label="女" size="medium">女</el-radio>
					<el-radio v-model="gender" label="保密" size="medium">保密</el-radio>
				</td>
			</tr>
			<tr>
				<td class="table-key">
					<span>生日:</span>
				</td>
				<td class="table-value">
					 <el-date-picker v-model="dateValue" type="date" placeholder="选择日期"> </el-date-picker>
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
	let gender=ref("男");
	let dateValue=ref("2050-12-12");
	let input=ref("");
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