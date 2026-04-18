# 会计管理系统 (Accounting Management System)

一个基于Python和Java开发的跨平台会计管理系统，包含Windows桌面端和Android移动端。

## 项目简介

本系统是一个完整的会计管理解决方案，提供科目管理、凭证管理、报表查询等核心会计功能。系统采用分层架构设计，支持普通操作自动提交、重要操作需确认的交互机制。

## 功能特性

### 核心功能
- **用户系统**: 用户注册、登录、资料编辑、修改密码、注销账户
- **科目管理**: 支持多级科目树结构，科目余额自动计算，增删改查完整功能
- **凭证管理**: 凭证录入、修改、删除、审核全流程管理
- **报表查询**: 科目余额表、资产负债表、利润表等财务报表
- **用户管理**: 用户认证、角色授权、权限控制
- **审计日志**: 完整的操作审计记录

### 特色功能
- **智能交互**: 普通操作自动保存，重要操作需确认
- **数据安全**: 密码加密存储，敏感信息脱敏
- **跨平台**: Windows桌面端 + Android移动端
- **无默认账户**: 首次使用需注册账户

## 技术架构

### Windows端 (Python)
- **UI框架**: PyQt6
- **数据库**: SQLAlchemy + SQLite
- **架构**: 分层架构（UI层、业务逻辑层、数据访问层、基础设施层）

### Android端 (Java)
- **UI框架**: AndroidX + Material Design
- **数据存储**: SharedPreferences
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
├── models/                         # 数据模型
├── infrastructure/                 # 基础设施层
├── tests/                          # 测试
├── main.py                         # 主程序入口
└── requirements.txt                # 依赖包

accounting_system_android/          # Android端项目
└── app/
    └── src/main/
        ├── java/com/example/accounting/
        │   ├── ui/                 # 表示层
        │   │   ├── MainActivity.java
        │   │   ├── LoginActivity.java
        │   │   ├── AccountFragment.java
        │   │   ├── VoucherFragment.java
        │   │   └── ReportFragment.java
        │   └── data/               # 数据层
        │       ├── UserManager.java
        │       ├── AccountManager.java
        │       └── VoucherManager.java
        └── res/                    # 资源文件
```

## 安装与运行

### 快速开始（推荐）

**从GitHub Releases下载已构建的应用：**

1. 访问 [Releases页面](https://github.com/zmjhdfw/accounting-management-system/releases)
2. 下载最新版本的文件：
   - **Windows端**: `AccountingSystem.exe`
   - **Android端**: `app-release.apk`

### Windows端

**方式一：直接运行（推荐）**
1. 从Releases下载 `AccountingSystem.exe`
2. 双击运行即可
3. 首次使用需注册账户

**方式二：从源码运行**
```bash
cd accounting_system_windows
pip install -r requirements.txt
python main.py
```

### Android端

**方式一：安装APK（推荐）**
1. 从Releases下载 `app-release.apk`
2. 在手机上安装APK文件
3. 打开应用，首次使用需注册账户

**方式二：从源码构建**
1. 使用Android Studio打开 `accounting_system_android` 项目
2. 同步Gradle依赖
3. 运行到模拟器或真机

## 使用说明

### 用户系统
1. 首次使用需注册账户
2. 登录后可在用户菜单中：
   - 查看账户信息
   - 编辑资料（昵称、邮箱）
   - 修改密码
   - 注销账户
   - 退出登录

### 科目管理
1. 在主界面点击"科目"标签
2. 点击右上角"+"按钮添加科目
3. 填写科目编码、名称、类型、余额、方向
4. 点击科目可编辑，长按可删除

### 凭证管理
1. 在主界面点击"凭证"标签
2. 点击右上角"+"按钮创建凭证
3. 填写凭证号、日期、摘要、借贷方科目、金额
4. 点击凭证可编辑，长按可删除

### 报表查询
1. 在主界面点击"报表"标签
2. 选择报表类型：
   - 科目余额表
   - 资产负债表
   - 利润表
3. 点击"查询"生成报表

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

### v1.1.0 (2026-04-19)
- 添加用户注册登录系统
- 添加用户账户管理功能
- 完善报表功能（科目余额表、资产负债表、利润表）
- 移除默认admin账户
- Windows端同步Android端功能

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
