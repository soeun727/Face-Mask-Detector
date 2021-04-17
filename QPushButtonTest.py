import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


class MyApp(QWidget):   #붕어ㅃㅇ틀

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):   #붕어빵 속에 있는애들
        btn1 = QPushButton('&Button1', self)    # 버튼 생성
        # self를 안붙이면 initUI에서만 유효한 함수 즉 붕어빵틀에 안들어가게 됨(self.btn1으로 하면 btn1은 밖의 함수에서도 사용할 수 있는 함수, 전역변수 개념)
        # self넣으면 얘도 붕어빵틀 안에 들어가게 됨
        btn1.setCheckable(True)             # button2와의 차이: 누른상태와 그렇지 않은 상태를 구분해줌
        btn1.toggle()                       # 상태를 바꿔줌

        btn2 = QPushButton(self)
        btn2.setText('Button&2')            # &: 바로가기 키를 지정하는 첨자, 실행시켰을 떄 alt+2 단축키를 사용하면 하면 바로 클릭이 활성화됨

        btn3 = QPushButton('Button3', self)
        btn3.setEnabled(False)      # False 설정시 버튼을 사용할 수 없음

        btn4 = QPushButton('Button4', self)
        btn4.setEnabled(False)  # False 설정시 버튼을 사용할 수 없음

        vbox = QVBoxLayout()  # 여러 위젯의 배치를 할 수 있도록 하는 요소(QVBoxLayout -> 수직 // QHBoxLayout -> 수평)
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        vbox.addWidget(btn4)

        self.setLayout(vbox)    # self 는 Qwidget을 상속 -> 즉 Qwidget의 레이아웃 처리
        self.setWindowTitle('QPushButton')
        self.setGeometry(300, 300, 300, 200)    # move랑 resize 기능을 하나의 함수(setGeometry)로 -> 앞에 두개는 위치 / 뒤에 두개는 크기
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()    #붕어빵 찍어내는 역할
    sys.exit(app.exec_())