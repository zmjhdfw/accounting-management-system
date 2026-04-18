"""
用户管理服务
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from dao.user_dao import UserDao, RoleDao
from dao.audit_log_dao import AuditLogDao
from models.user import User, Role
from infrastructure.logger import get_logger
from infrastructure.database import DatabaseManager

logger = get_logger(__name__)


class UserService:
    """用户管理服务"""
    
    def __init__(self, session: Session, current_user_id: int):
        self.session = session
        self.current_user_id = current_user_id
        self.user_dao = UserDao(session)
        self.role_dao = RoleDao(session)
        self.audit_log_dao = AuditLogDao(session)
    
    def create_user(self, username: str, password: str, real_name: str,
                   email: Optional[str] = None, phone: Optional[str] = None,
                   role_ids: Optional[List[int]] = None) -> Tuple[bool, Optional[User], str]:
        """创建用户"""
        # 检查用户名是否已存在
        if self.user_dao.get_by_username(username):
            return False, None, "用户名已存在"
        
        # 创建用户
        user = User(
            username=username,
            password_hash=DatabaseManager.hash_password(password),
            real_name=real_name,
            email=email,
            phone=phone,
            is_active=True
        )
        
        # 分配角色
        if role_ids:
            for role_id in role_ids:
                role = self.role_dao.get_by_id(role_id)
                if role:
                    user.roles.append(role)
        
        self.user_dao.create(user)
        
        # 记录审计日志
        self._log_operation('create', 'user', user.id, f"创建用户: {username}")
        
        logger.info(f"创建用户成功: {username}")
        return True, user, "用户创建成功"
    
    def update_user(self, user_id: int, real_name: Optional[str] = None,
                   email: Optional[str] = None, phone: Optional[str] = None,
                   is_active: Optional[bool] = None) -> Tuple[bool, str]:
        """更新用户"""
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return False, "用户不存在"
        
        old_value = f"real_name={user.real_name}, email={user.email}, phone={user.phone}, is_active={user.is_active}"
        
        if real_name is not None:
            user.real_name = real_name
        if email is not None:
            user.email = email
        if phone is not None:
            user.phone = phone
        if is_active is not None:
            user.is_active = is_active
        
        self.session.flush()
        
        new_value = f"real_name={user.real_name}, email={user.email}, phone={user.phone}, is_active={user.is_active}"
        self._log_operation('update', 'user', user_id, f"更新用户: {user.username}", old_value, new_value)
        
        logger.info(f"更新用户成功: {user.username}")
        return True, "用户更新成功"
    
    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """删除用户"""
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return False, "用户不存在"
        
        if user_id == self.current_user_id:
            return False, "不能删除当前用户"
        
        username = user.username
        self.user_dao.delete(user)
        
        self._log_operation('delete', 'user', user_id, f"删除用户: {username}")
        
        logger.info(f"删除用户成功: {username}")
        return True, "用户删除成功"
    
    def assign_role(self, user_id: int, role_id: int) -> Tuple[bool, str]:
        """分配角色"""
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return False, "用户不存在"
        
        role = self.role_dao.get_by_id(role_id)
        if not role:
            return False, "角色不存在"
        
        if role in user.roles:
            return False, "用户已拥有该角色"
        
        user.roles.append(role)
        self.session.flush()
        
        self._log_operation('assign_role', 'user', user_id, 
                           f"为用户 {user.username} 分配角色: {role.name}")
        
        logger.info(f"分配角色成功: user={user.username}, role={role.name}")
        return True, "角色分配成功"
    
    def revoke_role(self, user_id: int, role_id: int) -> Tuple[bool, str]:
        """撤销角色"""
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return False, "用户不存在"
        
        role = self.role_dao.get_by_id(role_id)
        if not role:
            return False, "角色不存在"
        
        if role not in user.roles:
            return False, "用户未拥有该角色"
        
        user.roles.remove(role)
        self.session.flush()
        
        self._log_operation('revoke_role', 'user', user_id,
                           f"撤销用户 {user.username} 的角色: {role.name}")
        
        logger.info(f"撤销角色成功: user={user.username}, role={role.name}")
        return True, "角色撤销成功"
    
    def get_user(self, user_id: int) -> Optional[User]:
        """获取用户"""
        return self.user_dao.get_by_id(user_id)
    
    def query_users(self, is_active: Optional[bool] = None) -> List[User]:
        """查询用户"""
        if is_active is not None:
            return self.user_dao.get_active_users()
        return self.user_dao.get_all()
    
    def check_permission(self, user_id: int, permission_name: str) -> bool:
        """检查权限"""
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return False
        return user.has_permission(permission_name)
    
    def _log_operation(self, operation: str, target_type: str, target_id: int,
                      description: str, old_value: Optional[str] = None,
                      new_value: Optional[str] = None):
        """记录操作日志"""
        current_user = self.user_dao.get_by_id(self.current_user_id)
        username = current_user.username if current_user else 'system'
        
        self.audit_log_dao.create_log(
            user_id=self.current_user_id,
            username=username,
            operation=operation,
            module='user',
            description=description,
            target_type=target_type,
            target_id=target_id,
            old_value=old_value,
            new_value=new_value
        )


from typing import Tuple
