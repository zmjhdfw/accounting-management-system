"""
凭证服务
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from datetime import date
from dao.voucher_dao import VoucherDao, VoucherDetailDao
from dao.account_dao import AccountDao
from dao.audit_log_dao import AuditLogDao
from models.voucher import Voucher, VoucherDetail, VoucherStatus
from decimal import Decimal
from infrastructure.logger import get_logger

logger = get_logger(__name__)


class VoucherService:
    """凭证服务"""
    
    def __init__(self, session: Session, current_user_id: int):
        self.session = session
        self.current_user_id = current_user_id
        self.voucher_dao = VoucherDao(session)
        self.voucher_detail_dao = VoucherDetailDao(session)
        self.account_dao = AccountDao(session)
        self.audit_log_dao = AuditLogDao(session)
    
    def create_voucher(self, voucher_date: date, period_id: int,
                      details: List[dict], remark: Optional[str] = None,
                      attachment_count: int = 0) -> Tuple[bool, Optional[Voucher], str]:
        """
        创建凭证
        details: [{'account_id': int, 'summary': str, 'debit_amount': Decimal, 'credit_amount': Decimal}, ...]
        """
        # 生成凭证号
        voucher_number = self.voucher_dao.get_next_voucher_number(period_id)
        if not voucher_number:
            return False, None, "无法生成凭证号"
        
        # 创建凭证
        voucher = Voucher(
            voucher_number=voucher_number,
            voucher_date=voucher_date,
            period_id=period_id,
            creator_id=self.current_user_id,
            remark=remark,
            attachment_count=attachment_count
        )
        
        self.voucher_dao.create(voucher)
        
        # 创建凭证明细
        voucher_details = []
        for i, detail in enumerate(details, 1):
            vd = VoucherDetail(
                voucher_id=voucher.id,
                account_id=detail['account_id'],
                summary=detail.get('summary', ''),
                debit_amount=detail.get('debit_amount', Decimal(0)),
                credit_amount=detail.get('credit_amount', Decimal(0)),
                line_number=i
            )
            voucher_details.append(vd)
        
        self.voucher_detail_dao.batch_create(voucher_details)
        
        # 计算借贷合计
        voucher.calculate_totals()
        self.session.flush()
        
        # 检查借贷平衡
        if not voucher.is_balanced():
            return False, None, "借贷不平衡"
        
        self._log_operation('create', 'voucher', voucher.id, f"创建凭证: {voucher_number}")
        
        logger.info(f"创建凭证成功: {voucher_number}")
        return True, voucher, "凭证创建成功"
    
    def update_voucher(self, voucher_id: int, voucher_date: Optional[date] = None,
                      details: Optional[List[dict]] = None,
                      remark: Optional[str] = None) -> Tuple[bool, str]:
        """更新凭证"""
        voucher = self.voucher_dao.get_by_id(voucher_id)
        if not voucher:
            return False, "凭证不存在"
        
        if voucher.status != VoucherStatus.DRAFT:
            return False, "只能修改草稿状态的凭证"
        
        if voucher_date is not None:
            voucher.voucher_date = voucher_date
        
        if remark is not None:
            voucher.remark = remark
        
        if details is not None:
            # 删除旧明细
            self.voucher_detail_dao.delete_details_by_voucher(voucher_id)
            
            # 创建新明细
            voucher_details = []
            for i, detail in enumerate(details, 1):
                vd = VoucherDetail(
                    voucher_id=voucher_id,
                    account_id=detail['account_id'],
                    summary=detail.get('summary', ''),
                    debit_amount=detail.get('debit_amount', Decimal(0)),
                    credit_amount=detail.get('credit_amount', Decimal(0)),
                    line_number=i
                )
                voucher_details.append(vd)
            
            self.voucher_detail_dao.batch_create(voucher_details)
            
            # 重新计算合计
            voucher.calculate_totals()
        
        self.session.flush()
        
        if not voucher.is_balanced():
            return False, "借贷不平衡"
        
        self._log_operation('update', 'voucher', voucher_id, f"更新凭证: {voucher.voucher_number}")
        
        logger.info(f"更新凭证成功: {voucher.voucher_number}")
        return True, "凭证更新成功"
    
    def delete_voucher(self, voucher_id: int) -> Tuple[bool, str]:
        """删除凭证"""
        voucher = self.voucher_dao.get_by_id(voucher_id)
        if not voucher:
            return False, "凭证不存在"
        
        if voucher.status != VoucherStatus.DRAFT:
            return False, "只能删除草稿状态的凭证"
        
        voucher_number = voucher.voucher_number
        
        # 删除明细
        self.voucher_detail_dao.delete_details_by_voucher(voucher_id)
        
        # 删除凭证
        self.voucher_dao.delete(voucher)
        
        self._log_operation('delete', 'voucher', voucher_id, f"删除凭证: {voucher_number}")
        
        logger.info(f"删除凭证成功: {voucher_number}")
        return True, "凭证删除成功"
    
    def submit_voucher(self, voucher_id: int) -> Tuple[bool, str]:
        """提交凭证"""
        voucher = self.voucher_dao.get_by_id(voucher_id)
        if not voucher:
            return False, "凭证不存在"
        
        if voucher.status != VoucherStatus.DRAFT:
            return False, "只能提交草稿状态的凭证"
        
        if not voucher.is_balanced():
            return False, "借贷不平衡，不能提交"
        
        self.voucher_dao.update_status(voucher_id, VoucherStatus.SUBMITTED)
        
        self._log_operation('submit', 'voucher', voucher_id, f"提交凭证: {voucher.voucher_number}")
        
        logger.info(f"提交凭证成功: {voucher.voucher_number}")
        return True, "凭证提交成功"
    
    def review_voucher(self, voucher_id: int, approved: bool,
                      comment: Optional[str] = None) -> Tuple[bool, str]:
        """审核凭证"""
        voucher = self.voucher_dao.get_by_id(voucher_id)
        if not voucher:
            return False, "凭证不存在"
        
        if voucher.status != VoucherStatus.SUBMITTED:
            return False, "只能审核已提交的凭证"
        
        if approved:
            # 更新状态
            self.voucher_dao.update_status(voucher_id, VoucherStatus.REVIEWED,
                                          self.current_user_id, comment)
            
            # 更新科目余额
            details = self.voucher_detail_dao.get_details_by_voucher(voucher_id)
            for detail in details:
                if detail.debit_amount > 0:
                    self.account_dao.update_balance(detail.account_id, 
                                                   detail.debit_amount, True)
                if detail.credit_amount > 0:
                    self.account_dao.update_balance(detail.account_id,
                                                   detail.credit_amount, False)
            
            self._log_operation('review', 'voucher', voucher_id, 
                              f"审核通过凭证: {voucher.voucher_number}")
            logger.info(f"审核凭证通过: {voucher.voucher_number}")
            return True, "凭证审核通过"
        else:
            self.voucher_dao.update_status(voucher_id, VoucherStatus.REJECTED,
                                          self.current_user_id, comment)
            
            self._log_operation('reject', 'voucher', voucher_id,
                              f"审核驳回凭证: {voucher.voucher_number}")
            logger.info(f"审核凭证驳回: {voucher.voucher_number}")
            return True, "凭证审核驳回"
    
    def query_vouchers(self, start_date: Optional[date] = None,
                      end_date: Optional[date] = None,
                      status: Optional[VoucherStatus] = None,
                      period_id: Optional[int] = None,
                      limit: int = 100, offset: int = 0) -> List[Voucher]:
        """查询凭证"""
        return self.voucher_dao.query_vouchers(start_date, end_date, status,
                                               period_id, limit, offset)
    
    def get_voucher_by_id(self, voucher_id: int) -> Optional[Voucher]:
        """根据ID获取凭证"""
        return self.voucher_dao.get_by_id(voucher_id)
    
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
            module='voucher',
            description=description,
            target_type=target_type,
            target_id=target_id
        )
