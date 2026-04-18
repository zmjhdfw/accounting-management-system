# 会计管理系统 (Accounting Management System)

一个基于Python和Java开发的跨平台会计管理系统，包含Windows桌面端和Android移动端。

## 项目简介

本系统是一个完整的会计管理解决方案，提供科目管理、凭证管理、报表查询等核心会计功能。系统采用分层架构设计，支持普通操作自动提交、重要操作需确认的交互机制。

## 功能特性

### 核心功能
- **科目管理**: 支持多级科目树结构，科目余额自动计算
- **凭证管理**: 凭证录入、修改、删除、审核全流程管理
- **报表查询**: 资产负债表、利润表、试算平衡表等财务报表
- **用户管理**: 用户认证、角色授权、权限控制
- **审计日志**: 完整的操作审计记录

### 特色功能
- **智能交互**: 普通操作自动保存，重要操作需确认
- **数据安全**: 密码加密存储，敏感信息脱敏
- **跨平台**: Windows桌面端 + Android移动端

## 技术架构

### Windows端 (Python)
- **UI框架**: PyQt6
- **数据库**: SQLAlchemy + SQLite
- **架构**: 分层架构（UI层、业务逻辑层、数据访问层、基础设施层）

### Android端 (Java)
- **UI框架**: AndroidX + Material Design
- **数据库**: Room
- **网络**: Retrofit
- **架构**: MVVM架构

## 项目结构

```
accounting_system_windows/          # Windows端项目
├── ui/                             # 表示层
│   ├── main_window.py             # 主窗口
│   ├── login_dialog.py            # 登录对话框
│   ├── account_view.py            # 科目管理视图
│   ├── voucher_view.py            # 凭证管理视图
│   └── report_view.py             # 报表查询视图
├── services/                       # 业务逻辑层
│   ├── auth_service.py            # 认证服务
│   ├── user_service.py            # 用户服务
│   ├── account_service.py         # 科目服务
│   ├── voucher_service.py         # 凭证服务
│   └── confirmation_service.py    # 操作确认机制
├── dao/                            # 数据访问层
│   ├── user_dao.py                # 用户DAO
│   ├── account_dao.py             # 科目DAO
│   ├── voucher_dao.py             # 凭证DAO
│   └── audit_log_dao.py           # 审计日志DAO
├── models/                         # 数据模型
│   ├── user.py                    # 用户模型
│   ├── account.py                 # 科目模型
│   ├── voucher.py                 # 凭证模型
│   └── audit_log.py               # 审计日志模型
├── infrastructure/                 # 基础设施层
│   ├── database.py                # 数据库管理
│   ├── logger.py                  # 日志管理
│   ├── config.py                  # 配置管理
│   └── cache.py                   # 缓存管理
├── config/                         # 配置文件
│   ├── app.yaml                   # 应用配置
│   ├── database.yaml              # 数据库配置
│   └── logging.yaml               # 日志配置
├── tests/                          # 测试
├── main.py                         # 主程序入口
└── requirements.txt                # 依赖包

accounting_system_android/          # Android端项目
└── app/
    └── src/main/
        ├── java/com/example/accounting/
        │   ├── ui/                 # 表示层
        │   ├── services/           # 业务逻辑层
        │   ├── data/               # 数据层
        │   ├── di/                 # 依赖注入
        │   └── utils/              # 工具类
        └── res/                    # 资源文件
```

## 安装与运行

### Windows端

1. **安装依赖**
```bash
cd accounting_system_windows
pip install -r requirements.txt
```

2. **运行程序**
```bash
python main.py
```

3. **默认登录**
- 用户名: `admin`
- 密码: `admin123`

### Android端

1. 使用Android Studio打开 `accounting_system_android` 项目
2. 同步Gradle依赖
3. 运行到模拟器或真机

## 使用说明

### 科目管理
1. 在主界面点击"科目管理"标签
2. 使用工具栏按钮新增、编辑、删除科目
3. 支持多级科目树结构
4. 右键菜单提供快捷操作

### 凭证管理
1. 在主界面点击"凭证管理"标签
2. 点击"新建凭证"创建新凭证
3. 填写凭证日期、摘要、科目、金额等信息
4. 系统自动检查借贷平衡
5. 提交凭证后可进行审核

### 报表查询
1. 在主界面点击"报表查询"标签
2. 选择报表类型和会计期间
3. 点击"查询"生成报表
4. 支持导出PDF和Excel格式

## 开发指南

### 代码规范
- 遵循PEP 8规范（Python）
- 遵循Google Java编程风格（Java）
- 使用有意义的变量名和函数名
- 编写必要的注释和文档字符串

### 测试
```bash
# 运行测试
pytest tests/

# 生成覆盖率报告
pytest --cov=. tests/
```

## 版本历史

### v1.0.0 (2026-04-19)
- 初始版本发布
- 实现核心会计功能
- Windows端基础UI完成
- Android端项目结构搭建

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或Pull Request。

---

**注意**: 本系统仅供学习和演示使用，不建议直接用于生产环境。生产使用前请进行充分测试和安全评估。
