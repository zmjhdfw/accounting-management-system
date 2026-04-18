"""
登录对话框
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent
from models.user import User
from services.auth_service import AuthService
from services.user_service import UserService
from infrastructure.database import get_db
from infrastructure.logger import get_logger

logger = get_logger(__name__)


class LoginDialog(QDialog):
    """登录对话框"""
    
    login_success = pyqtSignal(User)
    
    def __init__(self):
        super().__init__()
        self.auth_service = None
        self.user_service = None
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('会计管理系统 - 登录')
        self.setFixedSize(400, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # 标题
        title_label = QLabel('会计管理系统')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        layout.addWidget(title_label)
        
        # 用户名
        username_layout = QHBoxLayout()
        username_label = QLabel('用户名:')
        username_label.setFixedWidth(80)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('请输入用户名')
        self.username_edit.returnPressed.connect(self.on_login)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_edit)
        layout.addLayout(username_layout)
        
        # 密码
        password_layout = QHBoxLayout()
        password_label = QLabel('密码:')
        password_label.setFixedWidth(80)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText('请输入密码')
        self.password_edit.returnPressed.connect(self.on_login)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_edit)
        layout.addLayout(password_layout)
        
        # 记住密码
        self.remember_check = QCheckBox('记住密码')
        layout.addWidget(self.remember_check)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.login_button = QPushButton('登录')
        self.login_button.setFixedWidth(100)
        self.login_button.clicked.connect(self.on_login)
        button_layout.addWidget(self.login_button)
        
        self.register_button = QPushButton('注册')
        self.register_button.setFixedWidth(100)
        self.register_button.clicked.connect(self.on_register)
        button_layout.addWidget(self.register_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 设置焦点
        self.username_edit.setFocus()
    
    def on_login(self):
        """登录"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username:
            QMessageBox.warning(self, '警告', '请输入用户名')
            self.username_edit.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, '警告', '请输入密码')
            self.password_edit.setFocus()
            return
        
        # 禁用按钮
        self.login_button.setEnabled(False)
        self.login_button.setText('登录中...')
        
        try:
            # 获取数据库会话
            session = get_db()
            self.auth_service = AuthService(session)
            
            # 执行登录
            success, user, message = self.auth_service.login(username, password)
            
            if success:
                session.commit()
                logger.info(f"用户登录成功: {username}")
                self.login_success.emit(user)
                self.accept()
            else:
                session.rollback()
                QMessageBox.warning(self, '登录失败', message)
                self.password_edit.clear()
                self.password_edit.setFocus()
        except Exception as e:
            logger.error(f"登录异常: {str(e)}")
            QMessageBox.critical(self, '错误', f'登录失败: {str(e)}')
        finally:
            self.login_button.setEnabled(True)
            self.login_button.setText('登录')
    
    def on_register(self):
        """注册"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username:
            QMessageBox.warning(self, '警告', '请输入用户名')
            self.username_edit.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, '警告', '请输入密码')
            self.password_edit.setFocus()
            return
        
        # 确认密码
        confirm_password, ok = self.get_password_confirmation()
        if not ok:
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, '警告', '两次密码不一致')
            return
        
        try:
            session = get_db()
            self.user_service = UserService(session)
            
            # 注册用户
            success, user, message = self.user_service.create_user(
                username=username,
                password=password,
                nickname=username,
                role='user'
            )
            
            if success:
                session.commit()
                QMessageBox.information(self, '成功', '注册成功，请登录')
                logger.info(f"用户注册成功: {username}")
            else:
                session.rollback()
                QMessageBox.warning(self, '注册失败', message)
        except Exception as e:
            logger.error(f"注册异常: {str(e)}")
            QMessageBox.critical(self, '错误', f'注册失败: {str(e)}')
    
    def get_password_confirmation(self):
        """获取密码确认"""
        dialog = QDialog(self)
        dialog.setWindowTitle('确认密码')
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        layout.addWidget(QLabel('请再次输入密码:'))
        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(password_edit)
        
        button_layout = QHBoxLayout()
        ok_btn = QPushButton('确定')
        cancel_btn = QPushButton('取消')
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        result = [None]
        
        def on_ok():
            result[0] = password_edit.text()
            dialog.accept()
        
        def on_cancel():
            dialog.reject()
        
        ok_btn.clicked.connect(on_ok)
        cancel_btn.clicked.connect(on_cancel)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return result[0], True
        return None, False
    
    def keyPressEvent(self, event: QKeyEvent):
        """键盘事件"""
        if event.key() == Qt.Key.Key_Escape:
            # 禁用ESC键关闭
            return
        super().keyPressEvent(event)
