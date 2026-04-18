# EARS格式规范

## 概述
EARS (Easy Approach to Requirements Syntax) 是一种简化的需求语法方法，用于编写清晰、可测试的需求。

## EARS模式类型

### 1. 普遍性需求 (Ubiquitous)
**格式**: `The <system> shall <functionality>`

**说明**: 系统在所有情况下都必须满足的需求

**示例**:
- The accounting system shall validate all financial transactions before processing
- The system shall maintain audit logs for all user operations

### 2. 事件驱动需求 (Event-Driven)
**格式**: `When <trigger>, the <system> shall <response>`

**说明**: 当特定事件发生时，系统必须执行响应

**示例**:
- When a user submits a transaction, the system shall validate the transaction data
- When an important modification is requested, the system shall prompt for user confirmation

### 3. 状态驱动需求 (State-Driven)
**格式**: `While <state>, the <system> shall <functionality>`

**说明**: 在特定状态下，系统必须满足的功能

**示例**:
- While the system is in audit mode, the system shall log all data modifications
- While a transaction is pending approval, the system shall restrict further modifications

### 4. 可选功能需求 (Optional Feature)
**格式**: `Where <feature> is included, the <system> shall <functionality>`

**说明**: 当特定功能被包含时，系统必须满足的需求

**示例**:
- Where the multi-currency feature is included, the system shall support currency conversion
- Where the reporting module is included, the system shall generate financial statements

### 5. 异常处理需求 (Exception)
**格式**: `If <condition>, then the <system> shall <response>`

**说明**: 在异常或错误条件下，系统必须执行的响应

**示例**:
- If a transaction validation fails, then the system shall reject the transaction and notify the user
- If the database connection fails, then the system shall display an error message and retry connection

## 验收标准编写规则

### 结构要求
1. 每个需求必须使用上述五种EARS模式之一
2. 需求描述必须清晰、具体、可测试
3. 避免使用模糊词汇（如"适当"、"合理"、"等"）
4. 使用主动语态，明确系统行为

### 测试性要求
1. 每个需求必须能够通过测试验证
2. 明确输入条件和预期输出
3. 定义可测量的成功标准
4. 考虑边界条件和异常情况

### 层次结构
1. **功能需求**: 描述系统必须提供的功能
2. **非功能需求**: 描述系统的质量属性（性能、安全性、可用性等）
3. **约束需求**: 描述系统的限制条件

## 需求编号规范
- 格式: `REQ-[模块]-[序号]`
- 示例: `REQ-TRANS-001`, `REQ-REPORT-005`

## 需求优先级
- **P0**: 核心功能，必须实现
- **P1**: 重要功能，应当实现
- **P2**: 辅助功能，可选实现
- **P3**: 增强功能，未来考虑

## 示例模板

### 功能需求示例
```
**REQ-TRANS-001** [P0]
When a user creates a new transaction, the accounting system shall:
- Validate the transaction date is within the current accounting period
- Verify the debit and credit amounts are balanced
- Generate a unique transaction ID
- Save the transaction to the database
```

### 非功能需求示例
```
**REQ-PERF-001** [P1]
The accounting system shall process at least 1000 transactions per minute under normal operating conditions.
```

### 异常处理示例
```
**REQ-ERR-001** [P0]
If a database connection fails during transaction processing, then the system shall:
- Display an error message to the user
- Save the transaction to a local queue
- Automatically retry the connection every 30 seconds
- Process queued transactions when connection is restored
```
