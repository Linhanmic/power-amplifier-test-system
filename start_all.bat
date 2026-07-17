@echo off
echo ========================================
echo 功放测试管理系统 - 一键启动
echo ========================================

echo.
echo [1/2] 启动后端服务...
start "功放测试系统-后端" cmd /k "cd /d %~dp0 && call start_backend.bat"

echo.
echo [2/2] 等待3秒后启动前端服务...
timeout /t 3 /nobreak >nul
start "功放测试系统-前端" cmd /k "cd /d %~dp0 && call start_frontend.bat"

echo.
echo ========================================
echo 系统启动中...
echo 后端地址: http://localhost:5000
echo 前端地址: http://localhost:3000
echo ========================================
echo.
echo 按任意键退出此窗口...
pause >nul
