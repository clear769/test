"""
场景检测模块 - 自动检测视频场景变化和转场
"""

import cv2
import numpy as np
from typing import List, Tuple


class Clip:
    """视频片段类"""
    
    def __init__(self, start_time: float, end_time: float, score: float = 1.0):
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time
        self.score = score  # 片段质量评分
    
    def __repr__(self):
        return f"Clip({self.start_time:.2f}s - {self.end_time:.2f}s, score={self.score:.2f})"


class SceneDetector:
    """场景检测器 - 使用多种方法检测视频转场"""
    
    def __init__(self, method: str = "content", threshold: float = 0.3):
        """
        初始化场景检测器
        
        Args:
            method: 检测方法 ('content', 'optical_flow', 'histogram')
            threshold: 检测阈值 (0-1)
        """
        self.method = method
        self.threshold = threshold
    
    def detect_scenes(self, video_path: str, fps: int = 30) -> List[Clip]:
        """检测视频中的所有场景转场"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        sample_interval = max(1, int(video_fps / fps))
        
        print(f"[场景检测] 总帧数: {total_frames}, 视频FPS: {video_fps}")
        
        if self.method == "content":
            clips = self._detect_content_change(cap, total_frames, sample_interval, video_fps)
        else:
            clips = self._detect_content_change(cap, total_frames, sample_interval, video_fps)
        
        cap.release()
        return clips
    
    def _detect_content_change(self, cap, total_frames: int, sample_interval: int, video_fps: float) -> List[Clip]:
        """基于内容变化的场景检测"""
        frame_diffs = []
        prev_frame = None
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % sample_interval == 0:
                frame_small = cv2.resize(frame, (320, 240))
                frame_gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
                
                if prev_frame is not None:
                    diff = cv2.absdiff(prev_frame, frame_gray)
                    diff_score = np.mean(diff) / 255.0
                    frame_diffs.append(diff_score)
                
                prev_frame = frame_gray
            
            frame_count += 1
        
        clips = self._extract_clips_from_diffs(frame_diffs, video_fps, sample_interval)
        print(f"[场景检测] 检测到 {len(clips)} 个场景")
        return clips
    
    def _extract_clips_from_diffs(self, diffs: List[float], video_fps: float, sample_interval: int) -> List[Clip]:
        """从差异数组中提取片段"""
        if not diffs:
            return []
        
        diffs = np.array(diffs)
        mean_diff = np.mean(diffs)
        std_diff = np.std(diffs)
        threshold = mean_diff + self.threshold * std_diff
        transitions = np.where(diffs > threshold)[0]
        
        clips = []
        if len(transitions) == 0:
            total_duration = len(diffs) * sample_interval / video_fps
            clips.append(Clip(0, total_duration, 1.0))
        else:
            prev_transition = 0
            for transition in transitions:
                start_time = prev_transition * sample_interval / video_fps
                end_time = transition * sample_interval / video_fps
                if end_time - start_time > 0.5:
                    clips.append(Clip(start_time, end_time, 1.0))
                prev_transition = transition
            
            start_time = prev_transition * sample_interval / video_fps
            total_duration = len(diffs) * sample_interval / video_fps
            if total_duration - start_time > 0.5:
                clips.append(Clip(start_time, total_duration, 1.0))
        
        return clips
