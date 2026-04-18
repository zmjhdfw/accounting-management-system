"""
用户认证服务
"""
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from dao.user_dao import UserDao
from models.user import User
from infrastructure.logger import get_logger
from infrastructure.database import DatabaseManager

logger = get_logger(__name__)


class AuthService:
    """认证服务"""
    
    MAX_LOGIN_FAIL_COUNT = 5
    
    def __init__(self, session: Session):
        self.session = session
        self.user_dao = UserDao(session)
    
    def login(self, username: str, password: str) -> Tuple[bool, Optional[User], str]:
        """
        用户登录
        返回: (是否成功, 用户对象, 消息)
        """
        user = self.user_dao.get_by_username(username)
        
        if not user:
            logger.warning(f"登录失败: 用户不存在 - {username}")
            return False, None, "用户名或密码错误"
        
        if not user.is_active:
            logger.warning(f"登录失败: 用户已禁用 - {username}")
            return False, None, "用户已被禁用"
        
        if user.is_locked:
            logger.warning(f"登录失败: 用户已锁定 - {username}")
            return False, None, "用户已被锁定，请联系管理员"
        
        # 验证密码
        if not DatabaseManager.verify_password(password, user.password_hash):
            self.user_dao.increment_login_fail(user.id)
            
            # 检查是否需要锁定
            if user.login_fail_count >= self.MAX_LOGIN_FAIL_COUNT - 1:
                self.user_dao.lock_user(user.id)
                logger.warning(f"用户已锁定: {username}")
                return False, None, "登录失败次数过多，用户已被锁定"
            
            logger.warning(f"登录失败: 密码错误 - {username}")
            return False, None, f"用户名或密码错误，剩余尝试次数: {self.MAX_LOGIN_FAIL_COUNT - user.login_fail_count - 1}"
        
        # 登录成功
        self.user_dao.update_last_login(user.id)
        logger.info(f"用户登录成功: {username}")
        
        return True, user, "登录成功"
    
    def logout(self, user_id: int):
        """用户登出"""
        logger.info(f"用户登出: user_id={user_id}")
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        修改密码
        返回: (是否成功, 消息)
        """
        user = self.user_dao.get_by_id(user_id)
        
        if not user:
            return False, "用户不存在"
        
        # 验证旧密码
        if not DatabaseManager.verify_password(old_password, user.password_hash):
            return False, "原密码错误"
        
        # 更新密码
        user.password_hash = DatabaseManager.hash_password(new_password)
        self.session.flush()
        
        logger.info(f"用户修改密码成功: {user.username}")
        return True, "密码修改成功"
    
    def reset_password(self, user_id: int, new_password: str) -> Tuple[bool, str]:
        """
        重置密码（管理员操作）
        返回: (是否成功, 消息)
        """
        user = self.user_dao.get_by_id(user_id)
        
        if not user:
            return False, "用户不存在"
        
        # 更新密码
        user.password_hash = DatabaseManager.hash_password(new_password)
        user.is_locked = False
        user.login_fail_count = 0
        self.session.flush()
        
        logger.info(f"管理员重置用户密码: {user.username}")
        return True, "密码重置成功"
