"""
会计期间模型
"""
from sqlalchemy import Column, String, Boolean, Date, Integer
from models.base import BaseModel


class AccountingPeriod(BaseModel):
    """会计期间模型"""
    __tablename__ = 'accounting_periods'
    
    year = Column(Integer, nullable=False, comment='年份')
    month = Column(Integer, nullable=False, comment='月份')
    period_name = Column(String(20), unique=True, nullable=False, comment='期间名称')
    start_date = Column(Date, nullable=False, comment='开始日期')
    end_date = Column(Date, nullable=False, comment='结束日期')
    is_open = Column(Boolean, default=True, nullable=False, comment='是否开启')
    is_current = Column(Boolean, default=False, nullable=False, comment='是否当前期间')
    
    def __repr__(self):
        return f"<AccountingPeriod(id={self.id}, period_name='{self.period_name}')>"
    
    @staticmethod
    def generate_period_name(year, month):
        """生成期间名称"""
        return f"{year:04d}-{month:02d}"
