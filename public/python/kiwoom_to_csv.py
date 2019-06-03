import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *
import pandas as pd
from PyQt5.QtCore import *
from datetime import date, timedelta
from datetime import datetime
import time

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.day = (date.today() - timedelta(1)).strftime('%Y%m%d')

        # Kiwoom Login
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        # OpenAPI+ Event
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)

        label = QLabel('종목코드:', self)
        label.move(20, 20)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(80, 20)

        btn1 = QPushButton("CSV내보내기", self)
        btn1.move(190, 20)
        btn1.clicked.connect(self.btn1_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")

    # 데이터 갯수 카운팅
    def dataCount(self, trcode, rqname):
        cnt = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        print(cnt)
        return cnt

    def set_input_value(self, id, value):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()  
  
    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _opt10081(self, rqname, trcode):
        data_cnt = self.dataCount(trcode, rqname)
        for i in range(1, 91):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            # date = datetime.datetime.strptime(date, "%y%m%d")
            # date = datetime.datetime.strftime(date, "%y-%m-%d")
            ndate = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")

            self.kiwoom.ohlcv['date'].append(ndate)
            self.kiwoom.ohlcv['close'].append(int(close))

    # 데이터 받는 부분
    def receive_trdata(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        print("receive_tr_data call")
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10080_req":
            self._opt10080(rqname, trcode)
        elif rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def data_to_CSV(self, code):
        self.kiwoom.ohlcv = {'date': [], 'close': []}
        date = self.day
        print(date)

        # self.set_input_value("종목코드", code)
        # self.set_input_value("기준일자", date)
        # self.set_input_value("수정주가구분", 1)
        self.comm_rq_data("opt10081_req", "opt10081", 0, "0101")

        while self.remained_data == True:
             time.sleep(0.2)
             self.set_input_value("종목코드", code)
             self.set_input_value("기준일자", date)
             self.set_input_value("수정주가구분", 1)
             self.comm_rq_data("opt10081_req", "opt10081", 2, "0101")

        df = pd.DataFrame(self.kiwoom.ohlcv, columns=['close'], index=self.kiwoom.ohlcv['date'])
        df.to_csv('./' + self.get_master_code_name(code) + '.csv', mode='w')

    def get_master_code_name(self, code):
        code_name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

  # 버튼 클릭시
    def btn1_clicked(self):
        code = self.code_edit.text()
        if code is None:
            exit(1)
        self.text_edit.append("종목코드: " + code)
        self.kiwoom.ohlcv = {'date': [], 'close': []}

        # SetInputValue
        self.set_input_value("종목코드", code)
        self.set_input_value("기준일자", date)
        self.set_input_value("수정주가구분", "1")

        self.data_to_CSV(code)

# START!
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()