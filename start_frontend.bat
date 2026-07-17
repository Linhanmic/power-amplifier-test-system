@echo off
echo ========================================
echo 功放测试管理系统 - 前端启动脚本
echo ========================================

cd /d "%~dp0frontend"

echo.
echo [1/3] 检查Node.js环境...
node --version
if errorlevel 1 (
    echo 错误: 未找到Node.js，请先安装Node.js 16+
    pause
    exit /b 1
)

echo.
echo [2/3] 安装依赖...
call npm install --registry=https://registry.npmmirror.com

echo.
echo [3/3] 启动开发服务器...
echo 访问地址: http://localhost:3000
echo ========================================
call npm run dev
