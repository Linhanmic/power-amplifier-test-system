import json
from datetime import datetime
from . import db


class CANMatrix(db.Model):
    __tablename__ = 'can_matrices'

    id = db.Column(db.Integer, primary_key=True)
    matrix_name = db.Column(db.String(100), nullable=False, comment='矩阵名称')
    matrix_type = db.Column(db.String(20), comment='矩阵类型')
    dbc_file_path = db.Column(db.String(500), comment='DBC文件路径')
    description = db.Column(db.Text, comment='描述')
    version = db.Column(db.String(20), comment='版本')
    status = db.Column(db.String(20), default='active', comment='状态')
    created_by = db.Column(db.String(50), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    signals = db.relationship('SignalDefinition', backref='matrix', lazy='dynamic')
    test_cases = db.relationship('TestCase', backref='can_matrix', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'matrix_name': self.matrix_name,
            'matrix_type': self.matrix_type,
            'dbc_file_path': self.dbc_file_path,
            'description': self.description,
            'version': self.version,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'signal_count': self.signals.count()
        }


class SignalDefinition(db.Model):
    __tablename__ = 'signal_definitions'

    id = db.Column(db.Integer, primary_key=True)
    matrix_id = db.Column(db.Integer, db.ForeignKey('can_matrices.id'), nullable=False)
    signal_name = db.Column(db.String(100), nullable=False, comment='信号名称')
    message_id = db.Column(db.String(20), comment='报文ID')
    message_name = db.Column(db.String(100), comment='报文名称')
    signal_type = db.Column(db.String(20), comment='信号类型')
    data_length = db.Column(db.Integer, comment='数据长度(bit)')
    start_bit = db.Column(db.Integer, comment='起始位')
    factor = db.Column(db.Float, default=1.0, comment='系数')
    offset = db.Column(db.Float, default=0.0, comment='偏移量')
    min_value = db.Column(db.Float, comment='最小值')
    max_value = db.Column(db.Float, comment='最大值')
    unit = db.Column(db.String(20), comment='单位')
    value_table = db.Column(db.Text, comment='值表(JSON)')
    status = db.Column(db.String(20), default='active', comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'matrix_id': self.matrix_id,
            'signal_name': self.signal_name,
            'message_id': self.message_id,
            'message_name': self.message_name,
            'signal_type': self.signal_type,
            'data_length': self.data_length,
            'start_bit': self.start_bit,
            'factor': self.factor,
            'offset': self.offset,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'unit': self.unit,
            'value_table': json.loads(self.value_table) if self.value_table else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
