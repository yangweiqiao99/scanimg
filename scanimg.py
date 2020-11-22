# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets

import cv2
import sys


from Ui_scanimg import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initTimer()
        self.vc = cv2.VideoCapture(1)
        self.timer.start(200)
        self.treeWidget.setColumnCount(1)
        root=QtWidgets.QTreeWidgetItem(self.treeWidget)
        root.setText(0,'案卷名称')
        
    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_pic)
    
    def show_pic(self):
        ret, img = self.vc.read()
        if not ret:
            print('read error!\n')
            return
        img=cv2.transpose(img)   #图像转制
        img=cv2.flip(img, 1)         #旋转90度
        cur_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        heigt, width  = cur_frame.shape[:2]
        #M3 = cv2.getRotationMatrix2D((width/2, heigt/2), -90, 1)
        #rest=cv2.warpAffine(cur_frame, M3, (width, heigt))
        
        pixmap = QImage(cur_frame, width, heigt, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(pixmap)
        self.label.setPixmap(pixmap)
        
    def start(self):
        self.timer.start(100)    

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
