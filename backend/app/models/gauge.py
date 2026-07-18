import json
from datetime import datetime
from . import db


class GaugeProject(db.Model):
    """Gauge测试项目"""
    __tablename__ = 'gauge_projects'

    id = db.Column(db.Integer, primary_key=True)
    project_code = db.Column(db.String(50), nullable=False, unique=True, comment='项目编号')
    name = db.Column(db.String(200), nullable=False, comment='项目名称')
    description = db.Column(db.Text, comment='项目描述')
    root_path = db.Column(db.String(500), comment='项目根路径')
    gauge_version = db.Column(db.String(20), comment='Gauge版本')
    status = db.Column(db.String(20), default='active', comment='状态')
    created_by = db.Column(db.String(50), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    specs = db.relationship('GaugeSpec', backref='project', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'name': self.name,
            'description': self.description,
            'root_path': self.root_path,
            'gauge_version': self.gauge_version,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'spec_count': self.specs.count()
        }


class GaugeSpec(db.Model):
    """Gauge规格文件（.spec）"""
    __tablename__ = 'gauge_specs'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('gauge_projects.id'), nullable=False)
    spec_code = db.Column(db.String(50), nullable=False, unique=True, comment='规格编号')
    spec_name = db.Column(db.String(200), nullable=False, comment='规格名称')
    file_path = db.Column(db.String(500), comment='spec文件路径')
    tags = db.Column(db.Text, comment='标签(JSON)')
    execution_order = db.Column(db.Integer, default=0, comment='执行顺序')
    status = db.Column(db.String(20), default='active', comment='状态')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    scenarios = db.relationship('GaugeScenario', backref='spec', lazy='dynamic')

    @property
    def tags_list(self):
        if self.tags:
            return json.loads(self.tags)
        return []

    @tags_list.setter
    def tags_list(self, value):
        self.tags = json.dumps(value, ensure_ascii=False)

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'spec_code': self.spec_code,
            'spec_name': self.spec_name,
            'file_path': self.file_path,
            'tags': self.tags_list,
            'execution_order': self.execution_order,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'scenario_count': self.scenarios.count(),
            'scenarios': [{
                'id': s.id,
                'scenario_name': s.scenario_name,
                'scenario_type': s.scenario_type,
                'execution_order': s.execution_order,
                'status': s.status
            } for s in self.scenarios.order_by(GaugeScenario.execution_order)]
        }


class GaugeScenario(db.Model):
    """Gauge场景"""
    __tablename__ = 'gauge_scenarios'

    id = db.Column(db.Integer, primary_key=True)
    spec_id = db.Column(db.Integer, db.ForeignKey('gauge_specs.id'), nullable=False)
    scenario_name = db.Column(db.String(200), nullable=False, comment='场景名称')
    scenario_type = db.Column(db.String(20), default='basic', comment='场景类型: basic/table_driven/tags')
    tags = db.Column(db.Text, comment='场景标签(JSON)')
    execution_order = db.Column(db.Integer, default=0, comment='执行顺序')
    timeout = db.Column(db.Integer, default=60000, comment='执行超时时间(ms)')
    status = db.Column(db.String(20), default='active', comment='状态')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    steps = db.relationship('GaugeStep', backref='scenario', lazy='dynamic', order_by='GaugeStep.step_order')
    tables = db.relationship('GaugeTable', backref='scenario', lazy='dynamic')
    test_cases = db.relationship('TestCase', backref='gauge_scenario', lazy='dynamic')

    @property
    def tags_list(self):
        if self.tags:
            return json.loads(self.tags)
        return []

    @tags_list.setter
    def tags_list(self, value):
        self.tags = json.dumps(value, ensure_ascii=False)

    def to_dict(self):
        return {
            'id': self.id,
            'spec_id': self.spec_id,
            'spec_name': self.spec.spec_name if self.spec else None,
            'spec_code': self.spec.spec_code if self.spec else None,
            'project_name': self.spec.project.name if self.spec and self.spec.project else None,
            'scenario_name': self.scenario_name,
            'scenario_type': self.scenario_type,
            'tags': self.tags_list,
            'execution_order': self.execution_order,
            'timeout': self.timeout,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'steps': [s.to_dict() for s in self.steps],
            'tables': [t.to_dict() for t in self.tables],
            'test_case_count': self.test_cases.count()
        }


class GaugeStep(db.Model):
    """Gauge步骤"""
    __tablename__ = 'gauge_steps'

    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('gauge_scenarios.id'), nullable=False)
    step_order = db.Column(db.Integer, nullable=False, comment='步骤顺序')
    step_text = db.Column(db.Text, nullable=False, comment='步骤文本')
    step_type = db.Column(db.String(20), default='action', comment='步骤类型: setup/action/assertion/teardown')
    is_parametric = db.Column(db.Boolean, default=False, comment='是否参数化')
    parameters = db.Column(db.Text, comment='参数值(JSON)')
    status = db.Column(db.String(20), default='active', comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def parameters_list(self):
        if self.parameters:
            return json.loads(self.parameters)
        return []

    @parameters_list.setter
    def parameters_list(self, value):
        self.parameters = json.dumps(value, ensure_ascii=False)

    def to_dict(self):
        return {
            'id': self.id,
            'scenario_id': self.scenario_id,
            'step_order': self.step_order,
            'step_text': self.step_text,
            'step_type': self.step_type,
            'is_parametric': self.is_parametric,
            'parameters': self.parameters_list,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class GaugeTable(db.Model):
    """Gauge数据驱动表"""
    __tablename__ = 'gauge_tables'

    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('gauge_scenarios.id'), nullable=False)
    table_name = db.Column(db.String(100), nullable=False, comment='表名')
    table_type = db.Column(db.String(20), default='parameter', comment='表类型: parameter/context')
    headers = db.Column(db.Text, comment='表头(JSON)')
    rows_data = db.Column(db.Text, comment='行数据(JSON)')
    description = db.Column(db.Text, comment='表说明')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def headers_list(self):
        if self.headers:
            return json.loads(self.headers)
        return []

    @headers_list.setter
    def headers_list(self, value):
        self.headers = json.dumps(value, ensure_ascii=False)

    @property
    def rows_data_list(self):
        if self.rows_data:
            return json.loads(self.rows_data)
        return []

    @rows_data_list.setter
    def rows_data_list(self, value):
        self.rows_data = json.dumps(value, ensure_ascii=False)

    def to_dict(self):
        return {
            'id': self.id,
            'scenario_id': self.scenario_id,
            'table_name': self.table_name,
            'table_type': self.table_type,
            'headers': self.headers_list,
            'rows_data': self.rows_data_list,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
