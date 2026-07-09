"""
更新后的使用示例 - 使用剪映和D盘管理
"""

from src.video_processor import VideoProcessor
from src.file_manager import DiskFileManager
import os


def example_jianyingcuts_workflow():
    """示例1: 完整的剪映工作流"""
    print("\n" + "="*60)
    print("示例1: 完整的剪映工作流（推荐）")
    print("="*60 + "\n")
    
    processor = VideoProcessor(input_video='input.mp4')
    
    print("\n[步骤1] 启动剪映自动剪辑...")
    project = processor.auto_clip_with_jianyingcuts()
    
    if project:
        print(f"✅ 剪映项目已创建: {project.project_name}")
    
    print("\n[步骤2] 生成字幕...")
    subtitles = processor.add_subtitles_to_jianyingcuts()
    print(f"✅ 生成了 {len(subtitles)} 条字幕")
    
    print("\n[步骤3] 请在剪映中完成编辑和调整...")
    input("编辑完成后，按Enter继续...")
    
    print("\n[步骤4] 导出到D盘...")
    output_path = processor.export_to_d_drive()
    
    print("\n[步骤5] 查看输出文件...")
    processor.list_output_files()
    
    print("\n[步骤6] 查看D盘状态...")
    processor.show_d_drive_status()
    
    print("\n[项目信息]")
    info = processor.get_project_info()
    for key, value in info.items():
        print(f"  {key}: {value}")


def example_d_drive_management():
    """示例2: D盘文件管理"""
    print("\n" + "="*60)
    print("示例2: D盘文件管理")
    print("="*60 + "\n")
    
    print("1. 初始化D盘目录结构...")
    paths = DiskFileManager.init_project_structure()
    
    print("\n2. 列出所有项目...")
    projects = DiskFileManager.list_all_projects()
    print(f"找到 {len(projects)} 个项目:")
    for project in projects:
        print(f"  - {project}")
    
    print("\n3. 列出所有输出文件...")
    outputs = DiskFileManager.list_output_files()
    print(f"找到 {len(outputs)} 个输出文件:")
    for output in outputs:
        print(f"  - {output['name']} ({output['size']/1024/1024:.2f}MB)")
    
    print("\n4. D盘使用情况...")
    usage = DiskFileManager.get_disk_usage()
    for key, value in usage.items():
        print(f"  {key}: {value}")


if __name__ == '__main__':
    print("\n")
    print("█" * 60)
    print("█  自动剪辑信息流视频 - 剪映版本 - 使用示例")
    print("█" * 60)
    print("\n")
    
    print("可用的示例:")
    print("  1. example_jianyingcuts_workflow() - 完整剪映工作流（推荐）")
    print("  2. example_d_drive_management() - D盘文件管理")
    
    print("\n📊 使用方法:")
    print("  取消注释下面的示例函数调用来运行示例\n")
    
    # 取消注释下面的任何一个来运行示例
    # example_jianyingcuts_workflow()
    # example_d_drive_management()
    
    print("📌 提示:")
    print("  - 所有输出文件都会自动保存到 D:\\AutoClip_Projects\\outputs\\")
    print("  - 项目文件保存在 D:\\AutoClip_Projects\\projects\\")
    print("  - 临时文件保存在 D:\\AutoClip_Projects\\temp\\")
