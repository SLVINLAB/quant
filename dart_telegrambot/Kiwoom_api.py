import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3
from datetime import date

day = date.today()
day2 = day.strftime('%Y-%m-%d')
directory = "C:/Users/Jin/Desktop/"
file = directory + day2 + ".db"
stock = "005930"


class Kiwoom(QAxWidget):

# 로그인 세팅
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()


# 코스피, 코스닥 종목코드 불러오기
    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

# 앞으로 함수를 호출할 때 쿼리의 베이스가 되는 Input 설정
    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

# rq_data / Query ==> 데이터 호출 Base Function / 요청하는 데이터 코드에 따라 다른 데이터 호출 가능

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10001_req":
            self._opt10001(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10001(self, rqname, trcode):
        i=0
        code = self._comm_get_data(trcode, "", rqname, i, "종목명")
        price = self._comm_get_data(trcode, "", rqname, i, "현재가")
        volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
        sr = self._comm_get_data(trcode, "", rqname, i, "등락율")
        self.stock = {'stockname': code, 'price': price, 'volume' : volume, 'return' : sr}

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def check_order(self):
        df2 = pd.read_sql("SELECT * FROM data", con, index_col=None)
        ret = abs(float(df2['price'][0]) / float(df2.tail(1)['price'])) - 1
        if ret > 0.02 :
            return True
            self.send_order("send_order_req", "0101", account, 1, code, num, price, "03", "")
        else :
            print('not yet')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    #while True:
    for i in range(10):
        time.sleep(1)
        kiwoom.set_input_value("종목코드", "005930")
        kiwoom.comm_rq_data("opt10001_req", "opt10001", 0, "0101")
        data = kiwoom.stock
        df = pd.DataFrame(data, columns=['stockname', 'price', 'volume', 'return'], index = [0])
        print(df)
        con = sqlite3.connect("C:/Users/Jin/Desktop/stock.db")
        df.to_sql("data", con, if_exists='append')
        kiwoom.check_order()
        account = kiwoom.comboBox.currentText()
        print(account)