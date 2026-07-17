from datetime import datetime
from . import db


class VehicleModel(db.Model):
    __tablename__ = 'vehicle_models'

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, comment='车型名称')
    code = db.Column(db.String(50), nullable=False, unique=True, comment='车型编码')
    model_year = db.Column(db.String(10), comment='年款')
    status = db.Column(db.String(20), default='active', comment='状态')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    configs = db.relationship('VehicleConfig', backref='vehicle_model', lazy='dynamic')
    requirement_details = db.relationship('RequirementVehicleDetail', backref='vehicle_model', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'platform_id': self.platform_id,
            'platform_name': self.platform.name if self.platform else None,
            'name': self.name,
            'code': self.code,
            'model_year': self.model_year,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class VehicleConfig(db.Model):
    __tablename__ = 'vehicle_configs'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_model_id = db.Column(db.Integer, db.ForeignKey('vehicle_models.id'), nullable=False)
    config_name = db.Column(db.String(100), nullable=False, comment='配置名称')
    config_code = db.Column(db.String(50), nullable=False, comment='配置编码')
    speaker_count = db.Column(db.Integer, comment='扬声器数量')
    has_subwoofer = db.Column(db.Boolean, default=False, comment='是否有低音炮')
    has_dsp = db.Column(db.Boolean, default=False, comment='是否有DSP')
    amplifier_power = db.Column(db.Float, comment='功放功率')
    status = db.Column(db.String(20), default='active', comment='状态')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    speaker_mappings = db.relationship('SpeakerChannelMapping', backref='vehicle_config', lazy='dynamic')
    playback_matrices = db.relationship('PlaybackMatrix', backref='vehicle_config', lazy='dynamic')
    test_case_vehicles = db.relationship('TestCaseVehicle', backref='vehicle_config', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_model_id': self.vehicle_model_id,
            'vehicle_model_name': self.vehicle_model.name if self.vehicle_model else None,
            'config_name': self.config_name,
            'config_code': self.config_code,
            'speaker_count': self.speaker_count,
            'has_subwoofer': self.has_subwoofer,
            'has_dsp': self.has_dsp,
            'amplifier_power': self.amplifier_power,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
