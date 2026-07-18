import json
from app import create_app
from app.models import db
from app.models.platform import Platform
from app.models.vehicle import VehicleModel, VehicleConfig
from app.models.requirement import Requirement, RequirementVehicleDetail
from app.models.test_case import TestCaseGroup, TestCase, TestCaseVehicle
from app.models.test_script import TestScript, TestScenario, ScenarioParameter, ScenarioDataTable
from app.models.can_matrix import CANMatrix, SignalDefinition
from app.models.speaker_mapping import SpeakerChannelMapping
from app.models.audio_source import A2BSlot, AudioSourceType, AudioSourceSlotMapping
from app.models.playback_matrix import PlaybackMatrix, PlaybackMatrixEntry


def init_mock_data():
    app = create_app()
    with app.app_context():
        # 清空所有数据
        db.drop_all()
        db.create_all()

        print("开始初始化Mock数据...")

        # 1. 平台数据
        platforms = [
            Platform(name='MQB平台', code='MQB', remark='大众MQB平台'),
            Platform(name='MEB平台', code='MEB', remark='大众MEB电动车平台'),
            Platform(name='J528平台', code='J528', remark='高端车型平台'),
        ]
        db.session.add_all(platforms)
        db.session.flush()
        print(f"✓ 创建平台: {len(platforms)}个")

        # 2. 车型数据
        vehicle_models = [
            VehicleModel(platform_id=platforms[0].id, name='迈腾B9', code='MT-B9', model_year='2025'),
            VehicleModel(platform_id=platforms[0].id, name='帕萨特B9', code='PST-B9', model_year='2025'),
            VehicleModel(platform_id=platforms[1].id, name='ID.4 CROZZ', code='ID4-CROZZ', model_year='2025'),
            VehicleModel(platform_id=platforms[1].id, name='ID.6 CROZZ', code='ID6-CROZZ', model_year='2025'),
            VehicleModel(platform_id=platforms[2].id, name='奥迪A6L', code='A6L', model_year='2025'),
        ]
        db.session.add_all(vehicle_models)
        db.session.flush()
        print(f"✓ 创建车型: {len(vehicle_models)}个")

        # 3. 车辆配置
        vehicle_configs = [
            VehicleConfig(vehicle_model_id=vehicle_models[0].id, config_name='迈腾B9豪华版', config_code='MT-B9-LUX',
                         software_code='F1A0-V001.01.00', description='迈腾B9豪华版配置，8扬声器，支持蓝牙/USB/FM'),
            VehicleConfig(vehicle_model_id=vehicle_models[0].id, config_name='迈腾B9旗舰版', config_code='MT-B9-FLAG',
                         software_code='F1A0-V002.00.01', description='迈腾B9旗舰版配置，12扬声器，含低音炮和DSP'),
            VehicleConfig(vehicle_model_id=vehicle_models[2].id, config_name='ID.4 Pro版', config_code='ID4-PRO',
                         software_code='F1A0-V003.02.00', description='ID.4 Pro版电动车配置，8扬声器'),
            VehicleConfig(vehicle_model_id=vehicle_models[4].id, config_name='A6L豪华型', config_code='A6L-LUX',
                         software_code='F1A0-V001.03.01', description='奥迪A6L豪华型配置，16扬声器，高端音响系统'),
        ]
        db.session.add_all(vehicle_configs)
        db.session.flush()
        print(f"✓ 创建车辆配置: {len(vehicle_configs)}个")

        # 4. A2B Slot
        a2b_slots = [
            A2BSlot(slot_name='Slot 0', slot_number=0, slot_type='I2S', max_channels=8, description='主Slot'),
            A2BSlot(slot_name='Slot 1', slot_number=1, slot_type='I2S', max_channels=8, description='扩展Slot 1'),
            A2BSlot(slot_name='Slot 2', slot_number=2, slot_type='I2S', max_channels=8, description='扩展Slot 2'),
            A2BSlot(slot_name='Slot 3', slot_number=3, slot_type='I2S', max_channels=4, description='低音炮Slot'),
        ]
        db.session.add_all(a2b_slots)
        db.session.flush()
        print(f"✓ 创建A2B Slot: {len(a2b_slots)}个")

        # 5. 音源类型
        audio_sources = [
            AudioSourceType(source_name='蓝牙音乐', source_code='BT_MUSIC', description='蓝牙音频流'),
            AudioSourceType(source_name='USB音乐', source_code='USB_MUSIC', description='USB音频播放'),
            AudioSourceType(source_name='FM收音机', source_code='FM_RADIO', description='FM调频广播'),
            AudioSourceType(source_name='导航语音', source_code='NAV_VOICE', description='导航提示音'),
            AudioSourceType(source_name='电话语音', source_code='TEL_VOICE', description='蓝牙电话语音'),
            AudioSourceType(source_name='系统提示音', source_code='SYS_TONE', description='系统提示音效'),
        ]
        db.session.add_all(audio_sources)
        db.session.flush()
        print(f"✓ 创建音源类型: {len(audio_sources)}个")

        # 6. 音源Slot映射
        audio_slot_mappings = [
            AudioSourceSlotMapping(audio_source_id=audio_sources[0].id, a2b_slot_id=a2b_slots[0].id, priority=1, is_default=True),
            AudioSourceSlotMapping(audio_source_id=audio_sources[1].id, a2b_slot_id=a2b_slots[0].id, priority=2),
            AudioSourceSlotMapping(audio_source_id=audio_sources[2].id, a2b_slot_id=a2b_slots[1].id, priority=3),
            AudioSourceSlotMapping(audio_source_id=audio_sources[3].id, a2b_slot_id=a2b_slots[1].id, priority=4),
            AudioSourceSlotMapping(audio_source_id=audio_sources[4].id, a2b_slot_id=a2b_slots[0].id, priority=5),
            AudioSourceSlotMapping(audio_source_id=audio_sources[5].id, a2b_slot_id=a2b_slots[2].id, priority=6),
        ]
        db.session.add_all(audio_slot_mappings)
        db.session.flush()
        print(f"✓ 创建音源Slot映射: {len(audio_slot_mappings)}个")

        # 7. 扬声器通道映射
        speaker_mappings = [
            # 迈腾B9豪华版
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[0].id, speaker_name='左前高音', speaker_position='FL-Tweeter',
                                 channel_type='analog', channel_number=0, channel_name='CH0', power=25, impedance=4),
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[0].id, speaker_name='左前低音', speaker_position='FL-Woofer',
                                 channel_type='analog', channel_number=1, channel_name='CH1', power=50, impedance=4),
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[0].id, speaker_name='右前高音', speaker_position='FR-Tweeter',
                                 channel_type='analog', channel_number=2, channel_name='CH2', power=25, impedance=4),
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[0].id, speaker_name='右前低音', speaker_position='FR-Woofer',
                                 channel_type='analog', channel_number=3, channel_name='CH3', power=50, impedance=4),
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[0].id, speaker_name='左后高音', speaker_position='RL-Tweeter',
                                 channel_type='analog', channel_number=4, channel_name='CH4', power=25, impedance=4),
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[0].id, speaker_name='左后低音', speaker_position='RL-Woofer',
                                 channel_type='analog', channel_number=5, channel_name='CH5', power=50, impedance=4),
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[0].id, speaker_name='右后高音', speaker_position='RR-Tweeter',
                                 channel_type='analog', channel_number=6, channel_name='CH6', power=25, impedance=4),
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[0].id, speaker_name='右后低音', speaker_position='RR-Woofer',
                                 channel_type='analog', channel_number=7, channel_name='CH7', power=50, impedance=4),
            # A6L豪华型
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[3].id, speaker_name='左前高音', speaker_position='FL-Tweeter',
                                 channel_type='analog', channel_number=0, channel_name='CH0', power=50, impedance=4),
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[3].id, speaker_name='左前中音', speaker_position='FL-Mid',
                                 channel_type='analog', channel_number=1, channel_name='CH1', power=75, impedance=4),
            SpeakerChannelMapping(vehicle_config_id=vehicle_configs[3].id, speaker_name='左前低音', speaker_position='FL-Woofer',
                                 channel_type='analog', channel_number=2, channel_name='CH2', power=100, impedance=2),
        ]
        db.session.add_all(speaker_mappings)
        db.session.flush()
        print(f"✓ 创建扬声器映射: {len(speaker_mappings)}个")

        # 8. CAN矩阵
        can_matrices = [
            CANMatrix(matrix_name='功放控制矩阵', matrix_type='amplifier', description='功放控制相关CAN信号', version='V1.0'),
            CANMatrix(matrix_name='音频控制矩阵', matrix_type='audio', description='音频控制相关CAN信号', version='V1.0'),
        ]
        db.session.add_all(can_matrices)
        db.session.flush()
        print(f"✓ 创建CAN矩阵: {len(can_matrices)}个")

        # 9. 信号定义
        signal_definitions = [
            # 功放控制矩阵
            SignalDefinition(matrix_id=can_matrices[0].id, signal_name='AMP_PowerStatus', message_id='0x100',
                            message_name='AMP_PowerCtrl', signal_type='unsigned', data_length=8, start_bit=0,
                            factor=1, offset=0, min_value=0, max_value=3, unit='', status='active'),
            SignalDefinition(matrix_id=can_matrices[0].id, signal_name='AMP_Volume', message_id='0x100',
                            message_name='AMP_PowerCtrl', signal_type='unsigned', data_length=8, start_bit=8,
                            factor=1, offset=0, min_value=0, max_value=100, unit='%', status='active'),
            SignalDefinition(matrix_id=can_matrices[0].id, signal_name='AMP_Mute', message_id='0x101',
                            message_name='AMP_AudioCtrl', signal_type='unsigned', data_length=1, start_bit=0,
                            factor=1, offset=0, min_value=0, max_value=1, unit='', status='active'),
            # 音频控制矩阵
            SignalDefinition(matrix_id=can_matrices[1].id, signal_name='AUD_SourceSelect', message_id='0x200',
                            message_name='AUD_SourceCtrl', signal_type='unsigned', data_length=8, start_bit=0,
                            factor=1, offset=0, min_value=0, max_value=10, unit='', status='active'),
            SignalDefinition(matrix_id=can_matrices[1].id, signal_name='AUD_Balance', message_id='0x201',
                            message_name='AUD_EffectCtrl', signal_type='signed', data_length=8, start_bit=0,
                            factor=1, offset=0, min_value=-10, max_value=10, unit='', status='active'),
            SignalDefinition(matrix_id=can_matrices[1].id, signal_name='AUD_Fader', message_id='0x201',
                            message_name='AUD_EffectCtrl', signal_type='signed', data_length=8, start_bit=8,
                            factor=1, offset=0, min_value=-10, max_value=10, unit='', status='active'),
        ]
        db.session.add_all(signal_definitions)
        db.session.flush()
        print(f"✓ 创建信号定义: {len(signal_definitions)}个")

        # 10. 需求 (SWRS格式: SWRS-模块-序号)
        from datetime import date
        requirements = [
            Requirement(req_code='SWRS-PA-001', title='功放基本功能需求',
                       description='功放应支持基本的开关机、音量控制功能',
                       verification_scope='功放开关机功能、音量调节功能',
                       verification_criteria='1. 功放能在5秒内完成开机\n2. 音量调节范围0-100\n3. 静音功能正常',
                       priority='S', status='approved', designer='王工', design_date=date(2025, 1, 10)),
            Requirement(req_code='SWRS-PA-002', title='蓝牙音频播放需求',
                       description='功放应支持蓝牙音频播放功能',
                       verification_scope='蓝牙连接、音频播放、音量控制',
                       verification_criteria='1. 蓝牙配对时间<10秒\n2. 音频播放无卡顿\n3. 支持AVRCP协议',
                       priority='S', status='approved', designer='王工', design_date=date(2025, 1, 10)),
            Requirement(req_code='SWRS-PA-003', title='多音源切换需求',
                       description='功放应支持多音源切换功能',
                       verification_scope='音源切换、优先级管理',
                       verification_criteria='1. 切换时间<2秒\n2. 音源优先级正确\n3. 无爆音',
                       priority='A', status='approved', designer='李工', design_date=date(2025, 1, 15)),
            Requirement(req_code='SWRS-PA-004', title='扬声器通道需求',
                       description='功放应支持多通道扬声器输出',
                       verification_scope='通道配置、音频输出',
                       verification_criteria='1. 通道数符合配置\n2. 各通道独立可控\n3. 通道间无串扰',
                       priority='S', status='reviewing', designer='李工', design_date=date(2025, 1, 15)),
            Requirement(req_code='SWRS-PA-005', title='故障诊断需求',
                       description='功放应支持故障检测和诊断功能',
                       verification_scope='故障检测、诊断报告',
                       verification_criteria='1. 能检测扬声器断路\n2. 能检测过温保护\n3. 诊断信息准确',
                       priority='A', status='draft', designer='张工', design_date=date(2025, 1, 20)),
        ]
        db.session.add_all(requirements)
        db.session.flush()
        print(f"✓ 创建需求: {len(requirements)}个")

        # 11. 需求车型详情
        req_vehicle_details = [
            # 需求1: 功放基本功能测试 - 不同车型有差异
            RequirementVehicleDetail(requirement_id=requirements[0].id, vehicle_model_id=vehicle_models[0].id,
                                    feature_support=True, function_status='正常'),
            RequirementVehicleDetail(requirement_id=requirements[0].id, vehicle_model_id=vehicle_models[1].id,
                                    feature_support=True, function_status='正常'),
            RequirementVehicleDetail(requirement_id=requirements[0].id, vehicle_model_id=vehicle_models[2].id,
                                    feature_support=True, function_status='正常',
                                    difference_description='功放功率较低(350W)，音量最大值受限'),
            RequirementVehicleDetail(requirement_id=requirements[0].id, vehicle_model_id=vehicle_models[3].id,
                                    feature_support=True, function_status='降级',
                                    difference_description='仅支持6通道输出，低音炮通道不可用'),
            RequirementVehicleDetail(requirement_id=requirements[0].id, vehicle_model_id=vehicle_models[4].id,
                                    feature_support=False),  # 不适用车型
            # 需求2: 蓝牙音频播放测试 - 部分车型不支持
            RequirementVehicleDetail(requirement_id=requirements[1].id, vehicle_model_id=vehicle_models[0].id,
                                    feature_support=True, function_status='正常'),
            RequirementVehicleDetail(requirement_id=requirements[1].id, vehicle_model_id=vehicle_models[1].id,
                                    feature_support=True, function_status='正常'),
            RequirementVehicleDetail(requirement_id=requirements[1].id, vehicle_model_id=vehicle_models[2].id,
                                    feature_support=True, function_status='正常',
                                    difference_description='蓝牙5.0协议，延迟略高'),
            RequirementVehicleDetail(requirement_id=requirements[1].id, vehicle_model_id=vehicle_models[4].id,
                                    feature_support=False),  # 不适用车型
            # 需求3: 多音源切换测试 - 所有车型都支持，无差异
            RequirementVehicleDetail(requirement_id=requirements[2].id, vehicle_model_id=vehicle_models[0].id,
                                    feature_support=True, function_status='正常'),
            RequirementVehicleDetail(requirement_id=requirements[2].id, vehicle_model_id=vehicle_models[2].id,
                                    feature_support=True, function_status='正常'),
        ]
        db.session.add_all(req_vehicle_details)
        db.session.flush()
        print(f"✓ 创建需求车型详情: {len(req_vehicle_details)}个")

        # 12. 测试用例分组
        case_groups = [
            TestCaseGroup(name='功放基础功能', code='PA', description='功放基础功能测试用例', sort_order=1, level=0),
            TestCaseGroup(name='音频播放功能', code='AP', description='音频播放相关测试用例', sort_order=2, level=0),
            TestCaseGroup(name='通道控制功能', code='CH', description='扬声器通道控制测试用例', sort_order=3, level=0),
            TestCaseGroup(name='故障诊断功能', code='FD', description='故障诊断相关测试用例', sort_order=4, level=0),
        ]
        db.session.add_all(case_groups)
        db.session.flush()

        # 子分组
        sub_groups = [
            TestCaseGroup(parent_id=case_groups[0].id, name='开关机测试', code='PWR', description='功放开关机测试', sort_order=1, level=1),
            TestCaseGroup(parent_id=case_groups[0].id, name='音量控制测试', code='VOL', description='音量调节测试', sort_order=2, level=1),
            TestCaseGroup(parent_id=case_groups[1].id, name='蓝牙音频测试', code='BT', description='蓝牙音频播放测试', sort_order=1, level=1),
            TestCaseGroup(parent_id=case_groups[1].id, name='USB音频测试', code='USB', description='USB音频播放测试', sort_order=2, level=1),
        ]
        db.session.add_all(sub_groups)
        db.session.flush()
        print(f"✓ 创建测试用例分组: {len(case_groups) + len(sub_groups)}个")

        # 13. Gauge项目
        from app.models.gauge import GaugeProject, GaugeSpec, GaugeScenario, GaugeStep, GaugeTable
        gauge_projects = [
            GaugeProject(project_code='GPROJ-PA', name='功放测试项目', description='功放功能自动化测试项目',
                        root_path='tests/power_amplifier', gauge_version='1.5.0', status='active', created_by='系统'),
            GaugeProject(project_code='GPROJ-AUD', name='音频测试项目', description='音频系统集成测试项目',
                        root_path='tests/audio_system', gauge_version='1.5.0', status='active', created_by='系统'),
        ]
        db.session.add_all(gauge_projects)
        db.session.flush()
        print(f"✓ 创建Gauge项目: {len(gauge_projects)}个")

        # 14. Gauge Spec（规格文件）
        gauge_specs = [
            GaugeSpec(project_id=gauge_projects[0].id, spec_code='SPEC-PWR', spec_name='功放开关机规格',
                     file_path='specs/power_control.spec', tags=json.dumps(['功放', '开关机']),
                     execution_order=1, status='active'),
            GaugeSpec(project_id=gauge_projects[0].id, spec_code='SPEC-VOL', spec_name='音量控制规格',
                     file_path='specs/volume_control.spec', tags=json.dumps(['功放', '音量']),
                     execution_order=2, status='active'),
            GaugeSpec(project_id=gauge_projects[1].id, spec_code='SPEC-BT', spec_name='蓝牙音频规格',
                     file_path='specs/bluetooth_audio.spec', tags=json.dumps(['蓝牙', '音频']),
                     execution_order=1, status='active'),
        ]
        db.session.add_all(gauge_specs)
        db.session.flush()
        print(f"✓ 创建Gauge Spec: {len(gauge_specs)}个")

        # 15. Gauge Scenario（场景）
        gauge_scenarios = [
            GaugeScenario(spec_id=gauge_specs[0].id, scenario_name='功放开机测试',
                         scenario_type='basic', execution_order=1, timeout=30000, status='active'),
            GaugeScenario(spec_id=gauge_specs[0].id, scenario_name='功放关机测试',
                         scenario_type='basic', execution_order=2, timeout=30000, status='active'),
            GaugeScenario(spec_id=gauge_specs[1].id, scenario_name='音量调节测试',
                         scenario_type='table_driven', execution_order=1, timeout=60000, status='active'),
            GaugeScenario(spec_id=gauge_specs[2].id, scenario_name='蓝牙连接播放测试',
                         scenario_type='basic', execution_order=1, timeout=60000, status='active'),
        ]
        db.session.add_all(gauge_scenarios)
        db.session.flush()
        print(f"✓ 创建Gauge Scenario: {len(gauge_scenarios)}个")

        # 16. Gauge Step（步骤）
        gauge_steps = [
            # 功放开机测试步骤
            GaugeStep(scenario_id=gauge_scenarios[0].id, step_order=1, step_text='打开车辆电源', step_type='setup'),
            GaugeStep(scenario_id=gauge_scenarios[0].id, step_order=2, step_text='等待功放初始化完成', step_type='action'),
            GaugeStep(scenario_id=gauge_scenarios[0].id, step_order=3, step_text='检查功放状态为ON', step_type='assertion'),
            GaugeStep(scenario_id=gauge_scenarios[0].id, step_order=4, step_text='验证CAN信号AMP_PowerStatus=1', step_type='assertion'),
            # 功放关机测试步骤
            GaugeStep(scenario_id=gauge_scenarios[1].id, step_order=1, step_text='关闭车辆电源', step_type='setup'),
            GaugeStep(scenario_id=gauge_scenarios[1].id, step_order=2, step_text='等待功放关机', step_type='action'),
            GaugeStep(scenario_id=gauge_scenarios[1].id, step_order=3, step_text='检查功放状态为OFF', step_type='assertion'),
            # 音量调节测试步骤（参数化）
            GaugeStep(scenario_id=gauge_scenarios[2].id, step_order=1, step_text='设置音量为<target>', step_type='action',
                     is_parametric=True, parameters=json.dumps(['target'])),
            GaugeStep(scenario_id=gauge_scenarios[2].id, step_order=2, step_text='验证音量显示为<expected>', step_type='assertion',
                     is_parametric=True, parameters=json.dumps(['expected'])),
            # 蓝牙连接播放测试步骤
            GaugeStep(scenario_id=gauge_scenarios[3].id, step_order=1, step_text='建立蓝牙连接', step_type='setup'),
            GaugeStep(scenario_id=gauge_scenarios[3].id, step_order=2, step_text='播放手机音乐', step_type='action'),
            GaugeStep(scenario_id=gauge_scenarios[3].id, step_order=3, step_text='检查音频输出正常', step_type='assertion'),
        ]
        db.session.add_all(gauge_steps)
        db.session.flush()
        print(f"✓ 创建Gauge Step: {len(gauge_steps)}个")

        # 17. Gauge Table（数据驱动表）
        gauge_tables = [
            GaugeTable(scenario_id=gauge_scenarios[2].id, table_name='音量测试数据',
                      table_type='parameter',
                      headers=json.dumps(['target', 'expected']),
                      rows_data=json.dumps([
                          {'target': '0', 'expected': '静音'},
                          {'target': '25', 'expected': '低音量'},
                          {'target': '50', 'expected': '中等音量'},
                          {'target': '75', 'expected': '较高音量'},
                          {'target': '100', 'expected': '最大音量'}
                      ]),
                      description='不同音量级别的测试数据'),
        ]
        db.session.add_all(gauge_tables)
        db.session.flush()
        print(f"✓ 创建Gauge Table: {len(gauge_tables)}个")

        # 18. 测试用例 (SwQT格式: SwQT-模块编码-序号)
        from datetime import date
        test_cases = [
            TestCase(case_code='SwQT-PWR-001', group_id=sub_groups[0].id,
                    case_name='功放开机功能测试', test_purpose='验证功放能够正常开机',
                    level='S', preconditions='车辆电源OFF',
                    test_steps='1. 打开车辆电源\n2. 等待功放初始化\n3. 检查功放状态',
                    expected_results='功放状态为ON，CAN信号AMP_PowerStatus=1',
                    tags='冒烟,开机', designer='张三', design_date=date(2025, 1, 15), publish_date=date(2025, 2, 1),
                    status='Accepted', gauge_scenario_id=gauge_scenarios[0].id, can_matrix_id=can_matrices[0].id),
            TestCase(case_code='SwQT-PWR-002', group_id=sub_groups[0].id,
                    case_name='功放关机功能测试', test_purpose='验证功放能够正常关机',
                    level='S', preconditions='车辆电源ON，功放已开机',
                    test_steps='1. 关闭车辆电源\n2. 等待功放关机\n3. 检查功放状态',
                    expected_results='功放状态为OFF，CAN信号AMP_PowerStatus=0',
                    tags='冒烟,关机', designer='张三', design_date=date(2025, 1, 15), publish_date=date(2025, 2, 1),
                    status='Accepted', gauge_scenario_id=gauge_scenarios[1].id, can_matrix_id=can_matrices[0].id),
            TestCase(case_code='SwQT-VOL-001', group_id=sub_groups[1].id,
                    case_name='音量增加测试', test_purpose='验证音量能够正常增加',
                    level='A', preconditions='功放已开机，音量为0',
                    test_steps='1. 发送音量增加命令\n2. 检查音量变化\n3. 验证CAN信号',
                    expected_results='音量增加，CAN信号AMP_Volume递增',
                    tags='功能,音量', designer='李四', design_date=date(2025, 1, 20), publish_date=date(2025, 2, 5),
                    status='Accepted', gauge_scenario_id=gauge_scenarios[2].id, can_matrix_id=can_matrices[0].id),
            TestCase(case_code='SwQT-BT-001', group_id=sub_groups[2].id,
                    case_name='蓝牙连接音频播放测试', test_purpose='验证蓝牙连接后的音频播放功能',
                    level='A', preconditions='手机已蓝牙配对',
                    test_steps='1. 建立蓝牙连接\n2. 播放手机音乐\n3. 检查音频输出',
                    expected_results='音频正常播放，CAN信号AUD_SourceSelect=1',
                    tags='功能,蓝牙', designer='李四', design_date=date(2025, 1, 20),
                    status='Draft', gauge_scenario_id=gauge_scenarios[3].id, can_matrix_id=can_matrices[1].id),
        ]
        db.session.add_all(test_cases)
        db.session.flush()

        # 添加需求关联（多对多）
        test_cases[0].requirements.append(requirements[0])
        test_cases[1].requirements.append(requirements[0])
        test_cases[2].requirements.extend([requirements[0], requirements[2]])
        test_cases[3].requirements.extend([requirements[1], requirements[3]])
        db.session.flush()
        print(f"✓ 创建测试用例: {len(test_cases)}个")

        # 18. 测试用例车型关联
        test_case_vehicles = [
            TestCaseVehicle(test_case_id=test_cases[0].id, vehicle_config_id=vehicle_configs[0].id,
                           expected_result='功放正常开机'),
            TestCaseVehicle(test_case_id=test_cases[0].id, vehicle_config_id=vehicle_configs[2].id,
                           expected_result='功放正常开机'),
            TestCaseVehicle(test_case_id=test_cases[1].id, vehicle_config_id=vehicle_configs[0].id,
                           expected_result='功放正常关机'),
            TestCaseVehicle(test_case_id=test_cases[2].id, vehicle_config_id=vehicle_configs[0].id,
                           expected_result='音量正常增加'),
            TestCaseVehicle(test_case_id=test_cases[3].id, vehicle_config_id=vehicle_configs[0].id,
                           expected_result='蓝牙音频正常播放'),
        ]
        db.session.add_all(test_case_vehicles)
        db.session.flush()
        print(f"✓ 创建测试用例车型关联: {len(test_case_vehicles)}个")

        # 19. 播放矩阵
        playback_matrices = [
            PlaybackMatrix(vehicle_config_id=vehicle_configs[0].id, matrix_name='迈腾B9豪华版播放矩阵',
                          description='迈腾B9豪华版播放矩阵配置'),
            PlaybackMatrix(vehicle_config_id=vehicle_configs[3].id, matrix_name='A6L豪华型播放矩阵',
                          description='A6L豪华型播放矩阵配置'),
        ]
        db.session.add_all(playback_matrices)
        db.session.flush()
        print(f"✓ 创建播放矩阵: {len(playback_matrices)}个")

        # 20. 播放矩阵条目
        speaker_config_1 = json.dumps({
            '左前低音': '●', '左前中音': '●', '左前高音': '●', '中置': '●',
            '右前低音': '●', '右前中音': '●', '右前高音': '●',
            '左后低音': '●', '左后高音': '●', '右后低音': '●', '右后高音': '●',
            '重低音': '●', '左环绕': '●', '右环绕': '●'
        }, ensure_ascii=False)

        speaker_config_2 = json.dumps({
            '左前低音': '●', '左前中音': '●', '左前高音': '●',
            '右前低音': '●', '右前中音': '●', '右前高音': '●'
        }, ensure_ascii=False)

        speaker_config_3 = json.dumps({
            '左前低音': '●', '左前高音': '●', '右前低音': '●', '右前高音': '●'
        }, ensure_ascii=False)

        matrix_entries = [
            # 迈腾B9播放矩阵条目
            PlaybackMatrixEntry(matrix_id=playback_matrices[0].id, audio_source='媒体立体声',
                               a2b_channel='SLOT 1-SLOT 2', playback_position='全车',
                               headrest_mode='关闭', speaker_channels=speaker_config_1, sort_order=1),
            PlaybackMatrixEntry(matrix_id=playback_matrices[0].id, audio_source='杜比音源',
                               a2b_channel='SLOT 1', playback_position='Music_L（主驾媒体音左）',
                               headrest_mode='不判断头枕模式', speaker_channels=speaker_config_2, sort_order=2),
            PlaybackMatrixEntry(matrix_id=playback_matrices[0].id, audio_source='导航语音',
                               a2b_channel='SLOT 3', playback_position='全车',
                               headrest_mode='关闭', speaker_channels=speaker_config_1, sort_order=3),
            # A6L播放矩阵条目
            PlaybackMatrixEntry(matrix_id=playback_matrices[1].id, audio_source='媒体立体声',
                               a2b_channel='SLOT 1-SLOT 2', playback_position='全车',
                               headrest_mode='关闭', speaker_channels=speaker_config_1, sort_order=1),
            PlaybackMatrixEntry(matrix_id=playback_matrices[1].id, audio_source='杜比音源',
                               a2b_channel='SLOT 1', playback_position='Music_L（主驾媒体音左）',
                               headrest_mode='头枕环绕', speaker_channels=speaker_config_3, sort_order=2),
        ]
        db.session.add_all(matrix_entries)
        db.session.flush()
        print(f"✓ 创建播放矩阵条目: {len(matrix_entries)}个")

        # 提交所有数据
        db.session.commit()
        print("\n✅ Mock数据初始化完成！")
        print(f"总计创建:")
        print(f"  - 平台: {len(platforms)}个")
        print(f"  - 车型: {len(vehicle_models)}个")
        print(f"  - 车辆配置: {len(vehicle_configs)}个")
        print(f"  - A2B Slot: {len(a2b_slots)}个")
        print(f"  - 音源类型: {len(audio_sources)}个")
        print(f"  - 音源Slot映射: {len(audio_slot_mappings)}个")
        print(f"  - 扬声器映射: {len(speaker_mappings)}个")
        print(f"  - CAN矩阵: {len(can_matrices)}个")
        print(f"  - 信号定义: {len(signal_definitions)}个")
        print(f"  - 需求: {len(requirements)}个")
        print(f"  - 需求车型详情: {len(req_vehicle_details)}个")
        print(f"  - 测试用例分组: {len(case_groups) + len(sub_groups)}个")
        print(f"  - Gauge项目: {len(gauge_projects)}个")
        print(f"  - Gauge Spec: {len(gauge_specs)}个")
        print(f"  - Gauge Scenario: {len(gauge_scenarios)}个")
        print(f"  - Gauge Step: {len(gauge_steps)}个")
        print(f"  - Gauge Table: {len(gauge_tables)}个")
        print(f"  - 测试用例: {len(test_cases)}个")
        print(f"  - 测试用例车型关联: {len(test_case_vehicles)}个")
        print(f"  - 播放矩阵: {len(playback_matrices)}个")
        print(f"  - 播放矩阵条目: {len(matrix_entries)}个")


if __name__ == '__main__':
    init_mock_data()
