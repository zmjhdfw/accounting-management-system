"""
审计日志模型
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel


class AuditLog(BaseModel):
    """审计日志模型"""
    __tablename__ = 'audit_logs'
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='用户ID')
    username = Column(String(50), nullable=False, comment='用户名')
    operation = Column(String(50), nullable=False, comment='操作类型')
    module = Column(String(50), nullable=False, comment='模块名称')
    target_type = Column(String(50), comment='目标类型')
    target_id = Column(Integer, comment='目标ID')
    description = Column(Text, nullable=False, comment='操作描述')
    old_value = Column(Text, comment='旧值')
    new_value = Column(Text, comment='新值')
    ip_address = Column(String(50), comment='IP地址')
    user_agent = Column(String(200), comment='用户代理')
    is_success = Column(Boolean, default=True, nullable=False, comment='是否成功')
    error_message = Column(Text, comment='错误信息')
    
    # 关系
    user = relationship('User', back_populates='audit_logs')
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, operation='{self.operation}')>"
