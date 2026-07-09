"""
视频处理核心模块 - 集成剪映和D盘管理
"""

import os
from typing import List, Optional
from src.config import Config
from src.jianyingsdk import JianyingClipProcessor, JianyingProject
from src.scene_detection import SceneDetector, Clip
from src.subtitle_generator import SubtitleGenerator, Subtitle
from src.file_manager import DiskFileManager


class VideoProcessor:
    """视频处理器 - 集成剪映和D盘文件管理"""
    
    def __init__(self, input_video: str = None, config_path: str = "config.yaml"):
        self.input_video = input_video
        self.config = Config(config_path)
        
        print("[视频处理] 初始化D盘文件系统...")
        self.file_manager = DiskFileManager
        self.file_manager.init_project_structure()
        
        jianyingcuts_config = {
            'output_base_dir': self.config.get('output.project_dir', 'D:/AutoClip_Projects')
        }
        self.jianyingcuts_processor = JianyingClipProcessor(
            input_video=input_video,
            config=jianyingcuts_config
        )
        
        self.scene_detector = SceneDetector(
            method=self.config.get('scene_detection.method', 'content'),
            threshold=self.config.get('scene_detection.threshold', 0.3)
        )
        
        self.subtitle_generator = SubtitleGenerator(
            model_size=self.config.get('subtitles.model_size', 'base'),
            language=self.config.get('subtitles.language', 'zh')
        ) if self.config.get('subtitles.enabled', False) else None
        
        self.clips: List[Clip] = []
        self.subtitles: List[Subtitle] = []
        
        print("[视频处理] 初始化完成")
    
    def auto_clip_with_jianyingcuts(self) -> Optional[JianyingProject]:
        """使用剪映进行自动剪辑"""
        print(f"\n[视频处理] ========== 开始使用剪映剪辑 ==========")
        print(f"[视频处理] 输入视频: {self.input_video}")
        
        project = self.jianyingcuts_processor.auto_clip_with_jianyingcuts()
        return project
    
    def add_subtitles_to_jianyingcuts(self) -> List[Subtitle]:
        """生成字幕并添加到剪映项目"""
        print(f"\n[视频处理] 生成字幕...")
        
        if not self.subtitle_generator:
            print("[视频处理] ⚠️  字幕生成已禁用")
            return []
        
        subtitles = self.subtitle_generator.generate_subtitles(self.input_video)
        self.subtitles = subtitles
        
        if self.jianyingcuts_processor.project:
            self.jianyingcuts_processor.add_subtitles_to_project(subtitles)
        
        return subtitles
    
    def export_to_d_drive(self, output_filename: str = None) -> str:
        """导出最终视频到D盘"""
        print(f"\n[视频处理] ========== 导出到D盘 ==========")
        
        if output_filename is None:
            import time
            output_filename = f"douyin_output_{int(time.time())}.mp4"
        
        output_path = self.jianyingcuts_processor.export_to_douyin(output_filename)
        
        print(f"\n[视频处理] ✅ 导出完成！")
        print(f"[视频处理] 输出路径: {output_path}")
        print(f"\n[视频处理] 💾 D盘位置: D:\\AutoClip_Projects\\outputs\\{output_filename}")
        
        return output_path
    
    def get_project_info(self) -> dict:
        """获取当前项目信息"""
        info = {
            'input_video': self.input_video,
            'd_drive_base': self.jianyingcuts_processor.output_base,
            'project_path': self.jianyingcuts_processor.project_dir,
            'output_path': self.jianyingcuts_processor.output_dir,
            'temp_path': self.jianyingcuts_processor.temp_dir,
            'clips_count': len(self.clips),
            'subtitles_count': len(self.subtitles),
        }
        
        if self.jianyingcuts_processor.project:
            info['project_name'] = self.jianyingcuts_processor.project.project_name
        
        return info
    
    def list_output_files(self) -> List[dict]:
        """列出D盘中的所有输出文件"""
        files = self.file_manager.list_output_files()
        
        print(f"\n[视频处理] D盘输出文件:")
        for file in files:
            print(f"  - {file['name']} ({file['size']/1024/1024:.2f}MB)")
        
        return files
    
    def show_d_drive_status(self) -> dict:
        """显示D盘状态"""
        usage = self.file_manager.get_disk_usage()
        
        print(f"\n[视频处理] D盘状态:")
        for key, value in usage.items():
            print(f"  {key}: {value}")
        
        return usage
    
    def cleanup(self) -> None:
        """清理临时文件"""
        print(f"\n[视频处理] 清理临时文件...")
        self.jianyingcuts_processor.cleanup_temp_files()
        print(f"[视频处理] ✅ 清理完成")
