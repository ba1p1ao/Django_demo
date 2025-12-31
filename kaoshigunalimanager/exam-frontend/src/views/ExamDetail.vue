<template>
  <div class="exam-detail-container">
    <el-card>
      <template #header>
        <div class="header-container">
          <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
          <span class="title">考试详情</span>
        </div>
      </template>

      <!-- 考试基本信息 -->
      <div class="exam-info-section">
        <h3>考试基本信息</h3>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="试卷标题">{{ examInfo.title }}</el-descriptions-item>
          <el-descriptions-item label="试卷描述">{{ examInfo.description || '-' }}</el-descriptions-item>
          <el-descriptions-item label="总分">{{ examInfo.total_score }} 分</el-descriptions-item>
          <el-descriptions-item label="及格分">{{ examInfo.pass_score }} 分</el-descriptions-item>
          <el-descriptions-item label="考试时长">{{ examInfo.duration }} 分钟</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getExamStatusColor(examInfo.status)">{{ getExamStatusText(examInfo.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ examInfo.start_time || '-' }}</el-descriptions-item>
          <el-descriptions-item label="结束时间">{{ examInfo.end_time || '-' }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 考试统计信息 -->
      <div class="exam-statistics-section" v-if="statistics">
        <h3>考试统计</h3>
        <el-descriptions :column="3" border>
          <el-descriptions-item label="参加人数">{{ statistics.total_participants || 0 }}</el-descriptions-item>
          <el-descriptions-item label="未参加">{{ statistics.not_participated || 0 }}</el-descriptions-item>
          <el-descriptions-item label="及格率">{{ statistics.pass_rate !== null && statistics.pass_rate !== undefined ? (statistics.pass_rate * 100).toFixed(1) + '%' : '-' }}</el-descriptions-item>
          <el-descriptions-item label="平均分">{{ statistics.average_score !== null && statistics.average_score !== undefined ? statistics.average_score.toFixed(1) : '-' }}</el-descriptions-item>
          <el-descriptions-item label="最高分">{{ statistics.max_score !== null && statistics.max_score !== undefined ? statistics.max_score : '-' }}</el-descriptions-item>
          <el-descriptions-item label="最低分">{{ statistics.min_score !== null && statistics.min_score !== undefined ? statistics.min_score : '-' }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 学生成绩列表 -->
      <div class="student-records-section">
        <h3>学生成绩列表</h3>
        
        <!-- 学生成绩筛选表单 -->
        <el-form :inline="true" :model="searchForm" class="student-search-form">
          <el-form-item label="用户名">
            <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable style="width: 150px" />
          </el-form-item>
          <el-form-item label="昵称">
            <el-input v-model="searchForm.nickname" placeholder="请输入昵称" clearable style="width: 150px" />
          </el-form-item>
          <el-form-item label="考试状态">
            <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 150px">
              <el-option label="未开始" value="not_started" />
              <el-option label="进行中" value="in_progress" />
              <el-option label="已提交" value="submitted" />
              <el-option label="已阅卷" value="graded" />
            </el-select>
          </el-form-item>
          <el-form-item label="是否及格">
            <el-select v-model="searchForm.is_passed" placeholder="请选择" clearable style="width: 150px">
              <el-option label="是" :value="1" />
              <el-option label="否" :value="0" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">筛选</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>

        <el-table :data="filteredStudentRecords" v-loading="loading" border>
          <el-table-column prop="user_id" label="学生ID" width="100" />
          <el-table-column prop="username" label="用户名" width="120" />
          <el-table-column prop="nickname" label="昵称" width="120" />
          <el-table-column prop="role" label="角色" width="100">
            <template #default="{ row }">
              <el-tag size="small">{{ getRoleText(row.role) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="score" label="得分" width="100">
            <template #default="{ row }">
              <span v-if="row.score !== null" :style="{ color: row.is_passed ? '#67C23A' : '#F56C6C', fontWeight: 'bold' }">
                {{ row.score }} 分
              </span>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="score_rate" label="得分率" width="100">
            <template #default="{ row }">
              <span v-if="row.score !== null && examInfo.total_score">
                {{ ((row.score / examInfo.total_score) * 100).toFixed(1) }}%
              </span>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="is_passed" label="是否及格" width="100">
            <template #default="{ row }">
              <el-tag v-if="row.is_passed !== null" :type="row.is_passed ? 'success' : 'danger'" size="small">
                {{ row.is_passed ? '及格' : '不及格' }}
              </el-tag>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusColor(row.status)" size="small">{{ getStatusText(row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="start_time" label="开始时间" width="180" />
          <el-table-column prop="submit_time" label="提交时间" width="180" />
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="handleViewStudentRecord(row)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { getExamDetail, getExamStatistics, getGroupedExamRecords } from '@/api/exam'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const examInfo = ref({})
const statistics = ref(null)
const studentRecords = ref([])

const searchForm = reactive({
  username: '',
  nickname: '',
  status: '',
  is_passed: ''
})

const getExamStatusText = (status) => {
  const statusMap = {
    draft: '草稿',
    published: '已发布',
    closed: '已关闭'
  }
  return statusMap[status] || status
}

const getExamStatusColor = (status) => {
  const colorMap = {
    draft: 'info',
    published: 'success',
    closed: 'danger'
  }
  return colorMap[status] || ''
}

const getStatusText = (status) => {
  const statusMap = {
    not_started: '未开始',
    in_progress: '进行中',
    submitted: '已提交',
    graded: '已阅卷'
  }
  return statusMap[status] || status
}

const getStatusColor = (status) => {
  const colorMap = {
    not_started: 'info',
    in_progress: 'warning',
    submitted: 'primary',
    graded: 'success'
  }
  return colorMap[status] || ''
}

const getRoleText = (role) => {
  const roleMap = {
    student: '学生',
    teacher: '教师',
    admin: '管理员'
  }
  return roleMap[role] || role
}

const goBack = () => {
  router.back()
}

const loadExamInfo = async () => {
  const examId = route.params.id
  loading.value = true
  try {
    const res = await getExamDetail(examId)
    examInfo.value = res.data
  } catch (error) {
    console.error('加载考试信息失败:', error)
  } finally {
    loading.value = false
  }
}

const loadStatistics = async () => {
  const examId = route.params.id
  try {
    const res = await getExamStatistics(examId)
    statistics.value = res.data
  } catch (error) {
    console.error('加载统计信息失败:', error)
  }
}

const loadStudentRecords = async () => {
  const examId = route.params.id
  loading.value = true
  try {
    const res = await getGroupedExamRecords({ page: 1, size: 100 })
    const exam = res.data.list.find(e => e.id === parseInt(examId))
    if (exam && exam.student_records) {
      studentRecords.value = exam.student_records
    }
  } catch (error) {
    console.error('加载学生记录失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  // 筛选逻辑在 computed 中处理
}

const handleReset = () => {
  searchForm.username = ''
  searchForm.nickname = ''
  searchForm.status = ''
  searchForm.is_passed = ''
}

const filteredStudentRecords = computed(() => {
  let records = studentRecords.value || []
  
  const { username, nickname, status, is_passed } = searchForm
  
  return records.filter(record => {
    // 用户名筛选
    if (username && !record.username?.toLowerCase().includes(username.toLowerCase())) {
      return false
    }
    // 昵称筛选
    if (nickname && !record.nickname?.toLowerCase().includes(nickname.toLowerCase())) {
      return false
    }
    // 状态筛选
    if (status && record.status !== status) {
      return false
    }
    // 是否及格筛选
    if (is_passed !== '' && record.is_passed !== is_passed) {
      return false
    }
    return true
  })
})

const handleViewStudentRecord = (studentRecord) => {
  router.push(`/exam-record/${studentRecord.id}`)
}

onMounted(() => {
  loadExamInfo()
  loadStatistics()
  loadStudentRecords()
})
</script>

<style scoped>
.exam-detail-container {
  padding: 20px;
}

.header-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

.exam-info-section,
.exam-statistics-section,
.student-records-section {
  margin-top: 30px;
}

.exam-info-section h3,
.exam-statistics-section h3,
.student-records-section h3 {
  margin-bottom: 15px;
  color: #303133;
  font-weight: 600;
  font-size: 16px;
}

.student-search-form {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.student-search-form :deep(.el-form-item) {
  margin-bottom: 0;
}
</style>