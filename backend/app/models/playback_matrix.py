import json
from datetime import datetime
from . import db


class PlaybackMatrix(db.Model):
    __tablename__ = 'playback_matrices'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_config_id = db.Column(db.Integer, db.ForeignKey('vehicle_configs.id'), nullable=False)
    matrix_name = db.Column(db.String(100), nullable=False, comment='矩阵名称')
    matrix_type = db.Column(db.String(20), default='base', comment='矩阵类型: base/condition')
    description = db.Column(db.Text, comment='描述')
    status = db.Column(db.String(20), default='active', comment='状态')
    version = db.Column(db.String(20), default='1.0', comment='版本')
    created_by = db.Column(db.String(50), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    base_matrices = db.relationship('PlaybackMatrixBase', backref='playback_matrix', lazy='dynamic')
    conditions = db.relationship('PlaybackMatrixCondition', backref='playback_matrix', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_config_id': self.vehicle_config_id,
            'vehicle_config_name': self.vehicle_config.config_name if self.vehicle_config else None,
            'matrix_name': self.matrix_name,
            'matrix_type': self.matrix_type,
            'description': self.description,
            'status': self.status,
            'version': self.version,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'base_count': self.base_matrices.count(),
            'condition_count': self.conditions.count()
        }


class PlaybackMatrixBase(db.Model):
    __tablename__ = 'playback_matrix_base'

    id = db.Column(db.Integer, primary_key=True)
    matrix_id = db.Column(db.Integer, db.ForeignKey('playback_matrices.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('a2b_slots.id'), nullable=False)
    audio_source_id = db.Column(db.Integer, db.ForeignKey('audio_source_types.id'), nullable=False)
    is_enabled = db.Column(db.Boolean, default=True, comment='是否启用')
    channel_count = db.Column(db.Integer, default=2, comment='通道数')
    volume_level = db.Column(db.Integer, default=50, comment='音量等级')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关系
    slot = db.relationship('A2BSlot', backref='matrix_entries')
    audio_source = db.relationship('AudioSourceType', backref='matrix_entries')

    def to_dict(self):
        return {
            'id': self.id,
            'matrix_id': self.matrix_id,
            'slot_id': self.slot_id,
            'slot_name': self.slot.slot_name if self.slot else None,
            'audio_source_id': self.audio_source_id,
            'audio_source_name': self.audio_source.source_name if self.audio_source else None,
            'is_enabled': self.is_enabled,
            'channel_count': self.channel_count,
            'volume_level': self.volume_level,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PlaybackMatrixCondition(db.Model):
    __tablename__ = 'playback_matrix_conditions'

    id = db.Column(db.Integer, primary_key=True)
    matrix_id = db.Column(db.Integer, db.ForeignKey('playback_matrices.id'), nullable=False)
    condition_name = db.Column(db.String(100), nullable=False, comment='条件名称')
    condition_type = db.Column(db.String(20), comment='条件类型')
    condition_value = db.Column(db.Text, comment='条件值(JSON)')
    playback_config = db.Column(db.Text, nullable=False, comment='播放配置(JSON)')
    description = db.Column(db.Text, comment='描述')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def condition_value_dict(self):
        if self.condition_value:
            return json.loads(self.condition_value)
        return {}

    @condition_value_dict.setter
    def condition_value_dict(self, value):
        self.condition_value = json.dumps(value, ensure_ascii=False)

    @property
    def playback_config_dict(self):
        if self.playback_config:
            return json.loads(self.playback_config)
        return {}

    @playback_config_dict.setter
    def playback_config_dict(self, value):
        self.playback_config = json.dumps(value, ensure_ascii=False)

    def to_dict(self):
        return {
            'id': self.id,
            'matrix_id': self.matrix_id,
            'condition_name': self.condition_name,
            'condition_type': self.condition_type,
            'condition_value': self.condition_value_dict,
            'playback_config': self.playback_config_dict,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
