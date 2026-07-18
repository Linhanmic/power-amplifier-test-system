from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.test_case import TestCaseGroup, TestCase, TestCaseVehicle, test_case_requirements
from ..models.requirement import Requirement


class TestCaseGroupListAPI(Resource):
    def get(self):
        """获取用例分组树"""
        parent_id = request.args.get('parent_id', type=int)
        if parent_id:
            groups = TestCaseGroup.query.filter_by(parent_id=parent_id).order_by(
                TestCaseGroup.sort_order
            ).all()
        else:
            groups = TestCaseGroup.query.filter_by(parent_id=None).order_by(
                TestCaseGroup.sort_order
            ).all()

        return [g.to_dict() for g in groups]

    def post(self):
        """创建用例分组"""
        data = request.get_json()
        if not data or not data.get('name'):
            return {'error': '分组名称必填'}, 400

        group = TestCaseGroup(
            parent_id=data.get('parent_id'),
            name=data['name'],
            description=data.get('description'),
            sort_order=data.get('sort_order', 0),
            level=data.get('level', 0),
            status=data.get('status', 'active')
        )
        db.session.add(group)
        db.session.commit()
        return group.to_dict(), 201


class TestCaseGroupAPI(Resource):
    def get(self, group_id):
        """获取单个分组"""
        group = TestCaseGroup.query.get_or_404(group_id)
        result = group.to_dict()
        result['test_cases'] = [tc.to_dict() for tc in group.test_cases]
        return result

    def put(self, group_id):
        """更新分组"""
        group = TestCaseGroup.query.get_or_404(group_id)
        data = request.get_json()

        if data.get('name'):
            group.name = data['name']
        if 'parent_id' in data:
            group.parent_id = data['parent_id']
        if 'description' in data:
            group.description = data['description']
        if 'sort_order' in data:
            group.sort_order = data['sort_order']
        if 'level' in data:
            group.level = data['level']
        if 'status' in data:
            group.status = data['status']

        db.session.commit()
        return group.to_dict()

    def delete(self, group_id):
        """删除分组"""
        group = TestCaseGroup.query.get_or_404(group_id)
        if group.children.count() > 0:
            return {'error': '该分组下存在子分组，无法删除'}, 400
        if group.test_cases.count() > 0:
            return {'error': '该分组下存在测试用例，无法删除'}, 400

        db.session.delete(group)
        db.session.commit()
        return {'message': '删除成功'}


class TestCaseListAPI(Resource):
    def get(self):
        """获取测试用例列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        group_id = request.args.get('group_id', type=int)
        status = request.args.get('status')
        level = request.args.get('level')
        keyword = request.args.get('keyword')

        query = TestCase.query
        if group_id:
            query = query.filter_by(group_id=group_id)
        if status:
            query = query.filter_by(status=status)
        if level:
            query = query.filter_by(level=level)
        if keyword:
            query = query.filter(
                TestCase.case_name.contains(keyword) | TestCase.case_code.contains(keyword)
            )

        pagination = query.order_by(TestCase.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'items': [tc.to_dict() for tc in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建测试用例"""
        data = request.get_json()
        required_fields = ['case_code', 'group_id', 'case_name', 'test_steps', 'expected_results']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        if TestCase.query.filter_by(case_code=data['case_code']).first():
            return {'error': '用例编号已存在'}, 400

        test_case = TestCase(
            case_code=data['case_code'],
            group_id=data['group_id'],
            case_name=data['case_name'],
            test_purpose=data.get('test_purpose'),
            preconditions=data.get('preconditions'),
            test_steps=data['test_steps'],
            expected_results=data['expected_results'],
            level=data.get('level'),
            tags=data.get('tags'),
            designer=data.get('designer'),
            design_date=data.get('design_date'),
            publish_date=data.get('publish_date'),
            status=data.get('status', 'Draft'),
            script_id=data.get('script_id'),
            can_matrix_id=data.get('can_matrix_id')
        )
        db.session.add(test_case)
        db.session.flush()

        # 添加需求关联（多对多）
        requirement_ids = data.get('requirement_ids', [])
        for req_id in requirement_ids:
            req = Requirement.query.get(req_id)
            if req:
                test_case.requirements.append(req)

        # 添加车型关联
        vehicles = data.get('vehicles', [])
        for v in vehicles:
            tv = TestCaseVehicle(
                test_case_id=test_case.id,
                vehicle_config_id=v['vehicle_config_id'],
                expected_result=v.get('expected_result')
            )
            db.session.add(tv)

        db.session.commit()
        return test_case.to_dict(), 201


class TestCaseAPI(Resource):
    def get(self, case_id):
        """获取单个测试用例"""
        test_case = TestCase.query.get_or_404(case_id)
        return test_case.to_dict()

    def put(self, case_id):
        """更新测试用例"""
        test_case = TestCase.query.get_or_404(case_id)
        data = request.get_json()

        if data.get('case_code'):
            existing = TestCase.query.filter_by(case_code=data['case_code']).first()
            if existing and existing.id != case_id:
                return {'error': '用例编号已存在'}, 400
            test_case.case_code = data['case_code']
        if data.get('group_id'):
            test_case.group_id = data['group_id']
        if data.get('case_name'):
            test_case.case_name = data['case_name']
        if 'test_purpose' in data:
            test_case.test_purpose = data['test_purpose']
        if 'preconditions' in data:
            test_case.preconditions = data['preconditions']
        if data.get('test_steps'):
            test_case.test_steps = data['test_steps']
        if data.get('expected_results'):
            test_case.expected_results = data['expected_results']
        if 'level' in data:
            test_case.level = data['level']
        if 'tags' in data:
            test_case.tags = data['tags']
        if 'designer' in data:
            test_case.designer = data['designer']
        if 'design_date' in data:
            test_case.design_date = data['design_date']
        if 'publish_date' in data:
            test_case.publish_date = data['publish_date']
        if 'status' in data:
            test_case.status = data['status']
        if 'script_id' in data:
            test_case.script_id = data['script_id']
        if 'can_matrix_id' in data:
            test_case.can_matrix_id = data['can_matrix_id']

        # 更新需求关联（多对多）
        if 'requirement_ids' in data:
            test_case.requirements.clear()
            for req_id in data['requirement_ids']:
                req = Requirement.query.get(req_id)
                if req:
                    test_case.requirements.append(req)

        # 更新车型关联
        if 'vehicles' in data:
            TestCaseVehicle.query.filter_by(test_case_id=case_id).delete()
            for v in data['vehicles']:
                tv = TestCaseVehicle(
                    test_case_id=case_id,
                    vehicle_config_id=v['vehicle_config_id'],
                    expected_result=v.get('expected_result')
                )
                db.session.add(tv)

        db.session.commit()
        return test_case.to_dict()

    def delete(self, case_id):
        """删除测试用例"""
        test_case = TestCase.query.get_or_404(case_id)
        TestCaseVehicle.query.filter_by(test_case_id=case_id).delete()
        db.session.delete(test_case)
        db.session.commit()
        return {'message': '删除成功'}


api.add_resource(TestCaseGroupListAPI, '/test-case-groups')
api.add_resource(TestCaseGroupAPI, '/test-case-groups/<int:group_id>')
api.add_resource(TestCaseListAPI, '/test-cases')
api.add_resource(TestCaseAPI, '/test-cases/<int:case_id>')
