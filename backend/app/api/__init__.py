from flask import Blueprint, jsonify
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not Found', 'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500


# 导入API资源
from . import platform_api
from . import vehicle_api
from . import requirement_api
from . import test_case_api
from . import test_script_api
from . import gauge_api
from . import can_matrix_api
from . import speaker_mapping_api
from . import audio_source_api
from . import playback_matrix_api
from . import stats_api
