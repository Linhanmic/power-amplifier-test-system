# 功放测试管理系统

功率放大器测试管理全流程系统，涵盖需求分析、测试用例、测试脚本、CAN通讯矩阵、车型配置、扬声器通道映射和播放矩阵等模块。

## 技术栈

- **前端**: Vue 3 + Element Plus + Vite
- **后端**: Flask + SQLAlchemy + Flask-RESTful
- **数据库**: SQLite
- **测试框架**: Gauge（脚本管理）

## 项目结构

```
测试系统/
├── 设计方案.md              # 完整的系统设计方案
├── 数据导入提示词.md        # Excel数据导入AI提示词
├── backend/                 # 后端Flask项目（待创建）
├── frontend/                # 前端Vue项目（待创建）
└── data/                    # 数据文件目录（待创建）
```

## 核心功能

1. **需求分析管理** - 需求与多车型关联，支持矩阵视图
2. **测试用例管理** - 多级分组，适用车型选择
3. **测试脚本管理** - Gauge框架集成，场景-用例绑定
4. **CAN通讯矩阵** - 信号定义管理，支持值表
5. **车型配置管理** - 扬声器通道映射
6. **音源管理** - 音源类型、A2B SLOT、多对多映射
7. **播放矩阵管理** - 基本矩阵和工况矩阵双层设计
8. **数据导入** - Excel数据批量导入

## 数据表关系

详见 [设计方案.md](设计方案.md) 中的"核心实体关系图"章节。

## 快速开始

### 开发环境

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py

# 前端
cd frontend
npm install
npm run dev
```

### Docker部署

```bash
docker-compose up -d
```

## 许可证

私有项目
