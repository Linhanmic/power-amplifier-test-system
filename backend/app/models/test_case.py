from datetime import datetime
from . import db

# 测试用例与需求的多对多关联表
test_case_requirements = db.Table('test_case_requirements',
    db.Column('test_case_id', db.Integer, db.ForeignKey('test_cases.id'), primary_key=True),
    db.Column('requirement_id', db.Integer, db.ForeignKey('requirements.id'), primary_key=True)
)


class TestCaseGroup(db.Model):
    __tablename__ = 'test_case_groups'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('test_case_groups.id'), nullable=True, comment='父分组ID')
    name = db.Column(db.String(100), nullable=False, comment='分组名称')
    code = db.Column(db.String(20), nullable=True, comment='分组编码')
    description = db.Column(db.Text, comment='分组描述')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    level = db.Column(db.Integer, default=0, comment='层级')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关系
    children = db.relationship('TestCaseGroup', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    test_cases = db.relationship('TestCase', backref='group', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'sort_order': self.sort_order,
            'level': self.level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'children': [c.to_dict() for c in self.children]
        }


class TestCase(db.Model):
    __tablename__ = 'test_cases'

    id = db.Column(db.Integer, primary_key=True)
    case_code = db.Column(db.String(50), nullable=False, unique=True, comment='测试用例ID')
    group_id = db.Column(db.Integer, db.ForeignKey('test_case_groups.id'), nullable=True, comment='所属分组')
    case_name = db.Column(db.String(200), nullable=False, comment='测试用例名称')
    test_purpose = db.Column(db.Text, comment='测试目的')
    level = db.Column(db.String(10), comment='优先级')
    preconditions = db.Column(db.Text, comment='前置条件')
    test_steps = db.Column(db.Text, comment='测试步骤')
    expected_results = db.Column(db.Text, comment='预期结果')
    tags = db.Column(db.String(500), comment='标记')
    designer = db.Column(db.String(50), comment='测试用例设计者')
    design_date = db.Column(db.Date, comment='测试用例编制日期')
    publish_date = db.Column(db.Date, comment='测试用例发布日期')
    status = db.Column(db.String(20), default='Draft', comment='状态')
    scenario_id = db.Column(db.Integer, db.ForeignKey('test_scenarios.id'), nullable=True, comment='关联场景ID')
    can_matrix_id = db.Column(db.Integer, db.ForeignKey('can_matrices.id'), nullable=True, comment='关联CAN矩阵ID')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    scenario = db.relationship('TestScenario', backref='test_cases')
    requirements = db.relationship('Requirement', secondary=test_case_requirements, backref='test_cases')
    vehicles = db.relationship('TestCaseVehicle', backref='test_case', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'case_code': self.case_code,
            'group_id': self.group_id,
            'group_name': self.group.name if self.group else None,
            'case_name': self.case_name,
            'test_purpose': self.test_purpose,
            'level': self.level,
            'preconditions': self.preconditions,
            'test_steps': self.test_steps,
            'expected_results': self.expected_results,
            'tags': self.tags,
            'designer': self.designer,
            'design_date': self.design_date.isoformat() if self.design_date else None,
            'publish_date': self.publish_date.isoformat() if self.publish_date else None,
            'status': self.status,
            'scenario_id': self.scenario_id,
            'scenario_name': self.scenario.scenario_name if self.scenario else None,
            'script_id': self.scenario.script_id if self.scenario else None,
            'script_code': self.scenario.script.script_code if self.scenario and self.scenario.script else None,
            'script_title': self.scenario.script.title if self.scenario and self.scenario.script else None,
            'script_path': self.scenario.script.script_path if self.scenario and self.scenario.script else None,
            'spec_file': self.scenario.spec_file if self.scenario else None,
            'can_matrix_id': self.can_matrix_id,
            'can_matrix_name': self.can_matrix.matrix_name if self.can_matrix else None,
            'requirements': [r.to_dict() for r in self.requirements],
            'requirement_ids': [r.id for r in self.requirements],
            'vehicles': [v.to_dict() for v in self.vehicles],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class TestCaseVehicle(db.Model):
    __tablename__ = 'test_case_vehicles'

    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_cases.id'), nullable=False, comment='测试用例ID')
    vehicle_config_id = db.Column(db.Integer, db.ForeignKey('vehicle_configs.id'), nullable=False, comment='车辆配置ID')
    expected_result = db.Column(db.Text, comment='预期结果')
    actual_result = db.Column(db.Text, comment='实际结果')
    pass_fail = db.Column(db.String(10), comment='通过/失败')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关系
    vehicle_config = db.relationship('VehicleConfig', back_populates='test_case_vehicles')

    def to_dict(self):
        return {
            'id': self.id,
            'test_case_id': self.test_case_id,
            'vehicle_config_id': self.vehicle_config_id,
            'config_name': self.vehicle_config.config_name if self.vehicle_config else None,
            'config_code': self.vehicle_config.config_code if self.vehicle_config else None,
            'software_code': self.vehicle_config.software_code if self.vehicle_config else None,
            'model_name': self.vehicle_config.vehicle_model.name if self.vehicle_config and self.vehicle_config.vehicle_model else None,
            'expected_result': self.expected_result,
            'actual_result': self.actual_result,
            'pass_fail': self.pass_fail,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
