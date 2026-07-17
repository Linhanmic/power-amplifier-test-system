<template>
  <div class="test-case-list">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="group-card">
          <template #header>
            <div class="card-header">
              <span>用例分组</span>
              <el-button type="primary" link @click="handleAddGroup">
                <el-icon><Plus /></el-icon>
              </el-button>
            </div>
          </template>
          <el-tree
            :data="groupTree"
            :props="{ label: 'label', children: 'children' }"
            node-key="id"
            highlight-current
            @node-click="handleGroupClick"
          />
        </el-card>
      </el-col>
      <el-col :span="18">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>测试用例</span>
              <el-button type="primary" @click="handleAdd">
                <el-icon><Plus /></el-icon>新增用例
              </el-button>
            </div>
          </template>

          <el-form :inline="true" class="search-form">
            <el-form-item label="关键词">
              <el-input v-model="searchParams.keyword" placeholder="用例编号/标题" clearable @keyup.enter="loadData" />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchParams.status" placeholder="全部" clearable>
                <el-option label="草稿" value="draft" />
                <el-option label="就绪" value="ready" />
                <el-option label="已废弃" value="deprecated" />
              </el-select>
            </el-form-item>
            <el-form-item label="优先级">
              <el-select v-model="searchParams.level" placeholder="全部" clearable>
                <el-option label="P0" value="P0" />
                <el-option label="P1" value="P1" />
                <el-option label="P2" value="P2" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadData">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>

          <el-table :data="tableData" border style="width: 100%">
            <el-table-column prop="case_code" label="用例编号" width="120" />
            <el-table-column prop="title" label="用例标题" show-overflow-tooltip />
            <el-table-column prop="group_name" label="所属分组" width="120" />
            <el-table-column prop="level" label="优先级" width="80">
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.level)" size="small">{{ row.level }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="requirement_code" label="关联需求" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
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
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用例编号" prop="case_code">
              <el-input v-model="formData.case_code" placeholder="请输入用例编号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属分组" prop="group_id">
              <el-tree-select
                v-model="formData.group_id"
                :data="groupTree"
                :props="{ label: 'label', value: 'id', children: 'children' }"
                placeholder="请选择分组"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="用例标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入用例标题" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="优先级">
              <el-select v-model="formData.level" placeholder="请选择优先级">
                <el-option label="P0" value="P0" />
                <el-option label="P1" value="P1" />
                <el-option label="P2" value="P2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-select v-model="formData.status" placeholder="请选择状态">
                <el-option label="草稿" value="draft" />
                <el-option label="就绪" value="ready" />
                <el-option label="已废弃" value="deprecated" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="前置条件">
          <el-input v-model="formData.preconditions" type="textarea" :rows="2" placeholder="请输入前置条件" />
        </el-form-item>
        <el-form-item label="测试步骤" prop="test_steps">
          <el-input v-model="formData.test_steps" type="textarea" :rows="4" placeholder="请输入测试步骤" />
        </el-form-item>
        <el-form-item label="预期结果" prop="expected_results">
          <el-input v-model="formData.expected_results" type="textarea" :rows="4" placeholder="请输入预期结果" />
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
import { testCaseApi, testCaseGroupApi, statsApi } from '@/api'

const tableData = ref([])
const groupTree = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const editingId = ref(null)

const searchParams = reactive({
  page: 1,
  per_page: 20,
  group_id: '',
  keyword: '',
  status: '',
  level: ''
})

const formData = reactive({
  case_code: '',
  group_id: '',
  title: '',
  description: '',
  preconditions: '',
  test_steps: '',
  expected_results: '',
  level: 'P1',
  status: 'draft'
})

const formRules = {
  case_code: [{ required: true, message: '请输入用例编号', trigger: 'blur' }],
  group_id: [{ required: true, message: '请选择分组', trigger: 'change' }],
  title: [{ required: true, message: '请输入用例标题', trigger: 'blur' }],
  test_steps: [{ required: true, message: '请输入测试步骤', trigger: 'blur' }],
  expected_results: [{ required: true, message: '请输入预期结果', trigger: 'blur' }]
}

const getPriorityType = (priority) => {
  const map = { P0: 'danger', P1: 'warning', P2: 'success' }
  return map[priority] || 'info'
}

const getStatusType = (status) => {
  const map = { draft: 'info', ready: 'success', deprecated: 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { draft: '草稿', ready: '就绪', deprecated: '已废弃' }
  return map[status] || status
}

const loadGroupTree = async () => {
  try {
    groupTree.value = await statsApi.getTree('test-case-groups')
  } catch (error) {
    console.error('加载分组树失败:', error)
  }
}

const loadData = async () => {
  try {
    const res = await testCaseApi.getList(searchParams)
    tableData.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const handleGroupClick = (data) => {
  searchParams.group_id = data.id
  loadData()
}

const resetSearch = () => {
  searchParams.keyword = ''
  searchParams.status = ''
  searchParams.level = ''
  searchParams.group_id = ''
  searchParams.page = 1
  loadData()
}

const handleAddGroup = () => {
  ElMessage.info('新增分组功能开发中')
}

const handleAdd = () => {
  dialogTitle.value = '新增测试用例'
  editingId.value = null
  Object.assign(formData, {
    case_code: '', group_id: searchParams.group_id || '', title: '',
    description: '', preconditions: '', test_steps: '',
    expected_results: '', level: 'P1', status: 'draft'
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑测试用例'
  editingId.value = row.id
  Object.assign(formData, {
    case_code: row.case_code,
    group_id: row.group_id,
    title: row.title,
    description: row.description,
    preconditions: row.preconditions,
    test_steps: row.test_steps,
    expected_results: row.expected_results,
    level: row.level,
    status: row.status
  })
  dialogVisible.value = true
}

const handleDetail = (row) => {
  ElMessage.info('详情功能开发中')
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await testCaseApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await testCaseApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该测试用例吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await testCaseApi.delete(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

onMounted(() => {
  loadGroupTree()
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

.group-card {
  height: calc(100vh - 200px);
  overflow-y: auto;
}
</style>
