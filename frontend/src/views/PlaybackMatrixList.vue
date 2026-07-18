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
        <el-form-item label="关键词">
          <el-input v-model="searchParams.keyword" placeholder="矩阵名称" clearable @keyup.enter="loadData" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="matrix_name" label="矩阵名称" />
        <el-table-column prop="vehicle_config_name" label="车辆配置" />
        <el-table-column prop="entry_count" label="条目数" width="80" />
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">
              {{ row.status === 'active' ? '启用' : '停用' }}
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

    <!-- 新增/编辑对话框 -->
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
            <el-form-item label="版本">
              <el-input v-model="formData.version" placeholder="如: 1.0" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-radio-group v-model="formData.status">
                <el-radio value="active">启用</el-radio>
                <el-radio value="inactive">停用</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="播放矩阵详情" width="95%">
      <div style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <strong>{{ detailData.matrix_name }}</strong>
          <span style="margin-left: 10px; color: #909399;">{{ detailData.vehicle_config_name }}</span>
        </div>
        <div>
          <el-button type="success" size="small" @click="handleImportExcel">
            <el-icon><Upload /></el-icon>导入Excel
          </el-button>
          <el-button type="primary" size="small" @click="handleAddEntry">
            <el-icon><Plus /></el-icon>新增条目
          </el-button>
        </div>
      </div>

      <el-table :data="detailData.entries || []" border style="width: 100%" max-height="500">
        <el-table-column prop="audio_source" label="音源类型" width="120" fixed />
        <el-table-column prop="a2b_channel" label="A2B通道" width="120" />
        <el-table-column prop="playback_position" label="播出方位" width="150" show-overflow-tooltip />
        <el-table-column prop="headrest_mode" label="头枕模式" width="100" />
        <!-- 扬声器通道列 -->
        <el-table-column v-for="speaker in speakerColumns" :key="speaker.key" :label="speaker.label" width="80" align="center">
          <template #default="{ row }">
            <span :class="{ 'channel-on': row.speaker_channels?.[speaker.key] === '●' }">
              {{ row.speaker_channels?.[speaker.key] || '-' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEditEntry(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDeleteEntry(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 条目编辑对话框 -->
    <el-dialog v-model="entryDialogVisible" :title="entryDialogTitle" width="800px">
      <el-form ref="entryFormRef" :model="entryFormData" :rules="entryFormRules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="音源类型" prop="audio_source">
              <el-input v-model="entryFormData.audio_source" placeholder="如: 媒体立体声" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="A2B通道">
              <el-input v-model="entryFormData.a2b_channel" placeholder="如: SLOT 1-SLOT 2" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="播出方位">
              <el-input v-model="entryFormData.playback_position" placeholder="如: 全车" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="头枕模式">
              <el-select v-model="entryFormData.headrest_mode" placeholder="请选择" clearable>
                <el-option label="关闭" value="关闭" />
                <el-option label="头枕环绕" value="头枕环绕" />
                <el-option label="驾享模式" value="驾享模式" />
                <el-option label="独享模式" value="独享模式" />
                <el-option label="不判断头枕模式" value="不判断头枕模式" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider>扬声器通道配置</el-divider>
        <div class="speaker-grid">
          <div v-for="speaker in speakerColumns" :key="speaker.key" class="speaker-item">
            <el-checkbox
              v-model="speakerSelections[speaker.key]"
              :label="speaker.label"
            />
          </div>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="entryDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleEntrySubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { playbackMatrixApi, vehicleConfigApi } from '@/api'
import { exportToExcel, statusMap } from '@/utils/export'

// 扬声器列定义
const speakerColumns = [
  { key: '左前低音', label: '左前低音' },
  { key: '左前中音', label: '左前中音' },
  { key: '左前高音', label: '左前高音' },
  { key: '中置', label: '中置' },
  { key: '右前低音', label: '右前低音' },
  { key: '右前中音', label: '右前中音' },
  { key: '右前高音', label: '右前高音' },
  { key: '左后低音', label: '左后低音' },
  { key: '左后高音', label: '左后高音' },
  { key: '右后低音', label: '右后低音' },
  { key: '右后高音', label: '右后高音' },
  { key: '重低音', label: '重低音' },
  { key: '左环绕', label: '左环绕' },
  { key: '右环绕', label: '右环绕' },
  { key: '左前顶棚', label: '左前顶棚' },
  { key: '右前顶棚', label: '右前顶棚' },
  { key: '左后顶棚', label: '左后顶棚' },
  { key: '右后顶棚', label: '右后顶棚' },
  { key: '主驾头枕左', label: '主驾头枕左' },
  { key: '主驾头枕右', label: '主驾头枕右' },
  { key: 'AVAS', label: 'AVAS' }
]

const tableData = ref([])
const configs = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const entryDialogVisible = ref(false)
const dialogTitle = ref('')
const entryDialogTitle = ref('')
const formRef = ref(null)
const entryFormRef = ref(null)
const editingId = ref(null)
const entryEditingId = ref(null)
const currentMatrixId = ref(null)
const detailData = ref({ entries: [] })

// 扬声器选择状态
const speakerSelections = reactive({})

const searchParams = reactive({
  page: 1,
  per_page: 20,
  vehicle_config_id: '',
  keyword: ''
})

const formData = reactive({
  vehicle_config_id: '',
  matrix_name: '',
  description: '',
  version: '1.0',
  status: 'active'
})

const entryFormData = reactive({
  audio_source: '',
  a2b_channel: '',
  playback_position: '',
  headrest_mode: ''
})

const formRules = {
  vehicle_config_id: [{ required: true, message: '请选择车辆配置', trigger: 'change' }],
  matrix_name: [{ required: true, message: '请输入矩阵名称', trigger: 'blur' }]
}

const entryFormRules = {
  audio_source: [{ required: true, message: '请输入音源类型', trigger: 'blur' }]
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
    const res = await playbackMatrixApi.getList(searchParams)
    tableData.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const resetSearch = () => {
  searchParams.vehicle_config_id = ''
  searchParams.keyword = ''
  searchParams.page = 1
  loadData()
}

const handleAdd = () => {
  dialogTitle.value = '新增播放矩阵'
  editingId.value = null
  Object.assign(formData, {
    vehicle_config_id: searchParams.vehicle_config_id || '',
    matrix_name: '', description: '', version: '1.0', status: 'active'
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑播放矩阵'
  editingId.value = row.id
  Object.assign(formData, {
    vehicle_config_id: row.vehicle_config_id,
    matrix_name: row.matrix_name,
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
    detailVisible.value = true
  } catch (error) {
    console.error('获取详情失败:', error)
  }
}

const handleAddEntry = () => {
  entryDialogTitle.value = '新增条目'
  entryEditingId.value = null
  Object.assign(entryFormData, {
    audio_source: '', a2b_channel: '', playback_position: '', headrest_mode: ''
  })
  // 重置扬声器选择
  speakerColumns.forEach(s => {
    speakerSelections[s.key] = false
  })
  entryDialogVisible.value = true
}

const handleEditEntry = (row) => {
  entryDialogTitle.value = '编辑条目'
  entryEditingId.value = row.id
  Object.assign(entryFormData, {
    audio_source: row.audio_source,
    a2b_channel: row.a2b_channel,
    playback_position: row.playback_position,
    headrest_mode: row.headrest_mode
  })
  // 设置扬声器选择
  speakerColumns.forEach(s => {
    speakerSelections[s.key] = row.speaker_channels?.[s.key] === '●'
  })
  entryDialogVisible.value = true
}

const handleDeleteEntry = (row) => {
  ElMessageBox.confirm('确定要删除该条目吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await playbackMatrixApi.deleteEntry(row.id)
      ElMessage.success('删除成功')
      detailData.value = await playbackMatrixApi.getDetail(currentMatrixId.value)
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const handleEntrySubmit = async () => {
  try {
    await entryFormRef.value.validate()

    // 构建扬声器通道配置
    const speaker_channels = {}
    speakerColumns.forEach(s => {
      if (speakerSelections[s.key]) {
        speaker_channels[s.key] = '●'
      }
    })

    const submitData = {
      ...entryFormData,
      matrix_id: currentMatrixId.value,
      speaker_channels
    }

    if (entryEditingId.value) {
      await playbackMatrixApi.updateEntry(entryEditingId.value, submitData)
      ElMessage.success('更新成功')
    } else {
      await playbackMatrixApi.createEntry(submitData)
      ElMessage.success('创建成功')
    }
    entryDialogVisible.value = false
    detailData.value = await playbackMatrixApi.getDetail(currentMatrixId.value)
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleImportExcel = () => {
  ElMessage.info('Excel导入功能开发中')
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
    { prop: 'entry_count', label: '条目数', width: 10 },
    { prop: 'version', label: '版本', width: 10 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val }
  ]
  exportToExcel(tableData.value, columns, '播放矩阵列表')
  ElMessage.success('导出成功')
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

.speaker-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.speaker-item {
  min-width: 120px;
}

.channel-on {
  color: #67c23a;
  font-weight: bold;
}
</style>
