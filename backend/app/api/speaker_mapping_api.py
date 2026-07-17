from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.speaker_mapping import SpeakerChannelMapping


class SpeakerMappingListAPI(Resource):
    def get(self):
        """获取扬声器映射列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        vehicle_config_id = request.args.get('vehicle_config_id', type=int)
        status = request.args.get('status')

        query = SpeakerChannelMapping.query
        if vehicle_config_id:
            query = query.filter_by(vehicle_config_id=vehicle_config_id)
        if status:
            query = query.filter_by(status=status)

        pagination = query.order_by(SpeakerChannelMapping.channel_number).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'items': [m.to_dict() for m in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建扬声器映射"""
        data = request.get_json()
        required_fields = ['vehicle_config_id', 'speaker_name', 'channel_number']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        mapping = SpeakerChannelMapping(
            vehicle_config_id=data['vehicle_config_id'],
            speaker_name=data['speaker_name'],
            speaker_position=data.get('speaker_position'),
            channel_type=data.get('channel_type'),
            channel_number=data['channel_number'],
            channel_name=data.get('channel_name'),
            power=data.get('power'),
            impedance=data.get('impedance'),
            frequency_range=data.get('frequency_range'),
            a2b_slot_ids=data.get('a2b_slot_ids'),
            can_signal_name=data.get('can_signal_name'),
            status=data.get('status', 'active')
        )
        db.session.add(mapping)
        db.session.commit()
        return mapping.to_dict(), 201


class SpeakerMappingAPI(Resource):
    def get(self, mapping_id):
        """获取单个扬声器映射"""
        mapping = SpeakerChannelMapping.query.get_or_404(mapping_id)
        return mapping.to_dict()

    def put(self, mapping_id):
        """更新扬声器映射"""
        mapping = SpeakerChannelMapping.query.get_or_404(mapping_id)
        data = request.get_json()

        if data.get('speaker_name'):
            mapping.speaker_name = data['speaker_name']
        if 'speaker_position' in data:
            mapping.speaker_position = data['speaker_position']
        if 'channel_type' in data:
            mapping.channel_type = data['channel_type']
        if data.get('channel_number'):
            mapping.channel_number = data['channel_number']
        if 'channel_name' in data:
            mapping.channel_name = data['channel_name']
        if 'power' in data:
            mapping.power = data['power']
        if 'impedance' in data:
            mapping.impedance = data['impedance']
        if 'frequency_range' in data:
            mapping.frequency_range = data['frequency_range']
        if 'a2b_slot_ids' in data:
            mapping.a2b_slot_ids = data['a2b_slot_ids']
        if 'can_signal_name' in data:
            mapping.can_signal_name = data['can_signal_name']
        if 'status' in data:
            mapping.status = data['status']

        db.session.commit()
        return mapping.to_dict()

    def delete(self, mapping_id):
        """删除扬声器映射"""
        mapping = SpeakerChannelMapping.query.get_or_404(mapping_id)
        db.session.delete(mapping)
        db.session.commit()
        return {'message': '删除成功'}


api.add_resource(SpeakerMappingListAPI, '/speaker-mappings')
api.add_resource(SpeakerMappingAPI, '/speaker-mappings/<int:mapping_id>')
