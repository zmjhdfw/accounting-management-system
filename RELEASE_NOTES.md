# Release v1.0.0

## 会计管理系统 v1.0.0

### 🎉 首次发布

完整的跨平台会计管理系统，包含Windows桌面端和Android移动端。

### ✨ 功能特性

#### 核心功能
- **科目管理**: 多级科目树结构，科目余额自动计算
- **凭证管理**: 凭证录入、修改、删除、审核全流程管理
- **报表查询**: 资产负债表、利润表、试算平衡表等财务报表
- **用户管理**: 用户认证、角色授权、权限控制
- **审计日志**: 完整的操作审计记录

#### 特色功能
- **智能交互**: 普通操作自动保存，重要操作需确认
- **数据安全**: 密码加密存储，敏感信息脱敏
- **跨平台**: Windows桌面端 + Android移动端

### 📦 下载

#### Windows端
- 源码: `accounting_system_windows/`
- 依赖: Python 3.9+, PyQt6
- 安装: `pip install -r requirements.txt`
- 运行: `python main.py`
- 默认登录: admin / admin123

#### Android端
- 源码: `accounting_system_android/`
- 最低版本: Android 8.0 (API 26)
- 使用Android Studio打开项目编译

### 📝 更新内容

- 完成Windows端基础架构搭建
- 实现科目管理、凭证管理、报表查询核心功能
- 实现用户认证和权限管理
- 实现操作确认机制（普通操作自动保存，重要操作需确认）
- 完成Android端项目结构搭建
- 创建完整的README文档
- 配置CI/CD工作流

### 🐛 已知问题

- 部分测试用例因模型关系配置问题失败
- 报表导出功能待完善
- Android端UI待完善

### 📚 文档

详见 [README.md](README.md)

### 🤝 贡献

欢迎提交Issue和Pull Request！

---

**注意**: 本系统仅供学习和演示使用，不建议直接用于生产环境。
