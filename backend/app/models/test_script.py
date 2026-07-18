import json
from datetime import datetime
from . import db


class TestScript(db.Model):
    __tablename__ = 'test_scripts'

    id = db.Column(db.Integer, primary_key=True)
    script_code = db.Column(db.String(50), nullable=False, unique=True, comment='脚本编号')
    title = db.Column(db.String(200), nullable=False, comment='脚本标题')
    script_path = db.Column(db.String(500), comment='脚本路径')
    tags = db.Column(db.Text, comment='标签(JSON)')
    status = db.Column(db.String(20), default='draft', comment='状态')
    version = db.Column(db.String(20), default='1.0', comment='版本')
    remark = db.Column(db.Text, comment='备注')
    created_by = db.Column(db.String(50), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    scenarios = db.relationship('TestScenario', backref='script', lazy='dynamic')

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
            'script_code': self.script_code,
            'title': self.title,
            'script_path': self.script_path,
            'tags': self.tags_list,
            'status': self.status,
            'version': self.version,
            'remark': self.remark,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'scenarios': [s.to_dict() for s in self.scenarios]
        }


class TestScenario(db.Model):
    __tablename__ = 'test_scenarios'

    id = db.Column(db.Integer, primary_key=True)
    script_id = db.Column(db.Integer, db.ForeignKey('test_scripts.id'), nullable=False)
    scenario_name = db.Column(db.String(200), nullable=False, comment='场景名称')
    spec_file = db.Column(db.String(500), comment='spec文件路径')
    scenario_type = db.Column(db.String(20), comment='场景类型')
    table_driven = db.Column(db.Boolean, default=False, comment='是否为表驱动')
    value_table = db.Column(db.Text, comment='取值表(JSON)')
    execution_order = db.Column(db.Integer, default=0, comment='执行顺序')
    timeout = db.Column(db.Integer, default=60000, comment='执行超时时间(ms)')
    status = db.Column(db.String(20), default='active', comment='状态')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    parameters = db.relationship('ScenarioParameter', backref='scenario', lazy='dynamic')
    data_tables = db.relationship('ScenarioDataTable', backref='scenario', lazy='dynamic')

    @property
    def value_table_dict(self):
        if self.value_table:
            return json.loads(self.value_table)
        return {}

    @value_table_dict.setter
    def value_table_dict(self, value):
        self.value_table = json.dumps(value, ensure_ascii=False)

    def to_dict(self):
        return {
            'id': self.id,
            'script_id': self.script_id,
            'scenario_name': self.scenario_name,
            'spec_file': self.spec_file,
            'scenario_type': self.scenario_type,
            'table_driven': self.table_driven,
            'value_table': self.value_table_dict,
            'execution_order': self.execution_order,
            'timeout': self.timeout,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'parameters': [p.to_dict() for p in self.parameters],
            'data_tables': [d.to_dict() for d in self.data_tables]
        }


class ScenarioParameter(db.Model):
    __tablename__ = 'scenario_parameters'

    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('test_scenarios.id'), nullable=False)
    param_name = db.Column(db.String(50), nullable=False, comment='参数名')
    param_value = db.Column(db.String(200), comment='参数值')
    param_type = db.Column(db.String(20), default='string', comment='参数类型')
    is_required = db.Column(db.Boolean, default=False, comment='是否必填')
    description = db.Column(db.Text, comment='参数说明')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'scenario_id': self.scenario_id,
            'param_name': self.param_name,
            'param_value': self.param_value,
            'param_type': self.param_type,
            'is_required': self.is_required,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ScenarioDataTable(db.Model):
    __tablename__ = 'scenario_data_tables'

    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('test_scenarios.id'), nullable=False)
    row_name = db.Column(db.String(50), nullable=False, comment='行名')
    data_value = db.Column(db.Text, comment='数据值(JSON)')
    description = db.Column(db.Text, comment='行说明')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'scenario_id': self.scenario_id,
            'row_name': self.row_name,
            'data_value': json.loads(self.data_value) if self.data_value else None,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
