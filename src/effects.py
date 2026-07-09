"""
效果模块 - 转场、滤镜和特效
"""

import numpy as np


class FilterEffect:
    """滤镜效果"""
    
    @staticmethod
    def apply_brightness(frame: np.ndarray, factor: float) -> np.ndarray:
        """调整亮度"""
        if factor < 0:
            return np.zeros_like(frame)
        result = frame.astype(np.float32) * factor
        return np.clip(result, 0, 255).astype(np.uint8)
    
    @staticmethod
    def apply_contrast(frame: np.ndarray, factor: float) -> np.ndarray:
        """调整对比度"""
        mean = np.mean(frame)
        result = mean + factor * (frame.astype(np.float32) - mean)
        return np.clip(result, 0, 255).astype(np.uint8)
