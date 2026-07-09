# 自动剪辑信息流视频系统

一个功能强大的视频自动剪辑工具，专门为抖音、快手等信息流平台优化。**集成剪映PC客户端**，支持智能场景检测、自动字幕生成、转场效果等。

## 功能特性

✨ **智能剪辑（集成剪映）**
- 自动场景检测和转场识别
- 直接调用剪映PC客户端进行编辑
- 支持多种剪辑策略

📝 **字幕功能**
- 自动语音识别（中文）
- 智能字幕生成和位置优化
- 导入到剪映进行编辑

🎬 **视频优化**
- 自动转换为抖音竖屏格式（9:16）
- 背景填充和模糊处理
- 转场特效和滤镜

🎵 **音频处理**
- 背景音乐添加
- 音量自动调节
- 音效库集成

🖥️ **用户界面**
- Web界面支持
- 实时预览
- 批量处理能力

📁 **文件管理**
- 所有导出文件自动保存到 **D盘**
- 自动创建项目目录结构

## 快速开始

### 环境要求
- Python 3.8+
- FFmpeg
- 剪映PC客户端（已安装）
- Node.js 14+（前端可选）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基础使用

```python
from src.video_processor import VideoProcessor

# 使用剪映进行剪辑
processor = VideoProcessor(input_video='D:/videos/input.mp4')

# 自动检测并剪辑
processor.auto_clip_with_jianyingcuts()

# 添加字幕
processor.add_subtitles_to_jianyingcuts()

# 导出为抖音格式（自动保存到D盘）
processor.export_to_d_drive()
```

### 快速启动

```bash
python quickstart.py
```

### Web界面

```bash
python app.py
# 访问 http://localhost:5000
```

## 项目结构

```
test/
├── src/
│   ├── __init__.py
│   ├── jianyingsdk.py              # 剪映SDK集成
│   ├── scene_detection.py          # 场景检测
│   ├── subtitle_generator.py       # 字幕生成
│   ├── audio_processor.py          # 音频处理
│   ├── format_converter.py         # 格式转换
│   ├── effects.py                  # 特效处理
│   ├── config.py                   # 配置管理
│   └── file_manager.py             # D盘文件管理
├── app.py                          # Flask Web应用
├── quickstart.py                   # 快速启动脚本
├── example_usage.py                # 使用示例
├── requirements.txt                # 依赖列表
├── config.yaml                     # 配置文件
└── README.md                       # 项目说明
```

## 工作流程

```
输入视频 → 剪映PC客户端 → 字幕和特效 → 抖音格式转换 → D:\AutoClip_Projects\outputs
            ↓
        自动项目保存
```

## D盘文件结构

```
D:/
└── AutoClip_Projects/
    ├── projects/           # 剪映项目文件
    ├── outputs/            # 最终输出视频
    ├── uploads/            # 上传的视频
    ├── temp/               # 临时文件
    ├── videos/             # 视频存储
    ├── music/              # 背景音乐
    ├── subtitles/          # 字幕文件
    └── backups/            # 备份文件
```

## 配置文件

编辑 `config.yaml` 自定义：
- 输入输出路径（D盘位置）
- 剪映客户端路径
- 剪辑参数
- 字幕样式
- 导出格式

## 使用示例

### 示例1: 完整工作流

```python
from src.video_processor import VideoProcessor

processor = VideoProcessor(input_video='input.mp4')

# 使用剪映剪辑
project = processor.auto_clip_with_jianyingcuts()

# 生成字幕
subtitles = processor.add_subtitles_to_jianyingcuts()

# 导出到D盘
output_path = processor.export_to_d_drive()
print(f"输出文件: {output_path}")
```

### 示例2: 列出输出文件

```python
from src.file_manager import DiskFileManager

files = DiskFileManager.list_output_files()
for file in files:
    print(f"{file['name']} - {file['size']/1024/1024:.2f}MB")
```

### 示例3: 查看D盘状态

```python
from src.file_manager import DiskFileManager

usage = DiskFileManager.get_disk_usage()
print(usage)
```

## 许可证

MIT

## 联系方式

如有问题，请提交Issue或联系开发者。
