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
        if (now_time - dart_time).seconds <= 60:
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


def new_algorithm(new_list):
    no_need = list()
    if len(new_list) > 0:
        for company in new_list:
            no_need = ['기재정정', '코넥스', '증권발행']
            ## no_need 리스트 안에 없으면
            if len([item for item in no_need if company['title'] in item]) == 0:
                ## switch 함수를 통해 각 경우의 수를 나눔
                case = switch_company_title(company['title'])
                if case is 1 or 2 or 3:
                    strr = "종목 :: " + company['dc:creator'] + " \n제목 :: " + company['title'].split('-')[
                        1] + " \nlink :: " + company['link']
                    bot.sendMessage(chat_id=our_channel_id, text=strr)
                    print(company)

                elif case is 4 or 5:
                    strr = "종목 :: " + company['dc:creator'] + " \n제목 :: " + company['title'].split('-')[
                        1] + " \nlink :: " + company['link']
                    bot.sendMessage(chat_id=our_channel_id, text=strr)
                    print(company)


def switch_company_title(company_name):
    switcher = {
        "분할": 1,
        "무상": 2,
        "투자판단": 3,
        "상장": 4,
        "자율공시": 5
    }
    return switcher.get(company_name, " ")


if __name__ == '__main__':
    ## Telegram bot 설정
    bot_token = '474878865:AAG6GJl06WAVuS4vlsj88SXxbZXvFW89FXQ'
    our_channel_id = '-244440212'
    bot = telegram.Bot(token=bot_token)
    # bot.sendMessage(chat_id = our_channel_id, text = "크롤링 시작!!")

    while True:
        dart_list = request_dart_data()
        recent_1min_data = recent_data(dart_list)
        new_list = compare_data(recent_1min_data)
        print("will check :::: ", datetime.utcnow())

        new_algorithm(new_list)
        time.sleep(5)
        continue