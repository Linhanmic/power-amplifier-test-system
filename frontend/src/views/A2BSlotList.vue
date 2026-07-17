<template>
  <div class="a2b-slot-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>A2B Slot管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>新增Slot
          </el-button>
        </div>
      </template>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="slot_name" label="Slot名称" />
        <el-table-column prop="slot_number" label="Slot编号" width="100" />
        <el-table-column prop="slot_type" label="类型" width="100" />
        <el-table-column prop="max_channels" label="最大通道数" width="120" />
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
        <el-form-item label="Slot名称" prop="slot_name">
          <el-input v-model="formData.slot_name" placeholder="如: Slot 0" />
        </el-form-item>
        <el-form-item label="Slot编号" prop="slot_number">
          <el-input-number v-model="formData.slot_number" :min="0" :max="15" />
        </el-form-item>
        <el-form-item label="Slot类型">
          <el-select v-model="formData.slot_type" placeholder="请选择类型">
            <el-option label="I2S" value="I2S" />
            <el-option label="TDM" value="TDM" />
          </el-select>
        </el-form-item>
        <el-form-item label="最大通道数">
          <el-input-number v-model="formData.max_channels" :min="1" :max="32" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="2" placeholder="请输入描述" />
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
import { a2bSlotApi } from '@/api'

const tableData = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const editingId = ref(null)

const formData = reactive({
  slot_name: '',
  slot_number: 0,
  slot_type: 'I2S',
  max_channels: 8,
  description: '',
  status: 'active'
})

const formRules = {
  slot_name: [{ required: true, message: '请输入Slot名称', trigger: 'blur' }],
  slot_number: [{ required: true, message: '请输入Slot编号', trigger: 'blur' }]
}

const loadData = async () => {
  try {
    tableData.value = await a2bSlotApi.getList()
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增A2B Slot'
  editingId.value = null
  Object.assign(formData, {
    slot_name: '', slot_number: 0, slot_type: 'I2S',
    max_channels: 8, description: '', status: 'active'
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑A2B Slot'
  editingId.value = row.id
  Object.assign(formData, {
    slot_name: row.slot_name,
    slot_number: row.slot_number,
    slot_type: row.slot_type,
    max_channels: row.max_channels,
    description: row.description,
    status: row.status
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await a2bSlotApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await a2bSlotApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该Slot吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await a2bSlotApi.delete(row.id)
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
</style>
