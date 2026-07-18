<template>
  <div class="requirement-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>需求管理</span>
          <div>
            <el-button type="success" @click="handleExport">
              <el-icon><Download /></el-icon>导出Excel
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>新增需求
            </el-button>
          </div>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="关键词">
          <el-input v-model="searchParams.keyword" placeholder="需求编号/标题" clearable @keyup.enter="loadData" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchParams.status" placeholder="全部" clearable>
            <el-option label="草稿" value="draft" />
            <el-option label="评审中" value="reviewing" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="searchParams.category" placeholder="全部" clearable>
            <el-option label="功能测试" value="功能测试" />
            <el-option label="性能测试" value="性能测试" />
            <el-option label="可靠性测试" value="可靠性测试" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="req_code" label="需求编号" width="120" />
        <el-table-column prop="title" label="需求标题" show-overflow-tooltip />
        <el-table-column prop="category" label="分类" width="100" />
        <el-table-column prop="priority" label="优先级" width="80">
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)" size="small">
              {{ row.priority }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_by" label="创建人" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="primary" link @click="handleDetail(row)">详情</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="searchParams.page"
        v-model:page-size="searchParams.per_page"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 20px; justify-content: flex-end"
        @size-change="loadData"
        @current-change="loadData"
      />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="需求编号" prop="req_code">
              <el-input v-model="formData.req_code" placeholder="请输入需求编号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="优先级" prop="priority">
              <el-select v-model="formData.priority" placeholder="请选择优先级">
                <el-option label="S" value="S" />
                <el-option label="A" value="A" />
                <el-option label="B" value="B" />
                <el-option label="C" value="C" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="需求标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入需求标题" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分类" prop="category">
              <el-select v-model="formData.category" placeholder="请选择分类">
                <el-option label="功能测试" value="功能测试" />
                <el-option label="性能测试" value="性能测试" />
                <el-option label="可靠性测试" value="可靠性测试" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="formData.status" placeholder="请选择状态">
                <el-option label="草稿" value="draft" />
                <el-option label="评审中" value="reviewing" />
                <el-option label="已通过" value="approved" />
                <el-option label="已拒绝" value="rejected" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="需求描述">
          <el-input v-model="formData.description" type="textarea" :rows="4" placeholder="请输入需求描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="需求详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="需求编号">{{ detailData.req_code }}</el-descriptions-item>
        <el-descriptions-item label="优先级">
          <el-tag :type="getPriorityType(detailData.priority)" size="small">{{ detailData.priority }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="需求标题" :span="2">{{ detailData.title }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ detailData.category || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailData.status)">{{ getStatusText(detailData.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建人">{{ detailData.created_by || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailData.created_at }}</el-descriptions-item>
        <el-descriptions-item label="需求描述" :span="2">
          {{ detailData.description || '-' }}
        </el-descriptions-item>
      </el-descriptions>

      <el-divider>车型详情（按差异分组）</el-divider>

      <!-- 不适用车型 -->
      <div v-if="groupedVehicleDetails.not_applicable.length > 0" class="vehicle-group">
        <div class="group-header not-applicable">
          <el-tag type="info" size="large">不适用</el-tag>
          <span class="group-desc">以下车型不适用该需求</span>
        </div>
        <el-table :data="groupedVehicleDetails.not_applicable" border size="small" class="group-table">
          <el-table-column prop="vehicle_model_name" label="车型" width="150" />
          <el-table-column label="车型细节" min-width="200">
            <template #default>
              <span class="not-applicable-text">不适用</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 适用车型（按差异分组） -->
      <div v-for="(group, index) in groupedVehicleDetails.applicable_groups" :key="index" class="vehicle-group">
        <div class="group-header applicable">
          <el-tag type="success" size="large">差异组 {{ index + 1 }}</el-tag>
          <span class="group-desc">{{ group.description }}</span>
        </div>
        <el-table :data="group.vehicles" border size="small" class="group-table">
          <el-table-column prop="vehicle_model_name" label="车型" width="150" />
          <el-table-column label="功能状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.function_status === '正常' ? 'success' : 'warning'" size="small">
                {{ row.function_status || '-' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="通道数" width="80">
            <template #default="{ row }">
              {{ row.channel_count || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="功率(W)" width="80">
            <template #default="{ row }">
              {{ row.power_value || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="备注" min-width="150">
            <template #default="{ row }">
              {{ row.remark || '-' }}
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 无车型详情时显示 -->
      <el-empty v-if="!detailData.vehicle_details || detailData.vehicle_details.length === 0"
                description="暂无车型详情" :image-size="100" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { requirementApi } from '@/api'
import { exportToExcel, statusMap, priorityMap } from '@/utils/export'

const tableData = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const editingId = ref(null)
const detailData = ref({})

const searchParams = reactive({
  page: 1,
  per_page: 20,
  keyword: '',
  status: '',
  category: ''
})

const formData = reactive({
  req_code: '',
  title: '',
  description: '',
  category: '',
  priority: 'A',
  status: 'draft'
})

const formRules = {
  req_code: [{ required: true, message: '请输入需求编号', trigger: 'blur' }],
  title: [{ required: true, message: '请输入需求标题', trigger: 'blur' }]
}

// 按差异分组车型详情
const groupedVehicleDetails = computed(() => {
  const details = detailData.value.vehicle_details || []
  const result = {
    not_applicable: [],
    applicable_groups: []
  }

  // 分离不适用和适用车型
  const applicable = []
  details.forEach(d => {
    if (!d.feature_support) {
      result.not_applicable.push(d)
    } else {
      applicable.push(d)
    }
  })

  // 按差异分组（功能状态、通道数、功率）
  const groups = {}
  applicable.forEach(d => {
    const key = `${d.function_status || ''}_${d.channel_count || ''}_${d.power_value || ''}`
    if (!groups[key]) {
      groups[key] = {
        function_status: d.function_status,
        channel_count: d.channel_count,
        power_value: d.power_value,
        vehicles: [],
        description: ''
      }
    }
    groups[key].vehicles.push(d)
  })

  // 生成分组描述
  Object.values(groups).forEach(group => {
    const parts = []
    if (group.function_status) parts.push(`功能状态: ${group.function_status}`)
    if (group.channel_count) parts.push(`通道数: ${group.channel_count}`)
    if (group.power_value) parts.push(`功率: ${group.power_value}W`)
    group.description = parts.join(' | ') || '无差异信息'
    result.applicable_groups.push(group)
  })

  return result
})

const getPriorityType = (priority) => {
  const map = { S: 'danger', A: 'warning', B: 'success', C: 'info' }
  return map[priority] || 'info'
}

const getStatusType = (status) => {
  const map = { draft: 'info', reviewing: 'warning', approved: 'success', rejected: 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { draft: '草稿', reviewing: '评审中', approved: '已通过', rejected: '已拒绝' }
  return map[status] || status
}

const loadData = async () => {
  try {
    const res = await requirementApi.getList(searchParams)
    tableData.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const resetSearch = () => {
  searchParams.keyword = ''
  searchParams.status = ''
  searchParams.category = ''
  searchParams.page = 1
  loadData()
}

const handleAdd = () => {
  dialogTitle.value = '新增需求'
  editingId.value = null
  Object.assign(formData, {
    req_code: '', title: '', description: '',
    category: '', priority: 'A', status: 'draft'
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑需求'
  editingId.value = row.id
  Object.assign(formData, {
    req_code: row.req_code,
    title: row.title,
    description: row.description,
    category: row.category,
    priority: row.priority,
    status: row.status
  })
  dialogVisible.value = true
}

const handleDetail = async (row) => {
  try {
    detailData.value = await requirementApi.getDetail(row.id)
    detailVisible.value = true
  } catch (error) {
    console.error('获取详情失败:', error)
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await requirementApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await requirementApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该需求吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await requirementApi.delete(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const handleExport = () => {
  const columns = [
    { prop: 'req_code', label: '需求编号', width: 15 },
    { prop: 'title', label: '需求标题', width: 30 },
    { prop: 'category', label: '分类', width: 15 },
    { prop: 'priority', label: '优先级', width: 10 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val },
    { prop: 'created_by', label: '创建人', width: 10 },
    { prop: 'created_at', label: '创建时间', width: 20 }
  ]
  exportToExcel(tableData.value, columns, '需求列表')
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.vehicle-group {
  margin-bottom: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  overflow: hidden;
}

.group-header {
  padding: 10px 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.group-header.applicable {
  background-color: #f0f9eb;
  border-bottom: 1px solid #e1f3d8;
}

.group-header.not-applicable {
  background-color: #f4f4f5;
  border-bottom: 1px solid #e9e9eb;
}

.group-desc {
  color: #606266;
  font-size: 13px;
}

.group-table {
  margin: 0;
}

.group-table :deep(.el-table__header-wrapper) {
  background-color: #fafafa;
}

.not-applicable-text {
  color: #909399;
  font-style: italic;
}
</style>
