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
                <el-checkbox v-model="columnVisibility.gauge_info">Gauge场景</el-checkbox>
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
            <el-table-column v-if="columnVisibility.gauge_info" label="Gauge场景" width="180">
              <template #default="{ row }">
                <div v-if="row.gauge_scenario_id" class="gauge-info">
                  <el-button type="primary" link size="small" @click="showGaugeScenarioDetail(row.gauge_scenario_id)">
                    {{ row.scenario_name }}
                  </el-button>
                  <div class="gauge-path">
                    <span class="path-item">{{ row.project_name }}</span>
                    <span class="path-sep">/</span>
                    <span class="path-item">{{ row.spec_name }}</span>
                  </div>
                </div>
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
        <el-form-item label="关联Gauge场景">
          <el-cascader
            v-model="formData.gauge_scenario_path"
            :options="gaugeScenarioOptions"
            :props="{ checkStrictly: true }"
            placeholder="请选择: 项目 > Spec > 场景"
            clearable
            filterable
            @change="handleGaugeScenarioChange"
          />
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
      </el-descriptions>

      <el-divider>Gauge关联信息</el-divider>
      <el-descriptions :column="2" border v-if="detailData.gauge_scenario_id">
        <el-descriptions-item label="项目名称">{{ detailData.project_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="项目编号">{{ detailData.project_code || '-' }}</el-descriptions-item>
        <el-descriptions-item label="Spec名称">
          <el-button type="primary" link @click="showGaugeSpecDetail(detailData.spec_id)">
            {{ detailData.spec_name || '-' }}
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item label="Spec编号">{{ detailData.spec_code || '-' }}</el-descriptions-item>
        <el-descriptions-item label="场景名称">
          <el-button type="primary" link @click="showGaugeScenarioDetail(detailData.gauge_scenario_id)">
            {{ detailData.scenario_name || '-' }}
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item label="Spec文件">{{ detailData.spec_file || '-' }}</el-descriptions-item>
      </el-descriptions>
      <el-empty v-else description="未关联Gauge场景" :image-size="60" />

      <el-divider>适用车型</el-divider>
      <el-table :data="detailData.vehicles || []" border style="width: 100%">
        <el-table-column prop="config_name" label="车辆配置" />
        <el-table-column prop="model_name" label="车型" />
        <el-table-column prop="software_code" label="软件编码" />
        <el-table-column prop="expected_result" label="预期结果" show-overflow-tooltip />
      </el-table>
    </el-dialog>

    <!-- Gauge Spec详情弹窗 -->
    <el-dialog v-model="gaugeSpecDetailVisible" title="Gauge Spec详情" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="项目名称">{{ gaugeSpecDetailData.project_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="Spec编号">{{ gaugeSpecDetailData.spec_code }}</el-descriptions-item>
        <el-descriptions-item label="Spec名称" :span="2">{{ gaugeSpecDetailData.spec_name }}</el-descriptions-item>
        <el-descriptions-item label="文件路径" :span="2">{{ gaugeSpecDetailData.file_path || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="gaugeSpecDetailData.status === 'active' ? 'success' : 'info'" size="small">
            {{ gaugeSpecDetailData.status === 'active' ? '启用' : '停用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="场景数量">{{ gaugeSpecDetailData.scenario_count || 0 }}</el-descriptions-item>
      </el-descriptions>

      <el-divider>包含场景</el-divider>
      <el-table :data="gaugeSpecDetailData.scenarios || []" border style="width: 100%">
        <el-table-column prop="scenario_name" label="场景名称" />
        <el-table-column prop="scenario_type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag size="small">{{ row.scenario_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="execution_order" label="顺序" width="60" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="showGaugeScenarioDetail(row.id)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- Gauge场景详情弹窗 -->
    <el-dialog v-model="gaugeScenarioDetailVisible" title="Gauge场景详情" width="800px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="项目">{{ gaugeScenarioDetailData.project_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="Spec">{{ gaugeScenarioDetailData.spec_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="场景名称">{{ gaugeScenarioDetailData.scenario_name }}</el-descriptions-item>
        <el-descriptions-item label="场景类型">{{ gaugeScenarioDetailData.scenario_type }}</el-descriptions-item>
      </el-descriptions>

      <el-divider>步骤</el-divider>
      <el-table :data="gaugeScenarioDetailData.steps || []" border style="width: 100%">
        <el-table-column prop="step_order" label="顺序" width="60" />
        <el-table-column prop="step_text" label="步骤文本" min-width="200" />
        <el-table-column prop="step_type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getStepType(row.step_type)" size="small">{{ getStepTypeText(row.step_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_parametric" label="参数化" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_parametric ? 'success' : 'info'" size="small">
              {{ row.is_parametric ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <template v-if="gaugeScenarioDetailData.tables && gaugeScenarioDetailData.tables.length > 0">
        <el-divider>数据驱动表</el-divider>
        <div v-for="table in gaugeScenarioDetailData.tables" :key="table.id" class="gauge-table-item">
          <div class="table-header">{{ table.table_name }} ({{ table.table_type }})</div>
          <el-table :data="table.rows_data || []" border size="small" style="width: 100%">
            <el-table-column v-for="header in (table.headers || [])" :key="header" :prop="header" :label="header" />
          </el-table>
        </div>
      </template>
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
        <el-descriptions-item label="需求详情" :span="2">{{ reqDetailData.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="验证范围" :span="2">{{ reqDetailData.verification_scope || '-' }}</el-descriptions-item>
        <el-descriptions-item label="验证准则" :span="2">{{ reqDetailData.verification_criteria || '-' }}</el-descriptions-item>
      </el-descriptions>

      <el-divider>车型详情</el-divider>
      <div v-if="groupedReqVehicleDetails.length > 0" class="vehicle-groups">
        <div v-for="(group, index) in groupedReqVehicleDetails" :key="index" class="vehicle-group-item">
          <el-table :data="[group]" border style="width: 100%">
            <el-table-column label="适用车型" min-width="180">
              <template #default>
                <div class="vehicle-names">
                  <el-tag v-for="name in group.vehicle_names" :key="name" size="small" style="margin: 2px;">
                    {{ name }}
                  </el-tag>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="适用状态" width="100">
              <template #default>
                <el-tag :type="group.feature_support ? 'success' : 'info'" size="small">
                  {{ group.feature_support ? '适用' : '不适用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="车型差异" min-width="250">
              <template #default>
                <span v-if="!group.feature_support" class="not-applicable">不适用</span>
                <span v-else-if="group.difference_description">{{ group.difference_description }}</span>
                <span v-else class="no-difference">无</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { testCaseApi, testCaseGroupApi, statsApi, requirementApi, gaugeApi, canMatrixApi } from '@/api'
import { exportToExcel, statusMap, priorityMap } from '@/utils/export'

const tableData = ref([])
const groupTree = ref([])
const requirements = ref([])
const gaugeProjects = ref([])
const gaugeSpecs = ref([])
const gaugeScenarios = ref([])
const canMatrices = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const groupDialogVisible = ref(false)
const reqDetailVisible = ref(false)
const gaugeScenarioDetailVisible = ref(false)
const gaugeSpecDetailVisible = ref(false)
const dialogTitle = ref('')
const groupDialogTitle = ref('')
const formRef = ref(null)
const groupFormRef = ref(null)
const editingId = ref(null)
const groupEditingId = ref(null)
const detailData = ref({})
const reqDetailData = ref({})
const gaugeScenarioDetailData = ref({})
const gaugeSpecDetailData = ref({})

// 列显示控制
const columnVisibility = reactive({
  case_code: true,
  case_name: true,
  requirements: true,
  vehicles: true,
  level: true,
  test_triple: true,
  gauge_info: true,
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
  gauge_scenario_path: [],
  gauge_scenario_id: '',
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

// Gauge场景级联选择器选项
const gaugeScenarioOptions = computed(() => {
  return gaugeProjects.value.map(project => ({
    value: `project_${project.id}`,
    label: project.name,
    children: gaugeSpecs.value
      .filter(spec => spec.project_id === project.id)
      .map(spec => ({
        value: `spec_${spec.id}`,
        label: spec.spec_name,
        children: gaugeScenarios.value
          .filter(scenario => scenario.spec_id === spec.id)
          .map(scenario => ({
            value: scenario.id,
            label: scenario.scenario_name
          }))
      }))
  }))
})

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
      formData.case_code = `SwQT-${group.code}-`
    }
  }
}

// Gauge场景变化处理
const handleGaugeScenarioChange = (value) => {
  if (value && value.length === 3) {
    formData.gauge_scenario_id = value[2]
  } else {
    formData.gauge_scenario_id = ''
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

const getStepType = (type) => {
  const map = { setup: 'info', action: 'primary', assertion: 'success', teardown: 'warning' }
  return map[type] || 'info'
}

const getStepTypeText = (type) => {
  const map = { setup: '前置', action: '操作', assertion: '断言', teardown: '清理' }
  return map[type] || type
}

// 需求车型详情按差异分组
const groupedReqVehicleDetails = computed(() => {
  const details = reqDetailData.value.vehicle_details || []
  const groups = {}
  details.forEach(d => {
    const key = `${d.feature_support}_${d.difference_description || ''}`
    if (!groups[key]) {
      groups[key] = {
        feature_support: d.feature_support,
        difference_description: d.difference_description,
        vehicle_names: []
      }
    }
    groups[key].vehicle_names.push(d.vehicle_model_name)
  })
  return Object.values(groups)
})

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

const loadGaugeData = async () => {
  try {
    const [projectsRes, specsRes, scenariosRes] = await Promise.all([
      gaugeApi.getProjects({ per_page: 100 }),
      gaugeApi.getSpecs({ per_page: 100 }),
      gaugeApi.getScenarios({ per_page: 100 })
    ])
    gaugeProjects.value = projectsRes.items
    gaugeSpecs.value = specsRes.items
    gaugeScenarios.value = scenariosRes.items
  } catch (error) {
    console.error('加载Gauge数据失败:', error)
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
    status: 'Draft', gauge_scenario_path: [], gauge_scenario_id: '', can_matrix_id: ''
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑测试用例'
  editingId.value = row.id

  // 构建gauge_scenario_path
  let gauge_scenario_path = []
  if (row.gauge_scenario_id) {
    gauge_scenario_path = [`project_${row.project_id}`, `spec_${row.spec_id}`, row.gauge_scenario_id]
  }

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
    gauge_scenario_path: gauge_scenario_path,
    gauge_scenario_id: row.gauge_scenario_id || '',
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
    { prop: 'scenario_name', label: 'Gauge场景', width: 15 },
    { prop: 'project_name', label: 'Gauge项目', width: 15 },
    { prop: 'spec_name', label: 'Gauge Spec', width: 15 },
    { prop: 'designer', label: '编制人', width: 10 },
    { prop: 'design_date', label: '编制日期', width: 12 },
    { prop: 'status', label: '状态', width: 10, formatter: (val) => statusMap[val] || val }
  ]
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

const showGaugeScenarioDetail = async (id) => {
  try {
    gaugeScenarioDetailData.value = await gaugeApi.getScenarioDetail(id)
    gaugeScenarioDetailVisible.value = true
  } catch (error) {
    console.error('获取Gauge场景详情失败:', error)
  }
}

const showGaugeSpecDetail = async (id) => {
  try {
    gaugeSpecDetailData.value = await gaugeApi.getSpecDetail(id)
    gaugeSpecDetailVisible.value = true
  } catch (error) {
    console.error('获取Gauge Spec详情失败:', error)
  }
}

onMounted(() => {
  loadGroupTree()
  loadData()
  loadRequirements()
  loadGaugeData()
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

.gauge-info {
  font-size: 12px;
}

.gauge-path {
  color: #909399;
  margin-top: 4px;
  font-size: 11px;
}

.path-sep {
  margin: 0 4px;
}

.vehicle-groups {
  margin-top: 10px;
}

.vehicle-group-item {
  margin-bottom: 10px;
}

.vehicle-names {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.not-applicable {
  color: #909399;
  font-style: italic;
}

.no-difference {
  color: #67c23a;
  font-weight: 500;
}

.gauge-table-item {
  margin-bottom: 15px;
}

.table-header {
  font-weight: bold;
  margin-bottom: 8px;
  color: #606266;
}
</style>
