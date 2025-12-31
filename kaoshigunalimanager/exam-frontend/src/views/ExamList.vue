<template>
  <div class="exam-list-container">
    <el-card>
      <template #header>
        <span>考试列表</span>
      </template>

      <el-table :data="examList" v-loading="loading" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="试卷标题" show-overflow-tooltip />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="duration" label="时长(分钟)" width="120" />
        <el-table-column prop="total_score" label="总分" width="80" />
        <el-table-column prop="pass_score" label="及格分" width="80" />
        <el-table-column prop="start_time" label="开始时间" width="180" />
        <el-table-column prop="end_time" label="结束时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="handleTakeExam(row)"
              :disabled="!canTakeExam(row)"
            >
              参加考试
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getAvailableExamList } from '@/api/exam'

const router = useRouter()

const loading = ref(false)
const examList = ref([])

const canTakeExam = (exam) => {
  const now = new Date()
  const startTime = new Date(exam.start_time)
  const endTime = new Date(exam.end_time)
  return now >= startTime && now <= endTime
}

const loadExamList = async () => {
  loading.value = true
  try {
    const res = await getAvailableExamList()
    examList.value = res.data || []
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleTakeExam = async (exam) => {
  if (!canTakeExam(exam)) {
    ElMessage.warning('当前不在考试时间内')
    return
  }
  router.push(`/exam-take/${exam.id}`)
}

onMounted(() => {
  loadExamList()
})
</script>

<style scoped>
.exam-list-container {
  height: 100%;
}
</style>