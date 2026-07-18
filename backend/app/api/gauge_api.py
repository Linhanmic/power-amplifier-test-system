from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.gauge import GaugeProject, GaugeSpec, GaugeScenario, GaugeStep, GaugeTable


# ==================== Project API ====================
class GaugeProjectListAPI(Resource):
    def get(self):
        """获取Gauge项目列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        keyword = request.args.get('keyword', '')
        status = request.args.get('status', '')

        query = GaugeProject.query
        if keyword:
            query = query.filter(GaugeProject.name.contains(keyword) | GaugeProject.project_code.contains(keyword))
        if status:
            query = query.filter_by(status=status)

        pagination = query.order_by(GaugeProject.project_code.asc()).paginate(page=page, per_page=per_page)
        return {
            'items': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建Gauge项目"""
        data = request.get_json()
        required_fields = ['project_code', 'name']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        if GaugeProject.query.filter_by(project_code=data['project_code']).first():
            return {'error': '项目编号已存在'}, 400

        project = GaugeProject(
            project_code=data['project_code'],
            name=data['name'],
            description=data.get('description'),
            root_path=data.get('root_path'),
            gauge_version=data.get('gauge_version'),
            status=data.get('status', 'active'),
            created_by=data.get('created_by')
        )
        db.session.add(project)
        db.session.commit()
        return project.to_dict(), 201


class GaugeProjectAPI(Resource):
    def get(self, project_id):
        """获取单个Gauge项目"""
        project = GaugeProject.query.get_or_404(project_id)
        return project.to_dict()

    def put(self, project_id):
        """更新Gauge项目"""
        project = GaugeProject.query.get_or_404(project_id)
        data = request.get_json()

        if data.get('project_code'):
            existing = GaugeProject.query.filter_by(project_code=data['project_code']).first()
            if existing and existing.id != project_id:
                return {'error': '项目编号已存在'}, 400
            project.project_code = data['project_code']
        if data.get('name'):
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'root_path' in data:
            project.root_path = data['root_path']
        if 'gauge_version' in data:
            project.gauge_version = data['gauge_version']
        if 'status' in data:
            project.status = data['status']

        db.session.commit()
        return project.to_dict()

    def delete(self, project_id):
        """删除Gauge项目"""
        project = GaugeProject.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {'message': '删除成功'}


# ==================== Spec API ====================
class GaugeSpecListAPI(Resource):
    def get(self):
        """获取Spec列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        project_id = request.args.get('project_id', type=int)
        keyword = request.args.get('keyword', '')
        status = request.args.get('status', '')

        query = GaugeSpec.query
        if project_id:
            query = query.filter_by(project_id=project_id)
        if keyword:
            query = query.filter(GaugeSpec.spec_name.contains(keyword) | GaugeSpec.spec_code.contains(keyword))
        if status:
            query = query.filter_by(status=status)

        pagination = query.order_by(GaugeSpec.execution_order).paginate(page=page, per_page=per_page)
        return {
            'items': [s.to_dict() for s in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建Spec"""
        data = request.get_json()
        required_fields = ['project_id', 'spec_code', 'spec_name']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        if GaugeSpec.query.filter_by(spec_code=data['spec_code']).first():
            return {'error': '规格编号已存在'}, 400

        spec = GaugeSpec(
            project_id=data['project_id'],
            spec_code=data['spec_code'],
            spec_name=data['spec_name'],
            file_path=data.get('file_path'),
            tags=data.get('tags'),
            execution_order=data.get('execution_order', 0),
            status=data.get('status', 'active'),
            remark=data.get('remark')
        )
        db.session.add(spec)
        db.session.commit()
        return spec.to_dict(), 201


class GaugeSpecAPI(Resource):
    def get(self, spec_id):
        """获取单个Spec"""
        spec = GaugeSpec.query.get_or_404(spec_id)
        return spec.to_dict()

    def put(self, spec_id):
        """更新Spec"""
        spec = GaugeSpec.query.get_or_404(spec_id)
        data = request.get_json()

        if data.get('spec_code'):
            existing = GaugeSpec.query.filter_by(spec_code=data['spec_code']).first()
            if existing and existing.id != spec_id:
                return {'error': '规格编号已存在'}, 400
            spec.spec_code = data['spec_code']
        if data.get('spec_name'):
            spec.spec_name = data['spec_name']
        if 'file_path' in data:
            spec.file_path = data['file_path']
        if 'tags' in data:
            spec.tags = data['tags']
        if 'execution_order' in data:
            spec.execution_order = data['execution_order']
        if 'status' in data:
            spec.status = data['status']
        if 'remark' in data:
            spec.remark = data['remark']

        db.session.commit()
        return spec.to_dict()

    def delete(self, spec_id):
        """删除Spec"""
        spec = GaugeSpec.query.get_or_404(spec_id)
        db.session.delete(spec)
        db.session.commit()
        return {'message': '删除成功'}


# ==================== Scenario API ====================
class GaugeScenarioListAPI(Resource):
    def get(self):
        """获取Scenario列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        spec_id = request.args.get('spec_id', type=int)
        keyword = request.args.get('keyword', '')
        status = request.args.get('status', '')

        query = GaugeScenario.query
        if spec_id:
            query = query.filter_by(spec_id=spec_id)
        if keyword:
            query = query.filter(GaugeScenario.scenario_name.contains(keyword))
        if status:
            query = query.filter_by(status=status)

        pagination = query.order_by(GaugeScenario.execution_order).paginate(page=page, per_page=per_page)
        return {
            'items': [s.to_dict() for s in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }

    def post(self):
        """创建Scenario"""
        data = request.get_json()
        required_fields = ['spec_id', 'scenario_name']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        scenario = GaugeScenario(
            spec_id=data['spec_id'],
            scenario_name=data['scenario_name'],
            scenario_type=data.get('scenario_type', 'basic'),
            tags=data.get('tags'),
            execution_order=data.get('execution_order', 0),
            timeout=data.get('timeout', 60000),
            status=data.get('status', 'active'),
            remark=data.get('remark')
        )
        db.session.add(scenario)
        db.session.flush()

        # 添加步骤
        steps = data.get('steps', [])
        for i, step in enumerate(steps):
            s = GaugeStep(
                scenario_id=scenario.id,
                step_order=i + 1,
                step_text=step['step_text'],
                step_type=step.get('step_type', 'action'),
                is_parametric=step.get('is_parametric', False),
                parameters=step.get('parameters')
            )
            db.session.add(s)

        # 添加数据表
        tables = data.get('tables', [])
        for table in tables:
            t = GaugeTable(
                scenario_id=scenario.id,
                table_name=table['table_name'],
                table_type=table.get('table_type', 'parameter'),
                headers=table.get('headers'),
                rows_data=table.get('rows_data'),
                description=table.get('description')
            )
            db.session.add(t)

        db.session.commit()
        return scenario.to_dict(), 201


class GaugeScenarioAPI(Resource):
    def get(self, scenario_id):
        """获取单个Scenario"""
        scenario = GaugeScenario.query.get_or_404(scenario_id)
        return scenario.to_dict()

    def put(self, scenario_id):
        """更新Scenario"""
        scenario = GaugeScenario.query.get_or_404(scenario_id)
        data = request.get_json()

        if data.get('scenario_name'):
            scenario.scenario_name = data['scenario_name']
        if 'scenario_type' in data:
            scenario.scenario_type = data['scenario_type']
        if 'tags' in data:
            scenario.tags = data['tags']
        if 'execution_order' in data:
            scenario.execution_order = data['execution_order']
        if 'timeout' in data:
            scenario.timeout = data['timeout']
        if 'status' in data:
            scenario.status = data['status']
        if 'remark' in data:
            scenario.remark = data['remark']

        # 更新步骤
        if 'steps' in data:
            GaugeStep.query.filter_by(scenario_id=scenario_id).delete()
            for i, step in enumerate(data['steps']):
                s = GaugeStep(
                    scenario_id=scenario_id,
                    step_order=i + 1,
                    step_text=step['step_text'],
                    step_type=step.get('step_type', 'action'),
                    is_parametric=step.get('is_parametric', False),
                    parameters=step.get('parameters')
                )
                db.session.add(s)

        # 更新数据表
        if 'tables' in data:
            GaugeTable.query.filter_by(scenario_id=scenario_id).delete()
            for table in data['tables']:
                t = GaugeTable(
                    scenario_id=scenario_id,
                    table_name=table['table_name'],
                    table_type=table.get('table_type', 'parameter'),
                    headers=table.get('headers'),
                    rows_data=table.get('rows_data'),
                    description=table.get('description')
                )
                db.session.add(t)

        db.session.commit()
        return scenario.to_dict()

    def delete(self, scenario_id):
        """删除Scenario"""
        scenario = GaugeScenario.query.get_or_404(scenario_id)
        GaugeStep.query.filter_by(scenario_id=scenario_id).delete()
        GaugeTable.query.filter_by(scenario_id=scenario_id).delete()
        db.session.delete(scenario)
        db.session.commit()
        return {'message': '删除成功'}


# ==================== Step API ====================
class GaugeStepListAPI(Resource):
    def post(self):
        """创建Step"""
        data = request.get_json()
        required_fields = ['scenario_id', 'step_text']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        # 获取当前最大顺序
        max_order = db.session.query(db.func.max(GaugeStep.step_order)).filter_by(
            scenario_id=data['scenario_id']).scalar() or 0

        step = GaugeStep(
            scenario_id=data['scenario_id'],
            step_order=data.get('step_order', max_order + 1),
            step_text=data['step_text'],
            step_type=data.get('step_type', 'action'),
            is_parametric=data.get('is_parametric', False),
            parameters=data.get('parameters'),
            status=data.get('status', 'active')
        )
        db.session.add(step)
        db.session.commit()
        return step.to_dict(), 201


class GaugeStepAPI(Resource):
    def put(self, step_id):
        """更新Step"""
        step = GaugeStep.query.get_or_404(step_id)
        data = request.get_json()

        if 'step_text' in data:
            step.step_text = data['step_text']
        if 'step_type' in data:
            step.step_type = data['step_type']
        if 'step_order' in data:
            step.step_order = data['step_order']
        if 'is_parametric' in data:
            step.is_parametric = data['is_parametric']
        if 'parameters' in data:
            step.parameters = data['parameters']
        if 'status' in data:
            step.status = data['status']

        db.session.commit()
        return step.to_dict()

    def delete(self, step_id):
        """删除Step"""
        step = GaugeStep.query.get_or_404(step_id)
        db.session.delete(step)
        db.session.commit()
        return {'message': '删除成功'}


# ==================== Table API ====================
class GaugeTableListAPI(Resource):
    def post(self):
        """创建Table"""
        data = request.get_json()
        required_fields = ['scenario_id', 'table_name']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field}必填'}, 400

        table = GaugeTable(
            scenario_id=data['scenario_id'],
            table_name=data['table_name'],
            table_type=data.get('table_type', 'parameter'),
            headers=data.get('headers'),
            rows_data=data.get('rows_data'),
            description=data.get('description')
        )
        db.session.add(table)
        db.session.commit()
        return table.to_dict(), 201


class GaugeTableAPI(Resource):
    def put(self, table_id):
        """更新Table"""
        table = GaugeTable.query.get_or_404(table_id)
        data = request.get_json()

        if 'table_name' in data:
            table.table_name = data['table_name']
        if 'table_type' in data:
            table.table_type = data['table_type']
        if 'headers' in data:
            table.headers = data['headers']
        if 'rows_data' in data:
            table.rows_data = data['rows_data']
        if 'description' in data:
            table.description = data['description']

        db.session.commit()
        return table.to_dict()

    def delete(self, table_id):
        """删除Table"""
        table = GaugeTable.query.get_or_404(table_id)
        db.session.delete(table)
        db.session.commit()
        return {'message': '删除成功'}


# 注册路由
api.add_resource(GaugeProjectListAPI, '/gauge-projects')
api.add_resource(GaugeProjectAPI, '/gauge-projects/<int:project_id>')
api.add_resource(GaugeSpecListAPI, '/gauge-specs')
api.add_resource(GaugeSpecAPI, '/gauge-specs/<int:spec_id>')
api.add_resource(GaugeScenarioListAPI, '/gauge-scenarios')
api.add_resource(GaugeScenarioAPI, '/gauge-scenarios/<int:scenario_id>')
api.add_resource(GaugeStepListAPI, '/gauge-steps')
api.add_resource(GaugeStepAPI, '/gauge-steps/<int:step_id>')
api.add_resource(GaugeTableListAPI, '/gauge-tables')
api.add_resource(GaugeTableAPI, '/gauge-tables/<int:table_id>')
