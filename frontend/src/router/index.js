import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '系统概览' }
  },
  // 基础数据
  {
    path: '/platforms',
    name: 'Platforms',
    component: () => import('@/views/PlatformList.vue'),
    meta: { title: '平台管理' }
  },
  {
    path: '/vehicles',
    name: 'Vehicles',
    component: () => import('@/views/VehicleList.vue'),
    meta: { title: '车型管理' }
  },
  {
    path: '/configs',
    name: 'Configs',
    component: () => import('@/views/ConfigList.vue'),
    meta: { title: '车辆配置' }
  },
  // 测试管理
  {
    path: '/requirements',
    name: 'Requirements',
    component: () => import('@/views/RequirementList.vue'),
    meta: { title: '需求管理' }
  },
  {
    path: '/test-cases',
    name: 'TestCases',
    component: () => import('@/views/TestCaseList.vue'),
    meta: { title: '测试用例' }
  },
  {
    path: '/test-scripts',
    name: 'TestScripts',
    component: () => import('@/views/TestScriptList.vue'),
    meta: { title: '测试脚本' }
  },
  {
    path: '/test-scenarios',
    name: 'TestScenarios',
    component: () => import('@/views/ScenarioList.vue'),
    meta: { title: '测试场景' }
  },
  // CAN通讯
  {
    path: '/can-matrices',
    name: 'CANMatrices',
    component: () => import('@/views/CANMatrixList.vue'),
    meta: { title: 'CAN矩阵' }
  },
  {
    path: '/signals',
    name: 'Signals',
    component: () => import('@/views/SignalList.vue'),
    meta: { title: '信号定义' }
  },
  // 音频配置
  {
    path: '/speaker-mappings',
    name: 'SpeakerMappings',
    component: () => import('@/views/SpeakerMappingList.vue'),
    meta: { title: '扬声器映射' }
  },
  {
    path: '/a2b-slots',
    name: 'A2BSlots',
    component: () => import('@/views/A2BSlotList.vue'),
    meta: { title: 'A2B Slot' }
  },
  {
    path: '/audio-sources',
    name: 'AudioSources',
    component: () => import('@/views/AudioSourceList.vue'),
    meta: { title: '音源管理' }
  },
  {
    path: '/playback-matrices',
    name: 'PlaybackMatrices',
    component: () => import('@/views/PlaybackMatrixList.vue'),
    meta: { title: '播放矩阵' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
