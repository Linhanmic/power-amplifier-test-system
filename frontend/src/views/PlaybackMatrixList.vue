<template>
  <div class="playback-matrix-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>播放矩阵管理</span>
          <div>
            <el-button type="success" @click="handleExport">
              <el-icon><Download /></el-icon>导出Excel
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>新增矩阵
            </el-button>
          </div>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="车辆配置">
          <el-select v-model="searchParams.vehicle_config_id" placeholder="全部" clearable>
            <el-option v-for="c in configs" :key="c.id" :label="c.config_name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="searchParams.matrix_type" placeholder="全部" clearable>
            <el-option label="基础矩阵" value="base" />
            <el-option label="条件矩阵" value="condition" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="matrix_name" label="矩阵名称" />
        <el-table-column prop="vehicle_config_name" label="车辆配置" />
        <el-table-column prop="matrix_type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.matrix_type === 'base' ? 'success' : 'warning'" size="small">
              {{ row.matrix_type === 'base' ? '基础' : '条件' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="base_count" label="基础条目" width="100" />
        <el-table-column prop="condition_count" label="条件数" width="100" />
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">
              {{ row.status === 'active' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="车辆配置" prop="vehicle_config_id">
          <el-select v-model="formData.vehicle_config_id" placeholder="请选择配置">
            <el-option v-for="c in configs" :key="c.id" :label="c.config_name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="矩阵名称" prop="matrix_name">
          <el-input v-model="formData.matrix_name" placeholder="请输入矩阵名称" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="矩阵类型">
              <el-select v-model="formData.matrix_type" placeholder="请选择类型">
                <el-option label="基础矩阵" value="base" />
                <el-option label="条件矩阵" value="condition" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版本">
              <el-input v-model="formData.version" placeholder="如: 1.0" />
            </el-form-item>
          </el-col>
        </el-row>
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

    <el-dialog v-model="detailVisible" title="播放矩阵详情" width="900px">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基础矩阵" name="base">
          <div style="margin-bottom: 10px; text-align: right;">
            <el-button type="primary" size="small" @click="handleAddBaseEntry">
              <el-icon><Plus /></el-icon>新增条目
            </el-button>
          </div>
          <el-table :data="detailData.base_entries" border style="width: 100%">
            <el-table-column prop="slot_name" label="Slot" />
            <el-table-column prop="audio_source_name" label="音源" />
            <el-table-column prop="is_enabled" label="启用" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_enabled ? 'success' : 'info'" size="small">
                  {{ row.is_enabled ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="channel_count" label="通道数" width="80" />
            <el-table-column prop="volume_level" label="音量" width="80" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditBaseEntry(row)">编辑</el-button>
                <el-button type="danger" link size="small" @click="handleDeleteBaseEntry(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="条件矩阵" name="condition">
          <div style="margin-bottom: 10px; text-align: right;">
            <el-button type="primary" size="small" @click="handleAddCondition">
              <el-icon><Plus /></el-icon>新增条件
            </el-button>
          </div>
          <el-table :data="detailData.conditions" border style="width: 100%">
            <el-table-column prop="condition_name" label="条件名称" />
            <el-table-column prop="condition_type" label="类型" width="100" />
            <el-table-column prop="description" label="描述" show-overflow-tooltip />
            <el-table-column prop="is_active" label="激活" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
                  {{ row.is_active ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditCondition(row)">编辑</el-button>
                <el-button type="danger" link size="small" @click="handleDeleteCondition(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>

    <!-- 基础矩阵条目对话框 -->
    <el-dialog v-model="baseEntryVisible" :title="baseEntryDialogTitle" width="500px">
      <el-form ref="baseEntryFormRef" :model="baseEntryFormData" :rules="baseEntryFormRules" label-width="100px">
        <el-form-item label="Slot" prop="slot_id">
          <el-select v-model="baseEntryFormData.slot_id" placeholder="请选择Slot">
            <el-option v-for="s in slots" :key="s.id" :label="s.slot_name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="音源" prop="audio_source_id">
          <el-select v-model="baseEntryFormData.audio_source_id" placeholder="请选择音源">
            <el-option v-for="a in audioSources" :key="a.id" :label="a.source_name" :value="a.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="baseEntryFormData.is_enabled" />
        </el-form-item>
        <el-form-item label="通道数">
          <el-input-number v-model="baseEntryFormData.channel_count" :min="1" :max="16" />
        </el-form-item>
        <el-form-item label="音量">
          <el-slider v-model="baseEntryFormData.volume_level" :max="100" show-input />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="baseEntryVisible = false">取消</el-button>
        <el-button type="primary" @click="handleBaseEntrySubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 条件矩阵对话框 -->
    <el-dialog v-model="conditionVisible" :title="conditionDialogTitle" width="600px">
      <el-form ref="conditionFormRef" :model="conditionFormData" :rules="conditionFormRules" label-width="100px">
        <el-form-item label="条件名称" prop="condition_name">
          <el-input v-model="conditionFormData.condition_name" placeholder="请输入条件名称" />
        </el-form-item>
        <el-form-item label="条件类型">
          <el-select v-model="conditionFormData.condition_type" placeholder="请选择类型">
            <el-option label="音源切换" value="source" />
            <el-option label="优先级" value="priority" />
            <el-option label="场景" value="scenario" />
          </el-select>
        </el-form-item>
        <el-form-item label="条件值(JSON)">
          <el-input v-model="conditionFormData.condition_value_str" type="textarea" :rows="3" placeholder='{"source": "BT_MUSIC"}' />
        </el-form-item>
        <el-form-item label="播放配置(JSON)" prop="playback_config_str">
          <el-input v-model="conditionFormData.playback_config_str" type="textarea" :rows="5" placeholder='{"slot_0": {"enabled": true, "volume": 50}}' />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="conditionFormData.description" type="textarea" :rows="2" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="激活">
          <el-switch v-model="conditionFormData.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="conditionVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConditionSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { playbackMatrixApi, vehicleConfigApi, a2bSlotApi, audioSourceTypeApi } from '@/api'
import { exportToExcel, statusMap } from '@/utils/export'

const tableData = ref([])
const configs = ref([])
const slots = ref([])
const audioSources = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const baseEntryVisible = ref(false)
const conditionVisible = ref(false)
const dialogTitle = ref('')
const baseEntryDialogTitle = ref('')
const conditionDialogTitle = ref('')
const formRef = ref(null)
const baseEntryFormRef = ref(null)
const conditionFormRef = ref(null)
const editingId = ref(null)
const baseEntryEditingId = ref(null)
const conditionEditingId = ref(null)
const currentMatrixId = ref(null)
const activeTab = ref('base')
const detailData = ref({ base_entries: [], conditions: [] })

const searchParams = reactive({
  page: 1,
  per_page: 20,
  vehicle_config_id: '',
  matrix_type: ''
})

const formData = reactive({
  vehicle_config_id: '',
  matrix_name: '',
  matrix_type: 'base',
  description: '',
  version: '1.0',
  status: 'active'
})

const baseEntryFormData = reactive({
  matrix_id: '',
  slot_id: '',
  audio_source_id: '',
  is_enabled: true,
  channel_count: 2,
  volume_level: 50
})

const conditionFormData = reactive({
  matrix_id: '',
  condition_name: '',
  condition_type: '',
  condition_value_str: '',
  playback_config_str: '',
  description: '',
  is_active: true
})

const formRules = {
  vehicle_config_id: [{ required: true, message: '请选择车辆配置', trigger: 'change' }],
  matrix_name: [{ required: true, message: '请输入矩阵名称', trigger: 'blur' }]
}

const baseEntryFormRules = {
  slot_id: [{ required: true, message: '请选择Slot', trigger: 'change' }],
  audio_source_id: [{ required: true, message: '请选择音源', trigger: 'change' }]
}

const conditionFormRules = {
  condition_name: [{ required: true, message: '请输入条件名称', trigger: 'blur' }],
  playback_config_str: [{ required: true, message: '请输入播放配置', trigger: 'blur' }]
}

const loadConfigs = async () => {
  try {
    const res = await vehicleConfigApi.getList({ per_page: 100 })
    configs.value = res.items
  } catch (error) {
    console.error('加载配置失败:', error)
  }
}

const loadSlots = async () => {
  try {
    slots.value = await a2bSlotApi.getList()
  } catch (error) {
    console.error('加载Slots失败:', error)
  }
}

const loadAudioSources = async () => {
  try {
    audioSources.value = await audioSourceTypeApi.getList()
  } catch (error) {
    console.error('加载音源失败:', error)
  }
}

const loadData = async () => {
  try {
    const res = await playbackMatrixApi.getList(searchParams)
    tableData.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const resetSearch = () => {
  searchParams.vehicle_config_id = ''
  searchParams.matrix_type = ''
  searchParams.page = 1
  loadData()
}

const handleAdd = () => {
  dialogTitle.value = '新增播放矩阵'
  editingId.value = null
  Object.assign(formData, {
    vehicle_config_id: searchParams.vehicle_config_id || '', matrix_name: '',
    matrix_type: 'base', description: '', version: '1.0', status: 'active'
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑播放矩阵'
  editingId.value = row.id
  Object.assign(formData, {
    vehicle_config_id: row.vehicle_config_id,
    matrix_name: row.matrix_name,
    matrix_type: row.matrix_type,
    description: row.description,
    version: row.version,
    status: row.status
  })
  dialogVisible.value = true
}

const handleDetail = async (row) => {
  try {
    detailData.value = await playbackMatrixApi.getDetail(row.id)
    currentMatrixId.value = row.id
    activeTab.value = 'base'
    detailVisible.value = true
  } catch (error) {
    console.error('获取详情失败:', error)
  }
}

const handleAddBaseEntry = () => {
  baseEntryDialogTitle.value = '新增基础矩阵条目'
  baseEntryEditingId.value = null
  Object.assign(baseEntryFormData, {
    matrix_id: currentMatrixId.value, slot_id: '', audio_source_id: '',
    is_enabled: true, channel_count: 2, volume_level: 50
  })
  baseEntryVisible.value = true
}

const handleEditBaseEntry = (row) => {
  baseEntryDialogTitle.value = '编辑基础矩阵条目'
  baseEntryEditingId.value = row.id
  Object.assign(baseEntryFormData, {
    matrix_id: currentMatrixId.value, slot_id: row.slot_id,
    audio_source_id: row.audio_source_id, is_enabled: row.is_enabled,
    channel_count: row.channel_count, volume_level: row.volume_level
  })
  baseEntryVisible.value = true
}

const handleDeleteBaseEntry = (row) => {
  ElMessageBox.confirm('确定要删除该条目吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await playbackMatrixApi.deleteBaseEntry(row.id)
      ElMessage.success('删除成功')
      detailData.value = await playbackMatrixApi.getDetail(currentMatrixId.value)
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const handleBaseEntrySubmit = async () => {
  try {
    await baseEntryFormRef.value.validate()
    if (baseEntryEditingId.value) {
      await playbackMatrixApi.updateBaseEntry(baseEntryEditingId.value, baseEntryFormData)
      ElMessage.success('更新成功')
    } else {
      await playbackMatrixApi.addBaseEntry(baseEntryFormData)
      ElMessage.success('创建成功')
    }
    baseEntryVisible.value = false
    detailData.value = await playbackMatrixApi.getDetail(currentMatrixId.value)
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleAddCondition = () => {
  conditionDialogTitle.value = '新增条件矩阵'
  conditionEditingId.value = null
  Object.assign(conditionFormData, {
    matrix_id: currentMatrixId.value, condition_name: '', condition_type: '',
    condition_value_str: '{}', playback_config_str: '', description: '', is_active: true
  })
  conditionVisible.value = true
}

const handleEditCondition = (row) => {
  conditionDialogTitle.value = '编辑条件矩阵'
  conditionEditingId.value = row.id
  Object.assign(conditionFormData, {
    matrix_id: currentMatrixId.value, condition_name: row.condition_name,
    condition_type: row.condition_type,
    condition_value_str: JSON.stringify(row.condition_value || {}, null, 2),
    playback_config_str: JSON.stringify(row.playback_config || {}, null, 2),
    description: row.description, is_active: row.is_active
  })
  conditionVisible.value = true
}

const handleDeleteCondition = (row) => {
  ElMessageBox.confirm('确定要删除该条件吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await playbackMatrixApi.deleteCondition(row.id)
      ElMessage.success('删除成功')
      detailData.value = await playbackMatrixApi.getDetail(currentMatrixId.value)
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const handleConditionSubmit = async () => {
  try {
    await conditionFormRef.value.validate()
    const submitData = {
      ...conditionFormData,
      condition_value: JSON.parse(conditionFormData.condition_value_str),
      playback_config: JSON.parse(conditionFormData.playback_config_str)
    }
    if (conditionEditingId.value) {
      await playbackMatrixApi.updateCondition(conditionEditingId.value, submitData)
      ElMessage.success('更新成功')
    } else {
      await playbackMatrixApi.addCondition(submitData)
      ElMessage.success('创建成功')
    }
    conditionVisible.value = false
    detailData.value = await playbackMatrixApi.getDetail(currentMatrixId.value)
  } catch (error) {
    if (error instanceof SyntaxError) {
      ElMessage.error('JSON格式错误')
    } else {
      console.error('提交失败:', error)
    }
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await playbackMatrixApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await playbackMatrixApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该播放矩阵吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await playbackMatrixApi.delete(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const handleExport = () => {
  const columns = [
    { prop: 'matrix_name', label: '矩阵名称', width: 25 },
    { prop: 'vehicle_config_name', label: '车辆配置', width: 20 },
    { prop: 'matrix_type', label: '类型', width: 10, formatter: (val) => val === 'base' ? '基础' : '条件' },
    { prop: 'base_count', label: '基础条目', width: 10 },
    { prop: 'condition_count', label: '条件数', width: 10 },
    { prop: 'version', label: '版本', width: 10 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val }
  ]
  exportToExcel(tableData.value, columns, '播放矩阵列表')
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadConfigs()
  loadSlots()
  loadAudioSources()
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
