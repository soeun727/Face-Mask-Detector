import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap

class MyApp(QWidget):   #붕어ㅃㅇ틀

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):   #붕어빵 속에 있는애들
        self.pixmap = QPixmap('python.jpg')
        self.label = QLabel(self)

        self.label.resize(self.pixmap.width(), self.pixmap.height())

        self.btn1 = QPushButton('show', self)
        self.btn1.clicked.connect(self.showImage)

        vbox = QVBoxLayout()  # 여러 위젯의 배치를 할 수 있도록 하는 요소(QVBoxLayout -> 수직 // QHBoxLayout -> 수평)
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn1)

        self.setLayout(vbox)    # self 는 Qwidget을 상속 -> 즉 Qwidget의 레이아웃 처리
        self.setWindowTitle('QPushButton')
        self.setGeometry(300, 300, 300, 200)    # move랑 resize 기능을 하나의 함수(setGeometry)로 -> 앞에 두개는 위치 / 뒤에 두개는 크기
        self.show()

    def showImage(self):
        self.label.setPixmap(self.pixmap)
        self.label.setContentsMargins(10, 10, 10, 10)
        self.label.resize(self.pixmap.width(), self.pixmap.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()    #붕어빵 찍어내는 역할
    sys.exit(app.exec_())