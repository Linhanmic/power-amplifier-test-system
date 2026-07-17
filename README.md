# 功放测试管理系统 (Power Amplifier Test System)

## 项目简介

功放测试管理系统是一个用于管理功放测试全流程的Web应用，包括需求管理、测试用例管理、测试脚本管理、CAN通讯矩阵、扬声器通道映射、播放矩阵等功能模块。

## 技术栈

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Element Plus** - Vue 3组件库
- **Vite** - 下一代前端构建工具
- **Pinia** - Vue 状态管理
- **Vue Router** - Vue 路由管理
- **Axios** - HTTP 客户端

### 后端
- **Flask** - Python Web框架
- **SQLAlchemy** - ORM框架
- **Flask-RESTful** - REST API框架
- **SQLite** - 轻量级数据库

## 项目结构

```
测试系统/
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── api/           # API接口
│   │   ├── views/         # 页面组件
│   │   ├── router/        # 路由配置
│   │   ├── App.vue        # 主组件
│   │   └── main.js        # 入口文件
│   ├── package.json
│   └── vite.config.js
├── backend/                # 后端项目
│   ├── app/
│   │   ├── api/           # API接口
│   │   ├── models/        # 数据模型
│   │   └── __init__.py
│   ├── instance/          # 数据库文件
│   ├── config.py          # 配置文件
│   ├── run.py             # 启动文件
│   ├── init_mock_data.py  # Mock数据初始化
│   └── requirements.txt
├── 设计方案.md              # 系统设计方案
├── 数据导入提示词.md         # Excel数据导入提示词
├── start_all.bat           # 一键启动脚本
├── start_backend.bat       # 后端启动脚本
└── start_frontend.bat      # 前端启动脚本
```

## 核心功能模块

### 1. 基础数据管理
- **平台管理**: 管理车辆平台（MQB、MEB等）
- **车型管理**: 管理具体车型（迈腾、ID.4等）
- **车辆配置**: 管理车辆配置（豪华版、旗舰版等）

### 2. 测试管理
- **需求管理**: 管理测试需求，支持状态流转
- **测试用例**: 树形结构管理测试用例，支持关联需求
- **测试脚本**: 管理Gauge测试脚本和场景

### 3. CAN通讯管理
- **CAN矩阵**: 管理DBC文件和CAN信号定义
- **信号定义**: 定义CAN信号的详细参数

### 4. 音频配置管理
- **扬声器映射**: 配置扬声器与通道的映射关系
- **A2B Slot**: 管理A2B总线Slot配置
- **音源管理**: 管理蓝牙、USB、收音机等音源类型
- **播放矩阵**: 配置不同条件下的音频播放策略

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 一键启动

双击运行 `start_all.bat`，系统将自动：
1. 安装前后端依赖
2. 初始化数据库并填充Mock数据
3. 启动后端服务（http://localhost:5000）
4. 启动前端服务（http://localhost:3000）

### 手动启动

#### 启动后端

```bash
cd backend
pip install -r requirements.txt
python init_mock_data.py  # 首次运行，初始化数据库
python run.py
```

#### 启动前端

```bash
cd frontend
npm install
npm run dev
```

## 访问地址

- 前端页面: http://localhost:3000
- 后端API: http://localhost:5000/api

## Mock数据

系统内置了丰富的Mock数据，包括：
- 3个平台（MQB、MEB、J528）
- 5个车型（迈腾B9、帕萨特B9、ID.4、ID.6、A6L）
- 4个车辆配置
- 6种音源类型
- 4个A2B Slot
- 2个CAN矩阵及6个信号定义
- 5个测试需求
- 4个测试用例分组
- 4个测试用例
- 3个测试脚本及3个测试场景
- 2个播放矩阵

## 数据库表结构

系统共包含19张数据表：

| 表名 | 说明 |
|------|------|
| platforms | 平台表 |
| vehicle_models | 车型表 |
| vehicle_configs | 车辆配置表 |
| requirements | 需求表 |
| requirement_vehicle_details | 需求车型详情表 |
| test_case_groups | 测试用例分组表 |
| test_cases | 测试用例表 |
| test_case_vehicles | 测试用例车型关联表 |
| test_scripts | 测试脚本表 |
| test_scenarios | 测试场景表 |
| scenario_parameters | 场景参数表 |
| scenario_data_tables | 场景数据表 |
| can_matrices | CAN矩阵表 |
| signal_definitions | 信号定义表 |
| speaker_channel_mappings | 扬声器通道映射表 |
| a2b_slots | A2B Slot表 |
| audio_source_types | 音源类型表 |
| audio_source_slot_mappings | 音源Slot映射表 |
| playback_matrices | 播放矩阵表 |
| playback_matrix_base | 基础矩阵表 |
| playback_matrix_conditions | 条件矩阵表 |

## API接口

所有API接口遵循RESTful设计规范：

- `GET /api/{resource}` - 获取列表
- `GET /api/{resource}/{id}` - 获取详情
- `POST /api/{resource}` - 创建
- `PUT /api/{resource}/{id}` - 更新
- `DELETE /api/{resource}/{id}` - 删除

### 主要API模块

- `/api/platforms` - 平台管理
- `/api/vehicle-models` - 车型管理
- `/api/vehicle-configs` - 车辆配置
- `/api/requirements` - 需求管理
- `/api/test-cases` - 测试用例
- `/api/test-scripts` - 测试脚本
- `/api/can-matrices` - CAN矩阵
- `/api/speaker-mappings` - 扬声器映射
- `/api/playback-matrices` - 播放矩阵
- `/api/stats/overview` - 统计概览

## 开发说明

### 添加新功能模块

1. 在 `backend/app/models/` 添加数据模型
2. 在 `backend/app/api/` 添加API接口
3. 在 `frontend/src/api/index.js` 添加前端API调用
4. 在 `frontend/src/views/` 添加页面组件
5. 在 `frontend/src/router/index.js` 添加路由配置

### 数据导入

参考 `数据导入提示词.md` 文档，使用AI辅助将Excel数据导入系统。

## 部署说明

### 开发环境
使用上述快速开始步骤即可。

### 生产环境

1. 构建前端
```bash
cd frontend
npm run build
```

2. 部署后端
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

3. 使用Nginx反向代理前端静态文件和后端API

## 常见问题

### Q: 数据库文件在哪里？
A: SQLite数据库文件位于 `backend/instance/power_amplifier.db`

### Q: 如何重置数据？
A: 重新运行 `python init_mock_data.py` 即可重置为Mock数据

### Q: 如何导入Excel数据？
A: 参考 `数据导入提示词.md` 文档

## 许可证

内部项目，仅供学习和使用。
