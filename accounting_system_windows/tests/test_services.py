"""
测试业务逻辑层
"""
import pytest
import sys
import os
import tempfile

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.database import DatabaseManager
from services.auth_service import AuthService
from services.account_service import AccountService
from models.account import AccountType


def test_user_login():
    """测试用户登录"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # 初始化数据库
        db_manager = DatabaseManager(db_path)
        db_manager.init_database()
        db_manager.init_default_data()
        
        # 测试登录
        session = db_manager.get_session()
        auth_service = AuthService(session)
        
        # 正确登录
        success, user, message = auth_service.login('admin', 'admin123')
        assert success == True
        assert user is not None
        assert user.username == 'admin'
        
        # 错误密码
        success, user, message = auth_service.login('admin', 'wrong_password')
        assert success == False
        assert '错误' in message
        
        # 不存在的用户
        success, user, message = auth_service.login('nonexistent', 'password')
        assert success == False
        
        session.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_account_service():
    """测试科目服务"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # 初始化数据库
        db_manager = DatabaseManager(db_path)
        db_manager.init_database()
        db_manager.init_default_data()
        
        session = db_manager.get_session()
        
        # 获取admin用户ID
        from dao.user_dao import UserDao
        user_dao = UserDao(session)
        admin = user_dao.get_by_username('admin')
        
        account_service = AccountService(session, admin.id)
        
        # 测试创建科目
        success, account, message = account_service.create_account(
            code='9999',
            name='测试科目',
            account_type=AccountType.ASSET,
            balance_direction='debit'
        )
        assert success == True
        assert account is not None
        assert account.code == '9999'
        
        # 测试获取科目树
        tree = account_service.get_account_tree()
        assert len(tree) > 0
        
        session.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
