from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.audio_source import A2BSlot, AudioSourceType, AudioSourceSlotMapping


class A2BSlotListAPI(Resource):
    def get(self):
        """获取A2B Slot列表"""
        slots = A2BSlot.query.filter_by(status='active').order_by(A2BSlot.slot_number).all()
        return [s.to_dict() for s in slots]

    def post(self):
        """创建A2B Slot"""
        data = request.get_json()
        required_fields = ['slot_name', 'slot_number']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        if A2BSlot.query.filter_by(slot_name=data['slot_name']).first():
            return {'error': 'Slot名称已存在'}, 400

        slot = A2BSlot(
            slot_name=data['slot_name'],
            slot_number=data['slot_number'],
            slot_type=data.get('slot_type'),
            max_channels=data.get('max_channels'),
            description=data.get('description'),
            status=data.get('status', 'active')
        )
        db.session.add(slot)
        db.session.commit()
        return slot.to_dict(), 201


class A2BSlotAPI(Resource):
    def get(self, slot_id):
        """获取单个A2B Slot"""
        slot = A2BSlot.query.get_or_404(slot_id)
        return slot.to_dict()

    def put(self, slot_id):
        """更新A2B Slot"""
        slot = A2BSlot.query.get_or_404(slot_id)
        data = request.get_json()

        if data.get('slot_name'):
            existing = A2BSlot.query.filter_by(slot_name=data['slot_name']).first()
            if existing and existing.id != slot_id:
                return {'error': 'Slot名称已存在'}, 400
            slot.slot_name = data['slot_name']
        if data.get('slot_number'):
            slot.slot_number = data['slot_number']
        if 'slot_type' in data:
            slot.slot_type = data['slot_type']
        if 'max_channels' in data:
            slot.max_channels = data['max_channels']
        if 'description' in data:
            slot.description = data['description']
        if 'status' in data:
            slot.status = data['status']

        db.session.commit()
        return slot.to_dict()

    def delete(self, slot_id):
        """删除A2B Slot"""
        slot = A2BSlot.query.get_or_404(slot_id)
        slot.status = 'inactive'
        db.session.commit()
        return {'message': '删除成功'}


class AudioSourceTypeListAPI(Resource):
    def get(self):
        """获取音源类型列表"""
        sources = AudioSourceType.query.filter_by(status='active').all()
        return [s.to_dict() for s in sources]

    def post(self):
        """创建音源类型"""
        data = request.get_json()
        required_fields = ['source_name', 'source_code']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        if AudioSourceType.query.filter_by(source_code=data['source_code']).first():
            return {'error': '音源编码已存在'}, 400

        source = AudioSourceType(
            source_name=data['source_name'],
            source_code=data['source_code'],
            description=data.get('description'),
            status=data.get('status', 'active')
        )
        db.session.add(source)
        db.session.commit()
        return source.to_dict(), 201


class AudioSourceTypeAPI(Resource):
    def get(self, source_id):
        """获取单个音源类型"""
        source = AudioSourceType.query.get_or_404(source_id)
        return source.to_dict()

    def put(self, source_id):
        """更新音源类型"""
        source = AudioSourceType.query.get_or_404(source_id)
        data = request.get_json()

        if data.get('source_name'):
            source.source_name = data['source_name']
        if data.get('source_code'):
            existing = AudioSourceType.query.filter_by(source_code=data['source_code']).first()
            if existing and existing.id != source_id:
                return {'error': '音源编码已存在'}, 400
            source.source_code = data['source_code']
        if 'description' in data:
            source.description = data['description']
        if 'status' in data:
            source.status = data['status']

        db.session.commit()
        return source.to_dict()

    def delete(self, source_id):
        """删除音源类型"""
        source = AudioSourceType.query.get_or_404(source_id)
        source.status = 'inactive'
        db.session.commit()
        return {'message': '删除成功'}


class AudioSourceSlotMappingListAPI(Resource):
    def get(self):
        """获取音源Slot映射列表"""
        audio_source_id = request.args.get('audio_source_id', type=int)
        a2b_slot_id = request.args.get('a2b_slot_id', type=int)

        query = AudioSourceSlotMapping.query
        if audio_source_id:
            query = query.filter_by(audio_source_id=audio_source_id)
        if a2b_slot_id:
            query = query.filter_by(a2b_slot_id=a2b_slot_id)

        mappings = query.order_by(AudioSourceSlotMapping.priority).all()
        return [m.to_dict() for m in mappings]

    def post(self):
        """创建音源Slot映射"""
        data = request.get_json()
        required_fields = ['audio_source_id', 'a2b_slot_id']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        mapping = AudioSourceSlotMapping(
            audio_source_id=data['audio_source_id'],
            a2b_slot_id=data['a2b_slot_id'],
            priority=data.get('priority', 0),
            is_default=data.get('is_default', False),
            remark=data.get('remark')
        )
        db.session.add(mapping)
        db.session.commit()
        return mapping.to_dict(), 201


class AudioSourceSlotMappingAPI(Resource):
    def delete(self, mapping_id):
        """删除音源Slot映射"""
        mapping = AudioSourceSlotMapping.query.get_or_404(mapping_id)
        db.session.delete(mapping)
        db.session.commit()
        return {'message': '删除成功'}


api.add_resource(A2BSlotListAPI, '/a2b-slots')
api.add_resource(A2BSlotAPI, '/a2b-slots/<int:slot_id>')
api.add_resource(AudioSourceTypeListAPI, '/audio-source-types')
api.add_resource(AudioSourceTypeAPI, '/audio-source-types/<int:source_id>')
api.add_resource(AudioSourceSlotMappingListAPI, '/audio-source-slot-mappings')
api.add_resource(AudioSourceSlotMappingAPI, '/audio-source-slot-mappings/<int:mapping_id>')
