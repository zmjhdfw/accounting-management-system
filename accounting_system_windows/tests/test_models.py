"""
测试数据模型
"""
import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User, Role
from models.account import Account, AccountType
from models.voucher import Voucher, VoucherStatus


def test_role_creation():
    """测试角色创建"""
    role = Role(name='TestRole', description='测试角色')
    assert role.name == 'TestRole'
    assert role.description == '测试角色'
    assert role.is_active == True


def test_user_creation():
    """测试用户创建"""
    user = User(
        username='testuser',
        password_hash='hashed_password',
        real_name='测试用户'
    )
    assert user.username == 'testuser'
    assert user.real_name == '测试用户'
    assert user.is_active == True
    assert user.is_locked == False


def test_account_creation():
    """测试科目创建"""
    account = Account(
        code='1001',
        name='库存现金',
        account_type=AccountType.ASSET,
        balance_direction='debit'
    )
    assert account.code == '1001'
    assert account.name == '库存现金'
    assert account.account_type == AccountType.ASSET
    assert account.balance_direction == 'debit'
    assert account.level == 1
    assert account.is_leaf == True


def test_account_type_enum():
    """测试科目类型枚举"""
    assert AccountType.ASSET.value == 'asset'
    assert AccountType.LIABILITY.value == 'liability'
    assert AccountType.EQUITY.value == 'equity'
    assert AccountType.INCOME.value == 'income'
    assert AccountType.EXPENSE.value == 'expense'


def test_voucher_status_enum():
    """测试凭证状态枚举"""
    assert VoucherStatus.DRAFT.value == 'draft'
    assert VoucherStatus.SUBMITTED.value == 'submitted'
    assert VoucherStatus.REVIEWED.value == 'reviewed'
    assert VoucherStatus.REJECTED.value == 'rejected'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
