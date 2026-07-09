"""
配置管理模块
"""

import yaml
import os
from typing import Dict, Any


class Config:
    """配置类 - 管理所有系统配置"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载YAML配置文件"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值（支持点记号 如 'input.video_path'）"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, output_path: str = None) -> None:
        """保存配置到文件"""
        path = output_path or self.config_path
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
