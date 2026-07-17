from datetime import datetime
from . import db


class TestCaseGroup(db.Model):
    __tablename__ = 'test_case_groups'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('test_case_groups.id'), comment='父节点ID')
    name = db.Column(db.String(100), nullable=False, comment='分组名称')
    description = db.Column(db.Text, comment='描述')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    level = db.Column(db.Integer, default=0, comment='层级深度')
    status = db.Column(db.String(20), default='active', comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 自引用关系
    children = db.relationship('TestCaseGroup', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    test_cases = db.relationship('TestCase', backref='group', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'description': self.description,
            'sort_order': self.sort_order,
            'level': self.level,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'children': [c.to_dict() for c in self.children]
        }


class TestCase(db.Model):
    __tablename__ = 'test_cases'

    id = db.Column(db.Integer, primary_key=True)
    case_code = db.Column(db.String(50), nullable=False, unique=True, comment='用例编号')
    group_id = db.Column(db.Integer, db.ForeignKey('test_case_groups.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False, comment='用例标题')
    description = db.Column(db.Text, comment='用例描述')
    preconditions = db.Column(db.Text, comment='前置条件')
    test_steps = db.Column(db.Text, nullable=False, comment='测试步骤')
    expected_results = db.Column(db.Text, nullable=False, comment='预期结果')
    level = db.Column(db.String(20), comment='优先级')
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirements.id'), comment='关联需求')
    status = db.Column(db.String(20), default='draft', comment='状态')
    script_id = db.Column(db.Integer, db.ForeignKey('test_scripts.id'), comment='关联脚本')
    can_matrix_id = db.Column(db.Integer, db.ForeignKey('can_matrices.id'), comment='关联CAN矩阵')
    created_by = db.Column(db.String(50), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    vehicles = db.relationship('TestCaseVehicle', backref='test_case', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'case_code': self.case_code,
            'group_id': self.group_id,
            'group_name': self.group.name if self.group else None,
            'title': self.title,
            'description': self.description,
            'preconditions': self.preconditions,
            'test_steps': self.test_steps,
            'expected_results': self.expected_results,
            'level': self.level,
            'requirement_id': self.requirement_id,
            'requirement_code': self.requirement.req_code if self.requirement else None,
            'status': self.status,
            'script_id': self.script_id,
            'can_matrix_id': self.can_matrix_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'vehicles': [v.to_dict() for v in self.vehicles]
        }


class TestCaseVehicle(db.Model):
    __tablename__ = 'test_case_vehicles'

    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_cases.id'), nullable=False)
    vehicle_config_id = db.Column(db.Integer, db.ForeignKey('vehicle_configs.id'), nullable=False)
    expected_result = db.Column(db.Text, comment='车型预期结果')
    actual_result = db.Column(db.Text, comment='实际结果')
    test_status = db.Column(db.String(20), default='pending', comment='测试状态')
    executed_at = db.Column(db.DateTime, comment='执行时间')
    executed_by = db.Column(db.String(50), comment='执行人')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关系
    vehicle_config = db.relationship('VehicleConfig', back_populates='test_case_vehicles')

    def to_dict(self):
        return {
            'id': self.id,
            'test_case_id': self.test_case_id,
            'vehicle_config_id': self.vehicle_config_id,
            'vehicle_config_name': self.vehicle_config.config_name if self.vehicle_config else None,
            'expected_result': self.expected_result,
            'actual_result': self.actual_result,
            'test_status': self.test_status,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'executed_by': self.executed_by,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
