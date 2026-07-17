<template>
  <div class="config-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>车辆配置管理</span>
          <div>
            <el-button type="success" @click="handleExport">
              <el-icon><Download /></el-icon>导出Excel
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>新增配置
            </el-button>
          </div>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="车型">
          <el-select v-model="searchParams.vehicle_model_id" placeholder="全部" clearable>
            <el-option v-for="v in vehicleModels" :key="v.id" :label="v.name" :value="v.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="vehicle_model_name" label="车型" />
        <el-table-column prop="config_name" label="配置名称" />
        <el-table-column prop="config_code" label="配置编码" />
        <el-table-column prop="software_code" label="软件编码" />
        <el-table-column prop="description" label="详情" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="120px">
        <el-form-item label="所属车型" prop="vehicle_model_id">
          <el-select v-model="formData.vehicle_model_id" placeholder="请选择车型">
            <el-option v-for="v in vehicleModels" :key="v.id" :label="v.name" :value="v.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="配置名称" prop="config_name">
          <el-input v-model="formData.config_name" placeholder="请输入配置名称" />
        </el-form-item>
        <el-form-item label="配置编码" prop="config_code">
          <el-input v-model="formData.config_code" placeholder="请输入配置编码" />
        </el-form-item>
        <el-form-item label="软件编码">
          <el-input v-model="formData.software_code" placeholder="请输入软件编码" />
        </el-form-item>
        <el-form-item label="详情描述">
          <el-input v-model="formData.description" type="textarea" :rows="4" placeholder="请输入详情描述" />
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
import { vehicleConfigApi, vehicleModelApi } from '@/api'
import { exportToExcel, statusMap } from '@/utils/export'

const tableData = ref([])
const vehicleModels = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const editingId = ref(null)

const searchParams = reactive({
  page: 1,
  per_page: 20,
  vehicle_model_id: ''
})

const formData = reactive({
  vehicle_model_id: '',
  config_name: '',
  config_code: '',
  software_code: '',
  description: '',
  status: 'active',
  remark: ''
})

const formRules = {
  vehicle_model_id: [{ required: true, message: '请选择车型', trigger: 'change' }],
  config_name: [{ required: true, message: '请输入配置名称', trigger: 'blur' }],
  config_code: [{ required: true, message: '请输入配置编码', trigger: 'blur' }]
}

const loadVehicleModels = async () => {
  try {
    const res = await vehicleModelApi.getList({ per_page: 100 })
    vehicleModels.value = res.items
  } catch (error) {
    console.error('加载车型失败:', error)
  }
}

const loadData = async () => {
  try {
    const res = await vehicleConfigApi.getList(searchParams)
    tableData.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const resetSearch = () => {
  searchParams.vehicle_model_id = ''
  searchParams.page = 1
  loadData()
}

const handleAdd = () => {
  dialogTitle.value = '新增配置'
  editingId.value = null
  Object.assign(formData, {
    vehicle_model_id: '', config_name: '', config_code: '', software_code: '',
    description: '', status: 'active', remark: ''
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑配置'
  editingId.value = row.id
  Object.assign(formData, {
    vehicle_model_id: row.vehicle_model_id,
    config_name: row.config_name,
    config_code: row.config_code,
    software_code: row.software_code,
    description: row.description,
    status: row.status,
    remark: row.remark
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await vehicleConfigApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await vehicleConfigApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该配置吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await vehicleConfigApi.delete(row.id)
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
    { prop: 'vehicle_model_name', label: '车型', width: 15 },
    { prop: 'config_name', label: '配置名称', width: 20 },
    { prop: 'config_code', label: '配置编码', width: 15 },
    { prop: 'software_code', label: '软件编码', width: 20 },
    { prop: 'description', label: '详情', width: 30 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val }
  ]
  exportToExcel(tableData.value, columns, '车辆配置列表')
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadVehicleModels()
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
