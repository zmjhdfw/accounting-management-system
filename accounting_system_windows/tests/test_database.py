"""
测试数据库初始化
"""
import pytest
import sys
import os
import tempfile

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.database import DatabaseManager
from models.user import User, Role
from models.account import Account


def test_database_initialization():
    """测试数据库初始化"""
    # 使用临时文件
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # 初始化数据库
        db_manager = DatabaseManager(db_path)
        db_manager.init_database()
        
        # 验证数据库文件创建
        assert os.path.exists(db_path)
        
        # 验证默认数据
        with db_manager.session_scope() as session:
            # 检查角色
            roles = session.query(Role).all()
            assert len(roles) == 4
            assert any(r.name == 'Administrator' for r in roles)
            
            # 检查用户
            admin = session.query(User).filter_by(username='admin').first()
            assert admin is not None
            assert admin.real_name == '系统管理员'
            
            # 检查科目
            accounts = session.query(Account).all()
            assert len(accounts) > 0
            assert any(a.code == '1001' for a in accounts)
    finally:
        # 清理临时文件
        if os.path.exists(db_path):
            os.remove(db_path)


def test_password_hashing():
    """测试密码哈希"""
    password = 'test_password'
    hashed = DatabaseManager.hash_password(password)
    
    # 验证哈希不为空
    assert hashed is not None
    assert len(hashed) > 0
    
    # 验证密码验证
    assert DatabaseManager.verify_password(password, hashed) == True
    assert DatabaseManager.verify_password('wrong_password', hashed) == False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
