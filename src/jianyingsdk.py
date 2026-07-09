"""
剪映SDK集成模块 - 与剪映PC客户端交互
"""

import os
import json
import subprocess
import time
import shutil
from typing import List, Optional, Dict
from pathlib import Path
from src.scene_detection import Clip, SceneDetector
from src.subtitle_generator import Subtitle, SubtitleGenerator


class JianyingProject:
    """剪映项目类"""
    
    def __init__(self, project_path: str, project_name: str = "auto_clip"):
        self.project_path = project_path
        self.project_name = project_name
        self.project_dir = os.path.join(project_path, project_name)
        self.tracks = []
        self.audio_tracks = []
        self.metadata = {}
        
        os.makedirs(self.project_dir, exist_ok=True)
    
    def add_video_track(self, video_path: str, start_time: float = 0, duration: float = None) -> Dict:
        """添加视频轨道"""
        track = {
            'type': 'video',
            'path': video_path,
            'start_time': start_time,
            'duration': duration,
            'id': len(self.tracks)
        }
        self.tracks.append(track)
        print(f"[剪映项目] 添加视频轨道: {os.path.basename(video_path)}")
        return track
    
    def add_subtitle(self, text: str, start_time: float, end_time: float, style: Dict = None) -> Dict:
        """添加字幕"""
        subtitle = {
            'type': 'subtitle',
            'text': text,
            'start_time': start_time,
            'end_time': end_time,
            'style': style or {}
        }
        
        if 'subtitles' not in self.metadata:
            self.metadata['subtitles'] = []
        
        self.metadata['subtitles'].append(subtitle)
        return subtitle
    
    def save_project_file(self) -> str:
        """保存项目文件"""
        project_data = {
            'name': self.project_name,
            'version': '1.0',
            'tracks': self.tracks,
            'audio_tracks': self.audio_tracks,
            'metadata': self.metadata
        }
        
        project_file = os.path.join(self.project_dir, f"{self.project_name}.json")
        
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
        
        print(f"[剪映项目] 项目文件已保存: {project_file}")
        return project_file


class JianyingClipProcessor:
    """剪映剪辑处理器 - 与剪映PC客户端交互"""
    
    def __init__(self, input_video: str, config: Dict = None):
        self.input_video = input_video
        self.config = config or {}
        
        self.output_base = self.config.get('output_base_dir', 'D:/AutoClip_Projects')
        self.project_dir = os.path.join(self.output_base, 'projects')
        self.output_dir = os.path.join(self.output_base, 'outputs')
        self.temp_dir = os.path.join(self.output_base, 'temp')
        
        for dir_path in [self.project_dir, self.output_dir, self.temp_dir]:
            os.makedirs(dir_path, exist_ok=True)
            print(f"[剪映处理] 创建目录: {dir_path}")
        
        self.jianyingcuts_path = self._find_jianyingcuts()
        self.scene_detector = SceneDetector()
        self.subtitle_generator = SubtitleGenerator()
        self.project: Optional[JianyingProject] = None
        
        print("[剪映处理] 初始化完成")
    
    def _find_jianyingcuts(self) -> Optional[str]:
        """查找剪映PC客户端"""
        possible_paths = [
            "C:/Users/*/AppData/Local/JianyingPro/Jianyingcuts.exe",
            "C:/Program Files/JianyingPro/Jianyingcuts.exe",
            "C:/Program Files (x86)/JianyingPro/Jianyingcuts.exe",
            "D:/JianyingPro/Jianyingcuts.exe",
        ]
        
        for path_pattern in possible_paths:
            if '*' in path_pattern:
                from glob import glob
                matches = glob(path_pattern)
                for match in matches:
                    if os.path.exists(match):
                        return match
            else:
                if os.path.exists(path_pattern):
                    return path_pattern
        
        return None
    
    def create_project(self, project_name: str = "auto_clip") -> JianyingProject:
        """创建剪映项目"""
        print(f"[剪映处理] 创建项目: {project_name}")
        self.project = JianyingProject(self.project_dir, project_name)
        self.project.add_video_track(self.input_video)
        return self.project
    
    def auto_clip_with_jianyingcuts(self) -> Optional[JianyingProject]:
        """使用剪映自动剪辑"""
        print(f"[剪映处理] 开始自动剪辑: {self.input_video}")
        
        project_name = f"clip_{int(time.time())}"
        project = self.create_project(project_name)
        
        print("[剪映处理] 检测场景...")
        clips = self.scene_detector.detect_scenes(self.input_video)
        print(f"[剪映处理] 检测到 {len(clips)} 个场景")
        
        if self.jianyingcuts_path:
            self._launch_jianyingcuts_with_project(project)
        else:
            print("[剪映处理] ℹ️  提示: 请在剪映中手动编辑")
        
        return project
    
    def _launch_jianyingcuts_with_project(self, project: JianyingProject):
        """启动剪映客户端"""
        try:
            print(f"[剪映处理] 启动剪映客户端...")
            project_file = project.save_project_file()
            subprocess.Popen([self.jianyingcuts_path, project_file])
            print(f"[剪映处理] ✅ 剪映已启动")
        except Exception as e:
            print(f"[剪映处理] ❌ 启动剪映失败: {e}")
    
    def add_subtitles_to_project(self, subtitles: List[Subtitle] = None) -> None:
        """添加字幕到项目"""
        if not self.project:
            print("[剪映处理] ❌ 项目未创建")
            return
        
        if subtitles is None:
            print("[剪映处理] 生成字幕...")
            subtitles = self.subtitle_generator.generate_subtitles(self.input_video)
        
        print(f"[剪映处理] 添加 {len(subtitles)} 条字幕到项目")
        
        for subtitle in subtitles:
            self.project.add_subtitle(
                text=subtitle.text,
                start_time=subtitle.start_time,
                end_time=subtitle.end_time,
                style={'font_size': 40, 'color': 'white', 'background': 'black'}
            )
        
        self.project.save_project_file()
        print("[剪映处理] ✅ 字幕已添加到项目")
    
    def export_to_douyin(self, output_filename: str = None) -> str:
        """导出为抖音竖屏格式（到D盘）"""
        if output_filename is None:
            output_filename = f"douyin_{int(time.time())}.mp4"
        
        output_path = os.path.join(self.output_dir, output_filename)
        print(f"[剪映处理] 导出抖音竖屏格式")
        print(f"[剪映处理] 输出路径: {output_path}")
        
        info_file = os.path.join(self.output_dir, 'output_info.json')
        info_data = {
            'timestamp': int(time.time()),
            'input_video': self.input_video,
            'output_file': output_filename,
            'output_path': output_path,
            'format': 'mp4',
            'resolution': '1080x1920',
            'project': self.project.project_name if self.project else None
        }
        
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info_data, f, ensure_ascii=False, indent=2)
        
        print(f"[剪映处理] ✅ 导出信息已记录: {info_file}")
        return output_path
    
    def cleanup_temp_files(self) -> None:
        """清理临时文件"""
        print("[剪映处理] 清理临时文件...")
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            os.makedirs(self.temp_dir)
            print("[剪映处理] ✅ 临时文件已清理")
