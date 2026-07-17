<template>
  <div class="playback-matrix-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>播放矩阵管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>新增矩阵
          </el-button>
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
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="条件矩阵" name="condition">
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
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { playbackMatrixApi, vehicleConfigApi } from '@/api'

const tableData = ref([])
const configs = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const editingId = ref(null)
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

const formRules = {
  vehicle_config_id: [{ required: true, message: '请选择车辆配置', trigger: 'change' }],
  matrix_name: [{ required: true, message: '请输入矩阵名称', trigger: 'blur' }]
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
    activeTab.value = 'base'
    detailVisible.value = true
  } catch (error) {
    console.error('获取详情失败:', error)
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
