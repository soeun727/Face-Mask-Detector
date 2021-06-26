## Ex 3-1. 창 띄우기.
import sys
from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(QWidget):  # QWidget이 setwindow, move, resize를 모두 포함하고 있음(class는 붕어빵 틀- 이 틀을 찍어내는 instance가 ex)
    def __init__(self):  # 초기화자로 ex가 붕어빵을 찍어내는 순간 자동으로 가장 먼저 실행되는 함수
        super().__init__()  # super는 QWidget을 상속해서 생성자를 불러온다는 의미
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')
        self.move(300, 300)  # 창을 출력할 위치(창 안의 것들도 이동시키는 함수가 move)
        self.resize(400, 200)  # 창의 크기
        self.show()  # 창을 화면에 보여줌


if __name__ == '__main__':  # 자동으로 정의되어있는 키워드(__~), print(__name__) 출력하면 __main__출력됨
    app = QApplication(sys.argv)  # pyqt를 돌리기 위해서 필수적인 코드, app 만들어두기 위함
    ex = MyApp()  # 붕어빵을 찍어내는 역할의 ex / 이 라인을 거침으로써 실행가능한 붕어빵인 class 생성
    sys.exit(app.exec_())  # 생성된 애플리케이션을 자식 프로세스로 실행하기 위함(오류 발생시 디버깅 위한 코드)

