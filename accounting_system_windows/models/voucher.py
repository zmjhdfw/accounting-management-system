"""
凭证模型
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, Integer, Enum, Date, Text, DateTime
from sqlalchemy.orm import relationship
from models.base import BaseModel
import enum


class VoucherStatus(enum.Enum):
    """凭证状态枚举"""
    DRAFT = 'draft'           # 草稿
    SUBMITTED = 'submitted'   # 已提交
    REVIEWED = 'reviewed'     # 已审核
    REJECTED = 'rejected'     # 已驳回


class Voucher(BaseModel):
    """凭证模型"""
    __tablename__ = 'vouchers'
    
    voucher_number = Column(String(20), unique=True, nullable=False, comment='凭证号')
    voucher_date = Column(Date, nullable=False, comment='凭证日期')
    period_id = Column(Integer, ForeignKey('accounting_periods.id'), nullable=False, comment='会计期间ID')
    status = Column(Enum(VoucherStatus), default=VoucherStatus.DRAFT, nullable=False, comment='凭证状态')
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='制单人ID')
    reviewer_id = Column(Integer, ForeignKey('users.id'), comment='审核人ID')
    review_time = Column(DateTime, comment='审核时间')
    review_comment = Column(Text, comment='审核意见')
    total_debit = Column(Numeric(18, 2), default=0, nullable=False, comment='借方合计')
    total_credit = Column(Numeric(18, 2), default=0, nullable=False, comment='贷方合计')
    attachment_count = Column(Integer, default=0, comment='附件张数')
    remark = Column(Text, comment='备注')
    
    # 关系
    period = relationship('AccountingPeriod', back_populates='vouchers')
    creator = relationship('User', foreign_keys=[creator_id])
    reviewer = relationship('User', foreign_keys=[reviewer_id])
    details = relationship('VoucherDetail', back_populates='voucher', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Voucher(id={self.id}, voucher_number='{self.voucher_number}')>"
    
    def is_balanced(self):
        """检查借贷是否平衡"""
        return abs(self.total_debit - self.total_credit) < 0.01
    
    def calculate_totals(self):
        """计算借贷合计"""
        self.total_debit = sum(detail.debit_amount for detail in self.details)
        self.total_credit = sum(detail.credit_amount for detail in self.details)


class VoucherDetail(BaseModel):
    """凭证明细模型"""
    __tablename__ = 'voucher_details'
    
    voucher_id = Column(Integer, ForeignKey('vouchers.id'), nullable=False, comment='凭证ID')
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False, comment='科目ID')
    summary = Column(String(200), comment='摘要')
    debit_amount = Column(Numeric(18, 2), default=0, nullable=False, comment='借方金额')
    credit_amount = Column(Numeric(18, 2), default=0, nullable=False, comment='贷方金额')
    line_number = Column(Integer, nullable=False, comment='行号')
    
    # 关系
    voucher = relationship('Voucher', back_populates='details')
    account = relationship('Account', back_populates='voucher_details')
    
    def __repr__(self):
        return f"<VoucherDetail(id={self.id}, account_id={self.account_id})>"
