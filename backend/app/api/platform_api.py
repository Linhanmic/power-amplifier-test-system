from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.platform import Platform


class PlatformListAPI(Resource):
    def get(self):
        """获取平台列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        keyword = request.args.get('keyword')

        query = Platform.query
        if status:
            query = query.filter_by(status=status)
        if keyword:
            query = query.filter(
                Platform.name.contains(keyword) | Platform.code.contains(keyword)
            )

        pagination = query.order_by(Platform.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'items': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建平台"""
        data = request.get_json()
        if not data or not data.get('name') or not data.get('code'):
            return {'error': '名称和编码必填'}, 400

        if Platform.query.filter_by(code=data['code']).first():
            return {'error': '平台编码已存在'}, 400

        platform = Platform(
            name=data['name'],
            code=data['code'],
            status=data.get('status', 'active'),
            remark=data.get('remark')
        )
        db.session.add(platform)
        db.session.commit()
        return platform.to_dict(), 201


class PlatformAPI(Resource):
    def get(self, platform_id):
        """获取单个平台"""
        platform = Platform.query.get_or_404(platform_id)
        return platform.to_dict()

    def put(self, platform_id):
        """更新平台"""
        platform = Platform.query.get_or_404(platform_id)
        data = request.get_json()

        if data.get('name'):
            platform.name = data['name']
        if data.get('code'):
            existing = Platform.query.filter_by(code=data['code']).first()
            if existing and existing.id != platform_id:
                return {'error': '平台编码已存在'}, 400
            platform.code = data['code']
        if 'status' in data:
            platform.status = data['status']
        if 'remark' in data:
            platform.remark = data['remark']

        db.session.commit()
        return platform.to_dict()

    def delete(self, platform_id):
        """删除平台"""
        platform = Platform.query.get_or_404(platform_id)
        if platform.vehicle_models.count() > 0:
            return {'error': '该平台下存在车型，无法删除'}, 400

        db.session.delete(platform)
        db.session.commit()
        return {'message': '删除成功'}


api.add_resource(PlatformListAPI, '/platforms')
api.add_resource(PlatformAPI, '/platforms/<int:platform_id>')
