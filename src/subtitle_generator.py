"""
字幕生成模块 - 自动语音识别和字幕生成
"""

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

from typing import List
from dataclasses import dataclass


@dataclass
class Subtitle:
    """字幕类"""
    start_time: float  # 开始时间（秒）
    end_time: float    # 结束时间（秒）
    text: str          # 字幕文本
    
    def __repr__(self):
        return f"Subtitle({self.start_time:.2f}s-{self.end_time:.2f}s: {self.text})"


class SubtitleGenerator:
    """字幕生成器 - 使用Whisper进行语音识别"""
    
    def __init__(self, model_size: str = "base", language: str = "zh"):
        self.model_size = model_size
        self.language = language
        self.model = None
        if WHISPER_AVAILABLE:
            self._load_model()
    
    def _load_model(self):
        """加载Whisper模型"""
        print(f"[字幕生成] 加载Whisper模型 ({self.model_size})...")
        self.model = whisper.load_model(self.model_size)
        print(f"[字幕生成] 模型加载完成")
    
    def generate_subtitles(self, video_path: str) -> List[Subtitle]:
        """从视频生成字幕"""
        if not WHISPER_AVAILABLE:
            print(f"[字幕生成] ⚠️  Whisper未安装，跳过字幕生成")
            return []
        
        print(f"[字幕生成] 识别视频语音: {video_path}")
        
        result = self.model.transcribe(
            video_path,
            language=self.language,
            verbose=False
        )
        
        subtitles = []
        if "segments" in result:
            for segment in result["segments"]:
                subtitle = Subtitle(
                    start_time=segment["start"],
                    end_time=segment["end"],
                    text=segment["text"].strip()
                )
                subtitles.append(subtitle)
        
        print(f"[字幕生成] 生成了 {len(subtitles)} 条字幕")
        return subtitles
    
    def generate_srt_file(self, subtitles: List[Subtitle], output_path: str) -> None:
        """生成SRT字幕文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, subtitle in enumerate(subtitles, 1):
                start = self._seconds_to_srt_time(subtitle.start_time)
                end = self._seconds_to_srt_time(subtitle.end_time)
                
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{subtitle.text}\n")
                f.write("\n")
        
        print(f"[字幕生成] SRT文件已保存: {output_path}")
    
    @staticmethod
    def _seconds_to_srt_time(seconds: float) -> str:
        """将秒数转换为SRT时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
