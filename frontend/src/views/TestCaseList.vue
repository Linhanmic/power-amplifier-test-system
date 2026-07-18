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
              <div>
                <el-button type="success" @click="handleExport">
                  <el-icon><Download /></el-icon>导出Excel
                </el-button>
                <el-button type="primary" @click="handleAdd">
                  <el-icon><Plus /></el-icon>新增用例
                </el-button>
              </div>
            </div>
          </template>

          <el-form :inline="true" class="search-form">
            <el-form-item label="关键词">
              <el-input v-model="searchParams.keyword" placeholder="用例编号/名称" clearable @keyup.enter="loadData" />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchParams.status" placeholder="全部" clearable>
                <el-option label="草稿" value="Draft" />
                <el-option label="已接受" value="Accepted" />
                <el-option label="不接受" value="Not-Accepted" />
              </el-select>
            </el-form-item>
            <el-form-item label="优先级">
              <el-select v-model="searchParams.level" placeholder="全部" clearable>
                <el-option label="S" value="S" />
                <el-option label="A" value="A" />
                <el-option label="B" value="B" />
                <el-option label="C" value="C" />
                <el-option label="D" value="D" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadData">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>

          <!-- 列显示设置 -->
          <div class="column-settings">
            <el-popover placement="bottom" :width="400" trigger="click">
              <template #reference>
                <el-button size="small">
                  <el-icon><Setting /></el-icon> 列设置
                </el-button>
              </template>
              <div class="column-checkbox-group">
                <el-checkbox v-model="columnVisibility.case_code" disabled>测试用例ID</el-checkbox>
                <el-checkbox v-model="columnVisibility.case_name" disabled>用例名称</el-checkbox>
                <el-checkbox v-model="columnVisibility.requirements">上游需求ID</el-checkbox>
                <el-checkbox v-model="columnVisibility.vehicles">适用车型</el-checkbox>
                <el-checkbox v-model="columnVisibility.level">优先级</el-checkbox>
                <el-checkbox v-model="columnVisibility.test_triple">前置条件/步骤/结果</el-checkbox>
                <el-checkbox v-model="columnVisibility.scenario">测试场景</el-checkbox>
                <el-checkbox v-model="columnVisibility.designer">编制人</el-checkbox>
                <el-checkbox v-model="columnVisibility.design_date">编制日期</el-checkbox>
                <el-checkbox v-model="columnVisibility.status">状态</el-checkbox>
              </div>
            </el-popover>
          </div>

          <el-table :data="tableData" border style="width: 100%" :default-sort="{ prop: 'case_code', order: 'ascending' }">
            <el-table-column prop="case_code" label="测试用例ID" width="140" fixed sortable />
            <el-table-column v-if="columnVisibility.requirements" prop="requirements" label="上游需求ID" width="150">
              <template #default="{ row }">
                <template v-if="row.requirements && row.requirements.length > 0">
                  <el-button v-for="req in row.requirements" :key="req.id" type="primary" link size="small" @click="showRequirementDetail(req.id)" style="margin-right: 5px;">
                    {{ req.req_code }}
                  </el-button>
                </template>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column v-if="columnVisibility.case_name" prop="case_name" label="用例名称" show-overflow-tooltip min-width="150" />
            <el-table-column v-if="columnVisibility.vehicles" prop="vehicles" label="适用车型" width="150">
              <template #default="{ row }">
                <template v-if="row.vehicles && row.vehicles.length > 0">
                  <el-tag v-for="v in row.vehicles.slice(0, 2)" :key="v.id" size="small" style="margin-right: 4px;">
                    {{ v.model_name || v.config_name }}
                  </el-tag>
                  <el-tag v-if="row.vehicles.length > 2" size="small" type="info">+{{ row.vehicles.length - 2 }}</el-tag>
                </template>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column v-if="columnVisibility.level" prop="level" label="优先级" width="80" sortable>
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.level)" size="small">{{ row.level }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column v-if="columnVisibility.test_triple" label="前置条件/步骤/结果" min-width="300">
              <template #default="{ row }">
                <div class="test-triple">
                  <div class="triple-item">
                    <span class="triple-label">前置:</span>
                    <span class="triple-content">{{ row.preconditions || '-' }}</span>
                  </div>
                  <div class="triple-item">
                    <span class="triple-label">步骤:</span>
                    <span class="triple-content">{{ row.test_steps || '-' }}</span>
                  </div>
                  <div class="triple-item">
                    <span class="triple-label">预期:</span>
                    <span class="triple-content">{{ row.expected_results || '-' }}</span>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column v-if="columnVisibility.scenario" prop="scenario_name" label="测试场景" width="120">
              <template #default="{ row }">
                <el-button v-if="row.scenario_id" type="primary" link size="small" @click="showScenarioDetailById(row.scenario_id)">
                  {{ row.scenario_name }}
                </el-button>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column v-if="columnVisibility.designer" prop="designer" label="编制人" width="80" />
            <el-table-column v-if="columnVisibility.design_date" prop="design_date" label="编制日期" width="110" sortable />
            <el-table-column v-if="columnVisibility.status" prop="status" label="状态" width="90" sortable>
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">{{ getStatusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
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
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="测试用例ID" prop="case_code">
              <el-input v-model="formData.case_code" :placeholder="caseCodePlaceholder" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属分组" prop="group_id">
              <el-tree-select
                v-model="formData.group_id"
                :data="groupTree"
                :props="{ label: 'label', value: 'id', children: 'children' }"
                placeholder="请选择分组"
                @change="handleGroupChange"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="上游需求ID">
          <el-select v-model="formData.requirement_ids" placeholder="请选择需求" multiple filterable>
            <el-option v-for="r in requirements" :key="r.id" :label="`${r.req_code} - ${r.title}`" :value="r.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="测试用例名称" prop="case_name">
          <el-input v-model="formData.case_name" placeholder="请输入用例名称" />
        </el-form-item>
        <el-form-item label="测试目的">
          <el-input v-model="formData.test_purpose" type="textarea" :rows="2" placeholder="请输入测试目的" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="优先级">
              <el-select v-model="formData.level" placeholder="请选择优先级">
                <el-option label="S - 冒烟测试项" value="S" />
                <el-option label="A - 功能定义要求有效项" value="A" />
                <el-option label="B - 功能无效项" value="B" />
                <el-option label="C - 功能交叉项" value="C" />
                <el-option label="D - 不存在工况项" value="D" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-select v-model="formData.status" placeholder="请选择状态">
                <el-option label="草稿" value="Draft" />
                <el-option label="已接受" value="Accepted" />
                <el-option label="不接受" value="Not-Accepted" />
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
        <el-form-item label="标记">
          <el-input v-model="formData.tags" placeholder="请输入标记，多个用逗号分隔" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="编制人">
              <el-input v-model="formData.designer" placeholder="请输入编制人" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="编制日期">
              <el-date-picker v-model="formData.design_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="发布日期">
          <el-date-picker v-model="formData.publish_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="关联场景">
          <el-select v-model="formData.scenario_id" placeholder="请选择场景" clearable filterable>
            <el-option-group v-for="script in scripts" :key="script.id" :label="`${script.script_code} - ${script.title}`">
              <el-option v-for="s in script.scenarios" :key="s.id" :label="s.scenario_name" :value="s.id" />
            </el-option-group>
          </el-select>
        </el-form-item>
        <el-form-item label="CAN矩阵">
          <el-select v-model="formData.can_matrix_id" placeholder="请选择CAN矩阵" clearable>
            <el-option v-for="m in canMatrices" :key="m.id" :label="m.matrix_name" :value="m.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="测试用例详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="测试用例ID">{{ detailData.case_code }}</el-descriptions-item>
        <el-descriptions-item label="所属分组">{{ detailData.group_name }}</el-descriptions-item>
        <el-descriptions-item label="测试用例名称" :span="2">{{ detailData.case_name }}</el-descriptions-item>
        <el-descriptions-item label="上游需求ID" :span="2">
          <template v-if="detailData.requirements && detailData.requirements.length > 0">
            <el-button v-for="req in detailData.requirements" :key="req.id" type="primary" link @click="showRequirementDetail(req.id)" style="margin-right: 10px;">
              {{ req.req_code }} - {{ req.title }}
            </el-button>
          </template>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="优先级">
          <el-tag :type="getPriorityType(detailData.level)" size="small">{{ detailData.level }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailData.status)">{{ getStatusText(detailData.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="测试目的" :span="2">{{ detailData.test_purpose || '-' }}</el-descriptions-item>
        <el-descriptions-item label="前置条件" :span="2">{{ detailData.preconditions || '-' }}</el-descriptions-item>
        <el-descriptions-item label="测试步骤" :span="2">
          <pre style="white-space: pre-wrap; margin: 0;">{{ detailData.test_steps }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="预期结果" :span="2">
          <pre style="white-space: pre-wrap; margin: 0;">{{ detailData.expected_results }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="标记">{{ detailData.tags || '-' }}</el-descriptions-item>
        <el-descriptions-item label="编制人">{{ detailData.designer || '-' }}</el-descriptions-item>
        <el-descriptions-item label="编制日期">{{ detailData.design_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="发布日期">{{ detailData.publish_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="关联场景">
          <el-button v-if="detailData.scenario_id" type="primary" link @click="showScenarioDetailById(detailData.scenario_id)">
            {{ detailData.scenario_name }}
          </el-button>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="所属脚本">
          <el-button v-if="detailData.script_code" type="primary" link @click="showScriptDetail(detailData.script_id)">
            {{ detailData.script_code }} - {{ detailData.script_title }}
          </el-button>
          <span v-else>-</span>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider>适用车型</el-divider>
      <el-table :data="detailData.vehicles || []" border style="width: 100%">
        <el-table-column prop="config_name" label="车辆配置" />
        <el-table-column prop="model_name" label="车型" />
        <el-table-column prop="software_code" label="软件编码" />
        <el-table-column prop="expected_result" label="预期结果" show-overflow-tooltip />
      </el-table>
    </el-dialog>

    <!-- 分组管理对话框 -->
    <el-dialog v-model="groupDialogVisible" :title="groupDialogTitle" width="500px">
      <el-form ref="groupFormRef" :model="groupFormData" :rules="groupFormRules" label-width="100px">
        <el-form-item label="父分组">
          <el-tree-select
            v-model="groupFormData.parent_id"
            :data="groupTree"
            :props="{ label: 'label', value: 'id', children: 'children' }"
            placeholder="无（顶级分组）"
            clearable
            check-strictly
          />
        </el-form-item>
        <el-form-item label="分组名称" prop="name">
          <el-input v-model="groupFormData.name" placeholder="请输入分组名称" />
        </el-form-item>
        <el-form-item label="分组编码" prop="code">
          <el-input v-model="groupFormData.code" placeholder="如: PA, BT, VOL" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="groupFormData.description" type="textarea" :rows="2" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="groupFormData.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="groupDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleGroupSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 需求详情弹窗 -->
    <el-dialog v-model="reqDetailVisible" title="需求详情" width="800px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="需求编号">{{ reqDetailData.req_code }}</el-descriptions-item>
        <el-descriptions-item label="优先级">
          <el-tag :type="getPriorityType(reqDetailData.priority)" size="small">{{ reqDetailData.priority }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="需求标题" :span="2">{{ reqDetailData.title }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ reqDetailData.category || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(reqDetailData.status)">{{ getStatusText(reqDetailData.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="需求描述" :span="2">{{ reqDetailData.description || '-' }}</el-descriptions-item>
      </el-descriptions>

      <el-divider>车型详情</el-divider>
      <el-table :data="reqDetailData.vehicle_details || []" border style="width: 100%">
        <el-table-column prop="vehicle_model_name" label="车型" />
        <el-table-column prop="feature_support" label="是否支持" width="80">
          <template #default="{ row }">
            <el-tag :type="row.feature_support ? 'success' : 'info'" size="small">
              {{ row.feature_support ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="function_status" label="功能状态" width="100" />
        <el-table-column prop="channel_count" label="通道数" width="80" />
        <el-table-column prop="power_value" label="功率(W)" width="80" />
      </el-table>
    </el-dialog>

    <!-- 脚本详情弹窗 -->
    <el-dialog v-model="scriptDetailVisible" title="脚本详情 (Gauge框架)" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="脚本编号">{{ scriptDetailData.script_code }}</el-descriptions-item>
        <el-descriptions-item label="版本">{{ scriptDetailData.version }}</el-descriptions-item>
        <el-descriptions-item label="脚本标题" :span="2">{{ scriptDetailData.title }}</el-descriptions-item>
        <el-descriptions-item label="脚本路径" :span="2">{{ scriptDetailData.script_path }}</el-descriptions-item>
      </el-descriptions>

      <el-divider>测试场景</el-divider>
      <el-table :data="scriptDetailData.scenarios || []" border style="width: 100%">
        <el-table-column prop="scenario_name" label="场景名称" />
        <el-table-column prop="scenario_type" label="场景类型" width="100" />
        <el-table-column prop="spec_file" label="Spec文件" />
        <el-table-column prop="table_driven" label="表驱动" width="80">
          <template #default="{ row }">
            <el-tag :type="row.table_driven ? 'success' : 'info'" size="small">
              {{ row.table_driven ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="primary" link @click="showScenarioDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 场景详情弹窗 -->
    <el-dialog v-model="scenarioDetailVisible" title="场景详情" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="场景名称">{{ scenarioDetailData.scenario_name }}</el-descriptions-item>
        <el-descriptions-item label="场景类型">{{ scenarioDetailData.scenario_type }}</el-descriptions-item>
        <el-descriptions-item label="Spec文件" :span="2">{{ scenarioDetailData.spec_file }}</el-descriptions-item>
        <el-descriptions-item label="执行顺序">{{ scenarioDetailData.execution_order }}</el-descriptions-item>
        <el-descriptions-item label="超时时间">{{ scenarioDetailData.timeout }}ms</el-descriptions-item>
      </el-descriptions>

      <template v-if="scenarioDetailData.value_table && Object.keys(scenarioDetailData.value_table).length > 0">
        <el-divider>取值表</el-divider>
        <pre class="json-block">{{ JSON.stringify(scenarioDetailData.value_table, null, 2) }}</pre>
      </template>

      <template v-if="scenarioDetailData.parameters && scenarioDetailData.parameters.length > 0">
        <el-divider>场景参数</el-divider>
        <el-table :data="scenarioDetailData.parameters" border style="width: 100%">
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

      <template v-if="scenarioDetailData.data_tables && scenarioDetailData.data_tables.length > 0">
        <el-divider>数据表</el-divider>
        <el-table :data="scenarioDetailData.data_tables" border style="width: 100%">
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
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { testCaseApi, testCaseGroupApi, statsApi, requirementApi, testScriptApi, testScenarioApi, canMatrixApi } from '@/api'
import { exportToExcel, statusMap, priorityMap } from '@/utils/export'

const tableData = ref([])
const groupTree = ref([])
const requirements = ref([])
const scripts = ref([])
const scenarios = ref([])
const canMatrices = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const groupDialogVisible = ref(false)
const reqDetailVisible = ref(false)
const scriptDetailVisible = ref(false)
const scenarioDetailVisible = ref(false)
const dialogTitle = ref('')
const groupDialogTitle = ref('')
const formRef = ref(null)
const groupFormRef = ref(null)
const editingId = ref(null)
const groupEditingId = ref(null)
const detailData = ref({})
const reqDetailData = ref({})
const scriptDetailData = ref({})
const scenarioDetailData = ref({})

// 列显示控制
const columnVisibility = reactive({
  case_code: true,
  case_name: true,
  requirements: true,
  vehicles: true,
  level: true,
  test_triple: true,
  scenario: true,
  designer: true,
  design_date: true,
  status: true
})

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
  requirement_ids: [],
  case_name: '',
  test_purpose: '',
  level: 'A',
  preconditions: '',
  test_steps: '',
  expected_results: '',
  tags: '',
  designer: '',
  design_date: '',
  publish_date: '',
  status: 'Draft',
  scenario_id: '',
  can_matrix_id: ''
})

const groupFormData = reactive({
  parent_id: '',
  name: '',
  code: '',
  description: '',
  sort_order: 0
})

const formRules = {
  case_code: [{ required: true, message: '请输入测试用例ID', trigger: 'blur' }],
  group_id: [{ required: true, message: '请选择分组', trigger: 'change' }],
  case_name: [{ required: true, message: '请输入测试用例名称', trigger: 'blur' }],
  test_steps: [{ required: true, message: '请输入测试步骤', trigger: 'blur' }],
  expected_results: [{ required: true, message: '请输入预期结果', trigger: 'blur' }]
}

const groupFormRules = {
  name: [{ required: true, message: '请输入分组名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入分组编码', trigger: 'blur' }]
}

// 根据分组生成用例ID占位符
const caseCodePlaceholder = computed(() => {
  if (formData.group_id) {
    const group = findGroupById(groupTree.value, formData.group_id)
    if (group && group.code) {
      return `SwQT-${group.code}-XXX`
    }
  }
  return 'SwQT-模块-序号 (如: SwQT-PA-001)'
})

// 查找分组
const findGroupById = (groups, id) => {
  for (const group of groups) {
    if (group.id === id) return group
    if (group.children) {
      const found = findGroupById(group.children, id)
      if (found) return found
    }
  }
  return null
}

// 分组变化时更新用例ID
const handleGroupChange = (groupId) => {
  if (groupId && !editingId.value) {
    const group = findGroupById(groupTree.value, groupId)
    if (group && group.code) {
      // 自动生成用例ID前缀
      formData.case_code = `SwQT-${group.code}-`
    }
  }
}

const getPriorityType = (priority) => {
  const map = { S: 'danger', A: 'warning', B: 'success', C: 'info', D: '' }
  return map[priority] || 'info'
}

const getStatusType = (status) => {
  const map = { Draft: 'info', Accepted: 'success', 'Not-Accepted': 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { Draft: '草稿', Accepted: '已接受', 'Not-Accepted': '不接受' }
  return map[status] || status
}

const loadGroupTree = async () => {
  try {
    groupTree.value = await statsApi.getTree('test-case-groups')
  } catch (error) {
    console.error('加载分组树失败:', error)
  }
}

const loadRequirements = async () => {
  try {
    const res = await requirementApi.getList({ per_page: 100 })
    requirements.value = res.items
  } catch (error) {
    console.error('加载需求失败:', error)
  }
}

const loadScripts = async () => {
  try {
    const res = await testScriptApi.getList({ per_page: 100 })
    scripts.value = res.items
  } catch (error) {
    console.error('加载脚本失败:', error)
  }
}

const loadScenarios = async () => {
  try {
    const res = await testScenarioApi.getList({ per_page: 100 })
    scenarios.value = res.items
  } catch (error) {
    console.error('加载场景失败:', error)
  }
}

const loadCanMatrices = async () => {
  try {
    const res = await canMatrixApi.getList({ per_page: 100 })
    canMatrices.value = res.items
  } catch (error) {
    console.error('加载CAN矩阵失败:', error)
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
  groupDialogTitle.value = '新增分组'
  groupEditingId.value = null
  Object.assign(groupFormData, {
    parent_id: '', name: '', code: '', description: '', sort_order: 0
  })
  groupDialogVisible.value = true
}

const handleAdd = () => {
  dialogTitle.value = '新增测试用例'
  editingId.value = null
  Object.assign(formData, {
    case_code: '', group_id: searchParams.group_id || '', requirement_ids: [],
    case_name: '', test_purpose: '', level: 'A',
    preconditions: '', test_steps: '', expected_results: '',
    tags: '', designer: '', design_date: '', publish_date: '',
    status: 'Draft', scenario_id: '', can_matrix_id: ''
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑测试用例'
  editingId.value = row.id
  Object.assign(formData, {
    case_code: row.case_code,
    group_id: row.group_id,
    requirement_ids: row.requirement_ids || [],
    case_name: row.case_name,
    test_purpose: row.test_purpose,
    level: row.level,
    preconditions: row.preconditions,
    test_steps: row.test_steps,
    expected_results: row.expected_results,
    tags: row.tags,
    designer: row.designer,
    design_date: row.design_date,
    publish_date: row.publish_date,
    status: row.status,
    scenario_id: row.scenario_id || '',
    can_matrix_id: row.can_matrix_id || ''
  })
  dialogVisible.value = true
}

const handleDetail = async (row) => {
  try {
    detailData.value = await testCaseApi.getDetail(row.id)
    detailVisible.value = true
  } catch (error) {
    console.error('获取详情失败:', error)
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    // 验证用例ID格式
    if (!formData.case_code.startsWith('SwQT-')) {
      ElMessage.warning('测试用例ID须以 SwQT- 开头')
      return
    }
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

const handleExport = () => {
  const columns = [
    { prop: 'case_code', label: '测试用例ID', width: 18 },
    { prop: 'requirement_codes', label: '上游需求ID', width: 15 },
    { prop: 'case_name', label: '用例名称', width: 25 },
    { prop: 'vehicle_names', label: '适用车型', width: 15 },
    { prop: 'level', label: '优先级', width: 8 },
    { prop: 'preconditions', label: '前置条件', width: 20 },
    { prop: 'test_steps', label: '测试步骤', width: 30 },
    { prop: 'expected_results', label: '预期结果', width: 30 },
    { prop: 'scenario_name', label: '测试场景', width: 15 },
    { prop: 'designer', label: '编制人', width: 10 },
    { prop: 'design_date', label: '编制日期', width: 12 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val }
  ]
  // 处理导出数据
  const exportData = tableData.value.map(row => ({
    ...row,
    requirement_codes: row.requirements?.map(r => r.req_code).join(', ') || '-',
    vehicle_names: row.vehicles?.map(v => v.model_name || v.config_name).join(', ') || '-'
  }))
  exportToExcel(exportData, columns, '测试用例列表')
  ElMessage.success('导出成功')
}

const handleGroupSubmit = async () => {
  try {
    await groupFormRef.value.validate()
    if (groupEditingId.value) {
      await testCaseGroupApi.update(groupEditingId.value, groupFormData)
      ElMessage.success('更新成功')
    } else {
      await testCaseGroupApi.create(groupFormData)
      ElMessage.success('创建成功')
    }
    groupDialogVisible.value = false
    loadGroupTree()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

const showRequirementDetail = async (id) => {
  try {
    reqDetailData.value = await requirementApi.getDetail(id)
    reqDetailVisible.value = true
  } catch (error) {
    console.error('获取需求详情失败:', error)
  }
}

const showScriptDetail = async (scriptId) => {
  try {
    scriptDetailData.value = await testScriptApi.getDetail(scriptId)
    scriptDetailVisible.value = true
  } catch (error) {
    console.error('获取脚本详情失败:', error)
  }
}

const showScenarioDetail = async (row) => {
  try {
    scenarioDetailData.value = await testScenarioApi.getDetail(row.id)
    scenarioDetailVisible.value = true
  } catch (error) {
    console.error('获取场景详情失败:', error)
  }
}

const showScenarioDetailById = async (id) => {
  try {
    scenarioDetailData.value = await testScenarioApi.getDetail(id)
    scenarioDetailVisible.value = true
  } catch (error) {
    console.error('获取场景详情失败:', error)
  }
}

onMounted(() => {
  loadGroupTree()
  loadData()
  loadRequirements()
  loadScripts()
  loadCanMatrices()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 15px;
}

.column-settings {
  margin-bottom: 15px;
  display: flex;
  justify-content: flex-end;
}

.column-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.group-card {
  height: calc(100vh - 200px);
  overflow-y: auto;
}

.test-triple {
  font-size: 12px;
  line-height: 1.6;
}

.triple-item {
  display: flex;
  margin-bottom: 4px;
}

.triple-label {
  color: #909399;
  font-weight: bold;
  margin-right: 8px;
  white-space: nowrap;
}

.triple-content {
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
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
