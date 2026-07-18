from datetime import datetime
from . import db


class Requirement(db.Model):
    __tablename__ = 'requirements'

    id = db.Column(db.Integer, primary_key=True)
    req_code = db.Column(db.String(50), nullable=False, unique=True, comment='需求编号')
    title = db.Column(db.String(200), nullable=False, comment='需求标题')
    description = db.Column(db.Text, comment='需求详情')
    verification_scope = db.Column(db.Text, comment='验证范围')
    verification_criteria = db.Column(db.Text, comment='验证准则')
    priority = db.Column(db.String(20), comment='优先级')
    status = db.Column(db.String(20), default='draft', comment='状态')
    designer = db.Column(db.String(50), comment='编制人')
    design_date = db.Column(db.Date, comment='编制日期')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    vehicle_details = db.relationship('RequirementVehicleDetail', backref='requirement', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'req_code': self.req_code,
            'title': self.title,
            'description': self.description,
            'verification_scope': self.verification_scope,
            'verification_criteria': self.verification_criteria,
            'priority': self.priority,
            'status': self.status,
            'designer': self.designer,
            'design_date': self.design_date.isoformat() if self.design_date else None,
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
    difference_description = db.Column(db.Text, comment='差异描述')
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
            'difference_description': self.difference_description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
