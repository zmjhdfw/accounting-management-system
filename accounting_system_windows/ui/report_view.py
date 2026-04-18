"""
报表查询视图
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QDateEdit,
    QPushButton, QTableView, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from infrastructure.logger import get_logger

logger = get_logger(__name__)


class ReportView(QWidget):
    """报表查询视图"""
    
    def __init__(self, current_user_id: int):
        super().__init__()
        self.current_user_id = current_user_id
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        # 报表类型
        toolbar_layout.addWidget(self.create_label('报表类型:'))
        self.report_combo = QComboBox()
        self.report_combo.addItem('资产负债表', 'balance_sheet')
        self.report_combo.addItem('利润表', 'income_statement')
        self.report_combo.addItem('试算平衡表', 'trial_balance')
        self.report_combo.addItem('总账', 'general_ledger')
        self.report_combo.addItem('明细账', 'subsidiary_ledger')
        toolbar_layout.addWidget(self.report_combo)
        
        toolbar_layout.addWidget(self.create_label('会计期间:'))
        self.period_date = QDateEdit()
        self.period_date.setCalendarPopup(True)
        self.period_date.setDate(QDate.currentDate())
        self.period_date.setDisplayFormat('yyyy-MM')
        toolbar_layout.addWidget(self.period_date)
        
        self.query_button = QPushButton('查询')
        self.query_button.clicked.connect(self.on_query)
        toolbar_layout.addWidget(self.query_button)
        
        self.export_pdf_button = QPushButton('导出PDF')
        self.export_pdf_button.clicked.connect(self.on_export_pdf)
        toolbar_layout.addWidget(self.export_pdf_button)
        
        self.export_excel_button = QPushButton('导出Excel')
        self.export_excel_button.clicked.connect(self.on_export_excel)
        toolbar_layout.addWidget(self.export_excel_button)
        
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)
        
        # 报表显示
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table_view)
    
    def create_label(self, text):
        """创建标签"""
        from PyQt6.QtWidgets import QLabel
        label = QLabel(text)
        return label
    
    def on_query(self):
        """查询报表"""
        report_type = self.report_combo.currentData()
        
        QMessageBox.information(self, '提示', f'{self.report_combo.currentText()}功能开发中...')
        
        # 示例数据
        self.model.clear()
        
        if report_type == 'balance_sheet':
            self.model.setHorizontalHeaderLabels(['项目', '期末余额', '期初余额'])
            items = [
                ['资产', '', ''],
                ['  流动资产', '', ''],
                ['    货币资金', '100,000.00', '80,000.00'],
                ['    应收账款', '50,000.00', '60,000.00'],
                ['  资产合计', '150,000.00', '140,000.00'],
                ['', '', ''],
                ['负债', '', ''],
                ['  流动负债', '', ''],
                ['    应付账款', '30,000.00', '40,000.00'],
                ['  负债合计', '30,000.00', '40,000.00'],
                ['', '', ''],
                ['所有者权益', '', ''],
                ['  实收资本', '100,000.00', '100,000.00'],
                ['  未分配利润', '20,000.00', '0.00'],
                ['  所有者权益合计', '120,000.00', '100,000.00'],
            ]
            
            for row_data in items:
                items = [QStandardItem(cell) for cell in row_data]
                self.model.appendRow(items)
        
        elif report_type == 'trial_balance':
            self.model.setHorizontalHeaderLabels(['科目编码', '科目名称', '借方余额', '贷方余额'])
            items = [
                ['1001', '库存现金', '10,000.00', ''],
                ['1002', '银行存款', '90,000.00', ''],
                ['1122', '应收账款', '50,000.00', ''],
                ['2202', '应付账款', '', '30,000.00'],
                ['4001', '实收资本', '', '100,000.00'],
                ['合计', '', '150,000.00', '130,000.00'],
            ]
            
            for row_data in items:
                items = [QStandardItem(cell) for cell in row_data]
                self.model.appendRow(items)
    
    def on_export_pdf(self):
        """导出PDF"""
        from PyQt6.QtWidgets import QFileDialog
        from services.report_service import ReportService
        from infrastructure.database import get_db
        
        report_type = self.report_combo.currentData()
        report_name = self.report_combo.currentText()
        
        # 选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, '保存PDF文件', 
            f'{report_name}.pdf',
            'PDF文件 (*.pdf)'
        )
        
        if not file_path:
            return
        
        try:
            session = get_db()
            service = ReportService(session, self.current_user_id)
            
            # 获取当前期间ID（简化处理，使用1）
            period_id = 1
            
            success = service.export_report(report_type, period_id, file_path, 'pdf')
            
            if success:
                QMessageBox.information(self, '成功', f'PDF导出成功:\n{file_path}')
            else:
                QMessageBox.warning(self, '失败', 'PDF导出失败')
        except Exception as e:
            logger.error(f"导出PDF失败: {str(e)}")
            QMessageBox.critical(self, '错误', f'导出失败: {str(e)}')
    
    def on_export_excel(self):
        """导出Excel"""
        from PyQt6.QtWidgets import QFileDialog
        from services.report_service import ReportService
        from infrastructure.database import get_db
        
        report_type = self.report_combo.currentData()
        report_name = self.report_combo.currentText()
        
        # 选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, '保存Excel文件',
            f'{report_name}.xlsx',
            'Excel文件 (*.xlsx)'
        )
        
        if not file_path:
            return
        
        try:
            session = get_db()
            service = ReportService(session, self.current_user_id)
            
            # 获取当前期间ID（简化处理，使用1）
            period_id = 1
            
            success = service.export_report(report_type, period_id, file_path, 'excel')
            
            if success:
                QMessageBox.information(self, '成功', f'Excel导出成功:\n{file_path}')
            else:
                QMessageBox.warning(self, '失败', 'Excel导出失败')
        except Exception as e:
            logger.error(f"导出Excel失败: {str(e)}")
            QMessageBox.critical(self, '错误', f'导出失败: {str(e)}')
