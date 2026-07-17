<template>
  <div class="can-matrix-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>CAN矩阵管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>新增矩阵
          </el-button>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="关键词">
          <el-input v-model="searchParams.keyword" placeholder="矩阵名称" clearable @keyup.enter="loadData" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchParams.status" placeholder="全部" clearable>
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
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="matrix_name" label="矩阵名称" />
        <el-table-column prop="matrix_type" label="类型" width="100" />
        <el-table-column prop="version" label="版本" width="100" />
        <el-table-column prop="signal_count" label="信号数" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="primary" link @click="handleSignals(row)">信号</el-button>
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
        <el-form-item label="矩阵名称" prop="matrix_name">
          <el-input v-model="formData.matrix_name" placeholder="请输入矩阵名称" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="矩阵类型">
              <el-select v-model="formData.matrix_type" placeholder="请选择类型">
                <el-option label="功放控制" value="amplifier" />
                <el-option label="音频控制" value="audio" />
                <el-option label="诊断" value="diagnostic" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版本">
              <el-input v-model="formData.version" placeholder="如: V1.0" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="DBC文件路径">
          <el-input v-model="formData.dbc_file_path" placeholder="请输入DBC文件路径" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="formData.status">
            <el-radio value="active">启用</el-radio>
            <el-radio value="inactive">停用</el-radio>
          </el-radio-group>
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
import { canMatrixApi } from '@/api'

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
  matrix_name: '',
  matrix_type: '',
  dbc_file_path: '',
  description: '',
  version: '',
  status: 'active'
})

const formRules = {
  matrix_name: [{ required: true, message: '请输入矩阵名称', trigger: 'blur' }]
}

const loadData = async () => {
  try {
    const res = await canMatrixApi.getList(searchParams)
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
  dialogTitle.value = '新增CAN矩阵'
  editingId.value = null
  Object.assign(formData, {
    matrix_name: '', matrix_type: '', dbc_file_path: '',
    description: '', version: '', status: 'active'
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑CAN矩阵'
  editingId.value = row.id
  Object.assign(formData, {
    matrix_name: row.matrix_name,
    matrix_type: row.matrix_type,
    dbc_file_path: row.dbc_file_path,
    description: row.description,
    version: row.version,
    status: row.status
  })
  dialogVisible.value = true
}

const handleSignals = (row) => {
  ElMessage.info('信号管理功能开发中')
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await canMatrixApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await canMatrixApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该矩阵吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await canMatrixApi.delete(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
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
