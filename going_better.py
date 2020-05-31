from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
import sys
import qtawesome
import dlib
import numpy as np
import cv2
import pandas as pd
import os
import win32com.client
import time
from PyQt5.QtWidgets import *
from skimage import io
from register import Ui_MainWindow
from Adminui  import Ui_MainWindow2
import shutil
from datetime import timedelta, datetime

class Speak:
    def __init__(self):
        self.speak_out=win32com.client.Dispatch('SAPI.SPVOICE')
    def speak(self,data=''):
        self.speak_out.Speak(data)
        time.sleep(1)
path_make_dir = "face_image/"
cap = cv2.VideoCapture(0)
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
# Dlib 预测器 人脸检测
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 计算两个向量间的欧式距离 进行人脸识别
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    print("欧式距离: ", dist)
    if dist > 0.4:
        return "diff"
    else:
        return "same"

def get_128d_features(img_gray):
    dets = detector(img_gray, 1)
    shape = predictor(img_gray, dets[0])
    face_des = facerec.compute_face_descriptor(img_gray, shape)
    return face_des
#主界面
class MainUi(QtWidgets.QMainWindow):
    signal=QtCore.pyqtSignal()
    user_id=''
    def __init__(self):
        super().__init__()
        self.init_ui() #调用初始化的界面设置，展示界面的功能
    def init_ui(self):
        self.setFixedSize(1400, 1000)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.right_widget_1 = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget_1.setObjectName('right_widget_1')
        self.right_layout_1 = QtWidgets.QGridLayout()

        self.right_widget_2 = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget_2.setObjectName('right_widget_2')
        self.right_layout_2 = QtWidgets.QVBoxLayout()
        self.right_widget_2.setLayout(self.right_layout_2)  # 设置右侧部件布局为网格

        ##
        self.right_widget_1.setLayout(self.right_layout_1)  # 设置右侧部件布局为网格
        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.main_layout.addWidget(self.right_widget_1, 0, 2, 12, 10)  # 右侧部件_1在第0行第3列，占8行9列
##
        self.main_layout.addWidget(self.right_widget_2, 0, 2, 12, 10)

        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_max = QtWidgets.QPushButton("")  # 最大按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮

        self.left_label_1 = QtWidgets.QPushButton("注册功能")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("打卡功能")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("查看功能")
        self.left_label_3.setObjectName('left_label')
        self.left_label_4 = QtWidgets.QPushButton("扩展功能")
        self.left_label_4.setObjectName('left_label')

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.list-ol', color='white'), "人脸注册")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.user', color='white'), "上班打卡")
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.edit', color='white'), "下班打卡")
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.bar-chart', color='white'), "员工考勤查看")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.envelope', color='white'), "管理员考勤常看")
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.mail-reply', color='white'), "返回上层")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.weibo', color='white'), "员工注册")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.home', color='white'), "数据初始化")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.book', color='white'), "使用手册")
        self.left_button_9.setObjectName('left_button')
        self.left_xxx = QtWidgets.QPushButton(" ")
        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_max, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_4, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 12, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 13, 0, 1, 3)
        self.left_close.setFixedSize(20,20)  # 设置关闭按钮的大小
        self.left_max.setFixedSize(20,20)  # 设置最大化按钮大小
        self.left_mini.setFixedSize(20,20)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_max.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:20px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget#left_widget{
    background:gray;
    border-top:0px solid white;
    border-bottom:0px solid white;
    border-left:0px solid white;
    border-top-left-radius:10px;
    border-bottom-left-radius:10px;
}
        ''')
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        self.right_widget_1.setStyleSheet('''
                        QWidget#right_widget_1{
                            color:#232C51;
                            background:white;
                            border-top:0px solid darkGray;
                            border-bottom:0px solid darkGray;
                            border-right:0px solid darkGray;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                        }
                        QLabel#right_lable_1{
                            border:none;
                            font-size:16px;
                            font-weight:700;
                            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                        }
                    ''')



        self.init_right()
        self.init_right_show()
        self.setWindowOpacity(2)  # 设置窗口透明度
        self.right_widget.setStyleSheet("QWidget#right_widget{border-image:url(./picture/main2.jpg)}")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)
        self.left_close.clicked.connect(self.main_close)
        self.left_mini.clicked.connect(self.main_min)
        self.left_max.clicked.connect(self.main_max)
        self.left_button_1.clicked.connect(self.recode)
        self.left_button_2.clicked.connect(self.first_camera)
        self.left_button_3.clicked.connect(self.second_camera)
        self.left_button_4.clicked.connect(self.worker_table)
        self.left_button_5.clicked.connect(self.admin_table)
        self.left_button_6.clicked.connect(self.init_right)
        self.left_button_7.clicked.connect(self.register)
        self.left_button_8.clicked.connect(self.initDatabase)
        self.left_button_9.clicked.connect(self.how_work)

        self.right_widget.hide()
        self.right_widget_2.hide()
        self.register_flag = 0
        self.sc_number=0
#最小化最大化关闭
    def main_min(self):
        self.showMinimized()
    def main_max(self):  # 界面的最大化和正常化的切换
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    def main_close(self):
        exit()
#新建人员
    def recode(self):
        path_make_dir = "face_image/"
        self.id, self.okk = QInputDialog.getText(self, "标题", "输入工号：")
        name = self.read_name(self.id)
        if self.okk:
            if name is None:

                self.id = ''
                QMessageBox.question(self, "提示", "不存在该员工\n"
                                                 "请先注册", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                print(name)
                print(type(name[0]))
                self.name, self.ok = QInputDialog.getText(self, "标题", "输入姓名：")
                if self.ok:
                    if self.name == name[0]:
                        print(type(self.name))
                        os.makedirs(path_make_dir + self.id + self.name)
                        print("新建文件夹：" + self.id + self.name)
                        self.Duplicate_checking()
                    else:
                        self.name = ''
                        QMessageBox.question(self, "提示", "输入姓名有误\n"
                                                         "请先注册输入", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            '''接下来就是调用摄像头和受用者进行对比，如果数据库中的数据进行比对
                如果匹配成功，就不再提取，否则就提取使用者的脸部特征信息     '''
#人脸录入
    def Duplicate_checking(self):
        self.left_button1()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1000)
        self.sc_number=0
        # self.cap.open(0)
        while self.cap.isOpened():
            save_flag = 1
            flag, img_rd= self.cap.read()
            # QtWidgets.QApplication.processEvents()
            kk=cv2.waitKey(1)
            img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)
            # 人脸数 faces
            faces = detector(img_gray, 0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
            # 添加说明 / add some statements
            cv2.putText(img_rd, "S: Save current face", (20, 400), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
            if len(faces) != 0:
                # 矩形框 / show the rectangle box
                for k, d in enumerate(faces):
                    # 计算矩形大小
                    # we need to compute the width and height of the box
                    # (x,y), (宽度width, 高度height)
                    pos_start = tuple([d.left(), d.top()])
                    pos_end = tuple([d.right(), d.bottom()])
                    # 计算矩形框大小 / compute the size of rectangle box
                    height = (d.bottom() - d.top())
                    width = (d.right() - d.left())
                    hh = int(height / 2)
                    ww = int(width / 2)
                    # 设置颜色 / the color of rectangle of faces detected
                    color_rectangle = (255, 255, 255)
                    # 判断人脸矩形框是否超出 480x640
                    if (d.right() + ww) > 640 or (d.bottom() + hh > 480) or (d.left() - ww < 0) or (d.top() - hh < 0):
                        cv2.putText(img_rd, "OUT OF RANGE", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                        color_rectangle = (0, 0, 255)
                        save_flag = 0
                        if kk == ord('s'):
                            print("请调整位置 / Please adjust your position")
                    else:
                        color_rectangle = (255, 255, 255)
                        save_flag = 1
                    cv2.rectangle(img_rd,
                                  tuple([d.left() - ww, d.top() - hh]),
                                  tuple([d.right() + ww, d.bottom() + hh]),
                                  color_rectangle, 2)
                    # 根据人脸大小生成空的图像 / create blank image according to the size of face detected
                    im_blank = np.zeros((int(height * 2), width * 2, 3), np.uint8)
                    if save_flag:
                        # 按下 's' 保存摄像头中的人脸到本地 / press 's' to save faces into local images
                        if kk & 0xFF== ord('s'):
                            print("2")
                            self.sc_number += 1
                            for ii in range(height * 2):
                                for jj in range(width * 2):
                                    im_blank[ii][jj] = img_rd[d.top() - hh + ii][d.left() - ww + jj]
                            # cv2.imwrite(path_make_dir + self.name + "/img_face_" + str(self.sc_number) + ".jpg", im_blank)
                                    # print("标记3")
                            cv2.imencode('.jpg', im_blank)[1].tofile(
                                path_make_dir +self.id+ self.name + "/img_face_" + str(self.sc_number) + ".jpg")  # 正确方法
                            # print("标记4")
                            print("写入本地：", str(path_make_dir + self.name) + "/img_face_" + str(self.sc_number) + ".jpg")
                # cv2.rectangle(img_rd, tuple([faces[0].left(), faces[0].top()]), tuple([faces[0].right(), faces[0].bottom()]),
                #               (100, 255, 0), 2)
                # cv2.putText(img_rd,name,pos, font, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
            if kk == ord('q'):
                print("1")
                # self.right_label_0.close()
                self.Write_info()
                break
            cv2.namedWindow("camera", 0)
            cv2.imshow("camera", img_rd)

        self.cap.release()
        # self.Write_info()
        cv2.destroyAllWindows()



            # cv2.putText(img_rd, "faces: " + str(len(faces)), (10, 40), font, 1, (0, 255, 200), 1, cv2.LINE_AA)
            # height, width = img_rd.shape[:2]
            # image1 = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
            # showImage = QtGui.QImage(image1, width, height, QtGui.QImage.Format_RGB888)
            # self.right_label_0.setPixmap(QtGui.QPixmap.fromImage(showImage))
#信息写入
    def Write_info(self):
        if self.sc_number == 0 and len(self.id+self.name) > 0:
            if os.path.exists(path_make_dir +self.id+ self.name):
                shutil.rmtree(path_make_dir + self.id+ self.name)
                print("您未保存截图，已删除姓名文件夹", path_make_dir + self.id+ self.name)

        if self.register_flag == 0 and self.sc_number != 0:
            pics = os.listdir(path_make_dir + self.id+ self.name)
            feature_list = []
            feature_average = []
            for i in range(len(pics)):
                pic_path = path_make_dir + self.id+ self.name + "/" + pics[i]
                print("正在读的人脸图像：", pic_path)
                img = io.imread(pic_path)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                dets = detector(img_gray, 1)
                if len(dets) != 0:
                    shape = predictor(img_gray, dets[0])
                    face_descriptor = facerec.compute_face_descriptor(img_gray, shape)
                    feature_list.append(face_descriptor)
                else:
                    print("未在照片中识别到人脸")

            if len(feature_list) > 0:
                for j in range(128):
                    feature_average.append(0)
                    for i in range(len(feature_list)):
                        feature_average[j] += feature_list[i][j]
                        print(feature_list[i][j])
                        print(type(feature_list[i][j]))
                    feature_average[j] = (feature_average[j]) / len(feature_list)
                mysql_face=' '.join([str(x) for x in feature_average])
                self.add_info(self.id,self.name,mysql_face)
                begin = Speak()
                begin.speak("人脸信息入库成功")

    def left_button1(self):
        self.right_label_0 = QtWidgets.QLabel(self)
        self.right_label_0.setObjectName("right_label_0")
        pixmap = QtGui.QPixmap("picture/main.jpg")  # 按指定路径找到图片
        self.right_label_0.setPixmap(pixmap)  # 在label上显示图片
        self.right_label_0.setScaledContents(True)  # 让图片自适应label大小
        self.right_layout_1.addWidget(self.right_label_0, 1, 1, 1, 1)
#图背景
    def cap_close(self):
        pass
    def init_right(self):
        self.right_label_0 = QtWidgets.QLabel(self)
        self.right_label_0.setObjectName("right_label_0")
        pixmap = QtGui.QPixmap("picture/main.jpg")  # 按指定路径找到图片
        self.right_label_0.setPixmap(pixmap)  # 在label上显示图片
        self.right_label_0.setScaledContents(True)  # 让图片自适应label大小
        self.right_layout_1.addWidget(self.right_label_0, 1, 1, 1,1)
        movie=QtGui.QMovie('recognition.gif')
        movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.right_label_0.setMovie(movie)
        movie.start()
#使用手册
    def how_work(self):
        pixmap = QtGui.QPixmap("picture/how_work.png")  # 按指定路径找到图片
        self.right_label_0.setPixmap(pixmap)  # 在label上显示图片
        self.right_label_0.setScaledContents(True)  # 让图片自适应label大小
#签到
    def first_camera(self):
        self.left_button1()
        self.cap = cv2.VideoCapture()
        self.cap.open(0)
        features_known_arr = self.read_work()
        face_type = 1
        while self.cap.isOpened():
            flag, img = self.cap.read()
            QtWidgets.QApplication.processEvents()
            cv2.waitKey(1)
            begin = Speak()
            dets = detector(img, 1)

            font = cv2.FONT_HERSHEY_SIMPLEX
            if len(dets) != 0:
                shape = predictor(img, dets[0])
                features_cap = facerec.compute_face_descriptor(img, shape)
                name = "Welcome"
                pos = tuple([(int)((dets[0].left() + dets[0].right()) / 2) - 50
                                , dets[0].bottom() + 20])
                for i in range(len(features_known_arr)):
                    self.pun_day_num = 0
                    print('1111')
                    compare = return_euclidean_distance(features_cap, features_known_arr[i][1:])
                    if compare == "same":  # 找到了相似脸
                        name = features_known_arr[i][0]
                        print(name)
                        recoder = []
                        recoder.append(int(name[:6]))
                        recoder.append(name[6:])
                        now = time.time()
                        date = time.strftime('%Y/%m/%d', time.localtime(now))
                        s_time = time.strftime('%H:%M:%S', time.localtime(now))
                        number = int(now)
                        recoder.append(date)
                        recoder.append(s_time)
                        recoder.append(number)
                        a = self.find_time('sbdk', recoder)
                        if a == None:
                            begin = Speak()
                            begin.speak(data=str(name) + "签到成功")
                            self.add_dk(recoder, face_type)
                            print(str(name) + "签到成功")
                        else:
                            print(str(name) + '已签到,请勿重复签到')
                            begin.speak(data=str(name) + '已签到,请勿重复签到')
                            break

                cv2.rectangle(img, tuple([dets[0].left(), dets[0].top()]), tuple([dets[0].right(), dets[0].bottom()]),
                              (100, 255, 0), 2)
                cv2.putText(img, name, pos, font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(img, "faces: " + str(len(dets)), (10, 40), font, 1, (0, 255, 200), 1, cv2.LINE_AA)
            height, width = img.shape[:2]
            image1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(image1, width, height, QtGui.QImage.Format_RGB888)
            self.right_label_0.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def second_camera(self):
        self.left_button1()
        self.cap = cv2.VideoCapture()
        self.cap.open(0)
        features_known_arr=self.read_work()
        face_type=2
        while self.cap.isOpened():
            flag, img = self.cap.read()
            QtWidgets.QApplication.processEvents()
            cv2.waitKey(1)
            begin = Speak()
            dets = detector(img, 1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            if len(dets) != 0:
                shape = predictor(img, dets[0])
                features_cap = facerec.compute_face_descriptor(img, shape)
                name = "Welcome"
                pos = tuple([(int)((dets[0].left() + dets[0].right()) / 2) - 50
                                , dets[0].bottom() + 20])
                for i in range(len(features_known_arr)):
                    compare = return_euclidean_distance(features_cap, features_known_arr[i][1:])
                    if compare == "same":  # 找到了相似脸
                        name = features_known_arr[i][0]
                        print(name)
                        recoder = []
                        recoder.append(int(name[:6]))
                        recoder.append(name[6:])
                        now =time.time()
                        date = time.strftime('%Y/%m/%d',time.localtime(now))
                        s_time= time.strftime('%H:%M:%S',time.localtime(now))
                        number=int(now)
                        recoder.append(date)
                        recoder.append(s_time)
                        recoder.append(number)
                        late_time=self.find_time('xbdk',recoder)
                        if late_time==None:
                            begin = Speak()
                            begin.speak(data=str(name) + "签到成功")
                            first_time=self.find_time('sbdk',recoder)
                            # 判断工作时长是否满足要求
                            if number-first_time[0]<=28800:
                                yes_no='no'
                            else:
                                yes_no = 'yes'
                            recoder.append(yes_no)
                            self.add_dk(recoder, face_type)
                            print(2)
                        else:
                            begin.speak(data=str(name) + '已签到,请勿重复签到')
                            break

                cv2.rectangle(img, tuple([dets[0].left(), dets[0].top()]), tuple([dets[0].right(), dets[0].bottom()]),
                              (100, 255, 0), 2)
                cv2.putText(img, name, pos, font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(img, "faces: " + str(len(dets)), (10, 40), font, 1, (0, 255, 200), 1, cv2.LINE_AA)
            height, width = img.shape[:2]
            image1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(image1,width,height,QtGui.QImage.Format_RGB888)
            self.right_label_0.setPixmap(QtGui.QPixmap.fromImage(showImage))
#数据库操作
    #建立mysql库连接
    def con_mysql(self):
        return pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='face', charset='utf8')
    # 添加信息
    def add_info(self,id,name,face_date):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute("insert into worker_info values('%s','%s','%s')" % (id,name,face_date))
        conn.commit()
        cursor.close()

    def add_dk(self,recoders,type):
        conn = self.con_mysql()
        cursor = conn.cursor()
        if type == 1:
            cursor.execute("insert into sbdk values('%s','%s','%s','%s','%s')" % (recoders[0],recoders[1],recoders[2],
                                                                                  recoders[3],recoders[4]))
        if type == 2:
            cursor.execute("insert into xbdk values('%s','%s','%s','%s','%s','%s')" % (recoders[0], recoders[1], recoders[2],
                                                                                  recoders[3], recoders[4],recoders[5]))
        conn.commit()
        cursor.close()
    #查找信息
    def find_time(self,table, work):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute(
            "select number from %s where id='%s' and name='%s' and datetime='%s'" % (table, work[0], work[1], work[2]))
        r = cursor.fetchone()
        conn.commit()
        cursor.close()
        return r
    #
    def read_work(self):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute("select * from worker_info")
        r = list(cursor.fetchall())
        a = []
        for i in range(len(r)):
            b = [str(r[i][0]) + r[i][1]]
            for i in r[i][2].split(" "):
                b.append(float(i))
            a.append(b)
        conn.commit()
        cursor.close()
        return a

    def read_data(self,number):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute("select * from xbdk where id='%s'"%number)
        r = list(cursor.fetchall())
        conn.commit()
        cursor.close()
        return r

    def read_name(self,number):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute("select name from worker where id='%s'" % number)
        r = cursor.fetchone()
        conn.commit()
        cursor.close()
        return r

    def admin_power(self):
        self.admin, self.okk = QInputDialog.getText(self, "标题", "输入管理员工号：")
        if self.okk:
            self.admin_password, self.okok = QInputDialog.getText(self, "标题", "输入密码：")
            if self.okok:
                if self.admin=='admin' and self.admin_password=='admin':
                    return True
                else:
                    return False
# 数据可视化界面初始化界面构造函数
    def init_right_show(self):
        self.listw = QtWidgets.QListWidget()
        self._translate = QtCore.QCoreApplication.translate
        # self.right_combox = QtWidgets.QComboBox(self.right_widget_2)
        # self.right_combox.addItem("")
        # self.right_combox.addItem("")
        # self.right_combox.addItem("")
        # self.right_combox.addItem("")
        # self.right_combox.setMinimumSize(30, 30)
        # self.right_combox.currentIndexChanged.connect(self.right_combox_click)
        self.right_browser = QWebEngineView()
        # self.create_data_image()

        self.right_browser.load(QtCore.QUrl('D:/python/test/render.html'))
        self.right_browser.setMinimumSize(600, 600)
        # self.right_combox.setItemText(0, self._translate("right_widget_2", "lzf"))
        # self.right_combox.setItemText(1, self._translate("right_widget_2", "qz"))
        # self.right_combox.setItemText(2, self._translate("right_widget_2", "hzx"))
        # self.right_combox.setItemText(3, self._translate("right_widget_2", "  "))
        # self.right_layout_2.addWidget(self.right_combox, 0)
        self.right_layout_2.addWidget(self.right_browser, 1)
        self.right_widget_2.setStyleSheet('''
                                QWidget#right_widget_2{
                                    color:#232C51;
                                    background:white;
                                    border-top:1px solid darkGray;
                                    border-bottom:1px solid darkGray;
                                    border-right:1px solid darkGray;
                                    border-top-right-radius:10px;
                                    border-bottom-right-radius:10px;
                                }
                                QComboBox{
            border:none;
            color:gray;
            font-size:30px;
            height:40px;
            padding-left:5px;
            padding-right:10px;
            text-align:left;
        }
        QComboBox:hover{
            color:black;
            border:1px solid #F3F3F5;
            border-radius:10px;
            background:LightGray;
        }
                            ''')
#员工个人查看
    def worker_table(self):
        self.s = Table()
        self.s.show()
#管理员查看
    def admin_table(self):
        power=self.admin_power()
        if power is True:
            self.ad = Admin()
            self.ad.show()
        else:
            QMessageBox.question(self, "提示", "账号或密码错误", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

# #注册功能
    def register(self):
        power = self.admin_power()
        if power is True:
            self.zhuce = Register()
            self.zhuce.show()
        else:
            QMessageBox.question(self, "提示", "账号或密码错误", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
#数据初始化
    def initDatabase(self):

        power = self.admin_power()
        if power is True:
            conn = self.con_mysql()  # 建立数据库连接
            cur = conn.cursor()  # 得到游标对象
            cur.execute("drop table worker")
            cur.execute("drop table worker_info")
            cur.execute("drop table sbdk")
            cur.execute("drop table xbdk")
            cur.execute('''create table if not exists worker
                (id int not null primary key,
                password varchar(20) not null,
                name varchar(10) not null,
                sex varchar(10) not null,
                age varchar(10) not null,
                phone varchar(11) not null)''')
            cur.execute('''create table if not exists worker_info
            (id int not null primary key,
            name varchar(10) not null,
            face_feature text not null)''')
            cur.execute('''create table if not exists sbdk
             (id int not null,
             name varchar(10) not null,
             datetime text not null,
             s_time text not null,
             number int(11))''')

            cur.execute('''create table if not exists xbdk
                 (id int not null,
                 name varchar(10) not null,
                 datetime text not null,
                 x_time text not null,
                 number int(11),
                 yes_no varchar(10))''')
            cur.close()
            conn.commit()
            conn.close()
        else:
            QMessageBox.question(self, "提示", "账号或密码错误", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

#注册界面
class Register(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Register,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.set)

    def set(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='face', charset='utf8')
        cursor = conn.cursor()
        self.id = self.lineEdit.text()
        self.password = self.lineEdit_2.text()
        self.name = self.lineEdit_3.text()
        self.sex = self.lineEdit_4.text()
        self.age = self.lineEdit_5.text()
        self.phone=self.lineEdit_6.text()
        print(type(self.phone))
        cursor.execute("select * from worker where id = '%s'"%self.id)
        user =cursor.fetchall()
        if self.id == "" or self.password == "" or self.name == "" or self.sex == "" or self.age == ""or self.phone == "":
            QMessageBox.warning(self,
                                "警告",
                                "所填内容不能为空",
                                QMessageBox.Yes)
        elif self.id.isdigit() is False or len(self.id) !=6:
            QMessageBox.warning(self,
                                "警告",
                                "账号为数字，且为6位",
                                QMessageBox.Yes)
        elif user != ():
            QMessageBox.warning(self,
                                "警告",
                                "该员工已存在！",
                                QMessageBox.Yes)
        elif self.sex!='男' and self.sex!='女':
            QMessageBox.warning(self,
                                "警告",
                                "性别输入不规范，输入男或女",
                                QMessageBox.Yes)
        elif self.phone.isdigit() is False or len(self.phone)!=11:
            QMessageBox.warning(self,
                                "警告",
                                "手机号码为数字，且为11位",
                                QMessageBox.Yes)
        else:
            print('zhike')
            cursor.execute("insert into worker values('%s','%s','%s','%s','%s','%s')" % (
                  int(self.id),self.password,self.name,self.sex,self.age,self.phone))
            print('bing')
            conn.commit()
            cursor.close()
            QMessageBox.warning(self,
                                "警告",
                                "注册成功",
                                QMessageBox.Yes)
#员工个人考勤界面
class Table(QWidget):
    def __init__(self):
        super(Table, self).__init__()
        self.initUI()
    def initUI(self):
        #设置标题与初始大小
        self.setWindowTitle("员工个人考勤表")
        self.resize(430, 230);
        user_id, self.ook = QInputDialog.getText(self, "标题", "输入工号：")
        if self.ook:
            yg_password=self.read_password(user_id)
            password, self.ok = QInputDialog.getText(self, "标题", "输入密码：")
            if yg_password!=None and password==yg_password[0]:
                print('1111')
                table_data = self.read_data(user_id)
                len_table = len(table_data)
                self.tableWidget = QTableWidget(len_table, 6)
                self.tableWidget.setHorizontalHeaderLabels(['员工编号','员工姓名', '年月日', '上班打卡时间','下班打卡时间','是否满足工作时长'])
                layout = QVBoxLayout()
                layout.addWidget(self.tableWidget)
                for i in range(len_table):
                    for j in range(6):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(table_data[i][j])))
                self.setLayout(layout)
                self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            else:
                QMessageBox.question(self, "提示", "员工工号或密码错误", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                self.hide()
                print('1')


    def con_mysql(self):
        return pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='face', charset='utf8')
    def read_data(self,number):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute("select sbdk.id,sbdk.name,sbdk.datetime,sbdk.s_time,xbdk.x_time,xbdk.yes_no from sbdk"
                       " inner join xbdk on (sbdk.id=xbdk.id and sbdk.name=xbdk.name and sbdk.datetime=xbdk.datetime)"
                       " where sbdk.id='%s' "%number)
        r = list(cursor.fetchall())
        conn.commit()
        cursor.close()
        return r
    def read_password(self,number):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute("select password from worker where id='%s'" % number)
        r = cursor.fetchone()
        conn.commit()
        cursor.close()
        return r
#管理员界面
class Admin(QMainWindow,Ui_MainWindow2):
    def __init__(self):
        print('youhuai')
        super(Admin,self).__init__()
        self.setupUi(self)
        print('222')
        # self.pushButton.close()
        # setEnabled()设置按钮是否可以使用，当设置为False的时候，按钮变成不可用状态，点击它不会发射信号
        # self.btn3.setEnabled(False)
        self.actionlishi.triggered.connect(self.lishi)
        self.actionzuori.triggered.connect(self.yesterday)
        self.actionasda.triggered.connect(self.nowday)
        self.pushButton.clicked.connect(self.find_number)
        self.pushButton_2.clicked.connect(self.find_name)
        self.pushButton_3.clicked.connect(self.find_date)

        # self.actionasda.triggered.connect(self.)
    def nowday(self):
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        now = time.time()
        date = time.strftime('%Y/%m/%d', time.localtime(now))
        all_data = self.read_nowday(date)
        len_all = len(all_data)
        print('2')
        self.tableWidget.setColumnCount(6)  # 列
        self.tableWidget.setRowCount(len_all)  # 行
        self.tableWidget.setHorizontalHeaderLabels(['员工编号', '员工姓名', '年月日', '上班打卡时间', '下班打卡时间', '是否满足工作时长'])
        for i in range(len_all):
            for j in range(6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(all_data[i][j])))
        # self.setLayout(layout)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    def yesterday(self):
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        yesterday = datetime.today() + timedelta(-1)
        yesterday_format = yesterday.strftime('%Y/%m/%d')
        all_data = self.read_nowday(yesterday_format)
        len_all = len(all_data)
        print('2')
        self.tableWidget.setColumnCount(6)  # 列
        self.tableWidget.setRowCount(len_all)  # 行
        self.tableWidget.setHorizontalHeaderLabels(['员工编号', '员工姓名', '年月日', '上班打卡时间', '下班打卡时间', '是否满足工作时长'])
        for i in range(len_all):
            for j in range(6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(all_data[i][j])))
        # self.setLayout(layout)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def lishi(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        all_data=self.read_data()
        len_all=len(all_data)
        self.tableWidget.setColumnCount(6)#列
        self.tableWidget.setRowCount(len_all)#行
        self.tableWidget.setHorizontalHeaderLabels(['员工编号', '员工姓名', '年月日', '上班打卡时间', '下班打卡时间', '是否满足工作时长'])
        for i in range(len_all):
            for j in range(6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(all_data[i][j])))
        # self.setLayout(layout)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def find_number(self):
        # self.lineEdit.getTextMargins()
        id=self.lineEdit.text()
        print(id)
        all_data = self.find('sbdk.id',id)
        len_all = len(all_data)
        self.tableWidget.setColumnCount(6)  # 列
        self.tableWidget.setRowCount(len_all)  # 行
        self.tableWidget.setHorizontalHeaderLabels(['员工编号', '员工姓名', '年月日', '上班打卡时间', '下班打卡时间', '是否满足工作时长'])
        for i in range(len_all):
            for j in range(6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(all_data[i][j])))
        # self.setLayout(layout)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def find_name(self):
        # self.lineEdit.getTextMargins()
        name=self.lineEdit_2.text()
        print(name)
        all_data = self.find('sbdk.name',name)
        len_all = len(all_data)
        self.tableWidget.setColumnCount(6)  # 列
        self.tableWidget.setRowCount(len_all)  # 行
        self.tableWidget.setHorizontalHeaderLabels(['员工编号', '员工姓名', '年月日', '上班打卡时间', '下班打卡时间', '是否满足工作时长'])
        for i in range(len_all):
            for j in range(6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(all_data[i][j])))
        # self.setLayout(layout)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def find_date(self):
        # self.lineEdit.getTextMargins()
        f_month=self.comboBox.currentText()
        f_day=self.comboBox_2.currentText()
        print(type(f_month))
        print(f_day)
        if len(f_month)>0:
            f_date=f_month+'/'+f_day
            all_data = self.find_datetime(f_date)
            len_all = len(all_data)
            self.tableWidget.setColumnCount(6)  # 列
            self.tableWidget.setRowCount(len_all)  # 行
            self.tableWidget.setHorizontalHeaderLabels(['员工编号', '员工姓名', '年月日', '上班打卡时间', '下班打卡时间', '是否满足工作时长'])
            for i in range(len_all):
                for j in range(6):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(all_data[i][j])))
            # self.setLayout(layout)
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def con_mysql(self):
        return pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='face', charset='utf8')
    def read_nowday(self,data):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute("select sbdk.id,sbdk.name,sbdk.datetime,sbdk.s_time,xbdk.x_time,xbdk.yes_no from sbdk"
                       " inner join xbdk on (sbdk.id=xbdk.id and sbdk.name=xbdk.name and sbdk.datetime=xbdk.datetime)"
                       " where sbdk.datetime='%s' "%data)
        r = list(cursor.fetchall())
        conn.commit()
        cursor.close()
        return r
    def read_data(self):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute("select sbdk.id,sbdk.name,sbdk.datetime,sbdk.s_time,xbdk.x_time,xbdk.yes_no from sbdk"
                       " inner join xbdk on (sbdk.id=xbdk.id and sbdk.name=xbdk.name and sbdk.datetime=xbdk.datetime)"
                       )
        r = list(cursor.fetchall())
        conn.commit()
        cursor.close()
        return r
    def find(self,shuxing,number):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute("select sbdk.id,sbdk.name,sbdk.datetime,sbdk.s_time,xbdk.x_time,xbdk.yes_no from sbdk"
                       " inner join xbdk on (sbdk.id=xbdk.id and sbdk.name=xbdk.name and sbdk.datetime=xbdk.datetime)"
                       " where %s='%s' "%(shuxing,number))
        r = list(cursor.fetchall())
        conn.commit()
        cursor.close()
        return r
    def find_datetime(self,date):
        conn = self.con_mysql()
        cursor = conn.cursor()
        cursor.execute("select sbdk.id,sbdk.name,sbdk.datetime,sbdk.s_time,xbdk.x_time,xbdk.yes_no from sbdk"
                       " inner join xbdk on (sbdk.id=xbdk.id and sbdk.name=xbdk.name and sbdk.datetime=xbdk.datetime)"
                       " where sbdk.datetime LIKE '%%%s%%'"%date)
        r = list(cursor.fetchall())
        conn.commit()
        cursor.close()
        return r

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    # worker=Register_main()
    gui.show()
    # gui.signal.connect(worker.show)

    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
