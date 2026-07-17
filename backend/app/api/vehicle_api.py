from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.vehicle import VehicleModel, VehicleConfig


class VehicleModelListAPI(Resource):
    def get(self):
        """获取车型列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        platform_id = request.args.get('platform_id', type=int)
        status = request.args.get('status')
        keyword = request.args.get('keyword')

        query = VehicleModel.query
        if platform_id:
            query = query.filter_by(platform_id=platform_id)
        if status:
            query = query.filter_by(status=status)
        if keyword:
            query = query.filter(
                VehicleModel.name.contains(keyword) | VehicleModel.code.contains(keyword)
            )

        pagination = query.order_by(VehicleModel.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'items': [v.to_dict() for v in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建车型"""
        data = request.get_json()
        required_fields = ['platform_id', 'name', 'code']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        if VehicleModel.query.filter_by(code=data['code']).first():
            return {'error': '车型编码已存在'}, 400

        vehicle = VehicleModel(
            platform_id=data['platform_id'],
            name=data['name'],
            code=data['code'],
            model_year=data.get('model_year'),
            status=data.get('status', 'active'),
            remark=data.get('remark')
        )
        db.session.add(vehicle)
        db.session.commit()
        return vehicle.to_dict(), 201


class VehicleModelAPI(Resource):
    def get(self, vehicle_id):
        """获取单个车型"""
        vehicle = VehicleModel.query.get_or_404(vehicle_id)
        return vehicle.to_dict()

    def put(self, vehicle_id):
        """更新车型"""
        vehicle = VehicleModel.query.get_or_404(vehicle_id)
        data = request.get_json()

        if data.get('platform_id'):
            vehicle.platform_id = data['platform_id']
        if data.get('name'):
            vehicle.name = data['name']
        if data.get('code'):
            existing = VehicleModel.query.filter_by(code=data['code']).first()
            if existing and existing.id != vehicle_id:
                return {'error': '车型编码已存在'}, 400
            vehicle.code = data['code']
        if 'model_year' in data:
            vehicle.model_year = data['model_year']
        if 'status' in data:
            vehicle.status = data['status']
        if 'remark' in data:
            vehicle.remark = data['remark']

        db.session.commit()
        return vehicle.to_dict()

    def delete(self, vehicle_id):
        """删除车型"""
        vehicle = VehicleModel.query.get_or_404(vehicle_id)
        if vehicle.configs.count() > 0:
            return {'error': '该车型下存在配置，无法删除'}, 400

        db.session.delete(vehicle)
        db.session.commit()
        return {'message': '删除成功'}


class VehicleConfigListAPI(Resource):
    def get(self):
        """获取车辆配置列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        vehicle_model_id = request.args.get('vehicle_model_id', type=int)
        status = request.args.get('status')

        query = VehicleConfig.query
        if vehicle_model_id:
            query = query.filter_by(vehicle_model_id=vehicle_model_id)
        if status:
            query = query.filter_by(status=status)

        pagination = query.order_by(VehicleConfig.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'items': [c.to_dict() for c in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建车辆配置"""
        data = request.get_json()
        required_fields = ['vehicle_model_id', 'config_name', 'config_code']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        config = VehicleConfig(
            vehicle_model_id=data['vehicle_model_id'],
            config_name=data['config_name'],
            config_code=data['config_code'],
            speaker_count=data.get('speaker_count'),
            has_subwoofer=data.get('has_subwoofer', False),
            has_dsp=data.get('has_dsp', False),
            amplifier_power=data.get('amplifier_power'),
            status=data.get('status', 'active'),
            remark=data.get('remark')
        )
        db.session.add(config)
        db.session.commit()
        return config.to_dict(), 201


class VehicleConfigAPI(Resource):
    def get(self, config_id):
        """获取单个车辆配置"""
        config = VehicleConfig.query.get_or_404(config_id)
        return config.to_dict()

    def put(self, config_id):
        """更新车辆配置"""
        config = VehicleConfig.query.get_or_404(config_id)
        data = request.get_json()

        if data.get('vehicle_model_id'):
            config.vehicle_model_id = data['vehicle_model_id']
        if data.get('config_name'):
            config.config_name = data['config_name']
        if data.get('config_code'):
            config.config_code = data['config_code']
        if 'speaker_count' in data:
            config.speaker_count = data['speaker_count']
        if 'has_subwoofer' in data:
            config.has_subwoofer = data['has_subwoofer']
        if 'has_dsp' in data:
            config.has_dsp = data['has_dsp']
        if 'amplifier_power' in data:
            config.amplifier_power = data['amplifier_power']
        if 'status' in data:
            config.status = data['status']
        if 'remark' in data:
            config.remark = data['remark']

        db.session.commit()
        return config.to_dict()

    def delete(self, config_id):
        """删除车辆配置"""
        config = VehicleConfig.query.get_or_404(config_id)
        db.session.delete(config)
        db.session.commit()
        return {'message': '删除成功'}


api.add_resource(VehicleModelListAPI, '/vehicle-models')
api.add_resource(VehicleModelAPI, '/vehicle-models/<int:vehicle_id>')
api.add_resource(VehicleConfigListAPI, '/vehicle-configs')
api.add_resource(VehicleConfigAPI, '/vehicle-configs/<int:config_id>')
