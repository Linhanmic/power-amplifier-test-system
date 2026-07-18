from flask_restful import Resource
from . import api
from ..models.platform import Platform
from ..models.vehicle import VehicleModel, VehicleConfig
from ..models.requirement import Requirement
from ..models.test_case import TestCase, TestCaseGroup
from ..models.test_script import TestScript
from ..models.can_matrix import CANMatrix
from ..models.playback_matrix import PlaybackMatrix


class StatsOverviewAPI(Resource):
    def get(self):
        """获取系统概览统计"""
        return {
            'platforms': Platform.query.filter_by(status='active').count(),
            'vehicle_models': VehicleModel.query.filter_by(status='active').count(),
            'vehicle_configs': VehicleConfig.query.filter_by(status='active').count(),
            'requirements': Requirement.query.count(),
            'test_case_groups': TestCaseGroup.query.count(),
            'test_cases': TestCase.query.count(),
            'test_scripts': TestScript.query.count(),
            'can_matrices': CANMatrix.query.filter_by(status='active').count(),
            'playback_matrices': PlaybackMatrix.query.filter_by(status='active').count(),
            'requirement_status': {
                'draft': Requirement.query.filter_by(status='draft').count(),
                'reviewing': Requirement.query.filter_by(status='reviewing').count(),
                'approved': Requirement.query.filter_by(status='approved').count(),
                'rejected': Requirement.query.filter_by(status='rejected').count()
            },
            'test_case_status': {
                'Draft': TestCase.query.filter_by(status='Draft').count(),
                'Accepted': TestCase.query.filter_by(status='Accepted').count(),
                'Not-Accepted': TestCase.query.filter_by(status='Not-Accepted').count()
            }
        }


class TreeDataAPI(Resource):
    def get(self, tree_type):
        """获取树形数据"""
        if tree_type == 'test-case-groups':
            return self._get_test_case_group_tree()
        elif tree_type == 'platforms':
            return self._get_platform_tree()
        else:
            return {'error': '不支持的树类型'}, 400

    def _get_test_case_group_tree(self):
        """获取测试用例分组树"""
        groups = TestCaseGroup.query.filter_by(parent_id=None).order_by(
            TestCaseGroup.sort_order
        ).all()
        return [self._build_group_tree(g) for g in groups]

    def _build_group_tree(self, group):
        """递归构建分组树"""
        result = {
            'id': group.id,
            'label': group.name,
            'code': group.code,
            'children': []
        }
        for child in group.children.order_by(TestCaseGroup.sort_order):
            result['children'].append(self._build_group_tree(child))
        return result

    def _get_platform_tree(self):
        """获取平台-车型树"""
        platforms = Platform.query.filter_by(status='active').order_by(Platform.name).all()
        result = []
        for platform in platforms:
            node = {
                'id': platform.id,
                'label': platform.name,
                'children': []
            }
            for vm in platform.vehicle_models.filter_by(status='active'):
                vm_node = {
                    'id': vm.id,
                    'label': vm.name,
                    'children': []
                }
                for vc in vm.configs.filter_by(status='active'):
                    vm_node['children'].append({
                        'id': vc.id,
                        'label': vc.config_name
                    })
                node['children'].append(vm_node)
            result.append(node)
        return result


api.add_resource(StatsOverviewAPI, '/stats/overview')
api.add_resource(TreeDataAPI, '/tree/<string:tree_type>')
