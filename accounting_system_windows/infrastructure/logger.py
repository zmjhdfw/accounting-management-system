"""
日志管理模块
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
import re


class DesensitizingFilter(logging.Filter):
    """敏感信息脱敏过滤器"""
    
    SENSITIVE_FIELDS = ['password', 'token', 'secret', 'password_hash']
    
    def filter(self, record):
        """过滤日志记录，脱敏敏感信息"""
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            record.msg = self._desensitize(record.msg)
        if hasattr(record, 'args') and record.args:
            record.args = tuple(
                self._desensitize(str(arg)) if isinstance(arg, str) else arg
                for arg in record.args
            )
        return True
    
    def _desensitize(self, message):
        """脱敏处理"""
        for field in self.SENSITIVE_FIELDS:
            # 匹配 field=value 或 field: value 格式
            pattern = rf'({field}\s*[=:]\s*)[^\s,}}]+'
            message = re.sub(pattern, r'\1***', message, flags=re.IGNORECASE)
        return message


class LoggerManager:
    """日志管理器"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.loggers = {}
            self._initialized = True
    
    def setup(self, log_level='INFO', log_file='./logs/app.log', 
              max_size=10485760, backup_count=5, desensitize=True):
        """设置日志配置"""
        # 确保日志目录存在
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # 根日志配置
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level.upper()))
        
        # 清除现有处理器
        root_logger.handlers.clear()
        
        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 文件处理器
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        
        # 添加脱敏过滤器
        if desensitize:
            desensitizing_filter = DesensitizingFilter()
            file_handler.addFilter(desensitizing_filter)
            console_handler.addFilter(desensitizing_filter)
        
        # 添加处理器
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    
    def get_logger(self, name):
        """获取指定名称的日志器"""
        if name not in self.loggers:
            self.loggers[name] = logging.getLogger(name)
        return self.loggers[name]


# 全局日志管理器实例
logger_manager = LoggerManager()


def setup_logging(log_level='INFO', log_file='./logs/app.log', 
                  max_size=10485760, backup_count=5, desensitize=True):
    """设置日志配置"""
    logger_manager.setup(log_level, log_file, max_size, backup_count, desensitize)


def get_logger(name):
    """获取日志器"""
    return logger_manager.get_logger(name)
