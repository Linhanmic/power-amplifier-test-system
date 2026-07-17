<template>
  <div class="config-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>车辆配置管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>新增配置
          </el-button>
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
        <el-table-column prop="speaker_count" label="扬声器数" width="100" />
        <el-table-column prop="has_subwoofer" label="低音炮" width="80">
          <template #default="{ row }">
            <el-tag :type="row.has_subwoofer ? 'success' : 'info'" size="small">
              {{ row.has_subwoofer ? '有' : '无' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="has_dsp" label="DSP" width="80">
          <template #default="{ row }">
            <el-tag :type="row.has_dsp ? 'success' : 'info'" size="small">
              {{ row.has_dsp ? '有' : '无' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amplifier_power" label="功放功率(W)" width="120" />
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
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="扬声器数量">
              <el-input-number v-model="formData.speaker_count" :min="0" :max="32" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="功放功率(W)">
              <el-input-number v-model="formData.amplifier_power" :min="0" :max="2000" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="低音炮">
              <el-switch v-model="formData.has_subwoofer" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="DSP">
              <el-switch v-model="formData.has_dsp" />
            </el-form-item>
          </el-col>
        </el-row>
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
  speaker_count: 8,
  has_subwoofer: false,
  has_dsp: false,
  amplifier_power: 400,
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
    vehicle_model_id: '', config_name: '', config_code: '',
    speaker_count: 8, has_subwoofer: false, has_dsp: false,
    amplifier_power: 400, status: 'active', remark: ''
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
    speaker_count: row.speaker_count,
    has_subwoofer: row.has_subwoofer,
    has_dsp: row.has_dsp,
    amplifier_power: row.amplifier_power,
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
