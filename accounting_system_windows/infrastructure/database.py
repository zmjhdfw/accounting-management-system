"""
数据库初始化和管理
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from models import Base
from models.user import User, Role
from models.account import Account, AccountType
from models.accounting_period import AccountingPeriod
from datetime import datetime, date
from cryptography.fernet import Fernet
import hashlib


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path='./data/accounting.db'):
        self.db_path = db_path
        self.engine = None
        self.SessionLocal = None
        
    def init_database(self):
        """初始化数据库"""
        # 确保数据目录存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # 创建数据库引擎
        self.engine = create_engine(
            f'sqlite:///{self.db_path}',
            pool_pre_ping=True,
            echo=False
        )
        
        # 创建会话工厂
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        # 创建所有表
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self) -> Session:
        """获取数据库会话"""
        if not self.SessionLocal:
            self.init_database()
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self):
        """会话上下文管理器"""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def init_default_data(self):
        """初始化默认数据"""
        with self.session_scope() as session:
            # 检查是否已初始化
            if session.query(Role).first():
                return
            
            # 创建默认角色
            roles = [
                Role(name='Administrator', description='系统管理员'),
                Role(name='Accountant', description='会计'),
                Role(name='Reviewer', description='审核员'),
                Role(name='Viewer', description='查看者'),
            ]
            session.add_all(roles)
            session.flush()
            
            # 创建默认管理员账户
            admin_role = session.query(Role).filter_by(name='Administrator').first()
            admin_user = User(
                username='admin',
                password_hash=self.hash_password('admin123'),
                real_name='系统管理员',
                is_active=True
            )
            admin_user.roles.append(admin_role)
            session.add(admin_user)
            
            # 创建基础会计科目
            self._init_accounts(session)
            
            # 创建当前会计期间
            self._init_periods(session)
    
    def _init_accounts(self, session):
        """初始化基础会计科目"""
        accounts = [
            # 资产类
            Account(code='1001', name='库存现金', account_type=AccountType.ASSET, 
                   balance_direction='debit', level=1),
            Account(code='1002', name='银行存款', account_type=AccountType.ASSET,
                   balance_direction='debit', level=1),
            Account(code='1012', name='其他货币资金', account_type=AccountType.ASSET,
                   balance_direction='debit', level=1),
            Account(code='1101', name='交易性金融资产', account_type=AccountType.ASSET,
                   balance_direction='debit', level=1),
            Account(code='1121', name='应收票据', account_type=AccountType.ASSET,
                   balance_direction='debit', level=1),
            Account(code='1122', name='应收账款', account_type=AccountType.ASSET,
                   balance_direction='debit', level=1),
            Account(code='1221', name='其他应收款', account_type=AccountType.ASSET,
                   balance_direction='debit', level=1),
            Account(code='1401', name='原材料', account_type=AccountType.ASSET,
                   balance_direction='debit', level=1),
            Account(code='1405', name='库存商品', account_type=AccountType.ASSET,
                   balance_direction='debit', level=1),
            Account(code='1601', name='固定资产', account_type=AccountType.ASSET,
                   balance_direction='debit', level=1),
            Account(code='1602', name='累计折旧', account_type=AccountType.ASSET,
                   balance_direction='credit', level=1),
            
            # 负债类
            Account(code='2001', name='短期借款', account_type=AccountType.LIABILITY,
                   balance_direction='credit', level=1),
            Account(code='2201', name='应付票据', account_type=AccountType.LIABILITY,
                   balance_direction='credit', level=1),
            Account(code='2202', name='应付账款', account_type=AccountType.LIABILITY,
                   balance_direction='credit', level=1),
            Account(code='2211', name='应付职工薪酬', account_type=AccountType.LIABILITY,
                   balance_direction='credit', level=1),
            Account(code='2221', name='应交税费', account_type=AccountType.LIABILITY,
                   balance_direction='credit', level=1),
            Account(code='2501', name='长期借款', account_type=AccountType.LIABILITY,
                   balance_direction='credit', level=1),
            
            # 所有者权益类
            Account(code='4001', name='实收资本', account_type=AccountType.EQUITY,
                   balance_direction='credit', level=1),
            Account(code='4002', name='资本公积', account_type=AccountType.EQUITY,
                   balance_direction='credit', level=1),
            Account(code='4101', name='盈余公积', account_type=AccountType.EQUITY,
                   balance_direction='credit', level=1),
            Account(code='4103', name='本年利润', account_type=AccountType.EQUITY,
                   balance_direction='credit', level=1),
            Account(code='4104', name='利润分配', account_type=AccountType.EQUITY,
                   balance_direction='credit', level=1),
            
            # 收入类
            Account(code='6001', name='主营业务收入', account_type=AccountType.INCOME,
                   balance_direction='credit', level=1),
            Account(code='6051', name='其他业务收入', account_type=AccountType.INCOME,
                   balance_direction='credit', level=1),
            Account(code='6111', name='投资收益', account_type=AccountType.INCOME,
                   balance_direction='credit', level=1),
            Account(code='6301', name='营业外收入', account_type=AccountType.INCOME,
                   balance_direction='credit', level=1),
            
            # 费用类
            Account(code='6401', name='主营业务成本', account_type=AccountType.EXPENSE,
                   balance_direction='debit', level=1),
            Account(code='6402', name='其他业务成本', account_type=AccountType.EXPENSE,
                   balance_direction='debit', level=1),
            Account(code='6403', name='税金及附加', account_type=AccountType.EXPENSE,
                   balance_direction='debit', level=1),
            Account(code='6601', name='销售费用', account_type=AccountType.EXPENSE,
                   balance_direction='debit', level=1),
            Account(code='6602', name='管理费用', account_type=AccountType.EXPENSE,
                   balance_direction='debit', level=1),
            Account(code='6603', name='财务费用', account_type=AccountType.EXPENSE,
                   balance_direction='debit', level=1),
            Account(code='6711', name='营业外支出', account_type=AccountType.EXPENSE,
                   balance_direction='debit', level=1),
            Account(code='6801', name='所得税费用', account_type=AccountType.EXPENSE,
                   balance_direction='debit', level=1),
        ]
        session.add_all(accounts)
    
    def _init_periods(self, session):
        """初始化会计期间"""
        today = date.today()
        period = AccountingPeriod(
            year=today.year,
            month=today.month,
            period_name=AccountingPeriod.generate_period_name(today.year, today.month),
            start_date=date(today.year, today.month, 1),
            end_date=date(today.year, today.month, 
                         self._get_month_last_day(today.year, today.month)),
            is_open=True,
            is_current=True
        )
        session.add(period)
    
    @staticmethod
    def _get_month_last_day(year, month):
        """获取月份最后一天"""
        if month == 12:
            return 31
        next_month = date(year, month + 1, 1)
        return (next_month.replace(day=1) - date(year, month, 1)).days
    
    @staticmethod
    def hash_password(password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """验证密码"""
        return DatabaseManager.hash_password(password) == password_hash


# 全局数据库管理器实例
db_manager = DatabaseManager()


def init_db():
    """初始化数据库"""
    db_manager.init_database()
    db_manager.init_default_data()


def get_db():
    """获取数据库会话"""
    return db_manager.get_session()
