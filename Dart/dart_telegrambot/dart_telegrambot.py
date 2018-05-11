import telegram
import xmltodict 
import requests
import socket
import sys
import time
from datetime import datetime
from pprint import pprint
##test
recent_check_list = []

'''
dart 데이터 불러오기
06:00 ~ 09:00 까지 공시 출력하기
'''
def request_dart_data():
    ## dart 공시 가져와서 리스트에 저장하기
    dart_list = []
    URL = "http://dart.fss.or.kr/api/todayRSS.xml" 
    response = requests.get(URL)
    html = response.text
    ## 리스트 안의 OrderedDict 함수로 반환한다
    dart_list = xmltodict.parse(html)['rss']['channel']['item']  

    return dart_list

'''
최근 1분 이내 글 불러오기
'''
def recent_data(dart_list):
    ## 2분 이내 최신글 비교
    recent_data = []
    ## 현재 시간
    now_time = datetime.utcnow()
    for company in dart_list:
        ## 게시글 시간
        dart_time = datetime.strptime(company['dc:date'], "%Y-%m-%dT%H:%M:%S%fZ")
        if (now_time - dart_time).seconds <= 60 :
            recent_data.append(company)

    return recent_data
   
'''
최근 1분동안 뜬 공시랑 비교해서 중복되지 않은 것들만 뽑기
'''
def compare_data(recent_1min_data):
    ## 1분 별로 체크한 공시들을 누적하여 기록
    global recent_check_list 
    new_list = []
    
    ## 제일 처음 비교할 때
    if len(recent_check_list) == 0: 
        recent_check_list = recent_1min_data
        return recent_check_list
    
    else:
        for company in recent_1min_data:
            if company not in recent_check_list:
                recent_check_list.append(company)
                new_list.append(company)
    
    return new_list

'''
알고리즘
'''
def algorithm(new_list):

    if len(new_list) > 0:
        for company in new_list:
            print(type(company['title']))
            if('기재정정' not in company['title'] and '코넥스' not in company['title'] and '증권발행' not in company['title']):
                if('분할' in company['title'] or '무상' in company['title'] or '투자판단' in company['title'] or '상장폐지' in company['title'] or '상장 폐지' in company['title'] or '자율공시' in company['title']) :
                    strr = "종목 :: " + company['dc:creator'] + " \n제목 :: " +  company['title'].split('-')[1] + " \nlink :: " +company['link']
                    bot.sendMessage(chat_id=our_channel_id, text=strr)
                    print(company)
        
        

if __name__ == '__main__':
    ## Telegram bot 설정
    bot_token = '474878865:AAG6GJl06WAVuS4vlsj88SXxbZXvFW89FXQ'
    our_channel_id = '-244440212'
    bot = telegram.Bot(token = bot_token)
    #bot.sendMessage(chat_id = our_channel_id, text = "크롤링 시작!!")
    
    while True :
        dart_list = request_dart_data()
        recent_1min_data = recent_data(dart_list)
        new_list = compare_data(recent_1min_data)
        print("will check :::: ", datetime.utcnow())
        
        algorithm(new_list)
        time.sleep(5)        
        continue
                
