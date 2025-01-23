import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt

class PositionCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('开仓仓位计算器')
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 美元最大亏损输入
        self.max_loss_label = QLabel('美元最大亏损:')
        self.max_loss_input = QLineEdit()
        self.max_loss_input.setPlaceholderText('请输入最大亏损金额')
        layout.addWidget(self.max_loss_label)
        layout.addWidget(self.max_loss_input)

        # 止损点数输入
        self.stop_loss_label = QLabel('止损点数:')
        self.stop_loss_input = QLineEdit()
        self.stop_loss_input.setPlaceholderText('请输入止损点数')
        layout.addWidget(self.stop_loss_label)
        layout.addWidget(self.stop_loss_input)

        # 计算按钮
        self.calculate_button = QPushButton('计算')
        self.calculate_button.clicked.connect(self.calculate_positions)
        layout.addWidget(self.calculate_button)

        # 结果显示表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(['合约', '每点价值($)', '建议手数'])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.result_table)

        self.setLayout(layout)

    def calculate_positions(self):
        try:
            max_loss = float(self.max_loss_input.text())
            stop_loss_points = float(self.stop_loss_input.text())
        except ValueError:
            self.result_table.setRowCount(0)
            return

        contracts = [
            {'name': 'NQ', 'tick_value': 20},
            {'name': 'MNQ', 'tick_value': 2},
            {'name': 'ES', 'tick_value': 50},
            {'name': 'MES', 'tick_value': 5},
        ]

        results = []
        for contract in contracts:
            tick_value = contract['tick_value']
            suggested_lots = max_loss / (stop_loss_points * tick_value)  # 允许非整数手数
            if suggested_lots > 0:  # 只显示可以交易的合约
                results.append((contract['name'], tick_value, suggested_lots))

        self.result_table.setRowCount(len(results))
        for row, (name, tick_value, lots) in enumerate(results):
            self.result_table.setItem(row, 0, QTableWidgetItem(name))
            self.result_table.setItem(row, 1, QTableWidgetItem(f'{tick_value:.2f}'))
            self.result_table.setItem(row, 2, QTableWidgetItem(f'{lots:.4f}'))  # 显示4位小数

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = PositionCalculator()
    calculator.show()
    sys.exit(app.exec())
