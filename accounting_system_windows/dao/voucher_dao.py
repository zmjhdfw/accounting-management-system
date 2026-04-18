"""
凭证DAO
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date
from dao.base_dao import BaseDao
from models.voucher import Voucher, VoucherDetail, VoucherStatus


class VoucherDao(BaseDao):
    """凭证DAO"""
    
    def __init__(self, session: Session):
        super().__init__(session, Voucher)
    
    def get_by_number(self, voucher_number: str) -> Optional[Voucher]:
        """根据凭证号获取凭证"""
        return self.session.query(Voucher).filter_by(voucher_number=voucher_number).first()
    
    def query_vouchers(self, start_date: Optional[date] = None, 
                       end_date: Optional[date] = None,
                       status: Optional[VoucherStatus] = None,
                       period_id: Optional[int] = None,
                       limit: int = 100, offset: int = 0) -> List[Voucher]:
        """查询凭证"""
        query = self.session.query(Voucher)
        
        if start_date:
            query = query.filter(Voucher.voucher_date >= start_date)
        if end_date:
            query = query.filter(Voucher.voucher_date <= end_date)
        if status:
            query = query.filter(Voucher.status == status)
        if period_id:
            query = query.filter(Voucher.period_id == period_id)
        
        return query.order_by(Voucher.voucher_date.desc(), Voucher.voucher_number.desc()) \
                    .limit(limit).offset(offset).all()
    
    def update_status(self, voucher_id: int, status: VoucherStatus, 
                      reviewer_id: Optional[int] = None, 
                      review_comment: Optional[str] = None):
        """更新凭证状态"""
        from datetime import datetime
        voucher = self.get_by_id(voucher_id)
        if voucher:
            voucher.status = status
            if reviewer_id:
                voucher.reviewer_id = reviewer_id
                voucher.review_time = datetime.now()
            if review_comment:
                voucher.review_comment = review_comment
            self.session.flush()
    
    def get_vouchers_by_period(self, period_id: int) -> List[Voucher]:
        """获取指定期间的凭证"""
        return self.session.query(Voucher).filter_by(period_id=period_id) \
                           .order_by(Voucher.voucher_number).all()
    
    def get_next_voucher_number(self, period_id: int) -> str:
        """获取下一个凭证号"""
        from models.accounting_period import AccountingPeriod
        period = self.session.query(AccountingPeriod).filter_by(id=period_id).first()
        if not period:
            return None
        
        # 查询该期间的最大凭证号
        last_voucher = self.session.query(Voucher) \
                                   .filter_by(period_id=period_id) \
                                   .order_by(Voucher.voucher_number.desc()).first()
        
        if last_voucher:
            # 提取序号并加1
            try:
                parts = last_voucher.voucher_number.split('-')
                seq = int(parts[-1]) + 1
            except:
                seq = 1
        else:
            seq = 1
        
        return f"{period.period_name}-{seq:04d}"


class VoucherDetailDao(BaseDao):
    """凭证明细DAO"""
    
    def __init__(self, session: Session):
        super().__init__(session, VoucherDetail)
    
    def batch_create(self, details: List[VoucherDetail]):
        """批量创建凭证明细"""
        self.session.add_all(details)
        self.session.flush()
    
    def batch_update(self, details: List[VoucherDetail]):
        """批量更新凭证明细"""
        for detail in details:
            self.session.merge(detail)
        self.session.flush()
    
    def get_details_by_voucher(self, voucher_id: int) -> List[VoucherDetail]:
        """获取凭证的所有明细"""
        return self.session.query(VoucherDetail).filter_by(voucher_id=voucher_id) \
                           .order_by(VoucherDetail.line_number).all()
    
    def delete_details_by_voucher(self, voucher_id: int):
        """删除凭证的所有明细"""
        self.session.query(VoucherDetail).filter_by(voucher_id=voucher_id).delete()
        self.session.flush()
