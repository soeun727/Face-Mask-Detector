# https://m.blog.naver.com/PostView.nhn?blogId=smilewhj&logNo=221066451394&proxyReferer=https:%2F%2Fwww.google.com%2F
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #label1
        label1 = QLabel('First Label', self)
        label1.setAlignment(Qt.AlignCenter)
        #label2
        self.label2 = QLabel('Second Label', self)      #showImage에서도 써야하기 때문에 self를 붙여줘야함
        self.label2.resize(400,400)

        font1 = label1.font()
        font1.setPointSize(20)
        label1.setFont(font1)

        #버튼 생성
        btn1 = QPushButton('&Enter', self)
        btn1.clicked.connect(self.showImage)        #버튼 누르면 출력되도록

        btn2 = QPushButton('&Cancel', self)


# 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.label2)
        layout.addWidget(btn1)
        layout.addWidget(btn2)

        self.setLayout(layout)

        self.setWindowTitle('Image')
        self.setGeometry(300,300,300,200)
        self.show()

    def showImage(self):
        self.label2.setPixmap(QPixmap("python.jpg"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=MyApp()
    sys.exit(app.exec_())

