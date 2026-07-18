import json
import pandas as pd
from flask import request
from flask_restful import Resource
from . import api
from ..models import db
from ..models.playback_matrix import PlaybackMatrix, PlaybackMatrixEntry


class ImportPlaybackMatrixAPI(Resource):
    def post(self):
        """从Excel导入播放矩阵"""
        if 'file' not in request.files:
            return {'error': '未找到上传文件'}, 400

        file = request.files['file']
        vehicle_config_id = request.form.get('vehicle_config_id')
        matrix_name = request.form.get('matrix_name', '导入的播放矩阵')

        if not vehicle_config_id:
            return {'error': '请选择车辆配置'}, 400

        try:
            # 读取Excel文件
            df = pd.read_excel(file)

            # 定义扬声器列
            speaker_columns = [
                '左前低音', '左前中音', '左前高音', '中置',
                '右前低音', '右前中音', '右前高音',
                '左后低音', '左后高音', '右后低音', '右后高音',
                '重低音', '左环绕', '右环绕',
                '左前顶棚', '右前顶棚', '左后顶棚', '右后顶棚',
                '主驾头枕左', '主驾头枕右', 'AVAS'
            ]

            # 创建播放矩阵
            matrix = PlaybackMatrix(
                vehicle_config_id=int(vehicle_config_id),
                matrix_name=matrix_name,
                description=f'从Excel导入的播放矩阵',
                status='active',
                version='1.0'
            )
            db.session.add(matrix)
            db.session.flush()

            # 解析数据
            current_audio_source = None
            current_a2b_channel = None
            current_playback_position = None
            current_headrest_mode = None
            entries = []

            for idx, row in df.iterrows():
                # 跳过空行
                if pd.isna(row.get('音源类型')) and pd.isna(row.get('A2B通道')) and pd.isna(row.get('播出方位')) and pd.isna(row.get('头枕模式')):
                    continue

                # 更新当前值（如果不是NaN）
                if not pd.isna(row.get('音源类型')):
                    current_audio_source = str(row['音源类型']).strip()
                if not pd.isna(row.get('A2B通道')):
                    current_a2b_channel = str(row['A2B通道']).strip()
                if not pd.isna(row.get('播出方位')):
                    current_playback_position = str(row['播出方位']).strip()
                if not pd.isna(row.get('头枕模式')):
                    current_headrest_mode = str(row['头枕模式']).strip()

                # 构建扬声器通道配置
                speaker_channels = {}
                for col in speaker_columns:
                    if col in df.columns and not pd.isna(row.get(col)):
                        value = str(row[col]).strip()
                        if value == '●':
                            speaker_channels[col] = '●'

                # 只有有扬声器通道开启时才创建条目
                if speaker_channels:
                    entry = PlaybackMatrixEntry(
                        matrix_id=matrix.id,
                        audio_source=current_audio_source or '未知',
                        a2b_channel=current_a2b_channel,
                        playback_position=current_playback_position,
                        headrest_mode=current_headrest_mode,
                        speaker_channels=json.dumps(speaker_channels, ensure_ascii=False),
                        sort_order=len(entries) + 1
                    )
                    db.session.add(entry)
                    entries.append(entry)

            db.session.commit()

            return {
                'message': f'导入成功，共创建 {len(entries)} 个条目',
                'matrix_id': matrix.id,
                'entry_count': len(entries)
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': f'导入失败: {str(e)}'}, 500


# 注册路由
api.add_resource(ImportPlaybackMatrixAPI, '/import/playback-matrix')
