import sys
import datetime
import cv2
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

import db_opt
from detection import detector
import recognition_unit
from pic_maker import make_little_gray
from ui.Ui_detector import Ui_detector


class Child_2(QDialog, Ui_detector):
    def __init__(self, parent=None):
        super(Child_2, self).__init__()
        self.setupUi(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_viedo)
        self.pushButton.clicked.connect(self.video_button)
        self.pushButton_1.clicked.connect(self.go_recog)

        self.pushButton_1.setEnabled(False)
        self.on_recog = 0
        self.flag = 0
        self.current_row_num = 0
        self.tableWidget.setColumnWidth(0, 110)
        self.tableWidget.setColumnWidth(1, 90)
        self.tableWidget.setColumnWidth(2, 200)
        self.recog_times = 0

    def video_button(self):
        if (self.flag == 0):
            self.cap_video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.timer.start(50)
            self.flag += 1
            self.pushButton.setText("关闭摄像头")
            self.textBrowser.setText("已打开摄像头\n调整合适姿势后\n可点击”签到“按钮")
            self.pushButton_1.setEnabled(True)


        else:
            self.timer.stop()
            self.cap_video.release()
            self.label.clear()
            self.pushButton.setText("打开摄像头")
            self.textBrowser.setText("已关闭摄像头")
            self.flag = 0
            self.pushButton_1.setEnabled(False)

            # 关联人脸识别按钮
            self.on_recog = 0
            self.recognizer = None


    def catch_pic(self):
        self.on_cahch = 1
        self.textBrowser.setText(f'开始面部图片采集')


    def show_viedo(self):
        ret, self.img = self.cap_video.read()

        if ret:
            self.img, self.img_gray, face_tacle = detector(self.img, r"model/haarcascade_frontalface_default.xml")
            self.show_cv_img(self.img)
            if face_tacle != [0, 0, 0, 0]:
                if self.recog_times <= 20:
                    if self.on_recog == 1:
                        recog_id, confidence = recognition_unit.do_recognize(self.recognizer, make_little_gray(self.img_gray,face_tacle))
                        if confidence < 80:
                            print(f"confidence: {confidence}")
                            recog_name = db_opt.num2name(recog_id)
                            recog_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                            db_opt.sign2db(recog_id, recog_name, recog_time) # 存储至数据库

                            self.textBrowser.setText(f"签到成功！\n学号      姓名      签到时间\n{recog_id} {recog_name} {recog_time}")
                            j = 0

                            for i in [recog_id, recog_name, recog_time]:
                                newItem = QTableWidgetItem(f"{i}")
                                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) # 居中
                                self.tableWidget.setItem(self.current_row_num, j, newItem)
                                j += 1

                            self.current_row_num += 1
                            self.tableWidget.insertRow(self.current_row_num) # 在某行插入一空行
                            self.pushButton_1.setEnabled(True)
                            self.on_recog = 0
                            self.recog_times = 0
                        else:
                            self.recog_times += 1
                else:
                    self.recog_times = 0
                    self.on_recog = 0
                    self.textBrowser.setText(f"签到失败！请重新签到")
                    self.pushButton_1.setEnabled(True)


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

    def go_recog(self):
        if self.pushButton_1.text() == "签到":
            self.recognizer = recognition_unit.mk_recognizer()
            self.on_recog = 1
            self.textBrowser.setText(f'已开始识别人脸!')
            self.pushButton_1.setEnabled(False)


if __name__=="__main__":
    app = QApplication(sys.argv)
    myshow=Child_2()
    myshow.show()#显示
    sys.exit(app.exec_())