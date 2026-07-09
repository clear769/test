"""
自动剪辑信息流视频系统
"""

__version__ = "2.0.0"
__author__ = "Video Auto Clip"

from src.video_processor import VideoProcessor
from src.config import Config
from src.file_manager import DiskFileManager

__all__ = ["VideoProcessor", "Config", "DiskFileManager"]
