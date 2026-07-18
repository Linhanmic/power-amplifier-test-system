import json
from datetime import datetime
from . import db


class PlaybackMatrix(db.Model):
    """播放矩阵"""
    __tablename__ = 'playback_matrices'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_config_id = db.Column(db.Integer, db.ForeignKey('vehicle_configs.id'), nullable=False)
    matrix_name = db.Column(db.String(100), nullable=False, comment='矩阵名称')
    description = db.Column(db.Text, comment='描述')
    status = db.Column(db.String(20), default='active', comment='状态')
    version = db.Column(db.String(20), default='1.0', comment='版本')
    created_by = db.Column(db.String(50), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    vehicle_config = db.relationship('VehicleConfig', back_populates='playback_matrices')
    entries = db.relationship('PlaybackMatrixEntry', backref='matrix', lazy='dynamic',
                             order_by='PlaybackMatrixEntry.sort_order')

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_config_id': self.vehicle_config_id,
            'vehicle_config_name': self.vehicle_config.config_name if self.vehicle_config else None,
            'matrix_name': self.matrix_name,
            'description': self.description,
            'status': self.status,
            'version': self.version,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'entry_count': self.entries.count()
        }

    def to_detail_dict(self):
        """包含条目的详细信息"""
        result = self.to_dict()
        result['entries'] = [e.to_dict() for e in self.entries]
        return result


class PlaybackMatrixEntry(db.Model):
    """播放矩阵条目"""
    __tablename__ = 'playback_matrix_entries'

    id = db.Column(db.Integer, primary_key=True)
    matrix_id = db.Column(db.Integer, db.ForeignKey('playback_matrices.id'), nullable=False)

    # 基本信息
    audio_source = db.Column(db.String(50), nullable=False, comment='音源类型')
    a2b_channel = db.Column(db.String(50), comment='A2B通道')
    playback_position = db.Column(db.String(100), comment='播出方位')
    headrest_mode = db.Column(db.String(20), comment='头枕模式: 关闭/头枕环绕/驾享模式/独享模式/不判断头枕模式')

    # 扬声器通道配置 (JSON格式存储)
    speaker_channels = db.Column(db.Text, comment='扬声器通道配置(JSON)')

    # 排序和状态
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    status = db.Column(db.String(20), default='active', comment='状态')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def speaker_channels_dict(self):
        if self.speaker_channels:
            return json.loads(self.speaker_channels)
        return {}

    @speaker_channels_dict.setter
    def speaker_channels_dict(self, value):
        self.speaker_channels = json.dumps(value, ensure_ascii=False)

    def to_dict(self):
        return {
            'id': self.id,
            'matrix_id': self.matrix_id,
            'audio_source': self.audio_source,
            'a2b_channel': self.a2b_channel,
            'playback_position': self.playback_position,
            'headrest_mode': self.headrest_mode,
            'speaker_channels': self.speaker_channels_dict,
            'sort_order': self.sort_order,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
