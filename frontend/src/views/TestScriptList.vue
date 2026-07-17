<template>
  <div class="test-script-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>测试脚本管理</span>
          <div>
            <el-button type="success" @click="handleExport">
              <el-icon><Download /></el-icon>导出Excel
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>新增脚本
            </el-button>
          </div>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="关键词">
          <el-input v-model="searchParams.keyword" placeholder="脚本编号/标题" clearable @keyup.enter="loadData" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchParams.status" placeholder="全部" clearable>
            <el-option label="草稿" value="draft" />
            <el-option label="启用" value="active" />
            <el-option label="停用" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="script_code" label="脚本编号" width="120" />
        <el-table-column prop="title" label="脚本标题" show-overflow-tooltip />
        <el-table-column prop="script_path" label="脚本路径" show-overflow-tooltip />
        <el-table-column prop="script_type" label="类型" width="100" />
        <el-table-column prop="gauge_framework" label="Gauge框架" width="100">
          <template #default="{ row }">
            <el-tag :type="row.gauge_framework ? 'success' : 'info'" size="small">
              {{ row.gauge_framework ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="primary" link @click="handleScenarios(row)">场景</el-button>
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="脚本编号" prop="script_code">
          <el-input v-model="formData.script_code" placeholder="请输入脚本编号" />
        </el-form-item>
        <el-form-item label="脚本标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入脚本标题" />
        </el-form-item>
        <el-form-item label="脚本路径">
          <el-input v-model="formData.script_path" placeholder="如: specs/test.spec" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="脚本类型">
              <el-select v-model="formData.script_type" placeholder="请选择类型">
                <el-option label="spec" value="spec" />
                <el-option label="test" value="test" />
                <el-option label="util" value="util" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版本">
              <el-input v-model="formData.version" placeholder="如: 1.0" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="Gauge框架">
          <el-switch v-model="formData.gauge_framework" />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="formData.status">
            <el-radio value="draft">草稿</el-radio>
            <el-radio value="active">启用</el-radio>
            <el-radio value="inactive">停用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="formData.remark" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { testScriptApi } from '@/api'
import { exportToExcel, statusMap } from '@/utils/export'

const tableData = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const editingId = ref(null)

const searchParams = reactive({
  page: 1,
  per_page: 20,
  keyword: '',
  status: ''
})

const formData = reactive({
  script_code: '',
  title: '',
  script_path: '',
  script_type: 'spec',
  gauge_framework: true,
  version: '1.0',
  status: 'draft',
  remark: ''
})

const formRules = {
  script_code: [{ required: true, message: '请输入脚本编号', trigger: 'blur' }],
  title: [{ required: true, message: '请输入脚本标题', trigger: 'blur' }]
}

const getStatusType = (status) => {
  const map = { draft: 'info', active: 'success', inactive: 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { draft: '草稿', active: '启用', inactive: '停用' }
  return map[status] || status
}

const loadData = async () => {
  try {
    const res = await testScriptApi.getList(searchParams)
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
  dialogTitle.value = '新增脚本'
  editingId.value = null
  Object.assign(formData, {
    script_code: '', title: '', script_path: '',
    script_type: 'spec', gauge_framework: true,
    version: '1.0', status: 'draft', remark: ''
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑脚本'
  editingId.value = row.id
  Object.assign(formData, {
    script_code: row.script_code,
    title: row.title,
    script_path: row.script_path,
    script_type: row.script_type,
    gauge_framework: row.gauge_framework,
    version: row.version,
    status: row.status,
    remark: row.remark
  })
  dialogVisible.value = true
}

const handleScenarios = (row) => {
  ElMessage.info('场景管理功能开发中')
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await testScriptApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await testScriptApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该脚本吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await testScriptApi.delete(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const handleExport = () => {
  const columns = [
    { prop: 'script_code', label: '脚本编号', width: 15 },
    { prop: 'title', label: '脚本标题', width: 30 },
    { prop: 'script_path', label: '脚本路径', width: 30 },
    { prop: 'script_type', label: '类型', width: 10 },
    { prop: 'gauge_framework', label: 'Gauge框架', width: 10, formatter: (val) => val ? '是' : '否' },
    { prop: 'version', label: '版本', width: 10 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val }
  ]
  exportToExcel(tableData.value, columns, '测试脚本列表')
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
</style>
