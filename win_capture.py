import os
import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

from detection import detector
from pic_maker import make_pic, make_dir, make_little_gray
import db_opt
import train
import recognition_unit
from ui.Ui_capture import Ui_capture

class Child(QDialog, Ui_capture):
    def __init__(self, parent=None):
        super(Child, self).__init__()
        self.setupUi(self)
        # 控制显示按钮：最大化、最小化
        self.setWindowFlags(Qt.Dialog | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_viedo)
        self.pushButton.clicked.connect(self.video_button)
        self.pushButton_5.clicked.connect(self.catch_pic)
        self.pushButton_2.clicked.connect(self.open_folder) # 查看图片
        self.pushButton.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_4.clicked.connect(self.infor_confirm)
        self.pushButton_3.clicked.connect(self.go_train)
        self.pushButton_6.setEnabled(False)
        self.pushButton_6.clicked.connect(self.go_recog)
        self.cap_video = 0
        self.flag = 0
        self.img = []
        self.img_gray = []
        self.member_number = ""
        self.member_name = ""
        self.check_start = 0
        self.on_cahch = 0 # 保存图片状态:0，为不保存，1为保存
        self.on_recog = 0 # 识别状态:0，为不识别，1为识别
        self.pic_add = 0
        self.cbox1_ini()
        self.current_dir = "person_dir"
        self.set_valid()
        self.completer = QCompleter()
        self.recog_id = 0
        self.recog_name = ""

    def set_valid(self):
        validar = QtGui.QIntValidator()
        validar.setRange(0, 999999999)
        self.comboBox.setValidator(validar)

    def open_folder(self):
        os.startfile( self.current_dir)

    def cbox1_ini(self):
        self.comboBox.clear()
        item_list1 = db_opt.get_all_person_list()
        self.item_list2 = [f"{i[0]}" for i in item_list1]
        self.comboBox.addItems([""] + [f"{i[0]} {i[1]}" for i in item_list1])
        self.completer = QCompleter(self.item_list2)
        self.completer.setCompletionMode(QCompleter.InlineCompletion)
        self.comboBox.setCompleter(self.completer)
        self.comboBox.activated.connect(self.indexChange)

    def indexChange(self):
        if self.comboBox.currentIndex() > 0 and self.comboBox.currentIndex() <= len(self.item_list2):
            self.lineEdit_2.setText(f"{(self.comboBox.currentText()).split()[1]}")
            self.comboBox.setCurrentText(f"{(self.comboBox.currentText()).split()[0]}")

    def infor_confirm(self):
        if self.comboBox.currentText() != "" and self.lineEdit_2.text() != "":
            if db_opt.check_person_is_new(self.comboBox.currentText()) == []:
                if len(self.comboBox.currentText()) == 9:
                    self.member_number = self.comboBox.currentText()
                    self.member_name = self.lineEdit_2.text()
                    self.pushButton.setEnabled(True)
                    self.label_2.setText(f"当前学员：{self.member_number} {self.member_name}")
                    # 保存新人员信息
                    db_opt.record_person((self.member_number,self.member_name))
                    self.textBrowser.setText(f'该新学员已录入数据库！')
                    self.comboBox.addItem(f"{self.member_number} {self.member_name}")
                    self.check_start = make_dir(f"{self.member_number}")
                    self.current_dir = f"person_dir\{self.member_number}"
                else:
                    self.textBrowser.setText(f'学号请输入9位有效数字！')
            else:
                [(number, name)] = db_opt.check_person_is_new(self.comboBox.currentText())
                if name == self.lineEdit_2.text():

                    self.member_number = self.comboBox.currentText()
                    self.member_name = self.lineEdit_2.text()
                    self.pushButton.setEnabled(True)
                    self.label_2.setText(f"当前学员：{self.member_number} {self.member_name}")
                    self.textBrowser.setText(f'该学员既往已在数据库中！')
                    self.check_start = make_dir(f"{self.member_number}")
                    self.current_dir = f"person_dir\{self.member_number}"
                else:
                    self.textBrowser.setText(f'该学号的学员已存在，请重新输入：\n学号：{number}\n姓名：{name}')

        else:
            pass

    def video_button(self):

        if (self.flag == 0):
            self.cap_video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.timer.start(50)
            self.flag += 1
            self.pushButton.setText("关闭摄像头")
            self.textBrowser.setText("已打开摄像头\n调整合适姿势后\n可点击”开始采集“按钮可采集图片\n如已有图片，将覆盖之前图片")
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)

        else:
            self.timer.stop()
            self.cap_video.release()
            self.label.clear()
            self.pushButton.setText("打开摄像头")
            self.textBrowser.setText("已关闭摄像头")
            self.flag = 0
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.on_recog = 0
            self.recognizer = None
            self.pushButton_6.setText("启动识别")
            self.pushButton_3.setEnabled(True)


    def catch_pic(self):
        self.on_cahch = 1
        self.textBrowser.setText(f'开始面部图片采集')
        self.pushButton_4.setEnabled(False)

    def show_viedo(self):
        ret, self.img = self.cap_video.read()

        if ret:
            self.img, self.img_gray, face_tacle = detector(self.img, r"model/haarcascade_frontalface_default.xml")
            self.show_cv_img(self.img)
            if face_tacle != [0, 0, 0, 0]:

                if self.on_cahch == 1:
                    self.check_start += 1
                    self.pic_add += 1
                    self.textBrowser.setText(f'已采集面部灰度图x{self.pic_add}')
                    make_pic(self.img_gray, face_tacle, pic_name=f"person_dir/{self.member_number}/{self.check_start}.png")
                    if self.pic_add == 10:
                        self.on_cahch = 0
                        self.pic_add = 0
                        self.check_start = 0
                        self.textBrowser.setText(f'已完成采集')
                        self.pushButton_4.setEnabled(True)
                if self.on_recog == 1:
                    recog_id, confidence = recognition_unit.do_recognize(self.recognizer, make_little_gray(self.img_gray,face_tacle))
                    if self.recog_id == recog_id:
                        self.textBrowser.setText(f"学号      姓名      置信度\n{recog_id} {self.recog_name} {confidence}")
                    else:
                        name = db_opt.num2name(recog_id)
                        self.recog_id = recog_id
                        self.recog_name = name


    def show_cv_img(self, img):
        shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        QtImg = QtGui.QImage(shrink.data,
                             shrink.shape[1],
                             shrink.shape[0],
                             shrink.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        jpg_out = QtGui.QPixmap(QtImg).scaled(
            self.label.width(), self.label.height())
        self.label.setPixmap(jpg_out)

    def go_train(self):
        is_trained = train.train_model()
        if is_trained == 1:
            self.textBrowser.setText(f'模型训练完成！')
        else:
            self.textBrowser.setText(f'数据不足，模型未完成训练！')

    def go_recog(self):
        if self.pushButton_6.text() == "启动识别":
            self.recognizer = recognition_unit.mk_recognizer()
            self.on_recog = 1
            self.textBrowser.setText(f'已开始识别人脸!')
            self.pushButton_6.setText("关闭人脸识别")
            self.pushButton_3.setEnabled(False)
        else:
            self.on_recog = 0
            self.recognizer = None
            self.textBrowser.setText(f'已关闭人脸!')
            self.pushButton_6.setText("启动识别")
            self.pushButton_3.setEnabled(True)

if __name__=="__main__":
    app = QApplication(sys.argv)
    myshow=Child()
    myshow.show()#显示
    sys.exit(app.exec_())