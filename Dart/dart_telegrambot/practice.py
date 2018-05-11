import sys
from PyQt5.QtWidgets import *
import Kiwoom

# 자동로그인 및 종목 데이터 호출 세팅
app = QApplication(sys.argv)
kiwoom = Kiwoom.Kiwoom()
kiwoom.comm_connect()
account_number = kiwoom.get_login_info("ACCNO")
account_number = account_number.split(';')[0]


# 공시에서 받아올 종목 코드
stockcode = '006360'
quantity = 10
signal = "HOLD"
kiwoom.signal(signal, stockcode, account_number, quantity)
