<template>
  <div class="vehicle-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>车型管理</span>
          <div>
            <el-button type="success" @click="handleExport">
              <el-icon><Download /></el-icon>导出Excel
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>新增车型
            </el-button>
          </div>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="平台">
          <el-select v-model="searchParams.platform_id" placeholder="全部" clearable>
            <el-option v-for="p in platforms" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="searchParams.keyword" placeholder="车型名称/编码" clearable @keyup.enter="loadData" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="platform_name" label="所属平台" />
        <el-table-column prop="name" label="车型名称" />
        <el-table-column prop="code" label="车型编码" />
        <el-table-column prop="model_year" label="年款" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="所属平台" prop="platform_id">
          <el-select v-model="formData.platform_id" placeholder="请选择平台">
            <el-option v-for="p in platforms" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="车型名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入车型名称" />
        </el-form-item>
        <el-form-item label="车型编码" prop="code">
          <el-input v-model="formData.code" placeholder="请输入车型编码" />
        </el-form-item>
        <el-form-item label="年款">
          <el-input v-model="formData.model_year" placeholder="如: 2025" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
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
import { vehicleModelApi, platformApi } from '@/api'
import { exportToExcel, statusMap } from '@/utils/export'

const tableData = ref([])
const platforms = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const editingId = ref(null)

const searchParams = reactive({
  page: 1,
  per_page: 20,
  platform_id: '',
  keyword: ''
})

const formData = reactive({
  platform_id: '',
  name: '',
  code: '',
  model_year: '',
  status: 'active',
  remark: ''
})

const formRules = {
  platform_id: [{ required: true, message: '请选择平台', trigger: 'change' }],
  name: [{ required: true, message: '请输入车型名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入车型编码', trigger: 'blur' }]
}

const loadPlatforms = async () => {
  try {
    const res = await platformApi.getList({ per_page: 100 })
    platforms.value = res.items
  } catch (error) {
    console.error('加载平台失败:', error)
  }
}

const loadData = async () => {
  try {
    const res = await vehicleModelApi.getList(searchParams)
    tableData.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const resetSearch = () => {
  searchParams.platform_id = ''
  searchParams.keyword = ''
  searchParams.page = 1
  loadData()
}

const handleAdd = () => {
  dialogTitle.value = '新增车型'
  editingId.value = null
  Object.assign(formData, { platform_id: '', name: '', code: '', model_year: '', status: 'active', remark: '' })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑车型'
  editingId.value = row.id
  Object.assign(formData, {
    platform_id: row.platform_id,
    name: row.name,
    code: row.code,
    model_year: row.model_year,
    status: row.status,
    remark: row.remark
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await vehicleModelApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await vehicleModelApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该车型吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await vehicleModelApi.delete(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const handleExport = () => {
  const columns = [
    { prop: 'id', label: 'ID', width: 10 },
    { prop: 'platform_name', label: '所属平台', width: 15 },
    { prop: 'name', label: '车型名称', width: 20 },
    { prop: 'code', label: '车型编码', width: 15 },
    { prop: 'model_year', label: '年款', width: 10 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val },
    { prop: 'remark', label: '备注', width: 30 }
  ]
  exportToExcel(tableData.value, columns, '车型列表')
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadPlatforms()
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
