from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        # 导入所有模型确保它们被注册
        from .platform import Platform
        from .vehicle import VehicleModel, VehicleConfig
        from .requirement import Requirement, RequirementVehicleDetail
        from .test_case import TestCaseGroup, TestCase, TestCaseVehicle
        from .test_script import TestScript, TestScenario, ScenarioParameter, ScenarioDataTable
        from .gauge import GaugeProject, GaugeSpec, GaugeScenario, GaugeStep, GaugeTable
        from .can_matrix import CANMatrix, SignalDefinition
        from .speaker_mapping import SpeakerChannelMapping
        from .audio_source import A2BSlot, AudioSourceType, AudioSourceSlotMapping
        from .playback_matrix import PlaybackMatrix, PlaybackMatrixEntry

        db.create_all()
