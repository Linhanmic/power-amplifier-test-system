<template>
  <div class="audio-source-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>音源管理</span>
          <div>
            <el-button type="success" @click="handleExport">
              <el-icon><Download /></el-icon>导出Excel
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>新增音源
            </el-button>
          </div>
        </div>
      </template>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="source_name" label="音源名称" />
        <el-table-column prop="source_code" label="音源编码" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="音源名称" prop="source_name">
          <el-input v-model="formData.source_name" placeholder="请输入音源名称" />
        </el-form-item>
        <el-form-item label="音源编码" prop="source_code">
          <el-input v-model="formData.source_code" placeholder="如: BT_MUSIC" />
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
import { audioSourceTypeApi } from '@/api'
import { exportToExcel, statusMap } from '@/utils/export'

const tableData = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const editingId = ref(null)

const formData = reactive({
  source_name: '',
  source_code: '',
  description: '',
  status: 'active'
})

const formRules = {
  source_name: [{ required: true, message: '请输入音源名称', trigger: 'blur' }],
  source_code: [{ required: true, message: '请输入音源编码', trigger: 'blur' }]
}

const loadData = async () => {
  try {
    tableData.value = await audioSourceTypeApi.getList()
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增音源类型'
  editingId.value = null
  Object.assign(formData, {
    source_name: '', source_code: '', description: '', status: 'active'
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑音源类型'
  editingId.value = row.id
  Object.assign(formData, {
    source_name: row.source_name,
    source_code: row.source_code,
    description: row.description,
    status: row.status
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await audioSourceTypeApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await audioSourceTypeApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该音源类型吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await audioSourceTypeApi.delete(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const handleExport = () => {
  const columns = [
    { prop: 'source_name', label: '音源名称', width: 20 },
    { prop: 'source_code', label: '音源编码', width: 15 },
    { prop: 'description', label: '描述', width: 30 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val }
  ]
  exportToExcel(tableData.value, columns, '音源类型列表')
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
</style>
