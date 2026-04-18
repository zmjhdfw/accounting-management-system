"""
审计日志DAO
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from dao.base_dao import BaseDao
from models.audit_log import AuditLog


class AuditLogDao(BaseDao):
    """审计日志DAO"""
    
    def __init__(self, session: Session):
        super().__init__(session, AuditLog)
    
    def create_log(self, user_id: int, username: str, operation: str,
                   module: str, description: str, target_type: Optional[str] = None,
                   target_id: Optional[int] = None, old_value: Optional[str] = None,
                   new_value: Optional[str] = None, ip_address: Optional[str] = None,
                   user_agent: Optional[str] = None, is_success: bool = True,
                   error_message: Optional[str] = None) -> AuditLog:
        """创建审计日志"""
        log = AuditLog(
            user_id=user_id,
            username=username,
            operation=operation,
            module=module,
            description=description,
            target_type=target_type,
            target_id=target_id,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent,
            is_success=is_success,
            error_message=error_message
        )
        self.session.add(log)
        self.session.flush()
        return log
    
    def query_logs(self, user_id: Optional[int] = None,
                   operation: Optional[str] = None,
                   module: Optional[str] = None,
                   start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None,
                   limit: int = 100, offset: int = 0) -> List[AuditLog]:
        """查询审计日志"""
        query = self.session.query(AuditLog)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if operation:
            query = query.filter(AuditLog.operation == operation)
        if module:
            query = query.filter(AuditLog.module == module)
        if start_time:
            query = query.filter(AuditLog.created_at >= start_time)
        if end_time:
            query = query.filter(AuditLog.created_at <= end_time)
        
        return query.order_by(AuditLog.created_at.desc()) \
                    .limit(limit).offset(offset).all()
    
    def get_user_logs(self, user_id: int, limit: int = 100) -> List[AuditLog]:
        """获取用户的操作日志"""
        return self.session.query(AuditLog).filter_by(user_id=user_id) \
                           .order_by(AuditLog.created_at.desc()) \
                           .limit(limit).all()
    
    def get_operation_logs(self, operation: str, limit: int = 100) -> List[AuditLog]:
        """获取指定操作的日志"""
        return self.session.query(AuditLog).filter_by(operation=operation) \
                           .order_by(AuditLog.created_at.desc()) \
                           .limit(limit).all()
