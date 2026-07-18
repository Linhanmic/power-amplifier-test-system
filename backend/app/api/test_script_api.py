from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.test_script import TestScript, TestScenario, ScenarioParameter, ScenarioDataTable


class TestScriptListAPI(Resource):
    def get(self):
        """获取脚本列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        keyword = request.args.get('keyword')

        query = TestScript.query
        if status:
            query = query.filter_by(status=status)
        if keyword:
            query = query.filter(
                TestScript.title.contains(keyword) | TestScript.script_code.contains(keyword)
            )

        pagination = query.order_by(TestScript.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'items': [s.to_dict() for s in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建脚本"""
        data = request.get_json()
        required_fields = ['script_code', 'title']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        if TestScript.query.filter_by(script_code=data['script_code']).first():
            return {'error': '脚本编号已存在'}, 400

        script = TestScript(
            script_code=data['script_code'],
            title=data['title'],
            script_path=data.get('script_path'),
            tags=data.get('tags'),
            status=data.get('status', 'draft'),
            version=data.get('version', '1.0'),
            remark=data.get('remark'),
            created_by=data.get('created_by')
        )
        db.session.add(script)
        db.session.commit()
        return script.to_dict(), 201


class TestScriptAPI(Resource):
    def get(self, script_id):
        """获取单个脚本"""
        script = TestScript.query.get_or_404(script_id)
        return script.to_dict()

    def put(self, script_id):
        """更新脚本"""
        script = TestScript.query.get_or_404(script_id)
        data = request.get_json()

        if data.get('script_code'):
            existing = TestScript.query.filter_by(script_code=data['script_code']).first()
            if existing and existing.id != script_id:
                return {'error': '脚本编号已存在'}, 400
            script.script_code = data['script_code']
        if data.get('title'):
            script.title = data['title']
        if 'script_path' in data:
            script.script_path = data['script_path']
        if 'tags' in data:
            script.tags = data['tags']
        if 'status' in data:
            script.status = data['status']
        if 'version' in data:
            script.version = data['version']
        if 'remark' in data:
            script.remark = data['remark']

        db.session.commit()
        return script.to_dict()

    def delete(self, script_id):
        """删除脚本"""
        script = TestScript.query.get_or_404(script_id)
        if script.test_cases.count() > 0:
            return {'error': '该脚本已关联测试用例，无法删除'}, 400

        # 删除关联的场景和参数
        for scenario in script.scenarios:
            ScenarioParameter.query.filter_by(scenario_id=scenario.id).delete()
            ScenarioDataTable.query.filter_by(scenario_id=scenario.id).delete()
        TestScenario.query.filter_by(script_id=script_id).delete()

        db.session.delete(script)
        db.session.commit()
        return {'message': '删除成功'}


class TestScenarioListAPI(Resource):
    def get(self):
        """获取场景列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        script_id = request.args.get('script_id', type=int)
        keyword = request.args.get('keyword', '')
        status = request.args.get('status', '')

        query = TestScenario.query

        if script_id:
            query = query.filter_by(script_id=script_id)
        if keyword:
            query = query.filter(TestScenario.scenario_name.contains(keyword))
        if status:
            query = query.filter_by(status=status)

        pagination = query.order_by(TestScenario.script_id, TestScenario.execution_order).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'items': [s.to_dict() for s in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建场景"""
        data = request.get_json()
        required_fields = ['script_id', 'scenario_name']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        scenario = TestScenario(
            script_id=data['script_id'],
            scenario_name=data['scenario_name'],
            spec_file=data.get('spec_file'),
            scenario_type=data.get('scenario_type'),
            table_driven=data.get('scenario_type') == 'table_driven',
            value_table=data.get('value_table'),
            execution_order=data.get('execution_order', 0),
            timeout=data.get('timeout', 60000),
            status=data.get('status', 'active'),
            remark=data.get('remark')
        )
        db.session.add(scenario)
        db.session.flush()

        # 添加参数
        parameters = data.get('parameters', [])
        for p in parameters:
            param = ScenarioParameter(
                scenario_id=scenario.id,
                param_name=p['param_name'],
                param_value=p.get('param_value'),
                param_type=p.get('param_type', 'string'),
                is_required=p.get('is_required', False),
                description=p.get('description')
            )
            db.session.add(param)

        # 添加数据表
        data_tables = data.get('data_tables', [])
        for dt in data_tables:
            table = ScenarioDataTable(
                scenario_id=scenario.id,
                row_name=dt['row_name'],
                data_value=dt.get('data_value'),
                description=dt.get('description')
            )
            db.session.add(table)

        db.session.commit()
        return scenario.to_dict(), 201


class TestScenarioAPI(Resource):
    def get(self, scenario_id):
        """获取单个场景"""
        scenario = TestScenario.query.get_or_404(scenario_id)
        return scenario.to_dict()

    def put(self, scenario_id):
        """更新场景"""
        scenario = TestScenario.query.get_or_404(scenario_id)
        data = request.get_json()

        if data.get('scenario_name'):
            scenario.scenario_name = data['scenario_name']
        if 'spec_file' in data:
            scenario.spec_file = data['spec_file']
        if 'scenario_type' in data:
            scenario.scenario_type = data['scenario_type']
        if 'table_driven' in data:
            scenario.table_driven = data['table_driven']
        if 'value_table' in data:
            scenario.value_table = data['value_table']
        if 'execution_order' in data:
            scenario.execution_order = data['execution_order']
        if 'timeout' in data:
            scenario.timeout = data['timeout']
        if 'status' in data:
            scenario.status = data['status']
        if 'remark' in data:
            scenario.remark = data['remark']

        # 更新参数
        if 'parameters' in data:
            ScenarioParameter.query.filter_by(scenario_id=scenario_id).delete()
            for p in data['parameters']:
                param = ScenarioParameter(
                    scenario_id=scenario_id,
                    param_name=p['param_name'],
                    param_value=p.get('param_value'),
                    param_type=p.get('param_type', 'string'),
                    is_required=p.get('is_required', False),
                    description=p.get('description')
                )
                db.session.add(param)

        # 更新数据表
        if 'data_tables' in data:
            ScenarioDataTable.query.filter_by(scenario_id=scenario_id).delete()
            for dt in data['data_tables']:
                table = ScenarioDataTable(
                    scenario_id=scenario_id,
                    row_name=dt['row_name'],
                    data_value=dt.get('data_value'),
                    description=dt.get('description')
                )
                db.session.add(table)

        db.session.commit()
        return scenario.to_dict()

    def delete(self, scenario_id):
        """删除场景"""
        scenario = TestScenario.query.get_or_404(scenario_id)
        ScenarioParameter.query.filter_by(scenario_id=scenario_id).delete()
        ScenarioDataTable.query.filter_by(scenario_id=scenario_id).delete()
        db.session.delete(scenario)
        db.session.commit()
        return {'message': '删除成功'}


class ScenarioParameterAPI(Resource):
    def post(self):
        """创建场景参数"""
        data = request.get_json()
        required_fields = ['scenario_id', 'param_name']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        param = ScenarioParameter(
            scenario_id=data['scenario_id'],
            param_name=data['param_name'],
            param_value=data.get('param_value'),
            param_type=data.get('param_type', 'string'),
            is_required=data.get('is_required', False),
            description=data.get('description')
        )
        db.session.add(param)
        db.session.commit()
        return param.to_dict(), 201

    def put(self, param_id):
        """更新场景参数"""
        param = ScenarioParameter.query.get_or_404(param_id)
        data = request.get_json()

        if data.get('param_name'):
            param.param_name = data['param_name']
        if 'param_value' in data:
            param.param_value = data['param_value']
        if 'param_type' in data:
            param.param_type = data['param_type']
        if 'is_required' in data:
            param.is_required = data['is_required']
        if 'description' in data:
            param.description = data['description']

        db.session.commit()
        return param.to_dict()

    def delete(self, param_id):
        """删除场景参数"""
        param = ScenarioParameter.query.get_or_404(param_id)
        db.session.delete(param)
        db.session.commit()
        return {'message': '删除成功'}


api.add_resource(TestScriptListAPI, '/test-scripts')
api.add_resource(TestScriptAPI, '/test-scripts/<int:script_id>')
api.add_resource(TestScenarioListAPI, '/test-scenarios')
api.add_resource(TestScenarioAPI, '/test-scenarios/<int:scenario_id>')
api.add_resource(ScenarioParameterAPI, '/scenario-parameters', '/scenario-parameters/<int:param_id>')
