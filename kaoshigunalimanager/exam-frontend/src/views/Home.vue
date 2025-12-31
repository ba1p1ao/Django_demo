<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background-color: #409EFF">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-title">题目总数</div>
              <div class="stat-value">{{ stats.questionCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background-color: #67C23A">
              <el-icon><Notebook /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-title">试卷总数</div>
              <div class="stat-value">{{ stats.examCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background-color: #E6A23C">
              <el-icon><Edit /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-title">考试记录</div>
              <div class="stat-value">{{ stats.recordCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background-color: #F56C6C">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-title">用户总数</div>
              <div class="stat-value">{{ stats.userCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>欢迎来到在线考试系统</span>
            </div>
          </template>
          <div class="welcome-content">
            <p>当前用户：{{ userStore.userInfo?.nickname }}</p>
            <p>用户角色：{{ roleText }}</p>
            <p>注册时间：{{ userStore.userInfo?.create_time }}</p>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>快捷操作</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button v-if="isStudent" type="primary" @click="$router.push('/exam-list')">
              参加考试
            </el-button>
            <el-button v-if="isTeacherOrAdmin" type="success" @click="$router.push('/questions')">
              管理题库
            </el-button>
            <el-button v-if="isTeacherOrAdmin" type="warning" @click="$router.push('/exams')">
              创建试卷
            </el-button>
            <el-button @click="$router.push('/records')">
              查看记录
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getSystemStatistics } from '@/api/exam'

const userStore = useUserStore()

const stats = ref({
  questionCount: 0,
  examCount: 0,
  recordCount: 0,
  userCount: 0
})

const isStudent = computed(() => userStore.userInfo?.role === 'student')
const isTeacherOrAdmin = computed(() => ['teacher', 'admin'].includes(userStore.userInfo?.role))

const roleText = computed(() => {
  const roleMap = {
    student: '学生',
    teacher: '教师',
    admin: '管理员'
  }
  return roleMap[userStore.userInfo?.role] || '未知'
})

const loadStatistics = async () => {
  try {
    const res = await getSystemStatistics()
    stats.value = {
      questionCount: res.data.question_count || 0,
      examCount: res.data.exam_count || 0,
      recordCount: res.data.record_count || 0,
      userCount: res.data.user_count || 0
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

onMounted(() => {
  loadStatistics()
})
</script>

<style scoped>
.home-container {
  padding: 0;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
}

.stat-icon .el-icon {
  font-size: 30px;
  color: #fff;
}

.stat-content {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.card-header {
  font-weight: bold;
  color: #303133;
}

.welcome-content p {
  margin: 10px 0;
  color: #606266;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.quick-actions .el-button {
  margin: 0;
}
</style>