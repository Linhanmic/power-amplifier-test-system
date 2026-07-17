from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.requirement import Requirement, RequirementVehicleDetail
from ..models.vehicle import VehicleModel


class RequirementListAPI(Resource):
    def get(self):
        """获取需求列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        category = request.args.get('category')
        keyword = request.args.get('keyword')

        query = Requirement.query
        if status:
            query = query.filter_by(status=status)
        if category:
            query = query.filter_by(category=category)
        if keyword:
            query = query.filter(
                Requirement.title.contains(keyword) | Requirement.req_code.contains(keyword)
            )

        pagination = query.order_by(Requirement.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'items': [r.to_dict() for r in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建需求"""
        data = request.get_json()
        required_fields = ['req_code', 'title']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        if Requirement.query.filter_by(req_code=data['req_code']).first():
            return {'error': '需求编号已存在'}, 400

        requirement = Requirement(
            req_code=data['req_code'],
            title=data['title'],
            description=data.get('description'),
            category=data.get('category'),
            priority=data.get('priority'),
            status=data.get('status', 'draft'),
            created_by=data.get('created_by')
        )
        db.session.add(requirement)
        db.session.flush()

        # 添加车型详情
        vehicle_details = data.get('vehicle_details', [])
        for detail in vehicle_details:
            vd = RequirementVehicleDetail(
                requirement_id=requirement.id,
                vehicle_model_id=detail['vehicle_model_id'],
                feature_support=detail.get('feature_support'),
                function_status=detail.get('function_status'),
                channel_count=detail.get('channel_count'),
                power_value=detail.get('power_value'),
                remark=detail.get('remark')
            )
            db.session.add(vd)

        db.session.commit()
        return requirement.to_dict(), 201


class RequirementAPI(Resource):
    def get(self, req_id):
        """获取单个需求"""
        requirement = Requirement.query.get_or_404(req_id)
        return requirement.to_dict()

    def put(self, req_id):
        """更新需求"""
        requirement = Requirement.query.get_or_404(req_id)
        data = request.get_json()

        if data.get('req_code'):
            existing = Requirement.query.filter_by(req_code=data['req_code']).first()
            if existing and existing.id != req_id:
                return {'error': '需求编号已存在'}, 400
            requirement.req_code = data['req_code']
        if data.get('title'):
            requirement.title = data['title']
        if 'description' in data:
            requirement.description = data['description']
        if 'category' in data:
            requirement.category = data['category']
        if 'priority' in data:
            requirement.priority = data['priority']
        if 'status' in data:
            requirement.status = data['status']
        if 'created_by' in data:
            requirement.created_by = data['created_by']

        # 更新车型详情
        if 'vehicle_details' in data:
            # 删除旧详情
            RequirementVehicleDetail.query.filter_by(requirement_id=req_id).delete()
            # 添加新详情
            for detail in data['vehicle_details']:
                vd = RequirementVehicleDetail(
                    requirement_id=req_id,
                    vehicle_model_id=detail['vehicle_model_id'],
                    feature_support=detail.get('feature_support'),
                    function_status=detail.get('function_status'),
                    channel_count=detail.get('channel_count'),
                    power_value=detail.get('power_value'),
                    remark=detail.get('remark')
                )
                db.session.add(vd)

        db.session.commit()
        return requirement.to_dict()

    def delete(self, req_id):
        """删除需求"""
        requirement = Requirement.query.get_or_404(req_id)
        if requirement.test_cases.count() > 0:
            return {'error': '该需求已关联测试用例，无法删除'}, 400

        # 删除车型详情
        RequirementVehicleDetail.query.filter_by(requirement_id=req_id).delete()
        db.session.delete(requirement)
        db.session.commit()
        return {'message': '删除成功'}


api.add_resource(RequirementListAPI, '/requirements')
api.add_resource(RequirementAPI, '/requirements/<int:req_id>')
