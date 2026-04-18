"""
配置管理模块
"""
import os
import yaml
from typing import Any, Dict


class ConfigManager:
    """配置管理器"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.config = {}
            self._initialized = True
    
    def load_config(self, config_file='./config/app.yaml'):
        """加载配置文件"""
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"配置文件不存在: {config_file}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 环境变量覆盖
        self._override_from_env()
    
    def _override_from_env(self):
        """从环境变量覆盖配置"""
        # 数据库路径
        if os.environ.get('DB_PATH'):
            self.config.setdefault('database', {})['path'] = os.environ.get('DB_PATH')
        
        # 日志级别
        if os.environ.get('LOG_LEVEL'):
            self.config.setdefault('logging', {})['level'] = os.environ.get('LOG_LEVEL')
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持点分隔的键"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_all(self) -> Dict:
        """获取所有配置"""
        return self.config.copy()
    
    def validate(self):
        """验证配置"""
        required_keys = [
            'app.name',
            'database.type',
            'logging.level'
        ]
        
        for key in required_keys:
            if self.get(key) is None:
                raise ValueError(f"缺少必需的配置项: {key}")


# 全局配置管理器实例
config_manager = ConfigManager()


def load_config(config_file='./config/app.yaml'):
    """加载配置"""
    config_manager.load_config(config_file)


def get_config(key: str, default: Any = None) -> Any:
    """获取配置值"""
    return config_manager.get(key, default)
