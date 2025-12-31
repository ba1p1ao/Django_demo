<template>
	<div class="address">
		<div class="addAddressButton"  @click="addAddressDialogFormVisible = true">新增收获地址</div>
		<!-- 将来我们会对这里进行循环 -->
		<div class="info " v-for="(item,index) in allAddresses" :key="index">
			<div class="clearfix">
				<span class="title fl">{{item.signer_name}}</span>
				<div v-if="item.default" class="default fl">默认地址</div>
				<img class="fr cs" src="@/assets/images/profile/deletex.png" alt="" @click="">
			</div>

			<table>
				<tr>
					<td class="table-key">收货人:</td>
					<td class="table-value">{{item.signer_name}}</td>
				</tr>
				<tr>
					<td class="table-key">所在地区:</td>
					<td class="table-value">{{item.district}}</td>
				</tr>
				<tr>
					<td class="table-key">收货地址:</td>
					<td class="table-value">{{item.signer_address}}</td>
				</tr>
				<tr>
					<td class="table-key">手机:</td>
					<td class="table-value">{{item.telphone}}</td>
				</tr>
				<tr class="edit">
					<td class="table-key"></td>
					<td class="table-value" @click="editAddress(item.id)">编辑</td>
				</tr>
			</table>
		</div>
		
		<!-- 新增收获地址的弹出框 -->
		<el-dialog title="新增收货地址" v-model="addAddressDialogFormVisible">
		  <el-form :model="form">
		    <el-form-item label="收货人" :label-width="formLabelWidth">
		      <el-input v-model="form.signer_name" autocomplete="off"></el-input>
		    </el-form-item>
		    <el-form-item label="所在地区" :label-width="formLabelWidth">
		      <el-input v-model="form.district" autocomplete="off"></el-input>
		    </el-form-item>
			<el-form-item label="收获地址" :label-width="formLabelWidth">
			  <el-input v-model="form.signer_address" autocomplete="off"></el-input>
			</el-form-item>
			<el-form-item label="联系电话" :label-width="formLabelWidth">
			  <el-input v-model="form.telphone" autocomplete="off"></el-input>
			</el-form-item>
			<el-form-item label="是否默认地址" :label-width="formLabelWidth">
			  <el-switch v-model="form.default" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
			</el-form-item>
		  </el-form>
		  <template #footer>
		    <span class="dialog-footer">
		      <el-button @click="addAddressDialogFormVisible = false">取 消</el-button>
		      <el-button type="primary" @click="saveNewAddress"
		        >保 存</el-button
		      >
		    </span>
		  </template>
		</el-dialog>
		
		<!-- 编辑地址弹出框 -->
		<el-dialog title="编辑收货地址" v-model="editAddressDialogFormVisible">
		  <el-form :model="editAddressInfo">
		    <el-form-item label="收货人" :label-width="formLabelWidth">
		      <el-input v-model="editAddressInfo.signer_name" autocomplete="off"></el-input>
		    </el-form-item>
		    <el-form-item label="所在地区" :label-width="formLabelWidth">
		      <el-input v-model="editAddressInfo.district" autocomplete="off"></el-input>
		    </el-form-item>
			<el-form-item label="收获地址" :label-width="formLabelWidth">
			  <el-input v-model="editAddressInfo.signer_address" autocomplete="off"></el-input>
			</el-form-item>
			<el-form-item label="联系电话" :label-width="formLabelWidth">
			  <el-input v-model="editAddressInfo.telphone" autocomplete="off"></el-input>
			</el-form-item>
			<el-form-item label="是否默认地址" :label-width="formLabelWidth">
			  <el-switch v-model="editAddressInfo.default" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
			</el-form-item>
		  </el-form>
		  <template #footer>
		    <span class="dialog-footer">
		      <el-button @click="editAddressDialogFormVisible = false">取 消</el-button>
		      <el-button type="primary" @click="updateAddressInfo"
		        >更 新</el-button
		      >
		    </span>
		  </template>
		</el-dialog>
		
	</div>
</template>

<script setup>
	import {ref,reactive, onMounted} from 'vue';
	import {addAddressData, getAllAddressesData,editAddressData} from "@/network/address.js"
	let addAddressDialogFormVisible=ref(false);
	let form = reactive({
	          signer_name:"",
			  district:"",
			  signer_address:"",
			  telphone:"",
			  default:false
	        });
	 let formLabelWidth = ref('120px')
	 const saveNewAddress=() => {
	 	addAddressData(form).then(res=>{
			if(res.status=70000){
				alert("保存成功");
				
			}
		});
		getAllAddresses();
		addAddressDialogFormVisible.value = false;
		window.location.reload();
	 }
	 let allAddresses=ref([
		{
		  id:"",
		  signer_name:"",
		  district:"",
		  signer_address:"",
		  telphone:"",
		  default:false
		        } 
	 ])
	 const getAllAddresses= () => {
	 	getAllAddressesData().then(res=>{
			allAddresses.value=res.data;
		})
	 }
	 
	 onMounted( () => {
		 getAllAddresses();
	 } )
	 // 编辑收获地址逻辑
	 let editAddressDialogFormVisible = ref(false);
	 let editAddressInfo = reactive({
			  id:"",
	          signer_name:"",
			  district:"",
			  signer_address:"",
			  telphone:"",
			  default:false
	        });
	const editAddress=(id) => {
		allAddresses.value.forEach( (element) => {
			if(element.id==id){
				editAddressInfo = element;
				if(editAddressInfo.default==1){
					editAddressInfo.default=true;
				}else{
					editAddressInfo.default=false;
				}
			}
		} )
		editAddressDialogFormVisible.value=true;
	}
	
	const updateAddressInfo = () => {
		editAddressData(editAddressInfo).then(res=>{
			
		})
		getAllAddresses();
		window.location.reload();
		editAddressDialogFormVisible.value=false;
	}
	
</script>

<style lang="less" scoped>
	.address{
		padding-top: 20px;
		padding-left: 20px;
		padding-bottom: 20px;
		width: 870px;
		
		.addAddressButton{
			width: 115px;
			height: 30px;
			background-color: #f0f9e9;
			text-align: center;
			line-height: 30px;
			border:1px solid #bfd6af;
			font-weight: 700;
			&:hover{
				cursor: pointer;
			}
		}
		.info{
			margin-top: 10px;
			border:2px solid #e6e6e6;
			width: 830px;
			height: 180px;
			>div{
				padding: 10px;
			}
			.title{
				font-size: 14px;
				color:#666;
			}
			.default{
				margin-left: 20px;
				width: 55px;
				height: 20px;
				text-align: center;
				line-height: 20px;
				background-color: #ffaa45;
				color:white;
			}
			img{
				width: 16px;
			}
			table{
				margin-left: 30px;
				tr{
					td{
						padding-bottom: 10px;
					}
				}
				.table-key{
					text-align: right;
					color:#999999;
				
				}
				.table-value{
					padding-left: 10px;
					width: 710px;
				}
				.edit{
					text-align: right;
					color:#005ea7;
					&:hover{
						cursor: pointer;
						color:#e2231a;
					}
				}
			}
			
		}
	}
</style>