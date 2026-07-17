<template>
  <div class="speaker-mapping-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>扬声器通道映射</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>新增映射
          </el-button>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="车辆配置">
          <el-select v-model="searchParams.vehicle_config_id" placeholder="全部" clearable>
            <el-option v-for="c in configs" :key="c.id" :label="c.config_name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="speaker_name" label="喇叭名称" width="120" />
        <el-table-column prop="speaker_position" label="喇叭位置" />
        <el-table-column prop="channel_type" label="通道类型" width="100" />
        <el-table-column prop="channel_number" label="通道号" width="80" />
        <el-table-column prop="channel_name" label="通道名称" />
        <el-table-column prop="power" label="功率(W)" width="100" />
        <el-table-column prop="impedance" label="阻抗(Ω)" width="100" />
        <el-table-column prop="can_signal_name" label="CAN信号" />
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
        <el-form-item label="车辆配置" prop="vehicle_config_id">
          <el-select v-model="formData.vehicle_config_id" placeholder="请选择配置">
            <el-option v-for="c in configs" :key="c.id" :label="c.config_name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="喇叭名称" prop="speaker_name">
              <el-input v-model="formData.speaker_name" placeholder="如: 左前高音" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="喇叭位置">
              <el-input v-model="formData.speaker_position" placeholder="如: FL-Tweeter" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="通道类型">
              <el-select v-model="formData.channel_type" placeholder="请选择">
                <el-option label="模拟" value="analog" />
                <el-option label="数字" value="digital" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="通道号" prop="channel_number">
              <el-input-number v-model="formData.channel_number" :min="0" :max="31" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="通道名称">
              <el-input v-model="formData.channel_name" placeholder="如: CH0" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="功率(W)">
              <el-input-number v-model="formData.power" :min="0" :max="500" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="阻抗(Ω)">
              <el-input-number v-model="formData.impedance" :min="0" :max="32" />
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
        <el-form-item label="CAN信号">
          <el-input v-model="formData.can_signal_name" placeholder="请输入CAN信号名称" />
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
import { speakerMappingApi, vehicleConfigApi } from '@/api'

const tableData = ref([])
const configs = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const editingId = ref(null)

const searchParams = reactive({
  page: 1,
  per_page: 20,
  vehicle_config_id: ''
})

const formData = reactive({
  vehicle_config_id: '',
  speaker_name: '',
  speaker_position: '',
  channel_type: 'analog',
  channel_number: 0,
  channel_name: '',
  power: 50,
  impedance: 4,
  can_signal_name: '',
  status: 'active'
})

const formRules = {
  vehicle_config_id: [{ required: true, message: '请选择车辆配置', trigger: 'change' }],
  speaker_name: [{ required: true, message: '请输入喇叭名称', trigger: 'blur' }],
  channel_number: [{ required: true, message: '请输入通道号', trigger: 'blur' }]
}

const loadConfigs = async () => {
  try {
    const res = await vehicleConfigApi.getList({ per_page: 100 })
    configs.value = res.items
  } catch (error) {
    console.error('加载配置失败:', error)
  }
}

const loadData = async () => {
  try {
    const res = await speakerMappingApi.getList(searchParams)
    tableData.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const resetSearch = () => {
  searchParams.vehicle_config_id = ''
  searchParams.page = 1
  loadData()
}

const handleAdd = () => {
  dialogTitle.value = '新增扬声器映射'
  editingId.value = null
  Object.assign(formData, {
    vehicle_config_id: searchParams.vehicle_config_id || '', speaker_name: '',
    speaker_position: '', channel_type: 'analog', channel_number: 0,
    channel_name: '', power: 50, impedance: 4,
    can_signal_name: '', status: 'active'
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑扬声器映射'
  editingId.value = row.id
  Object.assign(formData, {
    vehicle_config_id: row.vehicle_config_id,
    speaker_name: row.speaker_name,
    speaker_position: row.speaker_position,
    channel_type: row.channel_type,
    channel_number: row.channel_number,
    channel_name: row.channel_name,
    power: row.power,
    impedance: row.impedance,
    can_signal_name: row.can_signal_name,
    status: row.status
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await speakerMappingApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await speakerMappingApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该映射吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await speakerMappingApi.delete(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

onMounted(() => {
  loadConfigs()
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
