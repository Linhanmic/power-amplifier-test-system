<template>
  <el-container class="app-container">
    <el-aside width="220px" class="app-aside">
      <div class="logo">
        <h2>功放测试系统</h2>
      </div>
      <el-menu
        :default-active="currentRoute"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>系统概览</span>
        </el-menu-item>

        <el-sub-menu index="base-data">
          <template #title>
            <el-icon><Grid /></el-icon>
            <span>基础数据</span>
          </template>
          <el-menu-item index="/platforms">平台管理</el-menu-item>
          <el-menu-item index="/vehicles">车型管理</el-menu-item>
          <el-menu-item index="/configs">车辆配置</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="test-manage">
          <template #title>
            <el-icon><Document /></el-icon>
            <span>测试管理</span>
          </template>
          <el-menu-item index="/requirements">需求管理</el-menu-item>
          <el-menu-item index="/test-cases">测试用例</el-menu-item>
          <el-menu-item index="/test-scripts">测试脚本</el-menu-item>
          <el-menu-item index="/test-scenarios">测试场景</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="can-manage">
          <template #title>
            <el-icon><Connection /></el-icon>
            <span>CAN通讯</span>
          </template>
          <el-menu-item index="/can-matrices">CAN矩阵</el-menu-item>
          <el-menu-item index="/signals">信号定义</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="audio-manage">
          <template #title>
            <el-icon><Microphone /></el-icon>
            <span>音频配置</span>
          </template>
          <el-menu-item index="/speaker-mappings">扬声器映射</el-menu-item>
          <el-menu-item index="/a2b-slots">A2B Slot</el-menu-item>
          <el-menu-item index="/audio-sources">音源管理</el-menu-item>
          <el-menu-item index="/playback-matrices">播放矩阵</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="app-header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentTitle">{{ currentTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              <el-icon><User /></el-icon>
              管理员
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人设置</el-dropdown-item>
                <el-dropdown-item divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const currentRoute = computed(() => route.path)
const currentTitle = computed(() => route.meta?.title || '')
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.app-container {
  height: 100vh;
}

.app-aside {
  background-color: #304156;
  overflow-y: auto;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  background-color: #263445;
}

.logo h2 {
  font-size: 16px;
  font-weight: 500;
}

.el-menu {
  border-right: none;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #606266;
}

.user-info .el-icon {
  margin-right: 8px;
}

.app-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
