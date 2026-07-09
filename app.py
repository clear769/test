"""
更新后Flask Web应用 - 集成剪映和D盘管理
"""

from flask import Flask, render_template, request, jsonify
import os
import json
import threading
from src.video_processor import VideoProcessor
from src.config import Config
from src.file_manager import DiskFileManager


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:/AutoClip_Projects/uploads'
app.config['OUTPUT_FOLDER'] = 'D:/AutoClip_Projects/outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

# 创建必要的目录
for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# 全局处理任务状态
tasks = {}


@app.route('/')
def index():
    """主页"""
    return jsonify({'message': 'API Server Running', 'version': '2.0.0'})


@app.route('/api/init', methods=['POST'])
def init_system():
    """初始化系统和D盘结构"""
    try:
        print("[Web] 初始化系统...")
        paths = DiskFileManager.init_project_structure()
        
        return jsonify({
            'success': True,
            'message': '系统初始化完成',
            'paths': paths
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/config', methods=['GET'])
def get_config():
    """获取当前配置"""
    try:
        config = Config('config.yaml')
        config_dict = {
            'scene_detection': {
                'threshold': config.get('scene_detection.threshold'),
            },
            'output': {
                'base_dir': config.get('output.project_dir'),
            }
        }
        return jsonify({'success': True, 'data': config_dict})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/process', methods=['POST'])
def process_video():
    """处理视频（后台任务）"""
    try:
        data = request.json
        video_path = data.get('video_path')
        task_id = data.get('task_id', 'default')
        
        if not os.path.exists(video_path):
            return jsonify({'success': False, 'error': '视频文件不存在'}), 400
        
        thread = threading.Thread(
            target=_process_video_background,
            args=(video_path, task_id)
        )
        thread.start()
        
        tasks[task_id] = {
            'status': 'processing',
            'progress': 0,
            'message': '启动剪映进行处理...'
        }
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '视频处理已启动'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def _process_video_background(video_path: str, task_id: str):
    """后台处理视频"""
    try:
        processor = VideoProcessor(video_path)
        
        tasks[task_id]['message'] = '启动剪映...'
        tasks[task_id]['progress'] = 20
        project = processor.auto_clip_with_jianyingcuts()
        
        tasks[task_id]['message'] = '生成字幕...'
        tasks[task_id]['progress'] = 40
        processor.add_subtitles_to_jianyingcuts()
        
        tasks[task_id]['message'] = '等待剪映编辑完成...'
        tasks[task_id]['progress'] = 60
        
        tasks[task_id]['message'] = '导出到D盘...'
        tasks[task_id]['progress'] = 80
        output_path = processor.export_to_d_drive()
        
        tasks[task_id]['message'] = '清理临时文件...'
        processor.cleanup()
        
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['message'] = '处理完成'
        tasks[task_id]['output_path'] = output_path
        tasks[task_id]['progress'] = 100
        
        print(f"[Web] 任务 {task_id} 完成")
    
    except Exception as e:
        tasks[task_id]['status'] = 'failed'
        tasks[task_id]['error'] = str(e)
        print(f"[Web] 任务 {task_id} 失败: {e}")


@app.route('/api/task/<task_id>', methods=['GET'])
def get_task_status(task_id: str):
    """获取任务状态"""
    if task_id not in tasks:
        return jsonify({'success': False, 'error': '任务不存在'}), 404
    
    return jsonify({'success': True, 'data': tasks[task_id]})


@app.route('/api/files', methods=['GET'])
def list_files():
    """列出D盘输出文件"""
    try:
        files = DiskFileManager.list_output_files()
        return jsonify({
            'success': True,
            'files': files,
            'count': len(files)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/disk-status', methods=['GET'])
def get_disk_status():
    """获取D盘状态"""
    try:
        usage = DiskFileManager.get_disk_usage()
        return jsonify({'success': True, 'data': usage})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/projects', methods=['GET'])
def list_projects():
    """列出所有项目"""
    try:
        projects = DiskFileManager.list_all_projects()
        return jsonify({
            'success': True,
            'projects': projects,
            'count': len(projects)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/info', methods=['GET'])
def get_info():
    """获取应用信息"""
    return jsonify({
        'name': '自动剪辑信息流视频系统 - 剪映版',
        'version': '2.0.0',
        'description': '使用剪映PC客户端自动剪辑和优化视频为抖音信息流格式',
        'output_location': 'D:/AutoClip_Projects/outputs'
    })


@app.errorhandler(404)
def not_found(error):
    """错误处理"""
    return jsonify({'success': False, 'error': '页面不存在'}), 404


if __name__ == '__main__':
    print("\n" + "="*60)
    print("█  自动剪辑信息流视频系统 - 剪映版")
    print("="*60)
    print("\n[Web] Flask应用启动中...")
    print("[Web] 访问地址: http://localhost:5000")
    print("[Web] 输出位置: D:/AutoClip_Projects/outputs/")
    print("[Web] 项目位置: D:/AutoClip_Projects/projects/")
    print("\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
