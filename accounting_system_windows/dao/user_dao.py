"""
用户DAO
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from dao.base_dao import BaseDao
from models.user import User, Role


class UserDao(BaseDao):
    """用户DAO"""
    
    def __init__(self, session: Session):
        super().__init__(session, User)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.session.query(User).filter_by(username=username).first()
    
    def get_active_users(self) -> List[User]:
        """获取所有活跃用户"""
        return self.session.query(User).filter_by(is_active=True).all()
    
    def update_last_login(self, user_id: int):
        """更新最后登录时间"""
        from datetime import datetime
        user = self.get_by_id(user_id)
        if user:
            user.last_login_time = datetime.now()
            user.login_fail_count = 0
            self.session.flush()
    
    def increment_login_fail(self, user_id: int):
        """增加登录失败次数"""
        user = self.get_by_id(user_id)
        if user:
            user.login_fail_count += 1
            self.session.flush()
    
    def lock_user(self, user_id: int):
        """锁定用户"""
        user = self.get_by_id(user_id)
        if user:
            user.is_locked = True
            self.session.flush()
    
    def unlock_user(self, user_id: int):
        """解锁用户"""
        user = self.get_by_id(user_id)
        if user:
            user.is_locked = False
            user.login_fail_count = 0
            self.session.flush()


class RoleDao(BaseDao):
    """角色DAO"""
    
    def __init__(self, session: Session):
        super().__init__(session, Role)
    
    def get_by_name(self, name: str) -> Optional[Role]:
        """根据角色名获取角色"""
        return self.session.query(Role).filter_by(name=name).first()
    
    def get_active_roles(self) -> List[Role]:
        """获取所有活跃角色"""
        return self.session.query(Role).filter_by(is_active=True).all()
