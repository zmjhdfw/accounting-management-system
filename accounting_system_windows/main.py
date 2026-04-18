"""
会计管理系统 - 主程序入口
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow
from infrastructure.database import init_db
from infrastructure.logger import setup_logging
from infrastructure.config import load_config
from infrastructure.logger import get_logger

logger = get_logger(__name__)


def main():
    """主函数"""
    # 设置高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName('会计管理系统')
    app.setApplicationVersion('1.0.0')
    
    try:
        # 初始化配置
        config_file = os.path.join(os.path.dirname(__file__), 'config', 'app.yaml')
        if os.path.exists(config_file):
            load_config(config_file)
        
        # 初始化日志
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'app.log')
        setup_logging(log_level='INFO', log_file=log_file)
        
        logger.info("系统启动")
        
        # 初始化数据库
        init_db()
        logger.info("数据库初始化完成")
        
        # 显示登录对话框
        login_dialog = LoginDialog()
        if login_dialog.exec() == LoginDialog.DialogCode.Accepted:
            # 登录成功，显示主窗口
            user = login_dialog.login_success_emitted[0] if hasattr(login_dialog, 'login_success_emitted') else None
            
            # 重新获取用户信息
            from infrastructure.database import get_db
            from dao.user_dao import UserDao
            session = get_db()
            user_dao = UserDao(session)
            user = user_dao.get_by_id(login_dialog.auth_service.current_user_id) if hasattr(login_dialog, 'auth_service') else None
            
            if user:
                main_window = MainWindow(user)
                main_window.show()
                
                logger.info(f"主窗口显示，用户: {user.username}")
                
                return app.exec()
            else:
                logger.error("无法获取用户信息")
                return 1
        else:
            logger.info("用户取消登录")
            return 0
    
    except Exception as e:
        logger.error(f"系统启动失败: {str(e)}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
