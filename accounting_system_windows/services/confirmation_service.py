"""
操作确认机制
"""
from typing import Callable, Optional
from enum import Enum
from infrastructure.logger import get_logger

logger = get_logger(__name__)


class OperationType(Enum):
    """操作类型枚举"""
    # 自动保存操作
    VOUCHER_CREATE_DRAFT = 'voucher_create_draft'
    VOUCHER_UPDATE_DRAFT = 'voucher_update_draft'
    ACCOUNT_CREATE = 'account_create'
    ACCOUNT_UPDATE = 'account_update'
    
    # 需确认操作
    VOUCHER_DELETE = 'voucher_delete'
    ACCOUNT_DELETE = 'account_delete'
    VOUCHER_SUBMIT = 'voucher_submit'
    VOUCHER_REVIEW = 'voucher_review'
    DATA_RESTORE = 'data_restore'
    DATA_IMPORT = 'data_import'


class AutoSaveManager:
    """自动保存管理器"""
    
    AUTO_SAVE_OPERATIONS = {
        OperationType.VOUCHER_CREATE_DRAFT,
        OperationType.VOUCHER_UPDATE_DRAFT,
        OperationType.ACCOUNT_CREATE,
        OperationType.ACCOUNT_UPDATE,
    }
    
    @classmethod
    def is_auto_save(cls, operation_type: OperationType) -> bool:
        """判断是否为自动保存操作"""
        return operation_type in cls.AUTO_SAVE_OPERATIONS
    
    @classmethod
    def execute_with_auto_save(cls, operation_type: OperationType,
                               operation: Callable, 
                               on_success: Optional[Callable] = None,
                               on_failure: Optional[Callable] = None):
        """
        执行操作并自动保存
        operation: 要执行的操作函数
        on_success: 成功回调
        on_failure: 失败回调
        """
        try:
            result = operation()
            
            if cls.is_auto_save(operation_type):
                logger.info(f"自动保存成功: {operation_type.value}")
                if on_success:
                    on_success(result)
            
            return True, result
        except Exception as e:
            logger.error(f"自动保存失败: {operation_type.value}, 错误: {str(e)}")
            if on_failure:
                on_failure(str(e))
            return False, str(e)


class ConfirmationManager:
    """确认对话框管理器"""
    
    CONFIRMATION_OPERATIONS = {
        OperationType.VOUCHER_DELETE,
        OperationType.ACCOUNT_DELETE,
        OperationType.VOUCHER_SUBMIT,
        OperationType.VOUCHER_REVIEW,
        OperationType.DATA_RESTORE,
        OperationType.DATA_IMPORT,
    }
    
    CONFIRMATION_MESSAGES = {
        OperationType.VOUCHER_DELETE: "确定要删除该凭证吗？此操作不可撤销。",
        OperationType.ACCOUNT_DELETE: "确定要删除该科目吗？此操作不可撤销。",
        OperationType.VOUCHER_SUBMIT: "确定要提交该凭证吗？提交后将不能修改。",
        OperationType.VOUCHER_REVIEW: "确定要审核该凭证吗？审核后将更新科目余额。",
        OperationType.DATA_RESTORE: "确定要恢复数据吗？当前数据将被覆盖。",
        OperationType.DATA_IMPORT: "确定要导入数据吗？将创建新的凭证记录。",
    }
    
    @classmethod
    def needs_confirmation(cls, operation_type: OperationType) -> bool:
        """判断是否需要确认"""
        return operation_type in cls.CONFIRMATION_OPERATIONS
    
    @classmethod
    def get_confirmation_message(cls, operation_type: OperationType) -> str:
        """获取确认消息"""
        return cls.CONFIRMATION_MESSAGES.get(operation_type, "确定要执行此操作吗？")
    
    @classmethod
    def execute_with_confirmation(cls, operation_type: OperationType,
                                  confirm_callback: Callable[[], bool],
                                  operation: Callable,
                                  on_success: Optional[Callable] = None,
                                  on_failure: Optional[Callable] = None):
        """
        执行需要确认的操作
        confirm_callback: 确认回调函数，返回True表示用户确认
        operation: 要执行的操作函数
        on_success: 成功回调
        on_failure: 失败回调
        """
        if cls.needs_confirmation(operation_type):
            # 需要确认
            confirmed = confirm_callback()
            if not confirmed:
                logger.info(f"用户取消操作: {operation_type.value}")
                return False, "用户取消操作"
        
        # 执行操作
        try:
            result = operation()
            logger.info(f"操作执行成功: {operation_type.value}")
            
            if on_success:
                on_success(result)
            
            return True, result
        except Exception as e:
            logger.error(f"操作执行失败: {operation_type.value}, 错误: {str(e)}")
            
            if on_failure:
                on_failure(str(e))
            
            return False, str(e)


class OperationExecutor:
    """操作执行器"""
    
    @staticmethod
    def execute(operation_type: OperationType,
                operation: Callable,
                confirm_callback: Optional[Callable[[], bool]] = None,
                on_success: Optional[Callable] = None,
                on_failure: Optional[Callable] = None):
        """
        执行操作
        根据操作类型自动判断是否需要确认或自动保存
        """
        if AutoSaveManager.is_auto_save(operation_type):
            return AutoSaveManager.execute_with_auto_save(
                operation_type, operation, on_success, on_failure
            )
        elif ConfirmationManager.needs_confirmation(operation_type):
            if confirm_callback is None:
                raise ValueError("需要确认的操作必须提供confirm_callback")
            
            return ConfirmationManager.execute_with_confirmation(
                operation_type, confirm_callback, operation, on_success, on_failure
            )
        else:
            # 普通操作，直接执行
            try:
                result = operation()
                if on_success:
                    on_success(result)
                return True, result
            except Exception as e:
                if on_failure:
                    on_failure(str(e))
                return False, str(e)
