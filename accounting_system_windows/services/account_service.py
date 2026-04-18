"""
会计科目服务
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from dao.account_dao import AccountDao
from dao.audit_log_dao import AuditLogDao
from models.account import Account, AccountType
from decimal import Decimal
from infrastructure.logger import get_logger

logger = get_logger(__name__)


class AccountService:
    """会计科目服务"""
    
    def __init__(self, session: Session, current_user_id: int):
        self.session = session
        self.current_user_id = current_user_id
        self.account_dao = AccountDao(session)
        self.audit_log_dao = AuditLogDao(session)
    
    def create_account(self, code: str, name: str, account_type: AccountType,
                      balance_direction: str, parent_id: Optional[int] = None,
                      description: Optional[str] = None) -> Tuple[bool, Optional[Account], str]:
        """创建科目"""
        # 检查编码唯一性
        if self.account_dao.get_by_code(code):
            return False, None, "科目编码已存在"
        
        # 验证父科目
        level = 1
        if parent_id:
            parent = self.account_dao.get_by_id(parent_id)
            if not parent:
                return False, None, "父科目不存在"
            level = parent.level + 1
            parent.is_leaf = False
        
        # 创建科目
        account = Account(
            code=code,
            name=name,
            account_type=account_type,
            balance_direction=balance_direction,
            parent_id=parent_id,
            level=level,
            is_leaf=True,
            description=description
        )
        
        self.account_dao.create(account)
        self._log_operation('create', 'account', account.id, f"创建科目: {code} {name}")
        
        logger.info(f"创建科目成功: {code} {name}")
        return True, account, "科目创建成功"
    
    def update_account(self, account_id: int, name: Optional[str] = None,
                      description: Optional[str] = None,
                      is_active: Optional[bool] = None) -> Tuple[bool, str]:
        """更新科目"""
        account = self.account_dao.get_by_id(account_id)
        if not account:
            return False, "科目不存在"
        
        if name is not None:
            account.name = name
        if description is not None:
            account.description = description
        if is_active is not None:
            account.is_active = is_active
        
        self.session.flush()
        self._log_operation('update', 'account', account_id, f"更新科目: {account.code}")
        
        logger.info(f"更新科目成功: {account.code}")
        return True, "科目更新成功"
    
    def delete_account(self, account_id: int) -> Tuple[bool, str]:
        """删除科目"""
        account = self.account_dao.get_by_id(account_id)
        if not account:
            return False, "科目不存在"
        
        # 检查是否被使用
        if self.account_dao.is_account_used(account_id):
            return False, "科目已被使用，不能删除"
        
        # 检查是否有余额
        if self.account_dao.has_balance(account_id):
            return False, "科目有余额，不能删除"
        
        # 检查是否有子科目
        children = self.account_dao.get_children_accounts(account_id)
        if children:
            return False, "科目有子科目，不能删除"
        
        code = account.code
        self.account_dao.delete(account)
        
        self._log_operation('delete', 'account', account_id, f"删除科目: {code}")
        
        logger.info(f"删除科目成功: {code}")
        return True, "科目删除成功"
    
    def get_account_tree(self) -> List[Account]:
        """获取科目树"""
        return self.account_dao.get_account_tree()
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """根据ID获取科目"""
        return self.account_dao.get_by_id(account_id)
    
    def get_account_by_code(self, code: str) -> Optional[Account]:
        """根据编码获取科目"""
        return self.account_dao.get_by_code(code)
    
    def get_all_accounts(self) -> List[Account]:
        """获取所有科目"""
        return self.account_dao.get_all_accounts_ordered()
    
    def get_accounts_by_type(self, account_type: AccountType) -> List[Account]:
        """根据类型获取科目"""
        return self.account_dao.get_accounts_by_type(account_type)
    
    def _log_operation(self, operation: str, target_type: str, target_id: int,
                      description: str):
        """记录操作日志"""
        from dao.user_dao import UserDao
        user_dao = UserDao(self.session)
        current_user = user_dao.get_by_id(self.current_user_id)
        username = current_user.username if current_user else 'system'
        
        self.audit_log_dao.create_log(
            user_id=self.current_user_id,
            username=username,
            operation=operation,
            module='account',
            description=description,
            target_type=target_type,
            target_id=target_id
        )
