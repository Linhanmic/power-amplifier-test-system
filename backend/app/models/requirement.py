from datetime import datetime
from . import db


class Requirement(db.Model):
    __tablename__ = 'requirements'

    id = db.Column(db.Integer, primary_key=True)
    req_code = db.Column(db.String(50), nullable=False, unique=True, comment='需求编号')
    title = db.Column(db.String(200), nullable=False, comment='需求标题')
    description = db.Column(db.Text, comment='需求描述')
    category = db.Column(db.String(50), comment='需求分类')
    priority = db.Column(db.String(20), comment='优先级')
    status = db.Column(db.String(20), default='draft', comment='状态')
    created_by = db.Column(db.String(50), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    vehicle_details = db.relationship('RequirementVehicleDetail', backref='requirement', lazy='dynamic')
    test_cases = db.relationship('TestCase', backref='requirement', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'req_code': self.req_code,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'vehicle_details': [d.to_dict() for d in self.vehicle_details]
        }


class RequirementVehicleDetail(db.Model):
    __tablename__ = 'requirement_vehicle_details'

    id = db.Column(db.Integer, primary_key=True)
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirements.id'), nullable=False)
    vehicle_model_id = db.Column(db.Integer, db.ForeignKey('vehicle_models.id'), nullable=False)
    feature_support = db.Column(db.Boolean, comment='是否支持')
    function_status = db.Column(db.String(20), comment='功能状态')
    channel_count = db.Column(db.Integer, comment='通道数量')
    power_value = db.Column(db.Float, comment='功率值')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关系
    vehicle_model = db.relationship('VehicleModel', back_populates='requirement_details')

    def to_dict(self):
        return {
            'id': self.id,
            'requirement_id': self.requirement_id,
            'vehicle_model_id': self.vehicle_model_id,
            'vehicle_model_name': self.vehicle_model.name if self.vehicle_model else None,
            'feature_support': self.feature_support,
            'function_status': self.function_status,
            'channel_count': self.channel_count,
            'power_value': self.power_value,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
