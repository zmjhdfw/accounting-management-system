"""
主窗口
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QToolBar, QStatusBar, QTabWidget,
    QMessageBox, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from models.user import User
from infrastructure.logger import get_logger

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """主窗口"""
    
    logout_signal = pyqtSignal()
    
    def __init__(self, current_user: User):
        super().__init__()
        self.current_user = current_user
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle(f"会计管理系统 - {self.current_user.real_name or self.current_user.username}")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建中心部件
        self.create_central_widget()
        
        # 创建状态栏
        self.create_status_bar()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')
        
        new_action = QAction('新建凭证', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.on_new_voucher)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction('数据备份', self)
        backup_action.triggered.connect(self.on_backup)
        file_menu.addAction(backup_action)
        
        restore_action = QAction('数据恢复', self)
        restore_action.triggered.connect(self.on_restore)
        file_menu.addAction(restore_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menubar.addMenu('视图(&V)')
        
        account_action = QAction('科目管理', self)
        account_action.triggered.connect(lambda: self.switch_tab(0))
        view_menu.addAction(account_action)
        
        voucher_action = QAction('凭证管理', self)
        voucher_action.triggered.connect(lambda: self.switch_tab(1))
        view_menu.addAction(voucher_action)
        
        report_action = QAction('报表查询', self)
        report_action.triggered.connect(lambda: self.switch_tab(2))
        view_menu.addAction(report_action)
        
        # 系统菜单
        system_menu = menubar.addMenu('系统(&S)')
        
        user_action = QAction('用户管理', self)
        user_action.triggered.connect(self.on_user_management)
        system_menu.addAction(user_action)
        
        settings_action = QAction('系统设置', self)
        settings_action.triggered.connect(self.on_settings)
        system_menu.addAction(settings_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')
        
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)
    
    def create_tool_bar(self):
        """创建工具栏"""
        toolbar = QToolBar('主工具栏')
        self.addToolBar(toolbar)
        
        new_voucher_action = QAction('新建凭证', self)
        new_voucher_action.triggered.connect(self.on_new_voucher)
        toolbar.addAction(new_voucher_action)
        
        toolbar.addSeparator()
        
        account_action = QAction('科目', self)
        account_action.triggered.connect(lambda: self.switch_tab(0))
        toolbar.addAction(account_action)
        
        voucher_action = QAction('凭证', self)
        voucher_action.triggered.connect(lambda: self.switch_tab(1))
        toolbar.addAction(voucher_action)
        
        report_action = QAction('报表', self)
        report_action.triggered.connect(lambda: self.switch_tab(2))
        toolbar.addAction(report_action)
    
    def create_central_widget(self):
        """创建中心部件"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 添加各个视图（占位符）
        from ui.account_view import AccountView
        from ui.voucher_view import VoucherView
        from ui.report_view import ReportView
        
        self.account_view = AccountView(self.current_user.id)
        self.voucher_view = VoucherView(self.current_user.id)
        self.report_view = ReportView(self.current_user.id)
        
        self.tab_widget.addTab(self.account_view, '科目管理')
        self.tab_widget.addTab(self.voucher_view, '凭证管理')
        self.tab_widget.addTab(self.report_view, '报表查询')
    
    def create_status_bar(self):
        """创建状态栏"""
        status_bar = self.statusBar()
        
        # 用户信息
        user_label = QLabel(f"当前用户: {self.current_user.real_name or self.current_user.username}")
        status_bar.addPermanentWidget(user_label)
        
        # 操作状态
        self.status_label = QLabel("就绪")
        status_bar.addWidget(self.status_label)
    
    def switch_tab(self, index: int):
        """切换标签页"""
        self.tab_widget.setCurrentIndex(index)
    
    def on_new_voucher(self):
        """新建凭证"""
        self.switch_tab(1)
        self.voucher_view.create_new_voucher()
    
    def on_backup(self):
        """数据备份"""
        QMessageBox.information(self, '提示', '数据备份功能开发中...')
    
    def on_restore(self):
        """数据恢复"""
        QMessageBox.information(self, '提示', '数据恢复功能开发中...')
    
    def on_user_management(self):
        """用户管理"""
        QMessageBox.information(self, '提示', '用户管理功能开发中...')
    
    def on_settings(self):
        """系统设置"""
        QMessageBox.information(self, '提示', '系统设置功能开发中...')
    
    def on_about(self):
        """关于"""
        QMessageBox.about(self, '关于', 
                         '会计管理系统 v1.0\n\n'
                         '基于Python和PyQt6开发\n'
                         '支持科目管理、凭证管理、报表查询等功能')
    
    def set_status(self, message: str):
        """设置状态信息"""
        self.status_label.setText(message)
    
    def closeEvent(self, event):
        """关闭事件"""
        reply = QMessageBox.question(
            self, '确认退出',
            '确定要退出系统吗？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            logger.info(f"用户退出系统: {self.current_user.username}")
            self.logout_signal.emit()
            event.accept()
        else:
            event.ignore()
