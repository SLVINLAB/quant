import sys
from PyQt5.QtWidgets import *
import pandas as pd
import Kiwoom

# 자동로그인 및 종목 데이터 호출 세팅
app = QApplication(sys.argv)
kiwoom = Kiwoom.Kiwoom()
kiwoom.comm_connect()
account_number = kiwoom.get_login_info("ACCNO")
account_number = account_number.split(';')[0]

# 공시에서 받아올 종목 코드
stockcode = '006360'

kiwoom.set_input_value("종목코드", stockcode)
kiwoom.comm_rq_data("opt10001_req", "opt10001", 0, "0101")
df_stock = pd.DataFrame()
# 구조 : 공시가 뜬 종목의 데이터를 데이터 프레임으로 계속 쌓고,
# [1] 2% 이상 주식이 올랐을 때 매수
# [2] 데이터를 쌓기 시작 한 후 고가대비 3% 떨어졌으면 매도함

while True :
    data = kiwoom.stock
    df = pd.DataFrame(data, columns=['stockname', 'price','volume', 'return', 'high'], index=[0])
    print(df)
    df_stock = df_stock.append(df, ignore_index=True)
    print(df_stock)

    # 비중 10%
    quantity = round( (100000000 * 0.1) / abs(float(df_stock.tail(1)['price'])) )
    print(quantity)
    ret_buy = abs(float(df_stock['price'][0]) / float(df_stock.tail(1)['price'])) - 1
    ret_sell = abs(float(df_stock.tail(1)['price']) / float(max(df_stock['price']))) - 1

    while True:
        if ret_buy > 0.02:
            kiwoom.send_order("send_order_req", "0101", "8103989611", 1, stockcode, quantity, 10000, "03", "")
        else:
            print('not yet [buy]')

        if ret_sell < -0.03:
            kiwoom.send_order("send_order_req", "0101", "8103989611", 2, stockcode, quantity, 10000, "03", "")
            break
        else:
            print('not yet [sell]')


# 수정해야할 점
# 1. 여러 종목이 공시가 나왔을 때에는 어떻게 처리해야할 것인가?
# 2. 함수 멈출 시점 계산하기
# 3. 웨이트는 어떻게
