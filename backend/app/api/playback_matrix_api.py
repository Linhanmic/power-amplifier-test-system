from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.playback_matrix import PlaybackMatrix, PlaybackMatrixEntry


class PlaybackMatrixListAPI(Resource):
    def get(self):
        """获取播放矩阵列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        vehicle_config_id = request.args.get('vehicle_config_id', type=int)
        keyword = request.args.get('keyword', '')
        status = request.args.get('status', '')

        query = PlaybackMatrix.query
        if vehicle_config_id:
            query = query.filter_by(vehicle_config_id=vehicle_config_id)
        if keyword:
            query = query.filter(PlaybackMatrix.matrix_name.contains(keyword))
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
            description=data.get('description'),
            status=data.get('status', 'active'),
            version=data.get('version', '1.0'),
            created_by=data.get('created_by')
        )
        db.session.add(matrix)
        db.session.flush()

        # 添加条目
        entries = data.get('entries', [])
        for i, entry_data in enumerate(entries):
            entry = PlaybackMatrixEntry(
                matrix_id=matrix.id,
                audio_source=entry_data['audio_source'],
                a2b_channel=entry_data.get('a2b_channel'),
                playback_position=entry_data.get('playback_position'),
                headrest_mode=entry_data.get('headrest_mode'),
                speaker_channels=entry_data.get('speaker_channels'),
                sort_order=i + 1
            )
            db.session.add(entry)

        db.session.commit()
        return matrix.to_detail_dict(), 201


class PlaybackMatrixAPI(Resource):
    def get(self, matrix_id):
        """获取单个播放矩阵"""
        matrix = PlaybackMatrix.query.get_or_404(matrix_id)
        return matrix.to_detail_dict()

    def put(self, matrix_id):
        """更新播放矩阵"""
        matrix = PlaybackMatrix.query.get_or_404(matrix_id)
        data = request.get_json()

        if data.get('matrix_name'):
            matrix.matrix_name = data['matrix_name']
        if 'description' in data:
            matrix.description = data['description']
        if 'status' in data:
            matrix.status = data['status']
        if 'version' in data:
            matrix.version = data['version']

        # 更新条目
        if 'entries' in data:
            # 删除旧条目
            PlaybackMatrixEntry.query.filter_by(matrix_id=matrix_id).delete()
            # 添加新条目
            for i, entry_data in enumerate(data['entries']):
                entry = PlaybackMatrixEntry(
                    matrix_id=matrix_id,
                    audio_source=entry_data['audio_source'],
                    a2b_channel=entry_data.get('a2b_channel'),
                    playback_position=entry_data.get('playback_position'),
                    headrest_mode=entry_data.get('headrest_mode'),
                    speaker_channels=entry_data.get('speaker_channels'),
                    sort_order=i + 1
                )
                db.session.add(entry)

        db.session.commit()
        return matrix.to_detail_dict()

    def delete(self, matrix_id):
        """删除播放矩阵"""
        matrix = PlaybackMatrix.query.get_or_404(matrix_id)
        PlaybackMatrixEntry.query.filter_by(matrix_id=matrix_id).delete()
        db.session.delete(matrix)
        db.session.commit()
        return {'message': '删除成功'}


class PlaybackMatrixEntryAPI(Resource):
    def post(self):
        """创建条目"""
        data = request.get_json()
        required_fields = ['matrix_id', 'audio_source']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        # 获取当前最大排序
        max_order = db.session.query(db.func.max(PlaybackMatrixEntry.sort_order)).filter_by(
            matrix_id=data['matrix_id']).scalar() or 0

        entry = PlaybackMatrixEntry(
            matrix_id=data['matrix_id'],
            audio_source=data['audio_source'],
            a2b_channel=data.get('a2b_channel'),
            playback_position=data.get('playback_position'),
            headrest_mode=data.get('headrest_mode'),
            speaker_channels=data.get('speaker_channels'),
            sort_order=data.get('sort_order', max_order + 1)
        )
        db.session.add(entry)
        db.session.commit()
        return entry.to_dict(), 201

    def put(self, entry_id):
        """更新条目"""
        entry = PlaybackMatrixEntry.query.get_or_404(entry_id)
        data = request.get_json()

        if 'audio_source' in data:
            entry.audio_source = data['audio_source']
        if 'a2b_channel' in data:
            entry.a2b_channel = data['a2b_channel']
        if 'playback_position' in data:
            entry.playback_position = data['playback_position']
        if 'headrest_mode' in data:
            entry.headrest_mode = data['headrest_mode']
        if 'speaker_channels' in data:
            entry.speaker_channels = data['speaker_channels']
        if 'sort_order' in data:
            entry.sort_order = data['sort_order']
        if 'status' in data:
            entry.status = data['status']

        db.session.commit()
        return entry.to_dict()

    def delete(self, entry_id):
        """删除条目"""
        entry = PlaybackMatrixEntry.query.get_or_404(entry_id)
        db.session.delete(entry)
        db.session.commit()
        return {'message': '删除成功'}


# 注册路由
api.add_resource(PlaybackMatrixListAPI, '/playback-matrices')
api.add_resource(PlaybackMatrixAPI, '/playback-matrices/<int:matrix_id>')
api.add_resource(PlaybackMatrixEntryAPI, '/playback-matrix-entries', '/playback-matrix-entries/<int:entry_id>')
