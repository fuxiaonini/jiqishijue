import sys
from PyQt5.QtWidgets import *

from ui.Ui_meniu import Ui_Window1
from win_capture import Child
from win_detector import Child_2
from win_recorder import Child_3

class mywindow(QMainWindow, Ui_Window1):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.show_child)
        self.pushButton_2.clicked.connect(self.show_child_2)
        self.pushButton_3.clicked.connect(self.show_child_3)

    def show_child(self):
        self.hide()
        child = Child(parent=self)
        if child.exec_():
            pass
        self.show()

    def show_child_2(self):
        self.hide()
        child_2 = Child_2(parent=self)
        if child_2.exec_():
            pass
        self.show()

    def show_child_3(self):
        self.hide()
        child_2 = Child_3(parent=self)
        if child_2.exec_():
            pass
        self.show()

if __name__=="__main__":
    app = QApplication(sys.argv)
    myshow=mywindow()
    myshow.show()
    sys.exit(app.exec_())