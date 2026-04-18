"""
会计科目模型
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, Integer, Enum
from sqlalchemy.orm import relationship
from models.base import BaseModel
import enum


class AccountType(enum.Enum):
    """科目类型枚举"""
    ASSET = 'asset'           # 资产
    LIABILITY = 'liability'   # 负债
    EQUITY = 'equity'         # 所有者权益
    INCOME = 'income'         # 收入
    EXPENSE = 'expense'       # 费用


class Account(BaseModel):
    """会计科目模型"""
    __tablename__ = 'accounts'
    
    code = Column(String(20), unique=True, nullable=False, comment='科目编码')
    name = Column(String(100), nullable=False, comment='科目名称')
    account_type = Column(Enum(AccountType), nullable=False, comment='科目类型')
    parent_id = Column(Integer, ForeignKey('accounts.id'), comment='父科目ID')
    level = Column(Integer, default=1, nullable=False, comment='科目级别')
    is_leaf = Column(Boolean, default=True, nullable=False, comment='是否末级科目')
    is_active = Column(Boolean, default=True, nullable=False, comment='是否启用')
    balance_direction = Column(String(10), nullable=False, comment='余额方向：debit/credit')
    current_balance = Column(Numeric(18, 2), default=0, nullable=False, comment='当前余额')
    description = Column(String(200), comment='科目说明')
    
    # 关系
    parent = relationship('Account', remote_side='Account.id', back_populates='children')
    children = relationship('Account', back_populates='parent')
    voucher_details = relationship('VoucherDetail', back_populates='account')
    
    def __repr__(self):
        return f"<Account(id={self.id}, code='{self.code}', name='{self.name}')>"
    
    def get_full_code_path(self):
        """获取完整科目编码路径"""
        if self.parent:
            return f"{self.parent.get_full_code_path()}-{self.code}"
        return self.code
    
    def get_full_name_path(self):
        """获取完整科目名称路径"""
        if self.parent:
            return f"{self.parent.get_full_name_path()}-{self.name}"
        return self.name
