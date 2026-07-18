<template>
  <div class="scenario-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>测试场景管理</span>
          <div>
            <el-button type="success" @click="handleExport">
              <el-icon><Download /></el-icon>导出Excel
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>新增场景
            </el-button>
          </div>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="关键词">
          <el-input v-model="searchParams.keyword" placeholder="场景名称" clearable @keyup.enter="loadData" />
        </el-form-item>
        <el-form-item label="脚本">
          <el-select v-model="searchParams.script_id" placeholder="全部" clearable>
            <el-option v-for="s in scripts" :key="s.id" :label="`${s.script_code} - ${s.title}`" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchParams.status" placeholder="全部" clearable>
            <el-option label="启用" value="active" />
            <el-option label="停用" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="scenario_name" label="场景名称" show-overflow-tooltip />
        <el-table-column prop="script_code" label="所属脚本" width="120">
          <template #default="{ row }">
            <el-button type="primary" link @click="showScriptDetail(row.script_id)">
              {{ row.script_code }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="spec_file" label="Spec文件" show-overflow-tooltip />
        <el-table-column prop="scenario_type" label="场景类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.scenario_type === 'table_driven' ? 'warning' : 'info'" size="small">
              {{ row.scenario_type === 'table_driven' ? '表驱动' : '基础' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="execution_order" label="执行顺序" width="80" />
        <el-table-column prop="timeout" label="超时(ms)" width="80" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">
              {{ row.status === 'active' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="primary" link @click="handleDetail(row)">详情</el-button>
            <el-button type="primary" link @click="handleParams(row)">参数</el-button>
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
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="所属脚本" prop="script_id">
          <el-select v-model="formData.script_id" placeholder="请选择脚本" filterable>
            <el-option v-for="s in scripts" :key="s.id" :label="`${s.script_code} - ${s.title}`" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="场景名称" prop="scenario_name">
          <el-input v-model="formData.scenario_name" placeholder="请输入场景名称" />
        </el-form-item>
        <el-form-item label="Spec文件">
          <el-input v-model="formData.spec_file" placeholder="如: specs/test.spec" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="场景类型">
              <el-select v-model="formData.scenario_type" placeholder="请选择类型">
                <el-option label="基础" value="basic" />
                <el-option label="表驱动" value="table_driven" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="执行顺序">
              <el-input-number v-model="formData.execution_order" :min="0" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="超时时间(ms)">
              <el-input-number v-model="formData.timeout" :min="1000" :step="1000" />
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
        <el-form-item label="备注">
          <el-input v-model="formData.remark" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="场景详情" width="800px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="场景ID">{{ detailData.id }}</el-descriptions-item>
        <el-descriptions-item label="场景名称">{{ detailData.scenario_name }}</el-descriptions-item>
        <el-descriptions-item label="所属脚本">
          <el-button type="primary" link @click="showScriptDetail(detailData.script_id)">
            {{ detailData.script_code }} - {{ detailData.script_title }}
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item label="Spec文件">{{ detailData.spec_file || '-' }}</el-descriptions-item>
        <el-descriptions-item label="场景类型">
          <el-tag :type="detailData.scenario_type === 'table_driven' ? 'warning' : 'info'" size="small">
            {{ detailData.scenario_type === 'table_driven' ? '表驱动' : '基础' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="执行顺序">{{ detailData.execution_order }}</el-descriptions-item>
        <el-descriptions-item label="超时时间">{{ detailData.timeout }}ms</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="detailData.status === 'active' ? 'success' : 'info'" size="small">
            {{ detailData.status === 'active' ? '启用' : '停用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ detailData.remark || '-' }}</el-descriptions-item>
      </el-descriptions>

      <template v-if="detailData.value_table && Object.keys(detailData.value_table).length > 0">
        <el-divider>取值表</el-divider>
        <pre class="json-block">{{ JSON.stringify(detailData.value_table, null, 2) }}</pre>
      </template>

      <template v-if="detailData.parameters && detailData.parameters.length > 0">
        <el-divider>场景参数</el-divider>
        <el-table :data="detailData.parameters" border style="width: 100%">
          <el-table-column prop="param_name" label="参数名" />
          <el-table-column prop="param_value" label="参数值" />
          <el-table-column prop="param_type" label="类型" width="80" />
          <el-table-column prop="is_required" label="必填" width="60">
            <template #default="{ row }">
              <el-tag :type="row.is_required ? 'danger' : 'info'" size="small">
                {{ row.is_required ? '是' : '否' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="说明" show-overflow-tooltip />
        </el-table>
      </template>

      <template v-if="detailData.data_tables && detailData.data_tables.length > 0">
        <el-divider>数据表</el-divider>
        <el-table :data="detailData.data_tables" border style="width: 100%">
          <el-table-column prop="row_name" label="行名" />
          <el-table-column prop="description" label="说明" />
          <el-table-column label="数据值">
            <template #default="{ row }">
              <pre class="json-inline">{{ JSON.stringify(row.data_value, null, 2) }}</pre>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </el-dialog>

    <!-- 参数管理对话框 -->
    <el-dialog v-model="paramDialogVisible" title="场景参数管理" width="800px">
      <div style="margin-bottom: 15px;">
        <el-button type="primary" size="small" @click="handleAddParam">
          <el-icon><Plus /></el-icon>添加参数
        </el-button>
      </div>
      <el-table :data="paramData" border style="width: 100%">
        <el-table-column prop="param_name" label="参数名" />
        <el-table-column prop="param_value" label="参数值" />
        <el-table-column prop="param_type" label="类型" width="80" />
        <el-table-column prop="is_required" label="必填" width="60">
          <template #default="{ row }">
            <el-tag :type="row.is_required ? 'danger' : 'info'" size="small">
              {{ row.is_required ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="说明" show-overflow-tooltip />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEditParam(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDeleteParam(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 参数编辑对话框 -->
    <el-dialog v-model="paramEditVisible" :title="paramEditTitle" width="500px">
      <el-form ref="paramFormRef" :model="paramFormData" :rules="paramFormRules" label-width="80px">
        <el-form-item label="参数名" prop="param_name">
          <el-input v-model="paramFormData.param_name" placeholder="请输入参数名" />
        </el-form-item>
        <el-form-item label="参数值">
          <el-input v-model="paramFormData.param_value" placeholder="请输入参数值" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="类型">
              <el-select v-model="paramFormData.param_type" placeholder="请选择类型">
                <el-option label="字符串" value="string" />
                <el-option label="整数" value="integer" />
                <el-option label="浮点数" value="float" />
                <el-option label="布尔" value="boolean" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="必填">
              <el-switch v-model="paramFormData.is_required" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="说明">
          <el-input v-model="paramFormData.description" type="textarea" :rows="2" placeholder="请输入说明" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="paramEditVisible = false">取消</el-button>
        <el-button type="primary" @click="handleParamSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 脚本详情弹窗 -->
    <el-dialog v-model="scriptDetailVisible" title="脚本详情 (Gauge框架)" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="脚本编号">{{ scriptDetailData.script_code }}</el-descriptions-item>
        <el-descriptions-item label="版本">{{ scriptDetailData.version }}</el-descriptions-item>
        <el-descriptions-item label="脚本标题" :span="2">{{ scriptDetailData.title }}</el-descriptions-item>
        <el-descriptions-item label="脚本路径" :span="2">{{ scriptDetailData.script_path }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute } from 'vue-router'
import { testScenarioApi, testScriptApi } from '@/api'
import { exportToExcel } from '@/utils/export'

const route = useRoute()

const tableData = ref([])
const scripts = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const paramDialogVisible = ref(false)
const paramEditVisible = ref(false)
const scriptDetailVisible = ref(false)
const dialogTitle = ref('')
const paramEditTitle = ref('')
const formRef = ref(null)
const paramFormRef = ref(null)
const editingId = ref(null)
const paramEditingId = ref(null)
const currentScenarioId = ref(null)
const detailData = ref({})
const paramData = ref([])
const scriptDetailData = ref({})

const searchParams = reactive({
  page: 1,
  per_page: 20,
  keyword: '',
  script_id: '',
  status: ''
})

const formData = reactive({
  script_id: '',
  scenario_name: '',
  spec_file: '',
  scenario_type: 'basic',
  execution_order: 0,
  timeout: 60000,
  status: 'active',
  remark: ''
})

const paramFormData = reactive({
  param_name: '',
  param_value: '',
  param_type: 'string',
  is_required: false,
  description: ''
})

const formRules = {
  script_id: [{ required: true, message: '请选择脚本', trigger: 'change' }],
  scenario_name: [{ required: true, message: '请输入场景名称', trigger: 'blur' }]
}

const paramFormRules = {
  param_name: [{ required: true, message: '请输入参数名', trigger: 'blur' }]
}

const loadScripts = async () => {
  try {
    const res = await testScriptApi.getList({ per_page: 100 })
    scripts.value = res.items
  } catch (error) {
    console.error('加载脚本失败:', error)
  }
}

const loadData = async () => {
  try {
    const res = await testScenarioApi.getList(searchParams)
    tableData.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const resetSearch = () => {
  searchParams.keyword = ''
  searchParams.script_id = ''
  searchParams.status = ''
  searchParams.page = 1
  loadData()
}

const handleAdd = () => {
  dialogTitle.value = '新增场景'
  editingId.value = null
  Object.assign(formData, {
    script_id: '', scenario_name: '', spec_file: '',
    scenario_type: 'basic', execution_order: 0,
    timeout: 60000, status: 'active', remark: ''
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑场景'
  editingId.value = row.id
  Object.assign(formData, {
    script_id: row.script_id,
    scenario_name: row.scenario_name,
    spec_file: row.spec_file,
    scenario_type: row.scenario_type,
    execution_order: row.execution_order,
    timeout: row.timeout,
    status: row.status,
    remark: row.remark
  })
  dialogVisible.value = true
}

const handleDetail = async (row) => {
  try {
    detailData.value = await testScenarioApi.getDetail(row.id)
    detailVisible.value = true
  } catch (error) {
    console.error('获取详情失败:', error)
  }
}

const handleParams = async (row) => {
  try {
    currentScenarioId.value = row.id
    const data = await testScenarioApi.getDetail(row.id)
    paramData.value = data.parameters || []
    paramDialogVisible.value = true
  } catch (error) {
    console.error('获取参数失败:', error)
  }
}

const handleAddParam = () => {
  paramEditTitle.value = '添加参数'
  paramEditingId.value = null
  Object.assign(paramFormData, {
    param_name: '', param_value: '', param_type: 'string',
    is_required: false, description: ''
  })
  paramEditVisible.value = true
}

const handleEditParam = (row) => {
  paramEditTitle.value = '编辑参数'
  paramEditingId.value = row.id
  Object.assign(paramFormData, {
    param_name: row.param_name,
    param_value: row.param_value,
    param_type: row.param_type,
    is_required: row.is_required,
    description: row.description
  })
  paramEditVisible.value = true
}

const handleDeleteParam = (row) => {
  ElMessageBox.confirm('确定要删除该参数吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await testScenarioApi.deleteParameter(row.id)
      ElMessage.success('删除成功')
      const data = await testScenarioApi.getDetail(currentScenarioId.value)
      paramData.value = data.parameters || []
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const handleParamSubmit = async () => {
  try {
    await paramFormRef.value.validate()
    const paramData = {
      scenario_id: currentScenarioId.value,
      ...paramFormData
    }
    if (paramEditingId.value) {
      await testScenarioApi.updateParameter(paramEditingId.value, paramFormData)
      ElMessage.success('更新成功')
    } else {
      await testScenarioApi.createParameter(paramData)
      ElMessage.success('创建成功')
    }
    paramEditVisible.value = false
    const data = await testScenarioApi.getDetail(currentScenarioId.value)
    paramData.value = data.parameters || []
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    if (editingId.value) {
      await testScenarioApi.update(editingId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await testScenarioApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该场景吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await testScenarioApi.delete(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

const showScriptDetail = async (scriptId) => {
  try {
    scriptDetailData.value = await testScriptApi.getDetail(scriptId)
    scriptDetailVisible.value = true
  } catch (error) {
    console.error('获取脚本详情失败:', error)
  }
}

const handleExport = () => {
  const columns = [
    { prop: 'id', label: 'ID', width: 8 },
    { prop: 'scenario_name', label: '场景名称', width: 25 },
    { prop: 'script_code', label: '所属脚本', width: 15 },
    { prop: 'spec_file', label: 'Spec文件', width: 25 },
    { prop: 'scenario_type', label: '场景类型', width: 10, formatter: (val) => val === 'table_driven' ? '表驱动' : '基础' },
    { prop: 'execution_order', label: '执行顺序', width: 10 },
    { prop: 'timeout', label: '超时(ms)', width: 10 },
    { prop: 'status', label: '状态', width: 8, formatter: (val) => val === 'active' ? '启用' : '停用' }
  ]
  exportToExcel(tableData.value, columns, '测试场景列表')
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadScripts()
  // 从URL参数中读取script_id
  if (route.query.script_id) {
    searchParams.script_id = parseInt(route.query.script_id)
  }
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

.json-block {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 12px;
  font-family: monospace;
  font-size: 12px;
  line-height: 1.5;
  overflow-x: auto;
}

.json-inline {
  background-color: #f5f7fa;
  border-radius: 2px;
  padding: 4px 8px;
  font-family: monospace;
  font-size: 11px;
  line-height: 1.4;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
