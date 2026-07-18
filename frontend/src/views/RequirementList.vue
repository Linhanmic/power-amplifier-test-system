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
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 列显示设置 -->
      <div class="column-settings">
        <el-popover placement="bottom" :width="400" trigger="click">
          <template #reference>
            <el-button size="small">
              <el-icon><Setting /></el-icon> 列设置
            </el-button>
          </template>
          <div class="column-checkbox-group">
            <el-checkbox v-model="columnVisibility.req_code" disabled>需求ID</el-checkbox>
            <el-checkbox v-model="columnVisibility.title" disabled>需求名称</el-checkbox>
            <el-checkbox v-model="columnVisibility.priority">优先级</el-checkbox>
            <el-checkbox v-model="columnVisibility.description">需求详情</el-checkbox>
            <el-checkbox v-model="columnVisibility.verification_scope">验证范围</el-checkbox>
            <el-checkbox v-model="columnVisibility.verification_criteria">验证准则</el-checkbox>
            <el-checkbox v-model="columnVisibility.designer">编制人</el-checkbox>
            <el-checkbox v-model="columnVisibility.design_date">编制日期</el-checkbox>
            <el-checkbox v-model="columnVisibility.status">状态</el-checkbox>
          </div>
        </el-popover>
      </div>

      <el-table :data="tableData" border style="width: 100%" :default-sort="{ prop: 'req_code', order: 'ascending' }">
        <el-table-column prop="req_code" label="需求ID" width="140" fixed sortable />
        <el-table-column v-if="columnVisibility.title" prop="title" label="需求名称" show-overflow-tooltip min-width="150" />
        <el-table-column v-if="columnVisibility.priority" prop="priority" label="优先级" width="80" sortable>
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)" size="small">
              {{ row.priority }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="columnVisibility.description" prop="description" label="需求详情" show-overflow-tooltip min-width="200" />
        <el-table-column v-if="columnVisibility.verification_scope" prop="verification_scope" label="验证范围" show-overflow-tooltip min-width="150" />
        <el-table-column v-if="columnVisibility.verification_criteria" prop="verification_criteria" label="验证准则" show-overflow-tooltip min-width="150" />
        <el-table-column v-if="columnVisibility.designer" prop="designer" label="编制人" width="80" />
        <el-table-column v-if="columnVisibility.design_date" prop="design_date" label="编制日期" width="110" sortable />
        <el-table-column v-if="columnVisibility.status" prop="status" label="状态" width="90" sortable>
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
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
            <el-form-item label="需求ID" prop="req_code">
              <el-input v-model="formData.req_code" :placeholder="reqCodePlaceholder" />
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
        <el-form-item label="需求名称" prop="title">
          <el-input v-model="formData.title" placeholder="请输入需求名称" />
        </el-form-item>
        <el-form-item label="需求详情">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入需求详情" />
        </el-form-item>
        <el-form-item label="验证范围">
          <el-input v-model="formData.verification_scope" type="textarea" :rows="2" placeholder="请输入验证范围" />
        </el-form-item>
        <el-form-item label="验证准则">
          <el-input v-model="formData.verification_criteria" type="textarea" :rows="2" placeholder="请输入验证准则" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="编制人">
              <el-input v-model="formData.designer" placeholder="请输入编制人" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="编制日期">
              <el-date-picker v-model="formData.design_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="状态">
          <el-select v-model="formData.status" placeholder="请选择状态">
            <el-option label="草稿" value="draft" />
            <el-option label="评审中" value="reviewing" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
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
        <el-descriptions-item label="需求ID">{{ detailData.req_code }}</el-descriptions-item>
        <el-descriptions-item label="优先级">
          <el-tag :type="getPriorityType(detailData.priority)" size="small">{{ detailData.priority }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="需求名称" :span="2">{{ detailData.title }}</el-descriptions-item>
        <el-descriptions-item label="需求详情" :span="2">{{ detailData.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="验证范围" :span="2">{{ detailData.verification_scope || '-' }}</el-descriptions-item>
        <el-descriptions-item label="验证准则" :span="2">{{ detailData.verification_criteria || '-' }}</el-descriptions-item>
        <el-descriptions-item label="编制人">{{ detailData.designer || '-' }}</el-descriptions-item>
        <el-descriptions-item label="编制日期">{{ detailData.design_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailData.status)">{{ getStatusText(detailData.status) }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider>车型详情</el-divider>

      <!-- 按差异分组显示 -->
      <div v-if="groupedVehicleDetails.length > 0" class="vehicle-groups">
        <div v-for="(group, index) in groupedVehicleDetails" :key="index" class="vehicle-group-item">
          <el-table :data="[group]" border style="width: 100%">
            <el-table-column label="适用车型" min-width="180">
              <template #default>
                <div class="vehicle-names">
                  <el-tag v-for="name in group.vehicle_names" :key="name" size="small" style="margin: 2px;">
                    {{ name }}
                  </el-tag>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="适用状态" width="100">
              <template #default>
                <el-tag :type="group.feature_support ? 'success' : 'info'" size="small">
                  {{ group.feature_support ? '适用' : '不适用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="车型差异" min-width="250">
              <template #default>
                <span v-if="!group.feature_support" class="not-applicable">不适用</span>
                <span v-else-if="group.difference_description">{{ group.difference_description }}</span>
                <span v-else class="no-difference">无</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
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

// 列显示控制
const columnVisibility = reactive({
  req_code: true,
  title: true,
  priority: true,
  description: true,
  verification_scope: true,
  verification_criteria: true,
  designer: true,
  design_date: true,
  status: true
})

const searchParams = reactive({
  page: 1,
  per_page: 20,
  keyword: '',
  status: ''
})

const formData = reactive({
  req_code: '',
  title: '',
  description: '',
  verification_scope: '',
  verification_criteria: '',
  priority: 'A',
  status: 'draft',
  designer: '',
  design_date: ''
})

const formRules = {
  req_code: [{ required: true, message: '请输入需求ID', trigger: 'blur' }],
  title: [{ required: true, message: '请输入需求名称', trigger: 'blur' }]
}

// 需求ID占位符
const reqCodePlaceholder = 'SWRS-模块-序号 (如: SWRS-PA-001)'

// 按差异分组车型详情
const groupedVehicleDetails = computed(() => {
  const details = detailData.value.vehicle_details || []
  const groups = {}

  details.forEach(d => {
    const key = `${d.feature_support}_${d.difference_description || ''}`
    if (!groups[key]) {
      groups[key] = {
        feature_support: d.feature_support,
        difference_description: d.difference_description,
        vehicle_names: []
      }
    }
    groups[key].vehicle_names.push(d.vehicle_model_name)
  })

  return Object.values(groups)
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
  searchParams.page = 1
  loadData()
}

const handleAdd = () => {
  dialogTitle.value = '新增需求'
  editingId.value = null
  Object.assign(formData, {
    req_code: '', title: '', description: '',
    verification_scope: '', verification_criteria: '',
    priority: 'A', status: 'draft', designer: '', design_date: ''
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
    verification_scope: row.verification_scope,
    verification_criteria: row.verification_criteria,
    priority: row.priority,
    status: row.status,
    designer: row.designer,
    design_date: row.design_date
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
    // 验证需求ID格式
    if (!formData.req_code.startsWith('SWRS-')) {
      ElMessage.warning('需求ID须以 SWRS- 开头')
      return
    }
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
    { prop: 'req_code', label: '需求ID', width: 18 },
    { prop: 'title', label: '需求名称', width: 25 },
    { prop: 'priority', label: '优先级', width: 8 },
    { prop: 'description', label: '需求详情', width: 30 },
    { prop: 'verification_scope', label: '验证范围', width: 20 },
    { prop: 'verification_criteria', label: '验证准则', width: 20 },
    { prop: 'designer', label: '编制人', width: 10 },
    { prop: 'design_date', label: '编制日期', width: 12 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val }
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
  margin-bottom: 15px;
}

.column-settings {
  margin-bottom: 15px;
  display: flex;
  justify-content: flex-end;
}

.column-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.vehicle-groups {
  margin-top: 10px;
}

.vehicle-group-item {
  margin-bottom: 10px;
}

.vehicle-names {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.not-applicable {
  color: #909399;
  font-style: italic;
}

.no-difference {
  color: #67c23a;
  font-weight: 500;
}
</style>
