"""
凭证管理视图
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, QPushButton,
    QDialog, QFormLayout, QLineEdit, QDateEdit, QSpinBox,
    QMessageBox, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from models.voucher import Voucher, VoucherStatus
from services.voucher_service import VoucherService
from infrastructure.database import get_db
from infrastructure.logger import get_logger

logger = get_logger(__name__)


class VoucherView(QWidget):
    """凭证管理视图"""
    
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
        
        self.add_button = QPushButton('新建凭证')
        self.add_button.clicked.connect(self.create_new_voucher)
        toolbar_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton('编辑凭证')
        self.edit_button.clicked.connect(self.on_edit_voucher)
        toolbar_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton('删除凭证')
        self.delete_button.clicked.connect(self.on_delete_voucher)
        toolbar_layout.addWidget(self.delete_button)
        
        self.submit_button = QPushButton('提交凭证')
        self.submit_button.clicked.connect(self.on_submit_voucher)
        toolbar_layout.addWidget(self.submit_button)
        
        self.review_button = QPushButton('审核凭证')
        self.review_button.clicked.connect(self.on_review_voucher)
        toolbar_layout.addWidget(self.review_button)
        
        self.refresh_button = QPushButton('刷新')
        self.refresh_button.clicked.connect(self.load_data)
        toolbar_layout.addWidget(self.refresh_button)
        
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)
        
        # 凭证列表
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.doubleClicked.connect(self.on_edit_voucher)
        
        # 设置表头
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            '凭证号', '凭证日期', '状态', '借方合计', '贷方合计', '制单人', '备注'
        ])
        self.table_view.setModel(self.model)
        
        # 设置列宽
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        
        self.table_view.setColumnWidth(0, 120)
        self.table_view.setColumnWidth(1, 100)
        self.table_view.setColumnWidth(2, 80)
        self.table_view.setColumnWidth(3, 120)
        self.table_view.setColumnWidth(4, 120)
        self.table_view.setColumnWidth(5, 100)
        
        layout.addWidget(self.table_view)
    
    def load_data(self):
        """加载数据"""
        self.model.clear()
        self.model.setHorizontalHeaderLabels([
            '凭证号', '凭证日期', '状态', '借方合计', '贷方合计', '制单人', '备注'
        ])
        
        try:
            session = get_db()
            service = VoucherService(session, self.current_user_id)
            
            vouchers = service.query_vouchers(limit=100)
            
            for voucher in vouchers:
                items = [
                    QStandardItem(voucher.voucher_number),
                    QStandardItem(voucher.voucher_date.strftime('%Y-%m-%d')),
                    QStandardItem(voucher.status.value),
                    QStandardItem(f"{voucher.total_debit:,.2f}"),
                    QStandardItem(f"{voucher.total_credit:,.2f}"),
                    QStandardItem(voucher.creator.real_name or voucher.creator.username),
                    QStandardItem(voucher.remark or '')
                ]
                
                # 存储凭证ID
                items[0].setData(voucher.id, Qt.ItemDataRole.UserRole)
                
                self.model.appendRow(items)
        except Exception as e:
            logger.error(f"加载凭证数据失败: {str(e)}")
            QMessageBox.critical(self, '错误', f'加载数据失败: {str(e)}')
    
    def create_new_voucher(self):
        """新建凭证"""
        dialog = VoucherEditDialog(self, self.current_user_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()
    
    def get_selected_voucher_id(self) -> int:
        """获取选中的凭证ID"""
        selected = self.table_view.selectionModel().selectedRows()
        if not selected:
            return None
        return self.model.item(selected[0].row(), 0).data(Qt.ItemDataRole.UserRole)
    
    def on_edit_voucher(self):
        """编辑凭证"""
        voucher_id = self.get_selected_voucher_id()
        if not voucher_id:
            QMessageBox.warning(self, '警告', '请选择要编辑的凭证')
            return
        
        dialog = VoucherEditDialog(self, self.current_user_id, voucher_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()
    
    def on_delete_voucher(self):
        """删除凭证"""
        voucher_id = self.get_selected_voucher_id()
        if not voucher_id:
            QMessageBox.warning(self, '警告', '请选择要删除的凭证')
            return
        
        reply = QMessageBox.question(
            self, '确认删除',
            '确定要删除该凭证吗？\n此操作不可撤销。',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                session = get_db()
                service = VoucherService(session, self.current_user_id)
                success, message = service.delete_voucher(voucher_id)
                
                if success:
                    session.commit()
                    QMessageBox.information(self, '成功', message)
                    self.load_data()
                else:
                    session.rollback()
                    QMessageBox.warning(self, '失败', message)
            except Exception as e:
                logger.error(f"删除凭证失败: {str(e)}")
                QMessageBox.critical(self, '错误', f'删除失败: {str(e)}')
    
    def on_submit_voucher(self):
        """提交凭证"""
        voucher_id = self.get_selected_voucher_id()
        if not voucher_id:
            QMessageBox.warning(self, '警告', '请选择要提交的凭证')
            return
        
        reply = QMessageBox.question(
            self, '确认提交',
            '确定要提交该凭证吗？\n提交后将不能修改。',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                session = get_db()
                service = VoucherService(session, self.current_user_id)
                success, message = service.submit_voucher(voucher_id)
                
                if success:
                    session.commit()
                    QMessageBox.information(self, '成功', message)
                    self.load_data()
                else:
                    session.rollback()
                    QMessageBox.warning(self, '失败', message)
            except Exception as e:
                logger.error(f"提交凭证失败: {str(e)}")
                QMessageBox.critical(self, '错误', f'提交失败: {str(e)}')
    
    def on_review_voucher(self):
        """审核凭证"""
        voucher_id = self.get_selected_voucher_id()
        if not voucher_id:
            QMessageBox.warning(self, '警告', '请选择要审核的凭证')
            return
        
        reply = QMessageBox.question(
            self, '确认审核',
            '确定要审核通过该凭证吗？\n审核后将更新科目余额。',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                session = get_db()
                service = VoucherService(session, self.current_user_id)
                success, message = service.review_voucher(voucher_id, True)
                
                if success:
                    session.commit()
                    QMessageBox.information(self, '成功', message)
                    self.load_data()
                else:
                    session.rollback()
                    QMessageBox.warning(self, '失败', message)
            except Exception as e:
                logger.error(f"审核凭证失败: {str(e)}")
                QMessageBox.critical(self, '错误', f'审核失败: {str(e)}')


class VoucherEditDialog(QDialog):
    """凭证编辑对话框"""
    
    def __init__(self, parent, current_user_id: int, voucher_id: int = None):
        super().__init__(parent)
        self.current_user_id = current_user_id
        self.voucher_id = voucher_id
        self.voucher = None
        
        if voucher_id:
            self.setWindowTitle('编辑凭证')
        else:
            self.setWindowTitle('新建凭证')
        
        self.setFixedSize(800, 600)
        self.init_ui()
        
        if voucher_id:
            self.load_data()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 基本信息
        form_layout = QFormLayout()
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form_layout.addRow('凭证日期:', self.date_edit)
        
        self.attachment_spin = QSpinBox()
        self.attachment_spin.setMinimum(0)
        form_layout.addRow('附件张数:', self.attachment_spin)
        
        self.remark_edit = QLineEdit()
        form_layout.addRow('备注:', self.remark_edit)
        
        layout.addLayout(form_layout)
        
        # 明细表格（简化版）
        from PyQt6.QtWidgets import QLabel
        layout.addWidget(QLabel('凭证明细（开发中...）'))
        
        # 按钮
        button_layout = QHBoxLayout()
        
        save_button = QPushButton('保存')
        save_button.clicked.connect(self.on_save)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton('取消')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def load_data(self):
        """加载数据"""
        try:
            session = get_db()
            service = VoucherService(session, self.current_user_id)
            self.voucher = service.get_voucher_by_id(self.voucher_id)
            
            if self.voucher:
                self.date_edit.setDate(QDate(
                    self.voucher.voucher_date.year,
                    self.voucher.voucher_date.month,
                    self.voucher.voucher_date.day
                ))
                self.attachment_spin.setValue(self.voucher.attachment_count)
                self.remark_edit.setText(self.voucher.remark or '')
        except Exception as e:
            logger.error(f"加载凭证数据失败: {str(e)}")
    
    def on_save(self):
        """保存"""
        QMessageBox.information(self, '提示', '凭证保存功能开发中...')
        self.accept()
