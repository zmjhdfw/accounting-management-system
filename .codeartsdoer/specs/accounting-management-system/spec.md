# 需求规格文档 - 会计管理系统

## 文档信息
- **项目名称**: 会计管理系统 (Accounting Management System)
- **文档版本**: v1.0
- **创建日期**: 2026-04-19
- **最后更新**: 2026-04-19
- **文档状态**: 草稿

## 1. 项目概述

### 1.1 项目背景
随着企业财务管理的规范化要求日益提高，传统手工记账方式已无法满足现代企业对财务数据准确性、实时性和可追溯性的需求。本项目旨在开发一套跨平台的会计管理系统，支持Windows桌面端和Android移动端，为企业提供便捷、高效的会计核算工具。

### 1.2 项目目标
- 提供完整的会计核算功能，包括科目管理、凭证管理、账簿查询、报表生成等
- 实现跨平台数据同步，支持Windows和Android双端使用
- 确保财务数据的准确性、安全性和可追溯性
- 提供友好的用户界面和流畅的操作体验
- 支持普通操作自动提交、重要操作需确认的交互模式

### 1.3 系统范围
**包含范围**:
- 用户管理与权限控制
- 会计科目管理
- 凭证录入与管理
- 账簿查询
- 财务报表生成
- 数据备份与恢复
- 操作日志审计

**排除范围**:
- 固定资产管理
- 成本核算
- 预算管理
- 多币种核算
- 在线支付集成

### 1.4 目标用户
- 企业会计人员：日常账务处理、凭证录入、报表生成
- 财务主管：账务审核、财务分析
- 企业管理者：查看财务报表、了解财务状况
- 系统管理员：用户管理、权限配置、系统维护

## 2. 功能需求

### 2.1 用户管理与权限控制

#### 2.1.1 功能描述
提供用户注册、登录、权限管理等功能，确保系统安全性和操作可追溯性。

#### 2.1.2 需求列表

**REQ-USER-001** [P0]
When a user attempts to log in, the accounting system shall:
- Validate the username and password
- Check the user account status (active/inactive)
- Generate a session token upon successful authentication
- Record the login timestamp and IP address

**验收标准**:
- [ ] 正确的用户名和密码可以成功登录
- [ ] 错误的凭证显示明确的错误提示
- [ ] 连续5次登录失败后账户锁定30分钟
- [ ] 登录成功后生成有效的会话令牌
- [ ] 登录记录保存到审计日志

**REQ-USER-002** [P0]
The accounting system shall support role-based access control (RBAC) with the following roles:
- Administrator: full system access
- Accountant: voucher entry and modification
- Reviewer: voucher review and approval
- Viewer: read-only access to reports

**验收标准**:
- [ ] 系统支持至少4种预定义角色
- [ ] 不同角色具有不同的权限集合
- [ ] 用户可以被分配一个或多个角色
- [ ] 权限变更立即生效

**REQ-USER-003** [P1]
When a user performs a critical operation, the accounting system shall:
- Prompt the user for confirmation
- Log the operation details including user ID, timestamp, and operation type
- Require re-authentication for sensitive operations

**验收标准**:
- [ ] 删除操作弹出确认对话框
- [ ] 审核操作需要确认
- [ ] 所有操作记录到审计日志
- [ ] 敏感操作需要重新验证密码

### 2.2 会计科目管理

#### 2.2.1 功能描述
支持会计科目的增删改查，维护科目体系的层次结构，支持科目余额查询。

#### 2.2.2 需求列表

**REQ-ACCT-001** [P0]
When a user creates a new accounting account, the accounting system shall:
- Validate the account code format (numeric, unique)
- Validate the account name (non-empty, unique within parent)
- Verify the parent account exists if specified
- Set the account level based on parent hierarchy
- Save the account to the database

**验收标准**:
- [ ] 科目编码必须唯一
- [ ] 科目名称不能为空
- [ ] 父科目必须存在
- [ ] 科目级别自动计算
- [ ] 科目创建后立即保存到数据库

**REQ-ACCT-002** [P0]
The accounting system shall support the following account types:
- Asset (资产)
- Liability (负债)
- Equity (所有者权益)
- Revenue (收入)
- Expense (费用)

**验收标准**:
- [ ] 系统支持5种基本科目类型
- [ ] 每种类型有正确的借贷方向
- [ ] 科目类型不能被修改

**REQ-ACCT-003** [P1]
When a user modifies an existing account, the accounting system shall:
- Validate the modification does not violate accounting rules
- Check if the account has been used in vouchers
- Prompt for confirmation if the account has transactions
- Update the account and log the modification

**验收标准**:
- [ ] 已使用的科目可以修改名称
- [ ] 已使用的科目不能修改编码
- [ ] 有余额的科目不能删除
- [ ] 修改操作记录到审计日志

**REQ-ACCT-004** [P1]
When a user queries the account tree, the accounting system shall:
- Retrieve all accounts in hierarchical structure
- Calculate the balance for each account
- Display the account tree in expandable/collapsible format
- Support filtering by account type

**验收标准**:
- [ ] 科目树正确显示层次关系
- [ ] 每个科目显示当前余额
- [ ] 支持展开/折叠操作
- [ ] 支持按类型筛选

### 2.3 凭证管理

#### 2.3.1 功能描述
支持凭证的录入、修改、删除、审核等操作，确保借贷平衡，维护凭证的连续性和完整性。

#### 2.3.2 需求列表

**REQ-VOUCH-001** [P0]
When a user creates a new voucher, the accounting system shall:
- Generate a sequential voucher number
- Validate the voucher date is within the current accounting period
- Validate each detail line has valid account and amount
- Verify the total debit equals total credit
- Save the voucher with "Draft" status

**验收标准**:
- [ ] 凭证号自动生成且连续
- [ ] 凭证日期必须在当前会计期间
- [ ] 每行必须有科目和金额
- [ ] 借贷必须平衡
- [ ] 新凭证状态为"草稿"

**REQ-VOUCH-002** [P0]
When a user submits a voucher for review, the accounting system shall:
- Validate the voucher is complete and balanced
- Change the voucher status to "Pending Review"
- Notify designated reviewers
- Lock the voucher from further editing

**验收标准**:
- [ ] 不平衡的凭证不能提交
- [ ] 提交后状态变为"待审核"
- [ ] 审核人员收到通知
- [ ] 提交后凭证不能修改

**REQ-VOUCH-003** [P0]
When a reviewer approves a voucher, the accounting system shall:
- Update the voucher status to "Approved"
- Update the account balances
- Record the reviewer ID and approval timestamp
- Make the voucher read-only

**验收标准**:
- [ ] 审核后状态变为"已审核"
- [ ] 科目余额正确更新
- [ ] 记录审核人和时间
- [ ] 审核后凭证不可修改

**REQ-VOUCH-004** [P1]
When a user modifies a draft voucher, the accounting system shall:
- Allow modification of all fields
- Automatically save changes without confirmation
- Maintain the voucher number
- Log the modification details

**验收标准**:
- [ ] 草稿凭证可以修改所有字段
- [ ] 修改自动保存
- [ ] 凭证号保持不变
- [ ] 修改记录到日志

**REQ-VOUCH-005** [P1]
When a user attempts to delete a voucher, the accounting system shall:
- Check the voucher status
- Prompt for confirmation if the voucher is in draft status
- Reject deletion if the voucher is approved
- Log the deletion operation

**验收标准**:
- [ ] 草稿凭证可以删除（需确认）
- [ ] 已审核凭证不能删除
- [ ] 删除前弹出确认对话框
- [ ] 删除操作记录到日志

### 2.4 账簿查询

#### 2.4.1 功能描述
提供总账、明细账、余额表等账簿查询功能，支持多维度查询和导出。

#### 2.4.2 需求列表

**REQ-LEDGER-001** [P0]
When a user queries the general ledger, the accounting system shall:
- Retrieve all vouchers for the specified account
- Calculate running balance for each transaction
- Display in chronological order
- Support date range filtering

**验收标准**:
- [ ] 正确显示指定科目的所有凭证
- [ ] 每笔交易显示累计余额
- [ ] 按日期顺序排列
- [ ] 支持日期范围筛选

**REQ-LEDGER-002** [P0]
When a user queries the subsidiary ledger, the accounting system shall:
- Retrieve detailed voucher information
- Display account, summary, debit, credit, and balance
- Support filtering by voucher number or summary
- Allow drill-down to original voucher

**验收标准**:
- [ ] 显示凭证详细信息
- [ ] 包含科目、摘要、借贷方、余额
- [ ] 支持凭证号和摘要搜索
- [ ] 可以查看原始凭证

**REQ-LEDGER-003** [P1]
When a user queries the trial balance, the accounting system shall:
- Calculate the balance for all accounts
- Verify total debits equal total credits
- Display accounts with non-zero balance
- Support export to Excel

**验收标准**:
- [ ] 显示所有科目的余额
- [ ] 借贷方合计相等
- [ ] 只显示有余额的科目
- [ ] 支持导出Excel格式

### 2.5 财务报表

#### 2.5.1 功能描述
生成资产负债表、利润表等标准财务报表，支持自定义报表模板。

#### 2.5.2 需求列表

**REQ-REPORT-001** [P0]
When a user generates a balance sheet, the accounting system shall:
- Calculate total assets from asset accounts
- Calculate total liabilities from liability accounts
- Calculate total equity from equity accounts
- Verify assets equal liabilities plus equity
- Display in standard balance sheet format

**验收标准**:
- [ ] 正确计算资产总额
- [ ] 正确计算负债总额
- [ ] 正确计算所有者权益
- [ ] 资产=负债+所有者权益
- [ ] 符合资产负债表格式

**REQ-REPORT-002** [P0]
When a user generates an income statement, the accounting system shall:
- Calculate total revenue from revenue accounts
- Calculate total expenses from expense accounts
- Calculate net income (revenue - expenses)
- Display in standard income statement format

**验收标准**:
- [ ] 正确计算收入总额
- [ ] 正确计算费用总额
- [ ] 正确计算净利润
- [ ] 符合利润表格式

**REQ-REPORT-003** [P1]
When a user exports a report, the accounting system shall:
- Support export to PDF format
- Support export to Excel format
- Include report title, period, and generation timestamp
- Maintain formatting and layout

**验收标准**:
- [ ] 支持PDF导出
- [ ] 支持Excel导出
- [ ] 包含报表标题和期间
- [ ] 格式保持一致

### 2.6 数据管理

#### 2.6.1 功能描述
提供数据备份、恢复、导入导出功能，确保数据安全。

#### 2.6.2 需求列表

**REQ-DATA-001** [P0]
When a user performs a data backup, the accounting system shall:
- Export all data to a compressed file
- Include database schema and data
- Encrypt the backup file with user-provided password
- Record the backup timestamp and file location

**验收标准**:
- [ ] 备份文件包含所有数据
- [ ] 备份文件已加密
- [ ] 记录备份时间和位置
- [ ] 备份文件可以恢复

**REQ-DATA-002** [P0]
When a user restores data from backup, the accounting system shall:
- Prompt for confirmation before overwriting existing data
- Validate the backup file integrity
- Decrypt the backup file with user-provided password
- Restore all data to the database

**验收标准**:
- [ ] 恢复前弹出确认对话框
- [ ] 验证备份文件完整性
- [ ] 正确解密备份文件
- [ ] 数据完整恢复

**REQ-DATA-003** [P1]
When a user imports voucher data, the accounting system shall:
- Validate the import file format (CSV/Excel)
- Validate each voucher for completeness and balance
- Prompt for confirmation before importing
- Log the import operation

**验收标准**:
- [ ] 支持CSV和Excel格式
- [ ] 验证凭证完整性和平衡性
- [ ] 导入前需确认
- [ ] 记录导入操作

### 2.7 操作确认机制

#### 2.7.1 功能描述
实现普通操作自动提交、重要操作需确认的交互机制。

#### 2.7.2 需求列表

**REQ-CONFIRM-001** [P0]
The accounting system shall automatically save the following operations without user confirmation:
- Creating a new draft voucher
- Modifying a draft voucher
- Creating a new account
- Modifying account properties (name, notes)
- Querying data

**验收标准**:
- [ ] 草稿凭证创建自动保存
- [ ] 草稿凭证修改自动保存
- [ ] 科目创建自动保存
- [ ] 科目属性修改自动保存
- [ ] 查询操作无需确认

**REQ-CONFIRM-002** [P0]
The accounting system shall require user confirmation for the following operations:
- Deleting a voucher
- Deleting an account
- Submitting a voucher for review
- Approving or rejecting a voucher
- Restoring data from backup
- Importing voucher data

**验收标准**:
- [ ] 删除凭证需确认
- [ ] 删除科目需确认
- [ ] 提交凭证需确认
- [ ] 审核凭证需确认
- [ ] 恢复数据需确认
- [ ] 导入数据需确认

**REQ-CONFIRM-003** [P1]
When prompting for confirmation, the accounting system shall:
- Display a clear message describing the operation
- Provide "Confirm" and "Cancel" buttons
- Allow keyboard shortcuts (Enter for confirm, Esc for cancel)
- Log the user's decision

**验收标准**:
- [ ] 显示操作描述信息
- [ ] 提供确认和取消按钮
- [ ] 支持快捷键操作
- [ ] 记录用户选择

## 3. 非功能需求

### 3.1 性能需求

**REQ-PERF-001** [P1]
The accounting system shall process at least 100 voucher entries per minute under normal operating conditions.

**验收标准**:
- [ ] 系统支持每分钟至少100笔凭证录入
- [ ] 单笔凭证保存时间 < 500ms
- [ ] 报表生成时间 < 10秒

**REQ-PERF-002** [P1]
The accounting system shall support concurrent access by at least 20 users without significant performance degradation.

**验收标准**:
- [ ] 支持20个用户同时在线
- [ ] 并发操作响应时间增加 < 50%
- [ ] 无数据冲突或丢失

### 3.2 安全性需求

**REQ-SEC-001** [P0]
The accounting system shall encrypt all user passwords using SHA-256 hashing algorithm with salt.

**验收标准**:
- [ ] 密码使用SHA-256加密
- [ ] 每个密码使用唯一盐值
- [ ] 数据库不存储明文密码

**REQ-SEC-002** [P0]
The accounting system shall maintain audit logs for all data modification operations including:
- User login/logout
- Voucher creation, modification, deletion
- Account creation, modification, deletion
- Data backup and restore

**验收标准**:
- [ ] 记录所有登录登出操作
- [ ] 记录所有凭证操作
- [ ] 记录所有科目操作
- [ ] 记录数据备份恢复操作
- [ ] 日志不可篡改

**REQ-SEC-003** [P1]
The accounting system shall prevent SQL injection, XSS, and other common security vulnerabilities.

**验收标准**:
- [ ] 所有输入参数经过验证
- [ ] 使用参数化查询
- [ ] 输出内容经过转义
- [ ] 通过安全扫描测试

### 3.3 可用性需求

**REQ-USA-001** [P1]
The accounting system shall provide user-friendly error messages that clearly describe the problem and suggest solutions.

**验收标准**:
- [ ] 错误信息清晰易懂
- [ ] 提供解决建议
- [ ] 不显示技术细节给普通用户

**REQ-USA-002** [P1]
The accounting system shall support keyboard shortcuts for common operations to improve efficiency.

**验收标准**:
- [ ] 支持常用快捷键
- [ ] 快捷键可自定义
- [ ] 提供快捷键帮助文档

### 3.4 兼容性需求

**REQ-COMP-001** [P0]
The Windows client shall run on Windows 10 and Windows 11 operating systems.

**验收标准**:
- [ ] 在Windows 10上正常运行
- [ ] 在Windows 11上正常运行
- [ ] 功能完整无缺失

**REQ-COMP-002** [P0]
The Android client shall run on Android 8.0 (API level 26) and above.

**验收标准**:
- [ ] 在Android 8.0上正常运行
- [ ] 在最新Android版本上正常运行
- [ ] 适配不同屏幕尺寸

**REQ-COMP-003** [P1]
The accounting system shall maintain data consistency between Windows and Android clients.

**验收标准**:
- [ ] 双端数据实时同步
- [ ] 冲突自动解决
- [ ] 数据一致性验证通过

## 4. 约束条件

### 4.1 技术约束
- Windows端必须使用Python 3.9或更高版本开发
- Android端必须使用Java开发
- 数据库必须支持ACID事务
- 系统必须支持离线操作（Android端）

### 4.2 业务约束
- 凭证日期不能早于系统启用日期
- 已审核的凭证不能修改或删除
- 会计期间关闭后不能录入新凭证
- 科目余额必须符合借贷记账规则

### 4.3 法规约束
- 系统必须符合《企业会计准则》要求
- 财务报表格式必须符合国家统一会计制度
- 数据保存期限不少于10年
- 必须支持税务检查数据导出

## 5. 数据需求

### 5.1 数据实体

**用户 (User)**
- id: 用户ID (主键)
- username: 用户名 (唯一)
- password_hash: 密码哈希
- role_id: 角色ID (外键)
- created_at: 创建时间
- updated_at: 更新时间

**角色 (Role)**
- id: 角色ID (主键)
- name: 角色名称
- permissions: 权限列表

**会计科目 (Account)**
- id: 科目ID (主键)
- code: 科目编码 (唯一)
- name: 科目名称
- type: 科目类型
- parent_id: 父科目ID (外键)
- level: 科目级别
- balance: 当前余额
- is_active: 是否启用

**凭证 (Voucher)**
- id: 凭证ID (主键)
- number: 凭证号 (唯一)
- date: 凭证日期
- period: 会计期间
- creator_id: 制单人ID (外键)
- reviewer_id: 审核人ID (外键)
- status: 凭证状态
- created_at: 创建时间

**凭证明细 (VoucherDetail)**
- id: 明细ID (主键)
- voucher_id: 凭证ID (外键)
- account_id: 科目ID (外键)
- debit: 借方金额
- credit: 贷方金额
- summary: 摘要

**审计日志 (AuditLog)**
- id: 日志ID (主键)
- user_id: 用户ID (外键)
- operation: 操作类型
- target_type: 目标类型
- target_id: 目标ID
- details: 操作详情
- timestamp: 时间戳

### 5.2 数据关系
- 用户与角色：多对一关系
- 科目与父科目：自引用关系
- 凭证与用户：多对一关系（制单人、审核人）
- 凭证与凭证明细：一对多关系
- 凭证明细与科目：多对一关系

### 5.3 数据存储
- Windows端：SQLite本地数据库
- Android端：SQLite本地数据库
- 数据同步：通过RESTful API
- 备份格式：加密的ZIP文件

## 6. 接口需求

### 6.1 用户界面

**Windows端**:
- 使用PyQt/PySide框架
- 支持多窗口和标签页
- 提供菜单栏、工具栏、状态栏
- 支持表格、树形视图、图表

**Android端**:
- 遵循Material Design设计规范
- 支持手势操作
- 适配不同屏幕尺寸
- 提供离线操作界面

### 6.2 系统接口
- 支持数据导入导出（CSV、Excel）
- 支持报表导出（PDF、Excel）
- 支持打印功能
- 支持邮件发送报表

### 6.3 API接口

**认证接口**:
- POST /api/v1/auth/login - 用户登录
- POST /api/v1/auth/logout - 用户登出
- GET /api/v1/auth/profile - 获取用户信息

**科目接口**:
- GET /api/v1/accounts - 获取科目列表
- GET /api/v1/accounts/{id} - 获取科目详情
- POST /api/v1/accounts - 创建科目
- PUT /api/v1/accounts/{id} - 更新科目
- DELETE /api/v1/accounts/{id} - 删除科目

**凭证接口**:
- GET /api/v1/vouchers - 查询凭证
- GET /api/v1/vouchers/{id} - 获取凭证详情
- POST /api/v1/vouchers - 创建凭证
- PUT /api/v1/vouchers/{id} - 更新凭证
- DELETE /api/v1/vouchers/{id} - 删除凭证
- POST /api/v1/vouchers/{id}/submit - 提交凭证
- POST /api/v1/vouchers/{id}/review - 审核凭证

**报表接口**:
- GET /api/v1/reports/balance-sheet - 资产负债表
- GET /api/v1/reports/income-statement - 利润表
- GET /api/v1/reports/trial-balance - 试算平衡表

## 7. 需求追踪矩阵

| 需求编号 | 需求描述 | 优先级 | 状态 | 备注 |
|---------|---------|--------|------|------|
| REQ-USER-001 | 用户登录验证 | P0 | 待开发 | |
| REQ-USER-002 | 角色权限控制 | P0 | 待开发 | |
| REQ-USER-003 | 关键操作确认 | P1 | 待开发 | |
| REQ-ACCT-001 | 创建会计科目 | P0 | 待开发 | |
| REQ-ACCT-002 | 科目类型支持 | P0 | 待开发 | |
| REQ-ACCT-003 | 修改会计科目 | P1 | 待开发 | |
| REQ-ACCT-004 | 查询科目树 | P1 | 待开发 | |
| REQ-VOUCH-001 | 创建凭证 | P0 | 待开发 | |
| REQ-VOUCH-002 | 提交凭证审核 | P0 | 待开发 | |
| REQ-VOUCH-003 | 审核凭证 | P0 | 待开发 | |
| REQ-VOUCH-004 | 修改草稿凭证 | P1 | 待开发 | |
| REQ-VOUCH-005 | 删除凭证 | P1 | 待开发 | |
| REQ-LEDGER-001 | 查询总账 | P0 | 待开发 | |
| REQ-LEDGER-002 | 查询明细账 | P0 | 待开发 | |
| REQ-LEDGER-003 | 查询试算平衡表 | P1 | 待开发 | |
| REQ-REPORT-001 | 生成资产负债表 | P0 | 待开发 | |
| REQ-REPORT-002 | 生成利润表 | P0 | 待开发 | |
| REQ-REPORT-003 | 导出报表 | P1 | 待开发 | |
| REQ-DATA-001 | 数据备份 | P0 | 待开发 | |
| REQ-DATA-002 | 数据恢复 | P0 | 待开发 | |
| REQ-DATA-003 | 数据导入 | P1 | 待开发 | |
| REQ-CONFIRM-001 | 自动保存操作 | P0 | 待开发 | |
| REQ-CONFIRM-002 | 需确认操作 | P0 | 待开发 | |
| REQ-CONFIRM-003 | 确认对话框 | P1 | 待开发 | |

## 8. 术语表

| 术语 | 定义 |
|-----|------|
| 凭证 | 记录经济业务的会计凭证，包含借贷方科目和金额 |
| 科目 | 会计科目，用于分类记录经济业务 |
| 借贷平衡 | 每笔凭证的借方金额合计等于贷方金额合计 |
| 会计期间 | 会计核算的时间范围，通常为月度或年度 |
| 草稿 | 凭证的初始状态，可以修改和删除 |
| 待审核 | 凭证已提交，等待审核人员审核 |
| 已审核 | 凭证已通过审核，不可修改 |
| 总账 | 按科目汇总的账簿 |
| 明细账 | 按凭证逐笔记录的账簿 |
| 试算平衡表 | 检验借贷是否平衡的报表 |
| 资产负债表 | 反映企业财务状况的报表 |
| 利润表 | 反映企业经营成果的报表 |

## 9. 附录

### 9.1 参考文档
- 《企业会计准则》
- 《会计基础工作规范》
- 《企业会计信息化工作规范》
- EARS需求编写规范

### 9.2 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
|-----|------|---------|--------|
| v1.0 | 2026-04-19 | 初始版本 | CodeArts Agent |
