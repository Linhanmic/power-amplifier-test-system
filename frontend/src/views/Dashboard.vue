<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #409eff">
            <el-icon size="32"><Grid /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.platforms || 0 }}</div>
            <div class="stat-label">平台数量</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #67c23a">
            <el-icon size="32"><Car /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.vehicle_models || 0 }}</div>
            <div class="stat-label">车型数量</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #e6a23c">
            <el-icon size="32"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.requirements || 0 }}</div>
            <div class="stat-label">需求数量</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #f56c6c">
            <el-icon size="32"><List /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.test_cases || 0 }}</div>
            <div class="stat-label">测试用例</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>需求状态分布</span>
          </template>
          <div class="chart-container">
            <div class="status-list">
              <div class="status-item" v-for="(count, status) in stats.requirement_status" :key="status">
                <span class="status-tag" :class="status">{{ statusText(status) }}</span>
                <span class="status-count">{{ count }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>测试用例状态分布</span>
          </template>
          <div class="chart-container">
            <div class="status-list">
              <div class="status-item" v-for="(count, status) in stats.test_case_status" :key="status">
                <span class="status-tag" :class="status">{{ statusText(status) }}</span>
                <span class="status-count">{{ count }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统资源统计</span>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="车辆配置">{{ stats.vehicle_configs || 0 }}</el-descriptions-item>
            <el-descriptions-item label="测试脚本">{{ stats.test_scripts || 0 }}</el-descriptions-item>
            <el-descriptions-item label="CAN矩阵">{{ stats.can_matrices || 0 }}</el-descriptions-item>
            <el-descriptions-item label="播放矩阵">{{ stats.playback_matrices || 0 }}</el-descriptions-item>
            <el-descriptions-item label="用例分组">{{ stats.test_case_groups || 0 }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>快捷操作</span>
          </template>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/requirements')">
              <el-icon><Plus /></el-icon>新建需求
            </el-button>
            <el-button type="success" @click="$router.push('/test-cases')">
              <el-icon><Plus /></el-icon>新建用例
            </el-button>
            <el-button type="warning" @click="$router.push('/test-scripts')">
              <el-icon><Plus /></el-icon>新建脚本
            </el-button>
            <el-button type="info" @click="$router.push('/playback-matrices')">
              <el-icon><Plus /></el-icon>新建矩阵
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { statsApi } from '@/api'

const stats = ref({})

const statusText = (status) => {
  const map = {
    draft: '草稿',
    reviewing: '评审中',
    approved: '已通过',
    rejected: '已拒绝',
    ready: '就绪',
    deprecated: '已废弃'
  }
  return map[status] || status
}

onMounted(async () => {
  try {
    stats.value = await statsApi.getOverview()
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.stat-cards {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  width: 100%;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-right: 16px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.chart-container {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-list {
  width: 100%;
}

.status-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.status-item:last-child {
  border-bottom: none;
}

.status-tag {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.status-tag.draft {
  background-color: #f4f4f5;
  color: #909399;
}

.status-tag.reviewing,
.status-tag.ready {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.status-tag.approved {
  background-color: #f0f9eb;
  color: #67c23a;
}

.status-tag.rejected,
.status-tag.deprecated {
  background-color: #fef0f0;
  color: #f56c6c;
}

.status-count {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 20px 0;
}
</style>
