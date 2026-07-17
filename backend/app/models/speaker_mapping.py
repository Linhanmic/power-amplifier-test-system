import json
from datetime import datetime
from . import db


class SpeakerChannelMapping(db.Model):
    __tablename__ = 'speaker_channel_mappings'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_config_id = db.Column(db.Integer, db.ForeignKey('vehicle_configs.id'), nullable=False)
    speaker_name = db.Column(db.String(50), nullable=False, comment='喇叭名称')
    speaker_position = db.Column(db.String(50), comment='喇叭位置')
    channel_type = db.Column(db.String(20), comment='通道类型: analog/digital')
    channel_number = db.Column(db.Integer, comment='通道号')
    channel_name = db.Column(db.String(50), comment='通道名称')
    power = db.Column(db.Float, comment='功率(W)')
    impedance = db.Column(db.Float, comment='阻抗(Ω)')
    frequency_range = db.Column(db.String(50), comment='频率范围')
    a2b_slot_ids = db.Column(db.Text, comment='A2B Slot ID列表(JSON)')
    can_signal_name = db.Column(db.String(100), comment='CAN信号名称')
    status = db.Column(db.String(20), default='active', comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def a2b_slot_ids_list(self):
        if self.a2b_slot_ids:
            return json.loads(self.a2b_slot_ids)
        return []

    @a2b_slot_ids_list.setter
    def a2b_slot_ids_list(self, value):
        self.a2b_slot_ids = json.dumps(value, ensure_ascii=False)

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_config_id': self.vehicle_config_id,
            'vehicle_config_name': self.vehicle_config.config_name if self.vehicle_config else None,
            'speaker_name': self.speaker_name,
            'speaker_position': self.speaker_position,
            'channel_type': self.channel_type,
            'channel_number': self.channel_number,
            'channel_name': self.channel_name,
            'power': self.power,
            'impedance': self.impedance,
            'frequency_range': self.frequency_range,
            'a2b_slot_ids': self.a2b_slot_ids_list,
            'can_signal_name': self.can_signal_name,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
