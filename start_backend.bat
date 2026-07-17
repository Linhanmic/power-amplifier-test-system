@echo off
echo ========================================
echo 功放测试管理系统 - 后端启动脚本
echo ========================================

cd /d "%~dp0backend"

echo.
echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/3] 安装依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [3/3] 初始化数据库并填充Mock数据...
python init_mock_data.py

echo.
echo ========================================
echo 启动Flask服务器...
echo 访问地址: http://localhost:5000
echo ========================================
python run.py
