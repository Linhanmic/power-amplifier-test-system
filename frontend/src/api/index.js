import request from './request'

// 平台API
export const platformApi = {
  getList: (params) => request.get('/platforms', { params }),
  getDetail: (id) => request.get(`/platforms/${id}`),
  create: (data) => request.post('/platforms', data),
  update: (id, data) => request.put(`/platforms/${id}`, data),
  delete: (id) => request.delete(`/platforms/${id}`)
}

// 车型API
export const vehicleModelApi = {
  getList: (params) => request.get('/vehicle-models', { params }),
  getDetail: (id) => request.get(`/vehicle-models/${id}`),
  create: (data) => request.post('/vehicle-models', data),
  update: (id, data) => request.put(`/vehicle-models/${id}`, data),
  delete: (id) => request.delete(`/vehicle-models/${id}`)
}

// 车辆配置API
export const vehicleConfigApi = {
  getList: (params) => request.get('/vehicle-configs', { params }),
  getDetail: (id) => request.get(`/vehicle-configs/${id}`),
  create: (data) => request.post('/vehicle-configs', data),
  update: (id, data) => request.put(`/vehicle-configs/${id}`, data),
  delete: (id) => request.delete(`/vehicle-configs/${id}`)
}

// 需求API
export const requirementApi = {
  getList: (params) => request.get('/requirements', { params }),
  getDetail: (id) => request.get(`/requirements/${id}`),
  create: (data) => request.post('/requirements', data),
  update: (id, data) => request.put(`/requirements/${id}`, data),
  delete: (id) => request.delete(`/requirements/${id}`)
}

// 测试用例分组API
export const testCaseGroupApi = {
  getList: (params) => request.get('/test-case-groups', { params }),
  getDetail: (id) => request.get(`/test-case-groups/${id}`),
  create: (data) => request.post('/test-case-groups', data),
  update: (id, data) => request.put(`/test-case-groups/${id}`, data),
  delete: (id) => request.delete(`/test-case-groups/${id}`)
}

// 测试用例API
export const testCaseApi = {
  getList: (params) => request.get('/test-cases', { params }),
  getDetail: (id) => request.get(`/test-cases/${id}`),
  create: (data) => request.post('/test-cases', data),
  update: (id, data) => request.put(`/test-cases/${id}`, data),
  delete: (id) => request.delete(`/test-cases/${id}`)
}

// 测试脚本API
export const testScriptApi = {
  getList: (params) => request.get('/test-scripts', { params }),
  getDetail: (id) => request.get(`/test-scripts/${id}`),
  create: (data) => request.post('/test-scripts', data),
  update: (id, data) => request.put(`/test-scripts/${id}`, data),
  delete: (id) => request.delete(`/test-scripts/${id}`)
}

// 测试场景API
export const testScenarioApi = {
  getList: (params) => request.get('/test-scenarios', { params }),
  getDetail: (id) => request.get(`/test-scenarios/${id}`),
  create: (data) => request.post('/test-scenarios', data),
  update: (id, data) => request.put(`/test-scenarios/${id}`, data),
  delete: (id) => request.delete(`/test-scenarios/${id}`),
  // 场景参数
  createParameter: (data) => request.post('/scenario-parameters', data),
  updateParameter: (id, data) => request.put(`/scenario-parameters/${id}`, data),
  deleteParameter: (id) => request.delete(`/scenario-parameters/${id}`)
}

// CAN矩阵API
export const canMatrixApi = {
  getList: (params) => request.get('/can-matrices', { params }),
  getDetail: (id) => request.get(`/can-matrices/${id}`),
  create: (data) => request.post('/can-matrices', data),
  update: (id, data) => request.put(`/can-matrices/${id}`, data),
  delete: (id) => request.delete(`/can-matrices/${id}`)
}

// 信号定义API
export const signalDefinitionApi = {
  getList: (params) => request.get('/signal-definitions', { params }),
  getDetail: (id) => request.get(`/signal-definitions/${id}`),
  create: (data) => request.post('/signal-definitions', data),
  update: (id, data) => request.put(`/signal-definitions/${id}`, data),
  delete: (id) => request.delete(`/signal-definitions/${id}`)
}

// 扬声器映射API
export const speakerMappingApi = {
  getList: (params) => request.get('/speaker-mappings', { params }),
  getDetail: (id) => request.get(`/speaker-mappings/${id}`),
  create: (data) => request.post('/speaker-mappings', data),
  update: (id, data) => request.put(`/speaker-mappings/${id}`, data),
  delete: (id) => request.delete(`/speaker-mappings/${id}`)
}

// A2B Slot API
export const a2bSlotApi = {
  getList: () => request.get('/a2b-slots'),
  getDetail: (id) => request.get(`/a2b-slots/${id}`),
  create: (data) => request.post('/a2b-slots', data),
  update: (id, data) => request.put(`/a2b-slots/${id}`, data),
  delete: (id) => request.delete(`/a2b-slots/${id}`)
}

// 音源类型API
export const audioSourceTypeApi = {
  getList: () => request.get('/audio-source-types'),
  getDetail: (id) => request.get(`/audio-source-types/${id}`),
  create: (data) => request.post('/audio-source-types', data),
  update: (id, data) => request.put(`/audio-source-types/${id}`, data),
  delete: (id) => request.delete(`/audio-source-types/${id}`)
}

// 音源Slot映射API
export const audioSourceSlotMappingApi = {
  getList: (params) => request.get('/audio-source-slot-mappings', { params }),
  create: (data) => request.post('/audio-source-slot-mappings', data),
  delete: (id) => request.delete(`/audio-source-slot-mappings/${id}`)
}

// 播放矩阵API
export const playbackMatrixApi = {
  getList: (params) => request.get('/playback-matrices', { params }),
  getDetail: (id) => request.get(`/playback-matrices/${id}`),
  create: (data) => request.post('/playback-matrices', data),
  update: (id, data) => request.put(`/playback-matrices/${id}`, data),
  delete: (id) => request.delete(`/playback-matrices/${id}`),
  // 基础矩阵条目
  addBaseEntry: (data) => request.post('/playback-matrix-base', data),
  updateBaseEntry: (id, data) => request.put(`/playback-matrix-base/${id}`, data),
  deleteBaseEntry: (id) => request.delete(`/playback-matrix-base/${id}`),
  // 条件矩阵
  addCondition: (data) => request.post('/playback-matrix-conditions', data),
  updateCondition: (id, data) => request.put(`/playback-matrix-conditions/${id}`, data),
  deleteCondition: (id) => request.delete(`/playback-matrix-conditions/${id}`)
}

// 基础矩阵API
export const playbackMatrixBaseApi = {
  getList: (params) => request.get('/playback-matrix-base', { params }),
  create: (data) => request.post('/playback-matrix-base', data),
  update: (id, data) => request.put(`/playback-matrix-base/${id}`, data),
  delete: (id) => request.delete(`/playback-matrix-base/${id}`)
}

// 条件矩阵API
export const playbackMatrixConditionApi = {
  getList: (params) => request.get('/playback-matrix-conditions', { params }),
  getDetail: (id) => request.get(`/playback-matrix-conditions/${id}`),
  create: (data) => request.post('/playback-matrix-conditions', data),
  update: (id, data) => request.put(`/playback-matrix-conditions/${id}`, data),
  delete: (id) => request.delete(`/playback-matrix-conditions/${id}`)
}

// 统计API
export const statsApi = {
  getOverview: () => request.get('/stats/overview'),
  getTree: (type) => request.get(`/tree/${type}`)
}
