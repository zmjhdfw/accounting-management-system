# 技术设计文档 - 会计管理系统

## 文档信息
- **项目名称**: 会计管理系统 (Accounting Management System)
- **文档版本**: v1.0
- **创建日期**: 2026-04-19
- **最后更新**: 2026-04-19
- **文档状态**: 草稿
- **对应需求版本**: v1.0

## 1. 系统架构

### 1.1 架构概述
本系统采用分层架构设计，实现表示层、业务逻辑层、数据访问层和基础设施层的分离。系统支持Windows桌面端和Android移动端双平台，通过RESTful API实现数据同步和业务协同。

**设计原则**:
- 高内聚、低耦合的模块化设计
- 单一职责原则，每个模块专注于特定功能
- 依赖倒置原则，通过接口解耦各层依赖
- 开闭原则，对扩展开放，对修改关闭

### 1.2 架构层次图
```
┌─────────────────────────────────────────────────────────────┐
│                    表示层 (Presentation)                     │
│  ┌──────────────────────┐    ┌──────────────────────┐      │
│  │   Windows Client      │    │   Android Client     │      │
│  │   (PyQt6/PySide6)     │    │   (Android SDK)      │      │
│  └──────────────────────┘    └──────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  业务逻辑层 (Business Logic)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │会计核心   │  │报表引擎   │  │权限管理   │  │数据同步   │   │
│  │Accounting│  │Reporting │  │Auth      │  │Sync      │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  数据访问层 (Data Access)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   ORM    │  │数据验证   │  │缓存管理   │  │事务管理   │   │
│  │SQLAlchemy│  │Validator │  │Cache     │  │Transaction│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  基硎设施层 (Infrastructure)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ 数据库    │  │  日志     │  │  配置     │  │  网络     │   │
│  │ Database │  │ Logging  │  │ Config   │  │ Network  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 组件交互图
```
用户操作流程:
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│  UI层   │───→│Service │───→│  DAO   │───→│Database│
│        │    │  层     │    │  层     │    │        │
└────────┘    └────────┘    └────────┘    └────────┘
     ↓              ↓              ↓              ↓
  显示结果      业务处理      数据操作      数据存储

跨平台数据同步:
┌─────────────┐              ┌─────────────┐
│Windows Client│              │Android Client│
└─────────────┘              └─────────────┘
       ↓                            ↓
       └──────────┬─────────────────┘
                  ↓
         ┌────────────────┐
         │  Sync Service  │
         │   (REST API)   │
         └────────────────┘
                  ↓
         ┌────────────────┐
         │   Database     │
         └────────────────┘
```

### 1.4 模块划分

#### Windows端模块结构
```
accounting_system/
├── ui/                    # 表示层
│   ├── main_window.py     # 主窗口
│   ├── widgets/           # 自定义控件
│   ├── dialogs/           # 对话框
│   └── views/             # 视图组件
├── services/              # 业务逻辑层
│   ├── account_service.py # 科目服务
│   ├── voucher_service.py # 凭证服务
│   ├── report_service.py  # 报表服务
│   ├── auth_service.py    # 认证服务
│   └── sync_service.py    # 同步服务
├── dao/                   # 数据访问层
│   ├── base_dao.py        # 基硎DAO
│   ├── account_dao.py     # 科目DAO
│   ├── voucher_dao.py     # 凭证DAO
│   └── user_dao.py        # 用户DAO
├── models/                # 数据模型
│   ├── base.py            # 基硎模型
│   ├── account.py         # 科目模型
│   ├── voucher.py         # 凭证模型
│   └── user.py            # 用户模型
├── infrastructure/        # 基硎设施层
│   ├── database.py        # 数据库管理
│   ├── config.py          # 配置管理
│   ├── logger.py          # 日志管理
│   └── cache.py           # 缓存管理
└── utils/                 # 工具类
    ├── validators.py      # 数据验证
    ├── converters.py      # 数据转换
    └── helpers.py         # 辅助函数
```

#### Android端模块结构
```
app/
├── ui/                    # 表示层
│   ├── activities/        # Activity
│   ├── fragments/         # Fragment
│   ├── adapters/          # 适配器
│   └── viewmodels/        # ViewModel
├── services/              # 业务逻辑层
│   ├── AccountService.java
│   ├── VoucherService.java
│   ├── ReportService.java
│   └── SyncService.java
├── data/                  # 数据层
│   ├── local/             # 本地数据
│   │   ├── dao/           # Room DAO
│   │   ├── entities/      # 实体类
│   │   └── database/      # 数据库
│   └── remote/            # 远程数据
│       ├── api/           # API接口
│       └── models/        # 数据模型
├── di/                    # 依赖注入
│   └── modules/           # DI模块
└── utils/                 # 工具类
    ├── validators/
    ├── converters/
    └── helpers/
```

## 2. 技术选型

### 2.1 Windows端技术栈

| 技术领域 | 技术选型 | 版本 | 选型理由 |
|---------|---------|------|---------|
| 编程语言 | Python | 3.9+ | 跨平台、丰富的库支持、开发效率高 |
| GUI框架 | PyQt6 | 6.4+ | 成熟的跨平台GUI框架、功能强大 |
| ORM框架 | SQLAlchemy | 2.0+ | 强大的ORM和SQL工具、支持多种数据库 |
| 数据库 | SQLite | 3.x | 軻量级、无需安装、适合桌面应用 |
| 日志框架 | logging | 内置 | Python标准库、功能完善 |
| 配置管理 | PyYAML | 6.0+ | YAML配置文件支持、易读易维护 |
| 数据验证 | Pydantic | 2.0+ | 数据验证和序列化、类型安全 |
| 加密库 | cryptography | 41.0+ | 密码加密、数据加密 |
| HTTP客户端 | requests | 2.31+ | HTTP请求库、简洁易用 |
| 测试框架 | pytest | 7.4+ | 单元测试框架、插件丰富 |
| 打包工具 | PyInstaller | 6.0+ | 打包为可执行文件 |

### 2.2 Android端技术栈

| 技术领域 | 技术选型 | 版本 | 选型理由 |
|---------|---------|------|---------|
| 编程语言 | Java | 11 | Android官方支持语言、稳定成熟 |
| 构建工具 | Gradle | 8.0+ | 灵活的构建系统、依赖管理 |
| UI框架 | Android SDK | API 26+ | Android原生开发、性能最优 |
| 架构组件 | Android Jetpack | 最新 | 官方架构组件、简化开发 |
| 数据库 | Room | 2.6+ | Android官方ORM、类型安全 |
| 网络框架 | Retrofit | 2.9+ | RESTful API客户端、简洁高效 |
| JSON解析 | Gson | 2.10+ | JSON序列化/反序列化 |
| 依赖注入 | Hilt | 2.48+ | Dagger封装、简化DI |
| 日志框架 | Timber | 5.0+ | 轻量级日志框架 |
| 数据验证 | Apache Validator | 1.7+ | 数据验证工具 |
| 测试框架 | JUnit | 4.13+ | 单元测试框架 |
| UI测试 | Espresso | 3.5+ | UI自动化测试 |

### 2.3 共享技术

| 技术领域 | 技术选型 | 说明 |
|---------|---------|------|
| 数据格式 | JSON | 跨平台数据交换格式、易解析 |
| 加密算法 | AES-256 | 数据加密标准、安全性高 |
| 哈希算法 | SHA-256 | 密码哈希算法、不可逆 |
| API协议 | RESTful | 统一API设计规范、易于理解 |
| 认证方式 | JWT | 无状态认证、适合分布式 |
| 版本控制 | Git | 代码版本管理 |

### 2.4 开发工具

| 工具类型 | 工具名称 | 用途 |
|---------|---------|------|
| IDE (Windows) | PyCharm / VS Code | Python开发 |
| IDE (Android) | Android Studio | Android开发 |
| 数据库工具 | DB Browser for SQLite | 数据库管理 |
| API测试 | Postman | API测试和文档 |
| 版本控制 | Git | 代码管理 |
| 项目管理 | Jira / Trello | 任务跟踪 |

## 3. 数据模型设计

### 3.1 实体关系图 (ER图)
```
┌──────────────────┐         ┌──────────────────┐
│     用户(User)     │         │     角色(Role)     │
├──────────────────┤         ├──────────────────┤
│ id (PK)           │         │ id (PK)           │
│ username          │         │ name              │
│ password_hash     │         │ permissions (JSON)│
│ salt              │         │ description       │
│ role_id (FK)      │────────→│ created_at        │
│ is_active         │         └──────────────────┘
│ last_login        │
│ created_at        │
│ updated_at        │
└──────────────────┘

┌──────────────────┐         ┌──────────────────┐
│   科目(Account)    │         │   凭证(Voucher)    │
├──────────────────┤         ├──────────────────┤
│ id (PK)           │         │ id (PK)           │
│ code              │         │ number            │
│ name              │         │ date              │
│ type              │         │ period            │
│ parent_id (FK)    │────────→│ creator_id (FK)   │
│ level             │         │ reviewer_id (FK)  │
│ direction         │         │ status            │
│ balance           │         │ total_debit       │
│ is_active         │         │ total_credit      │
│ created_at        │         │ created_at        │
│ updated_at        │         │ updated_at        │
└──────────────────┘         └──────────────────┘
                                      │
                                      ↓
                             ┌──────────────────┐
                             │ 凭证明细(Detail)   │
                             ├──────────────────┤
                             │ id (PK)           │
                             │ voucher_id (FK)   │
                             │ account_id (FK)   │
                             │ debit             │
                             │ credit            │
                             │ summary           │
                             │ order_num         │
                             └──────────────────┘

┌──────────────────┐         ┌──────────────────┐
│  审计日志(AuditLog) │         │ 会计期间(Period)   │
├──────────────────┤         ├──────────────────┤
│ id (PK)           │         │ id (PK)           │
│ user_id (FK)      │         │ period            │
│ operation         │         │ start_date        │
│ target_type       │         │ end_date          │
│ target_id         │         │ is_closed         │
│ old_value (JSON)  │         │ created_at        │
│ new_value (JSON)  │         └──────────────────┘
│ ip_address        │
│ timestamp         │
└──────────────────┘
```

### 3.2 核心数据表设计

#### 用户表 (users)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| username | VARCHAR(50) | UNIQUE NOT NULL | 用户名 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希值 |
| salt | VARCHAR(64) | NOT NULL | 密码盐值 |
| role_id | INTEGER | FOREIGN KEY REFERENCES roles(id) | 角色ID |
| is_active | BOOLEAN | DEFAULT TRUE | 是否激活 |
| last_login | TIMESTAMP | | 最后登录时间 |
| login_fail_count | INTEGER | DEFAULT 0 | 登录失败次数 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | | 更新时间 |

**索引**:
- UNIQUE INDEX idx_username ON users(username)
- INDEX idx_role ON users(role_id)

#### 角色表 (roles)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| name | VARCHAR(50) | UNIQUE NOT NULL | 角色名称 |
| permissions | TEXT | NOT NULL | 权限列表(JSON格式) |
| description | VARCHAR(255) | | 角色描述 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**权限JSON格式示例**:
```json
{
  "permissions": [
    "voucher:create",
    "voucher:edit",
    "voucher:delete",
    "voucher:review",
    "account:view",
    "report:view"
  ]
}
```

#### 会计科目表 (accounts)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| code | VARCHAR(20) | UNIQUE NOT NULL | 科目编码 |
| name | VARCHAR(100) | NOT NULL | 科目名称 |
| type | VARCHAR(20) | NOT NULL | 科目类型(asset/liability/equity/revenue/expense) |
| parent_id | INTEGER | FOREIGN KEY REFERENCES accounts(id) | 父科目ID |
| level | INTEGER | NOT NULL | 科目级别(1-5) |
| direction | VARCHAR(10) | NOT NULL | 借贷方向(debit/credit) |
| balance | DECIMAL(18,2) | DEFAULT 0.00 | 当前余额 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | | 更新时间 |

**索引**:
- UNIQUE INDEX idx_account_code ON accounts(code)
- INDEX idx_account_parent ON accounts(parent_id)
- INDEX idx_account_type ON accounts(type)

#### 凭证表 (vouchers)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| number | VARCHAR(20) | UNIQUE NOT NULL | 凭证号 |
| date | DATE | NOT NULL | 凭证日期 |
| period | VARCHAR(7) | NOT NULL | 会计期间(YYYY-MM) |
| creator_id | INTEGER | FOREIGN KEY REFERENCES users(id) | 制单人ID |
| reviewer_id | INTEGER | FOREIGN KEY REFERENCES users(id) | 审核人ID |
| status | VARCHAR(20) | NOT NULL DEFAULT 'draft' | 状态(draft/pending/approved/rejected) |
| total_debit | DECIMAL(18,2) | NOT NULL DEFAULT 0.00 | 借方合计 |
| total_credit | DECIMAL(18,2) | NOT NULL DEFAULT 0.00 | 贷方合计 |
| remark | TEXT | | 备注 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | | 更新时间 |

**索引**:
- UNIQUE INDEX idx_voucher_number ON vouchers(number)
- INDEX idx_voucher_date ON vouchers(date)
- INDEX idx_voucher_period ON vouchers(period)
- INDEX idx_voucher_status ON vouchers(status)
- INDEX idx_voucher_creator ON vouchers(creator_id)

#### 凭证明细表 (voucher_details)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| voucher_id | INTEGER | NOT NULL FOREIGN KEY REFERENCES vouchers(id) | 凭证ID |
| account_id | INTEGER | NOT NULL FOREIGN KEY REFERENCES accounts(id) | 科目ID |
| debit | DECIMAL(18,2) | NOT NULL DEFAULT 0.00 | 借方金额 |
| credit | DECIMAL(18,2) | NOT NULL DEFAULT 0.00 | 贷方金额 |
| summary | VARCHAR(255) | | 摘要 |
| order_num | INTEGER | NOT NULL | 行号 |

**索引**:
- INDEX idx_detail_voucher ON voucher_details(voucher_id)
- INDEX idx_detail_account ON voucher_details(account_id)

**约束**:
- CHECK (debit >= 0 AND credit >= 0)
- CHECK ((debit > 0 AND credit = 0) OR (debit = 0 AND credit > 0) OR (debit = 0 AND credit = 0))

#### 审计日志表 (audit_logs)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| user_id | INTEGER | FOREIGN KEY REFERENCES users(id) | 用户ID |
| operation | VARCHAR(50) | NOT NULL | 操作类型 |
| target_type | VARCHAR(50) | NOT NULL | 目标类型 |
| target_id | INTEGER | | 目标ID |
| old_value | TEXT | | 旧值(JSON) |
| new_value | TEXT | | 新值(JSON) |
| ip_address | VARCHAR(50) | | IP地址 |
| user_agent | VARCHAR(255) | | 用户代理 |
| timestamp | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 时间戳 |

**索引**:
- INDEX idx_audit_user ON audit_logs(user_id)
- INDEX idx_audit_operation ON audit_logs(operation)
- INDEX idx_audit_timestamp ON audit_logs(timestamp)

#### 会计期间表 (accounting_periods)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| period | VARCHAR(7) | UNIQUE NOT NULL | 期间(YYYY-MM) |
| start_date | DATE | NOT NULL | 开始日期 |
| end_date | DATE | NOT NULL | 结束日期 |
| is_closed | BOOLEAN | DEFAULT FALSE | 是否关闭 |
| closed_by | INTEGER | FOREIGN KEY REFERENCES users(id) | 关闭人ID |
| closed_at | TIMESTAMP | | 关闭时间 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**索引**:
- UNIQUE INDEX idx_period ON accounting_periods(period)

### 3.3 数据字典

#### 科目类型 (account_type)
| 值 | 名称 | 借贷方向 | 说明 |
|----|------|---------|------|
| asset | 资产 | 借 | 资产类科目，增加记借方 |
| liability | 负债 | 贷 | 负债类科目，增加记贷方 |
| equity | 所有者权益 | 贷 | 所有者权益类科目，增加记贷方 |
| revenue | 收入 | 贷 | 收入类科目，增加记贷方 |
| expense | 费用 | 借 | 费用类科目，增加记借方 |

#### 凭证状态 (voucher_status)
| 值 | 名称 | 可编辑 | 说明 |
|----|------|--------|------|
| draft | 草稿 | 是 | 新建凭证，可修改删除 |
| pending | 待审核 | 否 | 已提交，等待审核 |
| approved | 已审核 | 否 | 已通过审核，不可修改 |
| rejected | 已拒绝 | 是 | 审核拒绝，可修改后重新提交 |

#### 操作类型 (operation_type)
| 值 | 名称 | 说明 |
|----|------|------|
| login | 登录 | 用户登录系统 |
| logout | 登出 | 用户登出系统 |
| create | 创建 | 创建新记录 |
| update | 更新 | 更新记录 |
| delete | 删除 | 删除记录 |
| submit | 提交 | 提交凭证审核 |
| approve | 审核通过 | 审核凭证通过 |
| reject | 审核拒绝 | 审核凭证拒绝 |
| backup | 备份 | 数据备份 |
| restore | 恢复 | 数据恢复 |

## 4. 接口设计

### 4.1 内部接口 (Internal API)

#### Windows端业务逻辑层接口

**用户服务接口 (UserService)**
```python
class UserService:
    def login(username: str, password: str) -> Result[User]
    def logout(user_id: int) -> Result[None]
    def get_user_by_id(user_id: int) -> Result[User]
    def get_user_by_username(username: str) -> Result[User]
    def create_user(user: UserCreate) -> Result[User]
    def update_user(user_id: int, user: UserUpdate) -> Result[User]
    def delete_user(user_id: int) -> Result[None]
    def change_password(user_id: int, old_password: str, new_password: str) -> Result[None]
    def check_permission(user_id: int, permission: str) -> bool
```

**科目服务接口 (AccountService)**
```python
class AccountService:
    def create_account(account: AccountCreate) -> Result[Account]
    def update_account(account_id: int, account: AccountUpdate) -> Result[Account]
    def delete_account(account_id: int) -> Result[None]
    def get_account_by_id(account_id: int) -> Result[Account]
    def get_account_by_code(code: str) -> Result[Account]
    def get_account_tree() -> Result[List[AccountNode]]
    def get_account_children(parent_id: int) -> Result[List[Account]]
    def get_account_balance(account_id: int, period: str = None) -> Result[Decimal]
    def update_account_balance(account_id: int, amount: Decimal, direction: str) -> Result[None]
    def validate_account_code(code: str) -> bool
    def is_account_used(account_id: int) -> bool
```

**凭证服务接口 (VoucherService)**
```python
class VoucherService:
    def create_voucher(voucher: VoucherCreate) -> Result[Voucher]
    def update_voucher(voucher_id: int, voucher: VoucherUpdate) -> Result[Voucher]
    def delete_voucher(voucher_id: int) -> Result[None]
    def get_voucher_by_id(voucher_id: int) -> Result[Voucher]
    def get_voucher_by_number(number: str) -> Result[Voucher]
    def query_vouchers(criteria: VoucherQueryCriteria) -> Result[List[Voucher]]
    def submit_voucher(voucher_id: int) -> Result[Voucher]
    def review_voucher(voucher_id: int, approved: bool, comment: str = None) -> Result[Voucher]
    def generate_voucher_number(date: date) -> str
    def validate_voucher(voucher: Voucher) -> List[str]
    def is_voucher_balanced(voucher: Voucher) -> bool
    def calculate_totals(voucher: Voucher) -> Tuple[Decimal, Decimal]
```

**报表服务接口 (ReportService)**
```python
class ReportService:
    def generate_balance_sheet(period: str) -> Result[BalanceSheet]
    def generate_income_statement(start_period: str, end_period: str) -> Result[IncomeStatement]
    def generate_trial_balance(period: str) -> Result[TrialBalance]
    def generate_general_ledger(account_id: int, start_date: date, end_date: date) -> Result[GeneralLedger]
    def generate_subsidiary_ledger(account_id: int, start_date: date, end_date: date) -> Result[SubsidiaryLedger]
    def export_report(report: Report, format: str) -> Result[bytes]
```

**审计服务接口 (AuditService)**
```python
class AuditService:
    def log_operation(user_id: int, operation: str, target_type: str, target_id: int,
                      old_value: dict = None, new_value: dict = None) -> None
    def query_logs(criteria: AuditLogCriteria) -> Result[List[AuditLog]]
    def get_user_operations(user_id: int, start_time: datetime, end_time: datetime) -> Result[List[AuditLog]]
```

#### Android端业务逻辑层接口

**科目服务接口 (AccountService.java)**
```java
public interface AccountService {
    Single<Result<Account>> createAccount(AccountCreate account);
    Single<Result<Account>> updateAccount(int accountId, AccountUpdate account);
    Single<Result<Void>> deleteAccount(int accountId);
    Single<Result<Account>> getAccountById(int accountId);
    Single<Result<List<AccountNode>>> getAccountTree();
    Single<Result<BigDecimal>> getAccountBalance(int accountId, String period);
}
```

**凭证服务接口 (VoucherService.java)**
```java
public interface VoucherService {
    Single<Result<Voucher>> createVoucher(VoucherCreate voucher);
    Single<Result<Voucher>> updateVoucher(int voucherId, VoucherUpdate voucher);
    Single<Result<Void>> deleteVoucher(int voucherId);
    Single<Result<Voucher>> getVoucherById(int voucherId);
    Single<Result<List<Voucher>>> queryVouchers(VoucherQueryCriteria criteria);
    Single<Result<Voucher>> submitVoucher(int voucherId);
    Single<Result<Voucher>> reviewVoucher(int voucherId, boolean approved, String comment);
}
```

### 4.2 外部接口 (External API)

#### RESTful API设计

**基础信息**:
- 基硎路径: `/api/v1`
- 认证方式: Bearer Token (JWT)
- 数据格式: JSON
- 字符编码: UTF-8

**认证接口**:
```
POST   /auth/login              # 用户登录
请求体: { "username": "string", "password": "string" }
响应: { "token": "string", "refresh_token": "string", "user": {...} }

POST   /auth/logout             # 用户登出
请求头: Authorization: Bearer {token}
响应: { "message": "success" }

POST   /auth/refresh            # 刷新令牌
请求体: { "refresh_token": "string" }
响应: { "token": "string", "refresh_token": "string" }

GET    /auth/profile            # 获取用户信息
请求头: Authorization: Bearer {token}
响应: { "user": {...} }
```

**科目管理接口**:
```
GET    /accounts                # 获取科目列表
参数: ?type={type}&parent_id={parent_id}&is_active={true/false}
响应: { "accounts": [...] }

GET    /accounts/tree           # 获取科目树
响应: { "tree": [...] }

GET    /accounts/{id}           # 获取科目详情
响应: { "account": {...} }

POST   /accounts                # 创建科目
请求体: { "code": "string", "name": "string", "type": "string", "parent_id": int }
响应: { "account": {...} }

PUT    /accounts/{id}           # 更新科目
请求体: { "name": "string", "is_active": bool }
响应: { "account": {...} }

DELETE /accounts/{id}           # 删除科目
响应: { "message": "success" }

GET    /accounts/{id}/balance   # 获取科目余额
参数: ?period={period}
响应: { "balance": "decimal" }
```

**凭证管理接口**:
```
GET    /vouchers                # 查询凭证
参数: ?period={period}&status={status}&start_date={date}&end_date={date}&page={page}&size={size}
响应: { "vouchers": [...], "total": int, "page": int, "size": int }

GET    /vouchers/{id}           # 获取凭证详情
响应: { "voucher": {...}, "details": [...] }

POST   /vouchers                # 创建凭证
请求体: {
  "date": "date",
  "period": "string",
  "details": [
    { "account_id": int, "debit": "decimal", "credit": "decimal", "summary": "string" }
  ]
}
响应: { "voucher": {...} }

PUT    /vouchers/{id}           # 更新凭证
请求体: { "date": "date", "details": [...] }
响应: { "voucher": {...} }

DELETE /vouchers/{id}           # 删除凭证
响应: { "message": "success" }

POST   /vouchers/{id}/submit    # 提交凭证
响应: { "voucher": {...} }

POST   /vouchers/{id}/review    # 审核凭证
请求体: { "approved": bool, "comment": "string" }
响应: { "voucher": {...} }
```

**报表接口**:
```
GET    /reports/balance-sheet   # 资产负债表
参数: ?period={period}
响应: { "report": {...} }

GET    /reports/income-statement # 利润表
参数: ?start_period={period}&end_period={period}
响应: { "report": {...} }

GET    /reports/trial-balance   # 试算平衡表
参数: ?period={period}
响应: { "report": {...} }

GET    /reports/general-ledger  # 总账
参数: ?account_id={id}&start_date={date}&end_date={date}
响应: { "report": {...} }

GET    /reports/subsidiary-ledger # 明细账
参数: ?account_id={id}&start_date={date}&end_date={date}
响应: { "report": {...} }

GET    /reports/export          # 导出报表
参数: ?report_type={type}&format={pdf/excel}&...
响应: Content-Type: application/pdf 或 application/vnd.ms-excel
```

**数据管理接口**:
```
POST   /data/backup             # 数据备份
响应: Content-Type: application/zip

POST   /data/restore            # 数据恢复
请求体: multipart/form-data (backup file)
响应: { "message": "success" }

POST   /data/import/vouchers    # 导入凭证
请求体: multipart/form-data (csv/excel file)
响应: { "imported": int, "failed": int, "errors": [...] }
```

### 4.3 接口数据格式

#### 标准响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 业务数据
  },
  "timestamp": "2026-04-19T10:30:00Z"
}
```

#### 分页响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "size": 20,
    "total_pages": 5
  },
  "timestamp": "2026-04-19T10:30:00Z"
}
```

#### 错误响应格式
```json
{
  "code": 400,
  "message": "请求参数错误",
  "errors": [
    {
      "field": "debit",
      "message": "借方金额不能为负数"
    },
    {
      "field": "credit",
      "message": "贷方金额不能为负数"
    }
  ],
  "timestamp": "2026-04-19T10:30:00Z"
}
```

#### 凭证数据格式
```json
{
  "id": 1,
  "number": "202604-001",
  "date": "2026-04-19",
  "period": "2026-04",
  "creator": {
    "id": 1,
    "username": "accountant"
  },
  "reviewer": null,
  "status": "draft",
  "total_debit": 10000.00,
  "total_credit": 10000.00,
  "details": [
    {
      "id": 1,
      "account": {
        "id": 1001,
        "code": "1001",
        "name": "库存现金"
      },
      "debit": 10000.00,
      "credit": 0.00,
      "summary": "收到销售货款",
      "order_num": 1
    },
    {
      "id": 2,
      "account": {
        "id": 6001,
        "code": "6001",
        "name": "主营业务收入"
      },
      "debit": 0.00,
      "credit": 10000.00,
      "summary": "销售商品收入",
      "order_num": 2
    }
  ],
  "created_at": "2026-04-19T10:30:00Z",
  "updated_at": null
}
```

## 5. 安全设计

### 5.1 认证机制

**JWT Token认证流程**:
```
1. 用户登录 → 验证用户名密码
2. 生成JWT Token (有效期2小时)
3. 生成Refresh Token (有效期7天)
4. 客户端存储Token
5. 请求时携带Token: Authorization: Bearer {token}
6. 服务端验证Token有效性
7. Token过期时使用Refresh Token刷新
```

**Token载荷 (Payload)**:
```json
{
  "sub": 1,              // 用户ID
  "username": "accountant",
  "role": "accountant",
  "permissions": ["voucher:create", "voucher:edit"],
  "iat": 1713522600,     // 签发时间
  "exp": 1713529800      // 过期时间
}
```

**登录失败锁定策略**:
- 连续失败5次，锁定账户30分钟
- 锁定期间拒绝登录尝试
- 成功登录后重置失败计数

### 5.2 权限控制

**RBAC权限模型**:
```
用户(User) → 角色(Role) → 权限(Permission)
```

**预定义角色**:
| 角色名称 | 权限列表 |
|---------|---------|
| administrator | 所有权限 |
| accountant | voucher:create, voucher:edit, voucher:delete, account:view, report:view |
| reviewer | voucher:review, account:view, report:view |
| viewer | account:view, report:view |

**权限检查流程**:
```python
def check_permission(user_id: int, permission: str) -> bool:
    user = get_user(user_id)
    role = get_role(user.role_id)
    permissions = json.loads(role.permissions)
    return permission in permissions or "all" in permissions
```

**数据级权限**:
- 会计人员只能查看和修改自己创建的草稿凭证
- 审核人员可以查看所有待审核凭证
- 管理员可以查看所有数据

### 5.3 数据安全

**密码加密**:
```python
import hashlib
import secrets

def hash_password(password: str) -> tuple[str, str]:
    # 生成随机盐值
    salt = secrets.token_hex(32)
    # 使用SHA-256哈希
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash, salt

def verify_password(password: str, password_hash: str, salt: str) -> bool:
    computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return computed_hash == password_hash
```

**数据备份加密**:
```python
from cryptography.fernet import Fernet

def encrypt_backup(data: bytes, password: str) -> bytes:
    # 从密码生成密钥
    key = generate_key_from_password(password)
    fernet = Fernet(key)
    return fernet.encrypt(data)

def decrypt_backup(encrypted_data: bytes, password: str) -> bytes:
    key = generate_key_from_password(password)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data)
```

**SQL注入防护**:
- 使用参数化查询
- 使用ORM框架
- 输入验证和转义

**XSS防护**:
- 输出内容转义
- Content-Type正确设置
- CSP策略配置

### 5.4 审计日志

**记录的操作**:
- 用户登录/登出
- 凭证创建/修改/删除/提交/审核
- 科目创建/修改/删除
- 数据备份/恢复
- 权限变更

**日志格式**:
```json
{
  "id": 1,
  "user_id": 1,
  "operation": "create",
  "target_type": "voucher",
  "target_id": 100,
  "old_value": null,
  "new_value": {
    "number": "202604-001",
    "date": "2026-04-19",
    "total_debit": 10000.00,
    "total_credit": 10000.00
  },
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "timestamp": "2026-04-19T10:30:00Z"
}
```

## 6. 性能设计

### 6.1 性能指标

| 操作类型 | 响应时间要求 | 并发数 | 说明 |
|---------|-------------|--------|------|
| 用户登录 | < 500ms | 50 | 包含密码验证和Token生成 |
| 科目查询 | < 200ms | 100 | 科目树查询 |
| 凭证创建 | < 500ms | 50 | 包含验证和保存 |
| 凭证查询 | < 300ms | 100 | 分页查询 |
| 凭证审核 | < 800ms | 20 | 包含余额更新 |
| 总账查询 | < 1s | 20 | 单个科目总账 |
| 资产负债表 | < 3s | 10 | 全科目汇总 |
| 利润表 | < 3s | 10 | 收入费用汇总 |
| 数据备份 | < 30s | 5 | 全量备份 |

### 6.2 优化策略

**数据库优化**:
- 合理创建索引（见3.2节）
- 查询语句优化，避免N+1查询
- 使用连接池管理数据库连接
- 定期执行VACUUM和ANALYZE

**缓存策略**:
```python
# 科目树缓存（30分钟）
@cache(ttl=1800)
def get_account_tree() -> List[AccountNode]:
    ...

# 用户权限缓存（1小时）
@cache(ttl=3600)
def get_user_permissions(user_id: int) -> List[str]:
    ...

# 科目余额缓存（实时失效）
@cache(ttl=0, invalidate_on=["voucher:review"])
def get_account_balance(account_id: int) -> Decimal:
    ...
```

**异步处理**:
```python
# 报表生成异步处理
async def generate_report_async(report_type: str, params: dict) -> str:
    task_id = create_task(report_type, params)
    await execute_task(task_id)
    return task_id

# 数据导入异步处理
async def import_vouchers_async(file_path: str) -> ImportResult:
    ...
```

**批量操作优化**:
```python
# 批量插入凭证明细
def batch_insert_details(details: List[VoucherDetail]):
    session.bulk_save_objects(details)
    session.commit()
```

### 6.3 数据库连接池配置

**Windows端 (SQLAlchemy)**:
```python
from sqlalchemy import create_engine

engine = create_engine(
    'sqlite:///database.db',
    pool_size=10,           # 连接池大小
    max_overflow=20,        # 最大溢出连接数
    pool_timeout=30,        # 获取连接超时时间
    pool_recycle=3600,      # 连接回收时间
    echo=False              # 不输出SQL语句
)
```

**Android端 (Room)**:
```java
Room.databaseBuilder(context, AppDatabase.class, "database.db")
    .setJournalMode(JournalMode.TRUNCATE)  // 性能优化
    .build();
```

## 7. 异常处理设计

### 7.1 异常分类

**业务异常 (BusinessException)**:
- 可预期的业务错误
- 需要向用户显示明确的错误信息
- 不需要记录详细堆栈信息

**系统异常 (SystemException)**:
- 技术层面的错误
- 需要记录详细的错误日志
- 向用户显示友好的错误提示

**网絡异常 (NetworkException)**:
- 网络连接失败
- API请求超时
- 需要提供重试机制

### 7.2 异常处理流程
```
异常发生
    ↓
异常捕获 (try-except)
    ↓
异常分类
    ↓
┌─────────────┬─────────────┬─────────────┐
│ 业务异常     │ 系统异常     │ 网络异常     │
└─────────────┴─────────────┴─────────────┘
    ↓              ↓              ↓
记录日志        记录详细日志     记录日志
(简单)          (含堆栈)        (简单)
    ↓              ↓              ↓
显示错误        显示友好提示    显示重试选项
信息            + 通知管理员
    ↓              ↓              ↓
返回错误响应    返回错误响应    重试或返回错误
```

### 7.3 错误码规范

| 错误码范围 | 错误类型 | 示例 |
|-----------|---------|------|
| 1000-1999 | 用户相关错误 | 1001: 用户名不存在, 1002: 密码错误, 1003: 账户已锁定 |
| 2000-2999 | 科目相关错误 | 2001: 科目编码已存在, 2002: 科目已被使用, 2003: 父科目不存在 |
| 3000-3999 | 凭证相关错误 | 3001: 借贷不平衡, 3002: 凭证日期不在期间内, 3003: 凭证已审核 |
| 4000-4999 | 系统相关错误 | 4001: 数据库错误, 4002: 文件读写错误, 4003: 配置错误 |
| 5000-5999 | 网络相关错误 | 5001: 连接超时, 5002: 请求失败, 5003: 认证失败 |

### 7.4 异常处理实现

**Windows端 (Python)**:
```python
class AccountingException(Exception):
    def __init__(self, code: int, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)

class BusinessException(AccountingException):
    pass

class SystemException(AccountingException):
    pass

# 全局异常处理器
def handle_exception(e: Exception) -> dict:
    if isinstance(e, BusinessException):
        logger.warning(f"业务异常: {e.code} - {e.message}")
        return {
            "code": e.code,
            "message": e.message,
            "details": e.details
        }
    elif isinstance(e, SystemException):
        logger.error(f"系统异常: {e.code} - {e.message}", exc_info=True)
        return {
            "code": e.code,
            "message": "系统错误，请联系管理员",
            "details": {}
        }
    else:
        logger.error(f"未知异常: {str(e)}", exc_info=True)
        return {
            "code": 9999,
            "message": "未知错误",
            "details": {}
        }
```

**Android端 (Java)**:
```java
public class AccountingException extends Exception {
    private int code;
    private String message;
    private Map<String, Object> details;

    public AccountingException(int code, String message) {
        super(message);
        this.code = code;
        this.message = message;
        this.details = new HashMap<>();
    }
}

// 全局异常处理器
public class GlobalExceptionHandler implements Thread.UncaughtExceptionHandler {
    @Override
    public void uncaughtException(Thread thread, Throwable throwable) {
        if (throwable instanceof AccountingException) {
            AccountingException e = (AccountingException) throwable;
            Timber.w("业务异常: %d - %s", e.getCode(), e.getMessage());
            showErrorToast(e.getMessage());
        } else {
            Timber.e(throwable, "系统异常");
            showErrorToast("系统错误，请联系管理员");
        }
    }
}
```

## 8. 部署架构

### 8.1 Windows端部署

**安装包结构**:
```
AccountingSystem_Windows_v1.0.0/
├── accounting_system.exe      # 主程序
├── python39.dll               # Python运行时
├── config/                    # 配置文件
│   ├── app.yaml              # 应用配置
│   ├── database.yaml         # 数据库配置
│   └── logging.yaml          # 日志配置
├── data/                      # 数据目录
│   ├── database.db           # SQLite数据库
│   └── backups/              # 备份目录
├── logs/                      # 日志目录
│   ├── app.log               # 应用日志
│   └── audit.log             # 审计日志
├── resources/                 # 资源文件
│   ├── icons/                # 图标
│   ├── styles/               # 样式
│   └── templates/            # 模板
└── libs/                      # 依赖库
    ├── PyQt6/
    ├── sqlalchemy/
    └── ...
```

**配置文件示例 (app.yaml)**:
```yaml
app:
  name: "会计管理系统"
  version: "1.0.0"
  language: "zh_CN"

database:
  type: "sqlite"
  path: "./data/database.db"
  pool_size: 10

sync:
  enabled: true
  server_url: "https://api.example.com"
  sync_interval: 300  # 5分钟

ui:
  theme: "light"
  font_size: 12
  window_size:
    width: 1280
    height: 720
```

**打包脚本**:
```python
# build.py
import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name=accounting_system',
    '--onefile',
    '--windowed',
    '--add-data=config;config',
    '--add-data=resources;resources',
    '--icon=resources/icons/app.ico',
    '--clean'
])
```

### 8.2 Android端部署

**APK结构**:
```
AccountingSystem_v1.0.0.apk/
├── AndroidManifest.xml        # 清单文件
├── classes.dex                # 编译后的代码
├── resources.arsc             # 资源索引
├── res/                       # 资源文件
│   ├── drawable/             # 图片资源
│   ├── layout/               # 布局文件
│   ├── values/               # 字符串、样式等
│   └── mipmap/               # 应用图标
├── assets/                    # 资产文件
│   └── config.json           # 配置文件
├── lib/                       # 原生库
│   └── arm64-v8a/            # ARM64架构
└── META-INF/                  # 签名信息
```

**Gradle配置 (build.gradle)**:
```gradle
android {
    compileSdk 33

    defaultConfig {
        applicationId "com.example.accounting"
        minSdk 26
        targetSdk 33
        versionCode 1
        versionName "1.0.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.room:room-runtime:2.6.1'
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.google.dagger:hilt-android:2.48'
    // ...
}
```

### 8.3 数据同步架构

**同步策略**:
```
Android端                    服务器                     Windows端
    │                          │                          │
    │  1. 本地数据变更          │                          │
    │──────────────────────→  │                          │
    │                          │  2. 接收并存储            │
    │                          │                          │
    │                          │  3. 推送变更通知          │
    │                          │──────────────────────→  │
    │                          │                          │
    │                          │  4. Windows端同步         │
    │                          │←──────────────────────  │
    │                          │                          │
    │  5. 定期拉取更新          │                          │
    │←──────────────────────  │                          │
    │                          │                          │
```

**冲突解决策略**:
- 时间戳优先：最后修改时间戳大的优先
- 版本号检查：使用乐观锁避免冲突
- 手动解决：对于无法自动解决的冲突，提示用户选择

## 9. 测试策略

### 9.1 测试层次

**单元测试**:
- 覆盖率目标: > 80%
- 测试范围: 业务逻辑层、数据访问层
- 测试工具: pytest (Python), JUnit (Java)

**集成测试**:
- 测试范围: 模块间交互、数据库操作
- 测试数据: 使用独立的测试数据库
- 测试工具: pytest + SQLAlchemy (Python), AndroidX Test (Java)

**系统测试**:
- 测试范围: 端到端业务流程
- 测试环境: 接近生产环境
- 测试工具: 手动测试 + 自动化脚本

**性能测试**:
- 测试范围: 并发、响应时间、资源占用
- 测试工具: JMeter, Android Profiler

**用户验收测试**:
- 测试范围: 用户实际使用场景
- 测试人员: 实际用户或业务专家

### 9.2 测试用例示例

**凭证创建测试 (Python)**:
```python
import pytest
from services import VoucherService
from models import VoucherCreate

def test_create_voucher_success():
    """测试成功创建凭证"""
    service = VoucherService()
    voucher_data = VoucherCreate(
        date="2026-04-19",
        period="2026-04",
        details=[
            {"account_id": 1001, "debit": 10000, "credit": 0, "summary": "测试"},
            {"account_id": 6001, "debit": 0, "credit": 10000, "summary": "测试"}
        ]
    )

    result = service.create_voucher(voucher_data)

    assert result.success
    assert result.data.number is not None
    assert result.data.status == "draft"
    assert result.data.total_debit == 10000
    assert result.data.total_credit == 10000

def test_create_voucher_unbalanced():
    """测试创建不平衡凭证"""
    service = VoucherService()
    voucher_data = VoucherCreate(
        date="2026-04-19",
        period="2026-04",
        details=[
            {"account_id": 1001, "debit": 10000, "credit": 0, "summary": "测试"},
            {"account_id": 6001, "debit": 0, "credit": 5000, "summary": "测试"}
        ]
    )

    result = service.create_voucher(voucher_data)

    assert not result.success
    assert "借贷不平衡" in result.message
```

**凭证创建测试 (Java)**:
```java
@Test
public void testCreateVoucherSuccess() {
    VoucherService service = new VoucherService();
    VoucherCreate voucherData = new VoucherCreate();
    voucherData.setDate("2026-04-19");
    voucherData.setPeriod("2026-04");
    voucherData.setDetails(Arrays.asList(
        new VoucherDetail(1001, new BigDecimal("10000"), BigDecimal.ZERO, "测试"),
        new VoucherDetail(6001, BigDecimal.ZERO, new BigDecimal("10000"), "测试")
    ));

    Result<Voucher> result = service.createVoucher(voucherData).blockingGet();

    assertTrue(result.isSuccess());
    assertNotNull(result.getData().getNumber());
    assertEquals("draft", result.getData().getStatus());
    assertEquals(new BigDecimal("10000"), result.getData().getTotalDebit());
    assertEquals(new BigDecimal("10000"), result.getData().getTotalCredit());
}
```

### 9.3 测试数据管理

**测试数据库**:
- 使用独立的测试数据库文件
- 每次测试前初始化数据
- 测试后清理数据

**数据准备脚本**:
```python
# tests/conftest.py
import pytest
from database import init_db, SessionLocal

@pytest.fixture(scope="function")
def db_session():
    """创建测试数据库会话"""
    init_db()
    session = SessionLocal()

    # 准备测试数据
    prepare_test_data(session)

    yield session

    # 清理测试数据
    session.rollback()
    session.close()

def prepare_test_data(session):
    """准备测试数据"""
    # 创建测试用户
    user = User(username="test_user", role_id=1)
    session.add(user)

    # 创建测试科目
    account1 = Account(code="1001", name="库存现金", type="asset")
    account2 = Account(code="6001", name="主营业务收入", type="revenue")
    session.add_all([account1, account2])

    session.commit()
```

## 10. 技术风险与应对

### 10.1 风险识别

| 风险项 | 影响程度 | 发生概率 | 应对措施 |
|--------|---------|---------|---------|
| 数据一致性 | 高 | 中 | 使用数据库事务、实现乐观锁、定期数据校验 |
| 并发冲突 | 中 | 中 | 使用数据库锁机制、实现冲突检测和解决 |
| 网络中断 | 中 | 低 | 实现离线模式、数据本地缓存、自动重连机制 |
| 性能瓶颈 | 中 | 低 | 数据库索引优化、查询优化、缓存策略 |
| 数据丢失 | 高 | 低 | 定期自动备份、事务保护、操作日志 |
| 安全漏洞 | 高 | 低 | 输入验证、参数化查询、定期安全审计 |
| 跨平台兼容性 | 中 | 中 | 充分测试不同平台、使用标准数据格式 |

### 10.2 应对策略详细说明

**数据一致性保障**:
```python
# 使用数据库事务
def transfer_balance(from_account: int, to_account: int, amount: Decimal):
    with session.begin():
        # 借方科目
        account1 = session.query(Account).with_for_update().get(from_account)
        account1.balance -= amount

        # 贷方科目
        account2 = session.query(Account).with_for_update().get(to_account)
        account2.balance += amount

        # 自动提交或回滚
```

**并发冲突解决**:
```python
# 乐观锁实现
class Voucher(Base):
    __tablename__ = 'vouchers'

    id = Column(Integer, primary_key=True)
    version = Column(Integer, default=0)  # 版本号
    # ...

def update_voucher(voucher_id: int, data: dict, expected_version: int):
    voucher = session.query(Voucher).get(voucher_id)

    if voucher.version != expected_version:
        raise ConcurrentModificationError("数据已被其他用户修改")

    # 更新数据
    for key, value in data.items():
        setattr(voucher, key, value)

    voucher.version += 1
    session.commit()
```

**离线模式实现**:
```java
// Android端离线数据管理
public class OfflineDataManager {
    private LocalDatabase localDb;
    private Queue<PendingOperation> operationQueue;

    public void saveOffline(Voucher voucher) {
        // 保存到本地数据库
        localDb.voucherDao().insert(voucher);

        // 添加到待同步队列
        operationQueue.add(new PendingOperation("create", voucher));

        // 尝试同步
        trySync();
    }

    private void trySync() {
        if (isNetworkAvailable()) {
            while (!operationQueue.isEmpty()) {
                PendingOperation op = operationQueue.poll();
                syncOperation(op);
            }
        }
    }
}
```

## 11. 操作确认机制实现

### 11.1 自动保存操作

**Windows端实现**:
```python
class AutoSaveManager:
    """自动保存管理器"""

    AUTO_SAVE_OPERATIONS = {
        'voucher:create_draft',
        'voucher:update_draft',
        'account:create',
        'account:update_property',
        'data:query'
    }

    @staticmethod
    def should_auto_save(operation: str) -> bool:
        """判断是否应该自动保存"""
        return operation in AutoSaveManager.AUTO_SAVE_OPERATIONS

    @staticmethod
    def auto_save(operation: str, data: Any, callback: Callable):
        """执行自动保存"""
        if AutoSaveManager.should_auto_save(operation):
            try:
                result = callback(data)
                logger.info(f"自动保存成功: {operation}")
                return result
            except Exception as e:
                logger.error(f"自动保存失败: {operation}", exc_info=True)
                raise
```

**Android端实现**:
```java
public class AutoSaveManager {
    private static final Set<String> AUTO_SAVE_OPERATIONS = Set.of(
        "voucher:create_draft",
        "voucher:update_draft",
        "account:create",
        "account:update_property",
        "data:query"
    );

    public static boolean shouldAutoSave(String operation) {
        return AUTO_SAVE_OPERATIONS.contains(operation);
    }

    public static <T> Result<T> autoSave(String operation, T data, Function<T, Result<T>> callback) {
        if (shouldAutoSave(operation)) {
            try {
                Result<T> result = callback.apply(data);
                Timber.i("自动保存成功: %s", operation);
                return result;
            } catch (Exception e) {
                Timber.e(e, "自动保存失败: %s", operation);
                throw e;
            }
        }
        return Result.success(data);
    }
}
```

### 11.2 需确认操作

**Windows端实现**:
```python
from PyQt6.QtWidgets import QMessageBox

class ConfirmationManager:
    """确认对话框管理器"""

    CONFIRM_OPERATIONS = {
        'voucher:delete',
        'account:delete',
        'voucher:submit',
        'voucher:review',
        'data:restore',
        'data:import'
    }

    OPERATION_MESSAGES = {
        'voucher:delete': '确定要删除该凭证吗？删除后无法恢复。',
        'account:delete': '确定要删除该科目吗？删除后无法恢复。',
        'voucher:submit': '确定要提交该凭证进行审核吗？提交后将无法修改。',
        'voucher:review': '确定要审核该凭证吗？',
        'data:restore': '确定要从备份恢复数据吗？当前数据将被覆盖。',
        'data:import': '确定要导入凭证数据吗？'
    }

    @staticmethod
    def require_confirmation(operation: str) -> bool:
        """判断是否需要确认"""
        return operation in ConfirmationManager.CONFIRM_OPERATIONS

    @staticmethod
    def show_confirmation(parent: QWidget, operation: str) -> bool:
        """显示确认对话框"""
        if not ConfirmationManager.require_confirmation(operation):
            return True

        message = ConfirmationManager.OPERATION_MESSAGES.get(operation, '确定要执行此操作吗？')

        reply = QMessageBox.question(
            parent,
            '确认操作',
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        confirmed = reply == QMessageBox.StandardButton.Yes

        # 记录用户选择
        AuditService.log_operation(
            user_id=current_user.id,
            operation=f"{operation}:confirm",
            target_type="confirmation",
            new_value={"confirmed": confirmed}
        )

        return confirmed
```

**Android端实现**:
```java
public class ConfirmationManager {
    private static final Set<String> CONFIRM_OPERATIONS = Set.of(
        "voucher:delete",
        "account:delete",
        "voucher:submit",
        "voucher:review",
        "data:restore",
        "data:import"
    );

    private static final Map<String, String> OPERATION_MESSAGES = Map.of(
        "voucher:delete", "确定要删除该凭证吗？删除后无法恢复。",
        "account:delete", "确定要删除该科目吗？删除后无法恢复。",
        "voucher:submit", "确定要提交该凭证进行审核吗？提交后将无法修改。",
        "voucher:review", "确定要审核该凭证吗？",
        "data:restore", "确定要从备份恢复数据吗？当前数据将被覆盖。",
        "data:import", "确定要导入凭证数据吗？"
    );

    public static boolean requireConfirmation(String operation) {
        return CONFIRM_OPERATIONS.contains(operation);
    }

    public static void showConfirmation(
        Context context,
        String operation,
        OnConfirmationListener listener
    ) {
        if (!requireConfirmation(operation)) {
            listener.onConfirmed();
            return;
        }

        String message = OPERATION_MESSAGES.getOrDefault(operation, "确定要执行此操作吗？");

        new AlertDialog.Builder(context)
            .setTitle("确认操作")
            .setMessage(message)
            .setPositiveButton("确定", (dialog, which) -> {
                logConfirmation(operation, true);
                listener.onConfirmed();
            })
            .setNegativeButton("取消", (dialog, which) -> {
                logConfirmation(operation, false);
                listener.onCancelled();
            })
            .setCancelable(true)
            .show();
    }

    private static void logConfirmation(String operation, boolean confirmed) {
        AuditService.logOperation(
            UserService.getCurrentUserId(),
            operation + ":confirm",
            "confirmation",
            null,
            Map.of("confirmed", confirmed)
        );
    }

    public interface OnConfirmationListener {
        void onConfirmed();
        void onCancelled();
    }
}
```

### 11.3 使用示例

**Windows端使用示例**:
```python
# 凭证删除
def delete_voucher(voucher_id: int):
    if ConfirmationManager.show_confirmation(self, 'voucher:delete'):
        result = VoucherService.delete_voucher(voucher_id)
        if result.success:
            self.show_message("凭证删除成功")
            self.refresh_voucher_list()
        else:
            self.show_error(result.message)

# 凭证修改（自动保存）
def update_voucher(voucher_id: int, data: dict):
    result = AutoSaveManager.auto_save(
        'voucher:update_draft',
        data,
        lambda d: VoucherService.update_voucher(voucher_id, d)
    )
    if result.success:
        self.show_message("保存成功")
    else:
        self.show_error(result.message)
```

**Android端使用示例**:
```java
// 凭证删除
public void deleteVoucher(int voucherId) {
    ConfirmationManager.showConfirmation(
        this,
        "voucher:delete",
        new ConfirmationManager.OnConfirmationListener() {
            @Override
            public void onConfirmed() {
                voucherService.deleteVoucher(voucherId)
                    .subscribe(result -> {
                        if (result.isSuccess()) {
                            showMessage("凭证删除成功");
                            refreshVoucherList();
                        } else {
                            showError(result.getMessage());
                        }
                    });
            }

            @Override
            public void onCancelled() {
                // 用户取消操作
            }
        }
    );
}

// 凭证修改（自动保存）
public void updateVoucher(int voucherId, VoucherUpdate data) {
    AutoSaveManager.autoSave(
        "voucher:update_draft",
        data,
        d -> voucherService.updateVoucher(voucherId, d).blockingGet()
    );
}
```

## 12. 附录

### 12.1 技术参考文档

**Python相关**:
- Python官方文档: https://docs.python.org/3.9/
- PyQt6文档: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- SQLAlchemy文档: https://docs.sqlalchemy.org/en/2.0/

**Android相关**:
- Android官方文档: https://developer.android.com/
- Room文档: https://developer.android.com/training/data-storage/room
- Retrofit文档: https://square.github.io/retrofit/

**会计相关**:
- 企业会计准则: http://www.mof.gov.cn/
- 会计基础工作规范

### 12.2 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
|-----|------|---------|--------|
| v1.0 | 2026-04-19 | 初始版本 | CodeArts Agent |
