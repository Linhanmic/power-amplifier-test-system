import json
from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.playback_matrix import PlaybackMatrix, PlaybackMatrixBase, PlaybackMatrixCondition


class PlaybackMatrixListAPI(Resource):
    def get(self):
        """获取播放矩阵列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        vehicle_config_id = request.args.get('vehicle_config_id', type=int)
        matrix_type = request.args.get('matrix_type')
        status = request.args.get('status')

        query = PlaybackMatrix.query
        if vehicle_config_id:
            query = query.filter_by(vehicle_config_id=vehicle_config_id)
        if matrix_type:
            query = query.filter_by(matrix_type=matrix_type)
        if status:
            query = query.filter_by(status=status)

        pagination = query.order_by(PlaybackMatrix.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'items': [m.to_dict() for m in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建播放矩阵"""
        data = request.get_json()
        required_fields = ['vehicle_config_id', 'matrix_name']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        matrix = PlaybackMatrix(
            vehicle_config_id=data['vehicle_config_id'],
            matrix_name=data['matrix_name'],
            matrix_type=data.get('matrix_type', 'base'),
            description=data.get('description'),
            status=data.get('status', 'active'),
            version=data.get('version', '1.0'),
            created_by=data.get('created_by')
        )
        db.session.add(matrix)
        db.session.commit()
        return matrix.to_dict(), 201


class PlaybackMatrixAPI(Resource):
    def get(self, matrix_id):
        """获取单个播放矩阵"""
        matrix = PlaybackMatrix.query.get_or_404(matrix_id)
        result = matrix.to_dict()
        result['base_entries'] = [b.to_dict() for b in matrix.base_matrices]
        result['conditions'] = [c.to_dict() for c in matrix.conditions]
        return result

    def put(self, matrix_id):
        """更新播放矩阵"""
        matrix = PlaybackMatrix.query.get_or_404(matrix_id)
        data = request.get_json()

        if data.get('matrix_name'):
            matrix.matrix_name = data['matrix_name']
        if 'matrix_type' in data:
            matrix.matrix_type = data['matrix_type']
        if 'description' in data:
            matrix.description = data['description']
        if 'status' in data:
            matrix.status = data['status']
        if 'version' in data:
            matrix.version = data['version']

        db.session.commit()
        return matrix.to_dict()

    def delete(self, matrix_id):
        """删除播放矩阵"""
        matrix = PlaybackMatrix.query.get_or_404(matrix_id)
        PlaybackMatrixBase.query.filter_by(matrix_id=matrix_id).delete()
        PlaybackMatrixCondition.query.filter_by(matrix_id=matrix_id).delete()
        db.session.delete(matrix)
        db.session.commit()
        return {'message': '删除成功'}


class PlaybackMatrixBaseListAPI(Resource):
    def get(self):
        """获取基础矩阵列表"""
        matrix_id = request.args.get('matrix_id', type=int)
        if not matrix_id:
            return {'error': 'matrix_id必填'}, 400

        entries = PlaybackMatrixBase.query.filter_by(matrix_id=matrix_id).all()
        return [e.to_dict() for e in entries]

    def post(self):
        """创建基础矩阵条目"""
        data = request.get_json()
        required_fields = ['matrix_id', 'slot_id', 'audio_source_id']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        entry = PlaybackMatrixBase(
            matrix_id=data['matrix_id'],
            slot_id=data['slot_id'],
            audio_source_id=data['audio_source_id'],
            is_enabled=data.get('is_enabled', True),
            channel_count=data.get('channel_count', 2),
            volume_level=data.get('volume_level', 50),
            remark=data.get('remark')
        )
        db.session.add(entry)
        db.session.commit()
        return entry.to_dict(), 201


class PlaybackMatrixBaseAPI(Resource):
    def put(self, entry_id):
        """更新基础矩阵条目"""
        entry = PlaybackMatrixBase.query.get_or_404(entry_id)
        data = request.get_json()

        if data.get('slot_id'):
            entry.slot_id = data['slot_id']
        if data.get('audio_source_id'):
            entry.audio_source_id = data['audio_source_id']
        if 'is_enabled' in data:
            entry.is_enabled = data['is_enabled']
        if 'channel_count' in data:
            entry.channel_count = data['channel_count']
        if 'volume_level' in data:
            entry.volume_level = data['volume_level']
        if 'remark' in data:
            entry.remark = data['remark']

        db.session.commit()
        return entry.to_dict()

    def delete(self, entry_id):
        """删除基础矩阵条目"""
        entry = PlaybackMatrixBase.query.get_or_404(entry_id)
        db.session.delete(entry)
        db.session.commit()
        return {'message': '删除成功'}


class PlaybackMatrixConditionListAPI(Resource):
    def get(self):
        """获取条件矩阵列表"""
        matrix_id = request.args.get('matrix_id', type=int)
        if not matrix_id:
            return {'error': 'matrix_id必填'}, 400

        conditions = PlaybackMatrixCondition.query.filter_by(matrix_id=matrix_id).all()
        return [c.to_dict() for c in conditions]

    def post(self):
        """创建条件矩阵"""
        data = request.get_json()
        required_fields = ['matrix_id', 'condition_name', 'playback_config']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        condition = PlaybackMatrixCondition(
            matrix_id=data['matrix_id'],
            condition_name=data['condition_name'],
            condition_type=data.get('condition_type'),
            condition_value=json.dumps(data.get('condition_value', {}), ensure_ascii=False),
            playback_config=json.dumps(data['playback_config'], ensure_ascii=False),
            description=data.get('description'),
            is_active=data.get('is_active', True)
        )
        db.session.add(condition)
        db.session.commit()
        return condition.to_dict(), 201


class PlaybackMatrixConditionAPI(Resource):
    def get(self, condition_id):
        """获取单个条件矩阵"""
        condition = PlaybackMatrixCondition.query.get_or_404(condition_id)
        return condition.to_dict()

    def put(self, condition_id):
        """更新条件矩阵"""
        condition = PlaybackMatrixCondition.query.get_or_404(condition_id)
        data = request.get_json()

        if data.get('condition_name'):
            condition.condition_name = data['condition_name']
        if 'condition_type' in data:
            condition.condition_type = data['condition_type']
        if 'condition_value' in data:
            condition.condition_value = json.dumps(data['condition_value'], ensure_ascii=False)
        if 'playback_config' in data:
            condition.playback_config = json.dumps(data['playback_config'], ensure_ascii=False)
        if 'description' in data:
            condition.description = data['description']
        if 'is_active' in data:
            condition.is_active = data['is_active']

        db.session.commit()
        return condition.to_dict()

    def delete(self, condition_id):
        """删除条件矩阵"""
        condition = PlaybackMatrixCondition.query.get_or_404(condition_id)
        db.session.delete(condition)
        db.session.commit()
        return {'message': '删除成功'}


api.add_resource(PlaybackMatrixListAPI, '/playback-matrices')
api.add_resource(PlaybackMatrixAPI, '/playback-matrices/<int:matrix_id>')
api.add_resource(PlaybackMatrixBaseListAPI, '/playback-matrix-base')
api.add_resource(PlaybackMatrixBaseAPI, '/playback-matrix-base/<int:entry_id>')
api.add_resource(PlaybackMatrixConditionListAPI, '/playback-matrix-conditions')
api.add_resource(PlaybackMatrixConditionAPI, '/playback-matrix-conditions/<int:condition_id>')
