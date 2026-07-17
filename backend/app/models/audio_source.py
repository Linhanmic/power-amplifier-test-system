import json
from datetime import datetime
from . import db


class A2BSlot(db.Model):
    __tablename__ = 'a2b_slots'

    id = db.Column(db.Integer, primary_key=True)
    slot_name = db.Column(db.String(50), nullable=False, unique=True, comment='Slot名称')
    slot_number = db.Column(db.Integer, nullable=False, comment='Slot编号')
    slot_type = db.Column(db.String(20), comment='Slot类型')
    max_channels = db.Column(db.Integer, comment='最大通道数')
    description = db.Column(db.Text, comment='描述')
    status = db.Column(db.String(20), default='active', comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关系
    audio_mappings = db.relationship('AudioSourceSlotMapping', back_populates='a2b_slot', lazy='dynamic')
    matrix_entries = db.relationship('PlaybackMatrixBase', back_populates='slot', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'slot_name': self.slot_name,
            'slot_number': self.slot_number,
            'slot_type': self.slot_type,
            'max_channels': self.max_channels,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AudioSourceType(db.Model):
    __tablename__ = 'audio_source_types'

    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(50), nullable=False, unique=True, comment='音源名称')
    source_code = db.Column(db.String(20), nullable=False, unique=True, comment='音源编码')
    description = db.Column(db.Text, comment='描述')
    status = db.Column(db.String(20), default='active', comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关系
    slot_mappings = db.relationship('AudioSourceSlotMapping', back_populates='audio_source', lazy='dynamic')
    matrix_entries = db.relationship('PlaybackMatrixBase', back_populates='audio_source', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'source_name': self.source_name,
            'source_code': self.source_code,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AudioSourceSlotMapping(db.Model):
    __tablename__ = 'audio_source_slot_mappings'

    id = db.Column(db.Integer, primary_key=True)
    audio_source_id = db.Column(db.Integer, db.ForeignKey('audio_source_types.id'), nullable=False)
    a2b_slot_id = db.Column(db.Integer, db.ForeignKey('a2b_slots.id'), nullable=False)
    priority = db.Column(db.Integer, default=0, comment='优先级')
    is_default = db.Column(db.Boolean, default=False, comment='是否默认')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关系
    a2b_slot = db.relationship('A2BSlot', back_populates='audio_mappings')
    audio_source = db.relationship('AudioSourceType', back_populates='slot_mappings')

    def to_dict(self):
        return {
            'id': self.id,
            'audio_source_id': self.audio_source_id,
            'audio_source_name': self.audio_source.source_name if self.audio_source else None,
            'a2b_slot_id': self.a2b_slot_id,
            'a2b_slot_name': self.a2b_slot.slot_name if self.a2b_slot else None,
            'priority': self.priority,
            'is_default': self.is_default,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
