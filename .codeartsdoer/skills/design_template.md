# 技术设计文档模板

## 文档信息
- **项目名称**: [项目名称]
- **文档版本**: v1.0
- **创建日期**: [日期]
- **最后更新**: [日期]
- **文档状态**: 草稿/评审中/已批准
- **对应需求版本**: v1.0

## 1. 系统架构

### 1.1 架构概述
[描述整体架构设计思路和原则]

### 1.2 架构层次图
```
┌─────────────────────────────────────────┐
│           表示层 (Presentation)          │
│  Windows Client    │    Android Client  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         业务逻辑层 (Business Logic)       │
│   会计核心  │  报表引擎  │  权限管理      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         数据访问层 (Data Access)          │
│      ORM  │  数据验证  │  缓存管理       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         基硎设施层 (Infrastructure)       │
│   数据库  │  日志  │  配置  │  网络      │
└─────────────────────────────────────────┘
```

### 1.3 组件交互图
[描述主要组件之间的交互关系]

## 2. 技术选型

### 2.1 Windows端技术栈

| 技术领域 | 技术选型 | 版本 | 选型理由 |
|---------|---------|------|---------|
| 编程语言 | Python | 3.9+ | 跨平台、丰富的库支持 |
| GUI框架 | PyQt/PySide | 6.x | 成熟的跨平台GUI框架 |
| ORM框架 | SQLAlchemy | 2.x | 强大的ORM和SQL工具 |
| 数据库 | SQLite/PostgreSQL | - | 轻量级/企业级选择 |
| 日志框架 | logging | 内置 | Python标准库 |
| 配置管理 | PyYAML | 6.x | YAML配置文件支持 |

### 2.2 Android端技术栈

| 技术领域 | 技术选型 | 版本 | 选型理由 |
|---------|---------|------|---------|
| 编程语言 | Java | 11+ | Android官方支持语言 |
| UI框架 | Android SDK | - | Android原生开发 |
| 网络框架 | Retrofit | 2.x | RESTful API客户端 |
| 数据库 | Room | 2.x | Android官方ORM |
| 依赖注入 | Dagger2/Hilt | - | 依赖注入框架 |
| 日志框架 | Timber | 5.x | 轻量级日志框架 |

### 2.3 共享技术

| 技术领域 | 技术选型 | 说明 |
|---------|---------|------|
| 数据格式 | JSON | 跨平台数据交换格式 |
| 加密算法 | AES-256 | 数据加密标准 |
| 哈希算法 | SHA-256 | 密码哈希算法 |
| API协议 | RESTful | 统一API设计规范 |

## 3. 数据模型设计

### 3.1 实体关系图 (ER图)
```
┌──────────────┐       ┌──────────────┐
│   用户(User)   │       │  角色(Role)   │
├──────────────┤       ├──────────────┤
│ id (PK)       │       │ id (PK)       │
│ username      │       │ name          │
│ password_hash │       │ permissions   │
│ role_id (FK)  │──────→│ created_at    │
│ created_at    │       └──────────────┘
└──────────────┘

┌──────────────┐       ┌──────────────┐
│  科目(Account) │       │ 凭证(Voucher)  │
├──────────────┤       ├──────────────┤
│ id (PK)       │       │ id (PK)       │
│ code          │       │ number        │
│ name          │       │ date          │
│ type          │       │ creator_id(FK)│
│ parent_id(FK) │──────→│ status        │
│ balance       │       │ created_at    │
└──────────────┘       └──────────────┘
                              ↓
                       ┌──────────────┐
                       │凭证明细(Detail)│
                       ├──────────────┤
                       │ id (PK)       │
                       │ voucher_id(FK)│
                       │ account_id(FK)│
                       │ debit         │
                       │ credit        │
                       │ summary       │
                       └──────────────┘
```

### 3.2 核心数据表设计

#### 用户表 (users)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 主键 |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希 |
| role_id | INTEGER | FOREIGN KEY | 角色ID |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | | 更新时间 |

#### 会计科目表 (accounts)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 主键 |
| code | VARCHAR(20) | UNIQUE, NOT NULL | 科目编码 |
| name | VARCHAR(100) | NOT NULL | 科目名称 |
| type | VARCHAR(20) | NOT NULL | 科目类型 |
| parent_id | INTEGER | FOREIGN KEY | 父科目ID |
| level | INTEGER | NOT NULL | 科目级别 |
| balance | DECIMAL(18,2) | DEFAULT 0 | 余额 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |

#### 凭证表 (vouchers)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 主键 |
| number | VARCHAR(20) | UNIQUE, NOT NULL | 凭证号 |
| date | DATE | NOT NULL | 凭证日期 |
| period | VARCHAR(7) | NOT NULL | 会计期间 |
| creator_id | INTEGER | FOREIGN KEY | 制单人ID |
| reviewer_id | INTEGER | FOREIGN KEY | 审核人ID |
| status | VARCHAR(20) | NOT NULL | 状态 |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |

### 3.3 数据字典
[详细的数据字段说明和业务规则]

## 4. 接口设计

### 4.1 内部接口 (Internal API)

#### 业务逻辑层接口
```python
# 会计科目服务接口
class AccountService:
    def create_account(account: Account) -> Result
    def update_account(account_id: int, data: dict) -> Result
    def delete_account(account_id: int) -> Result
    def get_account_tree() -> List[Account]
    def get_account_balance(account_id: int) -> Decimal

# 凭证服务接口
class VoucherService:
    def create_voucher(voucher: Voucher) -> Result
    def submit_voucher(voucher_id: int) -> Result
    def review_voucher(voucher_id: int, approved: bool) -> Result
    def get_voucher_by_id(voucher_id: int) -> Voucher
    def query_vouchers(criteria: QueryCriteria) -> List[Voucher]
```

### 4.2 外部接口 (External API)

#### RESTful API设计
```
基础路径: /api/v1

用户管理:
POST   /users/login              # 用户登录
POST   /users/logout             # 用户登出
GET    /users/profile            # 获取用户信息

科目管理:
GET    /accounts                 # 获取科目列表
GET    /accounts/{id}            # 获取科目详情
POST   /accounts                 # 创建科目
PUT    /accounts/{id}            # 更新科目
DELETE /accounts/{id}            # 删除科目

凭证管理:
GET    /vouchers                 # 查询凭证
GET    /vouchers/{id}            # 获取凭证详情
POST   /vouchers                 # 创建凭证
PUT    /vouchers/{id}            # 更新凭证
POST   /vouchers/{id}/submit     # 提交凭证
POST   /vouchers/{id}/review     # 审核凭证
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
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### 错误响应格式
```json
{
  "code": 400,
  "message": "错误描述",
  "errors": [
    {
      "field": "字段名",
      "message": "错误详情"
    }
  ],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 5. 安全设计

### 5.1 认证机制
- JWT Token认证
- Token有效期: 2小时
- 刷新Token有效期: 7天
- 登录失败锁定策略

### 5.2 权限控制
- 基于角色的访问控制 (RBAC)
- 权限粒度: 功能级 + 数据级
- 操作审计日志

### 5.3 数据安全
- 敏感字段加密存储
- 传输层TLS加密
- SQL注入防护
- XSS攻击防护

## 6. 性能设计

### 6.1 性能指标
| 操作类型 | 响应时间要求 | 并发数 |
|---------|-------------|--------|
| 简单查询 | < 500ms | 100 |
| 复杂报表 | < 5s | 10 |
| 数据提交 | < 1s | 50 |
| 批量导入 | < 30s | 5 |

### 6.2 优化策略
- 数据库索引优化
- 查询语句优化
- 缓存策略
- 异步处理

## 7. 异常处理设计

### 7.1 异常分类
- 业务异常: 可预期的业务错误
- 系统异常: 技术层面的错误
- 网络异常: 通信相关错误

### 7.2 异常处理流程
```
异常发生 → 异常捕获 → 异常分类 → 
错误日志记录 → 用户提示 → 异常恢复/终止
```

### 7.3 错误码规范
| 错误码范围 | 错误类型 |
|-----------|---------|
| 1000-1999 | 用户相关错误 |
| 2000-2999 | 科目相关错误 |
| 3000-3999 | 凭证相关错误 |
| 4000-4999 | 系统相关错误 |
| 5000-5999 | 网络相关错误 |

## 8. 部署架构

### 8.1 Windows端部署
```
安装包结构:
├── accounting_system.exe      # 主程序
├── config/                    # 配置文件
│   ├── app.yaml              # 应用配置
│   └── database.yaml         # 数据库配置
├── data/                      # 数据目录
│   └── database.db           # SQLite数据库
├── logs/                      # 日志目录
└── resources/                 # 资源文件
```

### 8.2 Android端部署
```
APK结构:
├── app/                       # 应用模块
├── data/                      # 本地数据
├── libs/                      # 依赖库
└── res/                       # 资源文件
```

## 9. 测试策略

### 9.1 测试层次
- 单元测试: 覆盖率 > 80%
- 集成测试: 关键业务流程
- 系统测试: 端到端测试
- 性能测试: 并发和压力测试

### 9.2 测试工具
- Python: pytest, unittest
- Java: JUnit, Espresso
- API测试: Postman
- 性能测试: JMeter

## 10. 技术风险与应对

### 10.1 风险识别
| 风险项 | 影响程度 | 发生概率 | 应对措施 |
|--------|---------|---------|---------|
| 数据一致性 | 高 | 中 | 事务管理、数据校验 |
| 并发冲突 | 中 | 中 | 乐观锁、悲观锁 |
| 网络中断 | 中 | 低 | 离线模式、数据同步 |
| 性能瓶颈 | 中 | 低 | 缓存、异步处理 |

## 11. 附录

### 11.1 技术参考文档
[列出技术文档链接]

### 11.2 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
|-----|------|---------|--------|
| v1.0 | [日期] | 初始版本 | [姓名] |
