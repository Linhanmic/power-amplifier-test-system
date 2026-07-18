from flask import request
from flask_restful import Resource
from app.models import db
from app.models.test_case import TestCase, TestCaseGroup, TestCaseVehicle
from app.models.gauge import GaugeScenario


class TestCaseGroupListApi(Resource):
    def get(self):
        """获取测试用例分组树"""
        groups = TestCaseGroup.query.filter_by(parent_id=None).order_by(TestCaseGroup.sort_order).all()
        return [g.to_dict() for g in groups]

    def post(self):
        """创建测试用例分组"""
        data = request.get_json()
        group = TestCaseGroup(
            parent_id=data.get('parent_id'),
            name=data.get('name'),
            code=data.get('code'),
            description=data.get('description'),
            sort_order=data.get('sort_order', 0),
            level=data.get('level', 0)
        )
        db.session.add(group)
        db.session.commit()
        return group.to_dict(), 201


class TestCaseGroupApi(Resource):
    def get(self, group_id):
        """获取单个分组"""
        group = TestCaseGroup.query.get_or_404(group_id)
        return group.to_dict()

    def put(self, group_id):
        """更新分组"""
        group = TestCaseGroup.query.get_or_404(group_id)
        data = request.get_json()
        group.name = data.get('name', group.name)
        group.code = data.get('code', group.code)
        group.description = data.get('description', group.description)
        group.sort_order = data.get('sort_order', group.sort_order)
        group.level = data.get('level', group.level)
        db.session.commit()
        return group.to_dict()

    def delete(self, group_id):
        """删除分组"""
        group = TestCaseGroup.query.get_or_404(group_id)
        db.session.delete(group)
        db.session.commit()
        return {'message': '删除成功'}


class TestCaseListApi(Resource):
    def get(self):
        """获取测试用例列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        keyword = request.args.get('keyword', '')
        group_id = request.args.get('group_id', type=int)
        level = request.args.get('level', '')
        status = request.args.get('status', '')
        requirement_id = request.args.get('requirement_id', type=int)

        query = TestCase.query

        if keyword:
            query = query.filter(TestCase.case_name.contains(keyword) | TestCase.case_code.contains(keyword))
        if group_id:
            query = query.filter_by(group_id=group_id)
        if level:
            query = query.filter_by(level=level)
        if status:
            query = query.filter_by(status=status)
        if requirement_id:
            query = query.filter(TestCase.requirements.any(id=requirement_id))

        # 按用例ID排序
        pagination = query.order_by(TestCase.case_code.asc()).paginate(page=page, per_page=per_page)
        return {
            'items': [t.to_dict() for t in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page
        }

    def post(self):
        """创建测试用例"""
        data = request.get_json()
        test_case = TestCase(
            case_code=data.get('case_code'),
            group_id=data.get('group_id'),
            case_name=data.get('case_name'),
            test_purpose=data.get('test_purpose'),
            level=data.get('level'),
            preconditions=data.get('preconditions'),
            test_steps=data.get('test_steps'),
            expected_results=data.get('expected_results'),
            tags=data.get('tags'),
            designer=data.get('designer'),
            design_date=data.get('design_date'),
            publish_date=data.get('publish_date'),
            status=data.get('status', 'Draft'),
            gauge_scenario_id=data.get('gauge_scenario_id'),
            can_matrix_id=data.get('can_matrix_id')
        )

        # 处理多需求关联
        requirement_ids = data.get('requirement_ids', [])
        if requirement_ids:
            from app.models.requirement import Requirement
            requirements = Requirement.query.filter(Requirement.id.in_(requirement_ids)).all()
            test_case.requirements = requirements

        db.session.add(test_case)
        db.session.commit()
        return test_case.to_dict(), 201


class TestCaseApi(Resource):
    def get(self, case_id):
        """获取单个测试用例"""
        test_case = TestCase.query.get_or_404(case_id)
        return test_case.to_dict()

    def put(self, case_id):
        """更新测试用例"""
        test_case = TestCase.query.get_or_404(case_id)
        data = request.get_json()

        test_case.case_code = data.get('case_code', test_case.case_code)
        test_case.group_id = data.get('group_id', test_case.group_id)
        test_case.case_name = data.get('case_name', test_case.case_name)
        test_case.test_purpose = data.get('test_purpose', test_case.test_purpose)
        test_case.level = data.get('level', test_case.level)
        test_case.preconditions = data.get('preconditions', test_case.preconditions)
        test_case.test_steps = data.get('test_steps', test_case.test_steps)
        test_case.expected_results = data.get('expected_results', test_case.expected_results)
        test_case.tags = data.get('tags', test_case.tags)
        test_case.designer = data.get('designer', test_case.designer)
        test_case.design_date = data.get('design_date', test_case.design_date)
        test_case.publish_date = data.get('publish_date', test_case.publish_date)
        test_case.status = data.get('status', test_case.status)
        test_case.gauge_scenario_id = data.get('gauge_scenario_id', test_case.gauge_scenario_id)
        test_case.can_matrix_id = data.get('can_matrix_id', test_case.can_matrix_id)

        # 处理多需求关联
        if 'requirement_ids' in data:
            from app.models.requirement import Requirement
            requirement_ids = data.get('requirement_ids', [])
            requirements = Requirement.query.filter(Requirement.id.in_(requirement_ids)).all()
            test_case.requirements = requirements

        db.session.commit()
        return test_case.to_dict()

    def delete(self, case_id):
        """删除测试用例"""
        test_case = TestCase.query.get_or_404(case_id)
        db.session.delete(test_case)
        db.session.commit()
        return {'message': '删除成功'}


class TestCaseVehicleApi(Resource):
    def post(self, case_id):
        """添加测试用例车型关联"""
        test_case = TestCase.query.get_or_404(case_id)
        data = request.get_json()
        vehicle = TestCaseVehicle(
            test_case_id=case_id,
            vehicle_config_id=data.get('vehicle_config_id'),
            expected_result=data.get('expected_result')
        )
        db.session.add(vehicle)
        db.session.commit()
        return vehicle.to_dict(), 201

    def delete(self, case_id, vehicle_id):
        """删除测试用例车型关联"""
        vehicle = TestCaseVehicle.query.get_or_404(vehicle_id)
        db.session.delete(vehicle)
        db.session.commit()
        return {'message': '删除成功'}


class TestCaseGaugeScenarioListApi(Resource):
    def get(self):
        """获取Gauge场景列表（用于下拉选择）"""
        spec_id = request.args.get('spec_id', type=int)
        query = GaugeScenario.query.filter_by(status='active')
        if spec_id:
            query = query.filter_by(spec_id=spec_id)
        scenarios = query.order_by(GaugeScenario.execution_order).all()
        return [{
            'id': s.id,
            'scenario_name': s.scenario_name,
            'spec_id': s.spec_id,
            'spec_code': s.spec.spec_code if s.spec else None,
            'spec_name': s.spec.spec_name if s.spec else None,
            'project_name': s.spec.project.name if s.spec and s.spec.project else None
        } for s in scenarios]


# 注册路由
from . import api
api.add_resource(TestCaseGroupListApi, '/test-case-groups')
api.add_resource(TestCaseGroupApi, '/test-case-groups/<int:group_id>')
api.add_resource(TestCaseListApi, '/test-cases')
api.add_resource(TestCaseApi, '/test-cases/<int:case_id>')
api.add_resource(TestCaseVehicleApi, '/test-cases/<int:case_id>/vehicles', '/test-cases/<int:case_id>/vehicles/<int:vehicle_id>')
api.add_resource(TestCaseGaugeScenarioListApi, '/test-case-gauge-scenarios')
