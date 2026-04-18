"""
科目管理视图
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QDialog, QFormLayout, QLineEdit, QComboBox,
    QMessageBox, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal
from models.account import Account, AccountType
from services.account_service import AccountService
from services.confirmation_service import OperationType, OperationExecutor
from infrastructure.database import get_db
from infrastructure.logger import get_logger

logger = get_logger(__name__)


class AccountView(QWidget):
    """科目管理视图"""
    
    def __init__(self, current_user_id: int):
        super().__init__()
        self.current_user_id = current_user_id
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        self.add_button = QPushButton('新增科目')
        self.add_button.clicked.connect(self.on_add_account)
        toolbar_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton('编辑科目')
        self.edit_button.clicked.connect(self.on_edit_account)
        toolbar_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton('删除科目')
        self.delete_button.clicked.connect(self.on_delete_account)
        toolbar_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton('刷新')
        self.refresh_button.clicked.connect(self.load_data)
        toolbar_layout.addWidget(self.refresh_button)
        
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)
        
        # 科目树
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(['科目编码', '科目名称', '科目类型', '余额方向', '当前余额'])
        self.tree_widget.setColumnWidth(0, 150)
        self.tree_widget.setColumnWidth(1, 200)
        self.tree_widget.setColumnWidth(2, 100)
        self.tree_widget.setColumnWidth(3, 80)
        self.tree_widget.setColumnWidth(4, 120)
        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.on_context_menu)
        self.tree_widget.itemDoubleClicked.connect(self.on_edit_account)
        layout.addWidget(self.tree_widget)
    
    def load_data(self):
        """加载数据"""
        self.tree_widget.clear()
        
        try:
            session = get_db()
            service = AccountService(session, self.current_user_id)
            
            # 获取科目树
            root_accounts = service.get_account_tree()
            
            for account in root_accounts:
                self.add_tree_item(account, None)
            
            self.tree_widget.expandAll()
        except Exception as e:
            logger.error(f"加载科目数据失败: {str(e)}")
            QMessageBox.critical(self, '错误', f'加载数据失败: {str(e)}')
    
    def add_tree_item(self, account: Account, parent_item: QTreeWidgetItem):
        """添加树节点"""
        item = QTreeWidgetItem()
        item.setText(0, account.code)
        item.setText(1, account.name)
        item.setText(2, account.account_type.value)
        item.setText(3, account.balance_direction)
        item.setText(4, f"{account.current_balance:,.2f}")
        item.setData(0, Qt.ItemDataRole.UserRole, account.id)
        
        if parent_item:
            parent_item.addChild(item)
        else:
            self.tree_widget.addTopLevelItem(item)
        
        # 递归添加子科目
        session = get_db()
        service = AccountService(session, self.current_user_id)
        children = service.account_dao.get_children_accounts(account.id)
        
        for child in children:
            self.add_tree_item(child, item)
    
    def on_add_account(self):
        """新增科目"""
        dialog = AccountEditDialog(self, self.current_user_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()
    
    def on_edit_account(self):
        """编辑科目"""
        current_item = self.tree_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, '警告', '请选择要编辑的科目')
            return
        
        account_id = current_item.data(0, Qt.ItemDataRole.UserRole)
        dialog = AccountEditDialog(self, self.current_user_id, account_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()
    
    def on_delete_account(self):
        """删除科目"""
        current_item = self.tree_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, '警告', '请选择要删除的科目')
            return
        
        account_id = current_item.data(0, Qt.ItemDataRole.UserRole)
        account_name = current_item.text(1)
        
        # 确认对话框
        def confirm():
            reply = QMessageBox.question(
                self, '确认删除',
                f'确定要删除科目 "{account_name}" 吗？\n此操作不可撤销。',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            return reply == QMessageBox.StandardButton.Yes
        
        # 执行删除
        def operation():
            session = get_db()
            service = AccountService(session, self.current_user_id)
            success, message = service.delete_account(account_id)
            if success:
                session.commit()
            else:
                session.rollback()
            return success, message
        
        success, result = OperationExecutor.execute(
            OperationType.ACCOUNT_DELETE,
            operation,
            confirm
        )
        
        if success:
            QMessageBox.information(self, '成功', '科目删除成功')
            self.load_data()
        else:
            if result != "用户取消操作":
                QMessageBox.warning(self, '失败', str(result))
    
    def on_context_menu(self, pos):
        """右键菜单"""
        item = self.tree_widget.itemAt(pos)
        if not item:
            return
        
        menu = QMenu(self)
        
        add_action = menu.addAction('新增子科目')
        edit_action = menu.addAction('编辑科目')
        delete_action = menu.addAction('删除科目')
        
        action = menu.exec(self.tree_widget.mapToGlobal(pos))
        
        if action == add_action:
            account_id = item.data(0, Qt.ItemDataRole.UserRole)
            dialog = AccountEditDialog(self, self.current_user_id, parent_id=account_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_data()
        elif action == edit_action:
            self.on_edit_account()
        elif action == delete_action:
            self.on_delete_account()


class AccountEditDialog(QDialog):
    """科目编辑对话框"""
    
    def __init__(self, parent, current_user_id: int, account_id: int = None, parent_id: int = None):
        super().__init__(parent)
        self.current_user_id = current_user_id
        self.account_id = account_id
        self.parent_id = parent_id
        self.account = None
        
        if account_id:
            self.setWindowTitle('编辑科目')
        else:
            self.setWindowTitle('新增科目')
        
        self.setFixedSize(400, 300)
        self.init_ui()
        
        if account_id:
            self.load_data()
    
    def init_ui(self):
        """初始化UI"""
        layout = QFormLayout()
        self.setLayout(layout)
        
        # 科目编码
        self.code_edit = QLineEdit()
        layout.addRow('科目编码:', self.code_edit)
        
        # 科目名称
        self.name_edit = QLineEdit()
        layout.addRow('科目名称:', self.name_edit)
        
        # 科目类型
        self.type_combo = QComboBox()
        self.type_combo.addItem('资产', AccountType.ASSET)
        self.type_combo.addItem('负债', AccountType.LIABILITY)
        self.type_combo.addItem('所有者权益', AccountType.EQUITY)
        self.type_combo.addItem('收入', AccountType.INCOME)
        self.type_combo.addItem('费用', AccountType.EXPENSE)
        layout.addRow('科目类型:', self.type_combo)
        
        # 余额方向
        self.direction_combo = QComboBox()
        self.direction_combo.addItem('借方', 'debit')
        self.direction_combo.addItem('贷方', 'credit')
        layout.addRow('余额方向:', self.direction_combo)
        
        # 说明
        self.description_edit = QLineEdit()
        layout.addRow('说明:', self.description_edit)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        save_button = QPushButton('保存')
        save_button.clicked.connect(self.on_save)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton('取消')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addRow(button_layout)
    
    def load_data(self):
        """加载数据"""
        try:
            session = get_db()
            service = AccountService(session, self.current_user_id)
            self.account = service.get_account_by_id(self.account_id)
            
            if self.account:
                self.code_edit.setText(self.account.code)
                self.name_edit.setText(self.account.name)
                
                # 设置类型
                index = self.type_combo.findData(self.account.account_type)
                if index >= 0:
                    self.type_combo.setCurrentIndex(index)
                
                # 设置余额方向
                direction_index = self.direction_combo.findData(self.account.balance_direction)
                if direction_index >= 0:
                    self.direction_combo.setCurrentIndex(direction_index)
                
                self.description_edit.setText(self.account.description or '')
        except Exception as e:
            logger.error(f"加载科目数据失败: {str(e)}")
    
    def on_save(self):
        """保存"""
        code = self.code_edit.text().strip()
        name = self.name_edit.text().strip()
        account_type = self.type_combo.currentData()
        balance_direction = self.direction_combo.currentData()
        description = self.description_edit.text().strip()
        
        if not code:
            QMessageBox.warning(self, '警告', '请输入科目编码')
            return
        
        if not name:
            QMessageBox.warning(self, '警告', '请输入科目名称')
            return
        
        try:
            session = get_db()
            service = AccountService(session, self.current_user_id)
            
            if self.account_id:
                # 更新
                success, message = service.update_account(
                    self.account_id, name, description
                )
            else:
                # 创建
                success, account, message = service.create_account(
                    code, name, account_type, balance_direction,
                    self.parent_id, description
                )
            
            if success:
                session.commit()
                QMessageBox.information(self, '成功', message)
                self.accept()
            else:
                session.rollback()
                QMessageBox.warning(self, '失败', message)
        except Exception as e:
            logger.error(f"保存科目失败: {str(e)}")
            QMessageBox.critical(self, '错误', f'保存失败: {str(e)}')
