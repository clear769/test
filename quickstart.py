"""
快速开始脚本 - 使用剪映进行视频剪辑
"""

import os
import sys
from src.video_processor import VideoProcessor
from src.file_manager import DiskFileManager


def main():
    """主函数"""
    print("\n" + "█"*60)
    print("█  自动剪辑信息流视频系统 - 剪映版")
    print("█  快速开始")
    print("█"*60 + "\n")
    
    # 第1步: 初始化D盘
    print("[步骤1] 初始化D盘目录结构...")
    DiskFileManager.init_project_structure()
    print("✅ D盘目录已初始化\n")
    
    # 第2步: 选择输入视频
    print("[步骤2] 选择输入视频...")
    video_path = input("请输入视频路径 (默认: input.mp4): ").strip()
    if not video_path:
        video_path = 'input.mp4'
    
    if not os.path.exists(video_path):
        print(f"❌ 错误: 文件不存在 - {video_path}")
        sys.exit(1)
    
    print(f"✅ 视频文件: {video_path}\n")
    
    # 第3步: 初始化处理器
    print("[步骤3] 初始化处理器...")
    try:
        processor = VideoProcessor(input_video=video_path)
        print("✅ 处理器初始化完成\n")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)
    
    # 第4步: 使用剪映
    print("[步骤4] 启动剪映进行自动剪辑...")
    print("提示: 剪映将在后台启动，请在客户端中进行编辑和调整\n")
    
    try:
        project = processor.auto_clip_with_jianyingcuts()
        print("✅ 剪映已启动\n")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)
    
    # 第5步: 生成字幕
    print("[步骤5] 生成字幕...")
    try:
        subtitles = processor.add_subtitles_to_jianyingcuts()
        print(f"✅ 生成了 {len(subtitles)} 条字幕\n")
    except Exception as e:
        print(f"⚠️  字幕生成失败: {e}\n")
    
    # 第6步: 等待用户编辑
    print("[步骤6] 等待编辑完成...")
    print("请在剪映中完成视频编辑，然后回来按Enter继续\n")
    input("📌 编辑完成后，按Enter键继续...\n")
    
    # 第7步: 导出到D盘
    print("[步骤7] 导出到D盘...")
    try:
        output_path = processor.export_to_d_drive()
        print(f"✅ 导出完成！\n")
        print(f"📁 输出文件路径: {output_path}\n")
    except Exception as e:
        print(f"❌ 导出失败: {e}")
        sys.exit(1)
    
    # 第8步: 清理临时文件
    print("[步骤8] 清理临时文件...")
    try:
        processor.cleanup()
        print("✅ 临时文件已清理\n")
    except Exception as e:
        print(f"⚠️  清理失败: {e}\n")
    
    # 第9步: 显示最终信息
    print("[步骤9] 最终信息...")
    print("="*60)
    
    # 显示项目信息
    print("\n📊 项目信息:")
    info = processor.get_project_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # 显示D盘状态
    print("\n💾 D盘状态:")
    usage = processor.show_d_drive_status()
    
    # 列出输出文件
    print("\n📂 输出文件:")
    files = processor.list_output_files()
    
    print("\n" + "="*60)
    print("✅ 处理完成！")
    print(f"📁 所有文件都已保存到: D:\\AutoClip_Projects\\")
    print("="*60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)
