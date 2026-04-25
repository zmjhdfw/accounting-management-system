# Android数据持久化修复 - 发布说明

## v1.2.0 (2026-04-25)

### Bug修复
- **修复Android端界面切换后数据丢失的严重bug**
  - 问题：在任意界面下添加数据后，切换到其他界面再返回时，数据会消失
  - 原因：Fragment使用内存存储数据，未进行持久化，Fragment重建时数据丢失
  - 解决：引入MVVM架构，使用ViewModel和LiveData管理数据，Repository实现数据持久化

### 架构优化
- **引入MVVM架构模式**
  - UI层：Activity/Fragment负责UI展示
  - ViewModel层：管理UI数据，配置变更时保留数据
  - Repository层：封装数据访问，提供LiveData
  - 数据层：SharedPreferences持久化

- **使用Android Architecture Components**
  - ViewModel：在配置变更（如屏幕旋转）时保留数据
  - LiveData：实现数据观察，自动更新UI
  - Repository模式：统一数据访问接口

### 新增类
- `AccountItem.java` - 科目数据模型类
  - 位置：`com.example.accounting.data.model`
  - 功能：封装科目属性，提供序列化/反序列化方法
  
- `AccountRepository.java` - 科目数据仓库类
  - 位置：`com.example.accounting.data.repository`
  - 功能：单例模式，管理数据持久化，提供LiveData
  
- `AccountViewModel.java` - 科目ViewModel类
  - 位置：`com.example.accounting.ui.viewmodel`
  - 功能：管理UI数据，委托Repository执行操作

### 修改类
- `AccountFragment.java` - 科目管理Fragment
  - 移除内存数据存储（accountList）
  - 使用ViewModel管理数据
  - 观察LiveData自动更新UI
  - Adapter支持外部设置数据

- `build.gradle` - 项目依赖配置
  - 新增：`androidx.lifecycle:lifecycle-viewmodel:2.6.2`
  - 新增：`androidx.lifecycle:lifecycle-livedata:2.6.2`

### 技术细节
1. **数据持久化流程**：
   - 添加/修改/删除操作 → ViewModel → Repository（后台线程）
   - Repository保存到SharedPreferences → 更新LiveData
   - LiveData通知观察者 → Fragment自动更新UI

2. **数据格式兼容**：
   - 保持与原AccountManager相同的序列化格式
   - 格式：`code:name:type:balance:direction`
   - 多个科目用分号分隔

3. **线程安全**：
   - Repository使用ExecutorService执行后台操作
   - 使用postValue()更新LiveData（线程安全）
   - 使用Handler在主线程回调

### 测试建议
1. **功能测试**：
   - 添加科目 → 切换界面 → 返回 → 验证数据存在
   - 修改科目 → 切换界面 → 返回 → 验证数据已更新
   - 删除科目 → 切换界面 → 返回 → 验证数据已删除

2. **配置变更测试**：
   - 添加科目 → 旋转屏幕 → 验证数据保留

3. **应用重启测试**：
   - 添加科目 → 完全关闭应用 → 重新打开 → 验证数据存在

### 编译说明
由于Gradle Wrapper jar文件缺失，首次编译需要：
1. 确保已安装Gradle 8.0或更高版本
2. 运行：`gradle wrapper` 生成Wrapper文件
3. 或手动下载gradle-wrapper.jar到`gradle/wrapper`目录
4. 然后运行：`./gradlew assembleDebug`

### 下一步计划
- 为VoucherFragment实现相同的MVVM架构
- 添加单元测试和集成测试
- 考虑迁移到Room数据库替代SharedPreferences
- 添加数据验证和错误处理

---

## v1.0.0 (初始版本)
- 基础会计管理系统功能
- 科目管理、凭证管理、报表查询
- 用户登录注册功能
