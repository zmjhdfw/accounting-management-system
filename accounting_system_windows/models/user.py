"""
用户和角色模型
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Table, Integer, DateTime
from sqlalchemy.orm import relationship
from models.base import BaseModel

# 用户角色关联表（多对多）
user_role = Table(
    'user_role',
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)


class Role(BaseModel):
    """角色模型"""
    __tablename__ = 'roles'
    
    name = Column(String(50), unique=True, nullable=False, comment='角色名称')
    description = Column(String(200), comment='角色描述')
    is_active = Column(Boolean, default=True, nullable=False, comment='是否启用')
    
    # 关系
    users = relationship('User', secondary=user_role, back_populates='roles')
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"


class User(BaseModel):
    """用户模型"""
    __tablename__ = 'users'
    
    username = Column(String(50), unique=True, nullable=False, comment='用户名')
    password_hash = Column(String(255), nullable=False, comment='密码哈希')
    real_name = Column(String(50), comment='真实姓名')
    email = Column(String(100), comment='邮箱')
    phone = Column(String(20), comment='电话')
    is_active = Column(Boolean, default=True, nullable=False, comment='是否启用')
    is_locked = Column(Boolean, default=False, nullable=False, comment='是否锁定')
    login_fail_count = Column(Integer, default=0, comment='登录失败次数')
    last_login_time = Column(DateTime, comment='最后登录时间')
    
    # 关系
    roles = relationship('Role', secondary=user_role, back_populates='users')
    audit_logs = relationship('AuditLog', back_populates='user')
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    
    def has_permission(self, permission_name):
        """检查用户是否有指定权限"""
        for role in self.roles:
            if role.is_active and hasattr(role, 'permissions'):
                for permission in role.permissions:
                    if permission.name == permission_name:
                        return True
        return False
