"""
D盘文件管理模块 - 管理所有D盘上的项目文件
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class DiskFileManager:
    """D盘文件管理器"""
    
    D_DRIVE_ROOT = 'D:/'
    PROJECT_BASE = 'D:/AutoClip_Projects'
    
    @staticmethod
    def init_project_structure() -> Dict[str, str]:
        """初始化D盘项目目录结构"""
        paths = {
            'base': DiskFileManager.PROJECT_BASE,
            'projects': os.path.join(DiskFileManager.PROJECT_BASE, 'projects'),
            'outputs': os.path.join(DiskFileManager.PROJECT_BASE, 'outputs'),
            'temp': os.path.join(DiskFileManager.PROJECT_BASE, 'temp'),
            'videos': os.path.join(DiskFileManager.PROJECT_BASE, 'videos'),
            'music': os.path.join(DiskFileManager.PROJECT_BASE, 'music'),
            'subtitles': os.path.join(DiskFileManager.PROJECT_BASE, 'subtitles'),
            'backups': os.path.join(DiskFileManager.PROJECT_BASE, 'backups'),
        }
        
        for dir_path in paths.values():
            os.makedirs(dir_path, exist_ok=True)
            print(f"✓ 创建目录: {dir_path}")
        
        return paths
    
    @staticmethod
    def list_output_files() -> List[Dict[str, str]]:
        """列出所有输出文件"""
        output_dir = os.path.join(DiskFileManager.PROJECT_BASE, 'outputs')
        
        if not os.path.exists(output_dir):
            return []
        
        files = []
        for filename in os.listdir(output_dir):
            filepath = os.path.join(output_dir, filename)
            if os.path.isfile(filepath):
                files.append({
                    'name': filename,
                    'path': filepath,
                    'size': os.path.getsize(filepath),
                    'modified': datetime.fromtimestamp(
                        os.path.getmtime(filepath)
                    ).isoformat()
                })
        
        return files
    
    @staticmethod
    def list_all_projects() -> List[str]:
        """列出所有项目"""
        projects_dir = os.path.join(DiskFileManager.PROJECT_BASE, 'projects')
        
        if not os.path.exists(projects_dir):
            return []
        
        return [
            d for d in os.listdir(projects_dir)
            if os.path.isdir(os.path.join(projects_dir, d))
        ]
    
    @staticmethod
    def get_disk_usage() -> Dict[str, str]:
        """获取D盘使用情况"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(DiskFileManager.D_DRIVE_ROOT)
            
            def format_size(bytes_size):
                for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                    if bytes_size < 1024:
                        return f"{bytes_size:.2f} {unit}"
                    bytes_size /= 1024
                return f"{bytes_size:.2f} TB"
            
            return {
                'total': format_size(total),
                'used': format_size(used),
                'free': format_size(free),
                'percent_used': f"{(used / total) * 100:.1f}%"
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def cleanup_temp_files() -> int:
        """清理临时文件"""
        temp_dir = os.path.join(DiskFileManager.PROJECT_BASE, 'temp')
        
        if not os.path.exists(temp_dir):
            return 0
        
        count = 0
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    count += 1
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    count += 1
            except Exception as e:
                print(f"⚠️  无法删除 {item_path}: {e}")
        
        print(f"✓ 临时文件清理完成，共清理 {count} 项")
        return count
