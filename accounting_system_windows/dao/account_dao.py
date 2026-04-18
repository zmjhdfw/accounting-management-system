"""
会计科目DAO
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from dao.base_dao import BaseDao
from models.account import Account, AccountType
from decimal import Decimal


class AccountDao(BaseDao):
    """会计科目DAO"""
    
    def __init__(self, session: Session):
        super().__init__(session, Account)
    
    def get_by_code(self, code: str) -> Optional[Account]:
        """根据科目编码获取科目"""
        return self.session.query(Account).filter_by(code=code).first()
    
    def get_account_tree(self) -> List[Account]:
        """获取科目树（根节点）"""
        return self.session.query(Account).filter_by(parent_id=None).order_by(Account.code).all()
    
    def get_children_accounts(self, parent_id: int) -> List[Account]:
        """获取子科目"""
        return self.session.query(Account).filter_by(parent_id=parent_id).order_by(Account.code).all()
    
    def get_accounts_by_type(self, account_type: AccountType) -> List[Account]:
        """根据科目类型获取科目"""
        return self.session.query(Account).filter_by(account_type=account_type).order_by(Account.code).all()
    
    def get_leaf_accounts(self) -> List[Account]:
        """获取所有末级科目"""
        return self.session.query(Account).filter_by(is_leaf=True).order_by(Account.code).all()
    
    def update_balance(self, account_id: int, amount: Decimal, is_debit: bool):
        """更新科目余额"""
        account = self.get_by_id(account_id)
        if account:
            if account.balance_direction == 'debit':
                if is_debit:
                    account.current_balance += amount
                else:
                    account.current_balance -= amount
            else:  # credit
                if is_debit:
                    account.current_balance -= amount
                else:
                    account.current_balance += amount
            self.session.flush()
    
    def is_account_used(self, account_id: int) -> bool:
        """检查科目是否被使用"""
        from models.voucher import VoucherDetail
        count = self.session.query(VoucherDetail).filter_by(account_id=account_id).count()
        return count > 0
    
    def has_balance(self, account_id: int) -> bool:
        """检查科目是否有余额"""
        account = self.get_by_id(account_id)
        return account and account.current_balance != 0
    
    def get_all_accounts_ordered(self) -> List[Account]:
        """获取所有科目（按编码排序）"""
        return self.session.query(Account).order_by(Account.code).all()
