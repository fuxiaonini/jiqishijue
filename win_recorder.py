import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from ui.Ui_sign_record import Ui_sign_record
import db_opt

class Child_3(QDialog, Ui_sign_record):
    def __init__(self, parent=None):
        super(Child_3, self).__init__()
        self.setupUi(self)
        self.get_all_records()

    def get_all_records(self):
        data = db_opt.getall_sign_records()
        row_num = len(data)
        self.model = QStandardItemModel(row_num, 3)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 150)
        self.tableView.setColumnWidth(2, 400)
        self.column_name = ["学号", "姓名", "签到时间"]
        self.model.setHorizontalHeaderLabels(self.column_name)
        self.tableView.setSortingEnabled(True)

        for i in range(row_num):
            for j in range(3):
                newItem = QStandardItem(f"{data[i][j]}")
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 居中
                self.model.setItem(i, j, newItem)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(f"共计 {row_num} 条记录")

if __name__=="__main__":
    app = QApplication(sys.argv)
    myshow=Child_3()
    myshow.show()
    sys.exit(app.exec_())