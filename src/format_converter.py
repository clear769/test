"""
格式转换模块 - 转换为抖音竖屏格式
"""

import cv2
import numpy as np
from typing import Tuple


class FormatConverter:
    """格式转换器 - 处理视频宽高比和背景填充"""
    
    def __init__(self, target_width: int = 1080, target_height: int = 1920):
        self.target_width = target_width
        self.target_height = target_height
    
    def get_aspect_ratio(self) -> float:
        """获取目标宽高比"""
        return self.target_width / self.target_height
