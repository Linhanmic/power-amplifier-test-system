from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.can_matrix import CANMatrix, SignalDefinition


class CANMatrixListAPI(Resource):
    def get(self):
        """获取CAN矩阵列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        matrix_type = request.args.get('matrix_type')
        keyword = request.args.get('keyword')

        query = CANMatrix.query
        if status:
            query = query.filter_by(status=status)
        if matrix_type:
            query = query.filter_by(matrix_type=matrix_type)
        if keyword:
            query = query.filter(CANMatrix.matrix_name.contains(keyword))

        pagination = query.order_by(CANMatrix.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'items': [m.to_dict() for m in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建CAN矩阵"""
        data = request.get_json()
        if not data or not data.get('matrix_name'):
            return {'error': '矩阵名称必填'}, 400

        matrix = CANMatrix(
            matrix_name=data['matrix_name'],
            matrix_type=data.get('matrix_type'),
            dbc_file_path=data.get('dbc_file_path'),
            description=data.get('description'),
            version=data.get('version'),
            status=data.get('status', 'active'),
            created_by=data.get('created_by')
        )
        db.session.add(matrix)
        db.session.commit()
        return matrix.to_dict(), 201


class CANMatrixAPI(Resource):
    def get(self, matrix_id):
        """获取单个CAN矩阵"""
        matrix = CANMatrix.query.get_or_404(matrix_id)
        result = matrix.to_dict()
        result['signals'] = [s.to_dict() for s in matrix.signals]
        return result

    def put(self, matrix_id):
        """更新CAN矩阵"""
        matrix = CANMatrix.query.get_or_404(matrix_id)
        data = request.get_json()

        if data.get('matrix_name'):
            matrix.matrix_name = data['matrix_name']
        if 'matrix_type' in data:
            matrix.matrix_type = data['matrix_type']
        if 'dbc_file_path' in data:
            matrix.dbc_file_path = data['dbc_file_path']
        if 'description' in data:
            matrix.description = data['description']
        if 'version' in data:
            matrix.version = data['version']
        if 'status' in data:
            matrix.status = data['status']

        db.session.commit()
        return matrix.to_dict()

    def delete(self, matrix_id):
        """删除CAN矩阵"""
        matrix = CANMatrix.query.get_or_404(matrix_id)
        if matrix.test_cases.count() > 0:
            return {'error': '该矩阵已关联测试用例，无法删除'}, 400

        SignalDefinition.query.filter_by(matrix_id=matrix_id).delete()
        db.session.delete(matrix)
        db.session.commit()
        return {'message': '删除成功'}


class SignalDefinitionListAPI(Resource):
    def get(self):
        """获取信号定义列表"""
        matrix_id = request.args.get('matrix_id', type=int)
        if not matrix_id:
            return {'error': 'matrix_id必填'}, 400

        signals = SignalDefinition.query.filter_by(matrix_id=matrix_id).order_by(
            SignalDefinition.message_id, SignalDefinition.start_bit
        ).all()

        return [s.to_dict() for s in signals]

    def post(self):
        """创建信号定义"""
        data = request.get_json()
        required_fields = ['matrix_id', 'signal_name', 'message_id']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        signal = SignalDefinition(
            matrix_id=data['matrix_id'],
            signal_name=data['signal_name'],
            message_id=data['message_id'],
            message_name=data.get('message_name'),
            signal_type=data.get('signal_type'),
            data_length=data.get('data_length'),
            start_bit=data.get('start_bit'),
            factor=data.get('factor', 1.0),
            offset=data.get('offset', 0.0),
            min_value=data.get('min_value'),
            max_value=data.get('max_value'),
            unit=data.get('unit'),
            value_table=data.get('value_table'),
            status=data.get('status', 'active')
        )
        db.session.add(signal)
        db.session.commit()
        return signal.to_dict(), 201


class SignalDefinitionAPI(Resource):
    def get(self, signal_id):
        """获取单个信号定义"""
        signal = SignalDefinition.query.get_or_404(signal_id)
        return signal.to_dict()

    def put(self, signal_id):
        """更新信号定义"""
        signal = SignalDefinition.query.get_or_404(signal_id)
        data = request.get_json()

        if data.get('signal_name'):
            signal.signal_name = data['signal_name']
        if data.get('message_id'):
            signal.message_id = data['message_id']
        if 'message_name' in data:
            signal.message_name = data['message_name']
        if 'signal_type' in data:
            signal.signal_type = data['signal_type']
        if 'data_length' in data:
            signal.data_length = data['data_length']
        if 'start_bit' in data:
            signal.start_bit = data['start_bit']
        if 'factor' in data:
            signal.factor = data['factor']
        if 'offset' in data:
            signal.offset = data['offset']
        if 'min_value' in data:
            signal.min_value = data['min_value']
        if 'max_value' in data:
            signal.max_value = data['max_value']
        if 'unit' in data:
            signal.unit = data['unit']
        if 'value_table' in data:
            signal.value_table = data['value_table']
        if 'status' in data:
            signal.status = data['status']

        db.session.commit()
        return signal.to_dict()

    def delete(self, signal_id):
        """删除信号定义"""
        signal = SignalDefinition.query.get_or_404(signal_id)
        db.session.delete(signal)
        db.session.commit()
        return {'message': '删除成功'}


api.add_resource(CANMatrixListAPI, '/can-matrices')
api.add_resource(CANMatrixAPI, '/can-matrices/<int:matrix_id>')
api.add_resource(SignalDefinitionListAPI, '/signal-definitions')
api.add_resource(SignalDefinitionAPI, '/signal-definitions/<int:signal_id>')
