<template>
  <div class="signal-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>信号定义管理</span>
          <div>
            <el-button type="success" @click="handleExport">
              <el-icon><Download /></el-icon>导出Excel
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>新增信号
            </el-button>
          </div>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="CAN矩阵">
          <el-select v-model="searchParams.matrix_id" placeholder="全部" clearable>
            <el-option v-for="m in matrices" :key="m.id" :label="m.matrix_name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="signal_name" label="信号名称" width="150" />
        <el-table-column prop="message_id" label="报文ID" width="100" />
        <el-table-column prop="message_name" label="报文名称" />
        <el-table-column prop="signal_type" label="类型" width="100" />
        <el-table-column prop="data_length" label="长度(bit)" width="100" />
        <el-table-column prop="start_bit" label="起始位" width="80" />
        <el-table-column prop="factor" label="系数" width="80" />
        <el-table-column prop="offset" label="偏移" width="80" />
        <el-table-column prop="min_value" label="最小值" width="80" />
        <el-table-column prop="max_value" label="最大值" width="80" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">
              {{ row.status === 'active' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="所属矩阵" prop="matrix_id">
          <el-select v-model="formData.matrix_id" placeholder="请选择矩阵">
            <el-option v-for="m in matrices" :key="m.id" :label="m.matrix_name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="信号名称" prop="signal_name">
              <el-input v-model="formData.signal_name" placeholder="请输入信号名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="报文ID" prop="message_id">
              <el-input v-model="formData.message_id" placeholder="如: 0x100" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="报文名称">
              <el-input v-model="formData.message_name" placeholder="请输入报文名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="信号类型">
              <el-select v-model="formData.signal_type" placeholder="请选择类型">
                <el-option label="unsigned" value="unsigned" />
                <el-option label="signed" value="signed" />
                <el-option label="float" value="float" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="数据长度">
              <el-input-number v-model="formData.data_length" :min="1" :max="64" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="起始位">
              <el-input-number v-model="formData.start_bit" :min="0" :max="63" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="单位">
              <el-input v-model="formData.unit" placeholder="单位" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="系数">
              <el-input-number v-model="formData.factor" :precision="4" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="偏移量">
              <el-input-number v-model="formData.offset" :precision="4" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="状态">
              <el-radio-group v-model="formData.status">
                <el-radio value="active">启用</el-radio>
                <el-radio value="inactive">停用</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="最小值">
              <el-input-number v-model="formData.min_value" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="最大值">
              <el-input-number v-model="formData.max_value" />
            </el-form-item>
          </el-col>
        </el-row>
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
import { signalDefinitionApi, canMatrixApi } from '@/api'
import { exportToExcel, statusMap } from '@/utils/export'

const tableData = ref([])
const matrices = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const editingId = ref(null)

const searchParams = reactive({
  matrix_id: ''
})

const formData = reactive({
  matrix_id: '',
  signal_name: '',
  message_id: '',
  message_name: '',
  signal_type: 'unsigned',
  data_length: 8,
  start_bit: 0,
  factor: 1,
  offset: 0,
  min_value: 0,
  max_value: 255,
  unit: '',
  status: 'active'
})

const formRules = {
  matrix_id: [{ required: true, message: '请选择矩阵', trigger: 'change' }],
  signal_name: [{ required: true, message: '请输入信号名称', trigger: 'blur' }],
  message_id: [{ required: true, message: '请输入报文ID', trigger: 'blur' }]
}

const loadMatrices = async () => {
  try {
    const res = await canMatrixApi.getList({ per_page: 100 })
    matrices.value = res.items
  } catch (error) {
    console.error('加载矩阵失败:', error)
  }
}

const loadData = async () => {
  if (!searchParams.matrix_id) {
    tableData.value = []
    return
  }
  try {
    tableData.value = await signalDefinitionApi.getList(searchParams)
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const resetSearch = () => {
  searchParams.matrix_id = ''
  tableData.value = []
}

const handleAdd = () => {
  dialogTitle.value = '新增信号定义'
  editingId.value = null
  Object.assign(formData, {
    matrix_id: searchParams.matrix_id || '', signal_name: '', message_id: '',
    message_name: '', signal_type: 'unsigned', data_length: 8,
    start_bit: 0, factor: 1, offset: 0, min_value: 0, max_value: 255,
    unit: '', status: 'active'
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑信号定义'
  editingId.value = row.id
  Object.assign(formData, {
    matrix_id: row.matrix_id,
    signal_name: row.signal_name,
    message_id: row.message_id,
    message_name: row.message_name,
    signal_type: row.signal_type,
    data_length: row.data_length,
    start_bit: row.start_bit,
    factor: row.factor,
    offset: row.offset,
    min_value: row.min_value,
    max_value: row.max_value,
    unit: row.unit,
    status: row.status
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await signalDefinitionApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await signalDefinitionApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该信号定义吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await signalDefinitionApi.delete(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const handleExport = () => {
  const columns = [
    { prop: 'signal_name', label: '信号名称', width: 20 },
    { prop: 'message_id', label: '报文ID', width: 12 },
    { prop: 'message_name', label: '报文名称', width: 20 },
    { prop: 'signal_type', label: '类型', width: 10 },
    { prop: 'data_length', label: '长度(bit)', width: 10 },
    { prop: 'start_bit', label: '起始位', width: 10 },
    { prop: 'factor', label: '系数', width: 10 },
    { prop: 'offset', label: '偏移', width: 10 },
    { prop: 'min_value', label: '最小值', width: 10 },
    { prop: 'max_value', label: '最大值', width: 10 },
    { prop: 'unit', label: '单位', width: 10 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val }
  ]
  exportToExcel(tableData.value, columns, '信号定义列表')
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadMatrices()
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
