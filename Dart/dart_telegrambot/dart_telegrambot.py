import telegram
import xmltodict 
import requests
import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup
import config
import json
##test
recent_check_list = []
signal = ''

# '''
# 공시 데이터 들고오기
# '''

def request_dart_data():
    ## dart 공시 가져와서 리스트에 저장하기
    dart_list = []
    URL = config.dart_url
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
        if (now_time - dart_time).seconds <= 1300 :
            recent_data.append(company)

    return recent_data

   
'''
최근 1분동안 뜬 공시랑 비교해서 중복되지 않은 것들만 뽑기
'''
def compare_data(recent_1min_data):
    ## 2분 별로 체크한 공시들을 누적하여 기록
    global recent_check_list 
    new_list = []
    
    ## 제일 처음 비교할 때
    if len(recent_check_list) == 0: 
        recent_check_list = recent_1min_data
        return recent_check_list
    
    else:
        for company in recent_1min_data:
            ## 공시 중복된 것 제외하기
            if company not in recent_check_list:
                recent_check_list.append(company)
                new_list.append(company)
    
    return new_list

## Send message to Telegrambot
def send_message(company,signal,case):
    try:
        strr = ("종목 :: " + company['dc:creator'] + " \n제목 :: " +  company['title'].split('-')[1] + " \nlink :: " + company['link']+ "\nsignal :: " + signal + "\ncase :: " + str(case))
        bot.sendMessage(chat_id=config.telegram_bot['our_channel_id'], text=strr)
    except:
        print("Send Message Error")
                

'''
알고리즘
'''     
def new_algorithm(new_list):
    no_need = list()
    ## 새로운 공시가 뜨면
    if len(new_list) > 0:
        for company in new_list:
            print(company['title'])
            no_need = ['기재정정', '코넥스', '증권발행', '첨부추가', '첨부정정', '연장결정', '(기타)']
            ## no_need의 key가 title에 없을 경우에만 돌아감
            if not any(key in company['title'] for key in no_need):
                ## switch 함수를 통해 각 경우의 수를 나눔
                case = title_to_num(company['title'])
                signal = 'WATCH'
                # case 값이 숫자가 아니면 break되어서 빠져나감
                if not str(case).isdigit():
                    break
                
                ## Link 안에 테이블 따로 분리
                '''
                link = requests.get(company['link']).text
                soup = BeautifulSoup(link, 'html.parser')          
                table = soup.find('div', class_='xforms')
                pprint(table)
                '''
                # 주식분할결정
                if case == 1:
                    ## 주식분할결정은 100% 매수
                    signal = 'BUY'
                    case = "1, 주식분할"

                # 투자판단, 자율공시, 주요사항보고
                elif case == 2:
                    if '취소' in company['title']:
                        signal = 'SELL'
                        case = "2, 취소"
                    elif all(word in company['title'] for word in ['기술', '이전']):
                        signal = 'BUY'
                        case = "2, 기술이전"
                    elif any(word in company['title'] for word in ['FDA', '임상']):
                        signal = 'BUY'
                        case = "2, FDA or 임상"                      
                    elif any(word in company['title'] for word in ['승인']):
                        signal = 'HOLD'
                        case = "2, 승인"
                    elif any(word in company['title'] for word in ['타법인주식']):
                        if '양도' in company['title']:
                            signal = "HOLD"
                            case = "2, 주식양도, 양도금액 자기자본 대비 % 확인"
                            #내용 확인
                        elif '양수' in company['title']:
                            signal = "HOLD"
                            case = "2, 주식양수. 양수기업 상장사 여부 확인"
                            #내용 확인
                # 최대주주변경을수반하는주식양수도계약체결
                elif case == 3:
                    signal = "BUY"
                    case = "3, (급격한 상승 or 하락. 상승 가능성 높음 )"
                    """상승 가능성이 훨씬 높음"""

                # 공개매수, 자기주식취득, 자진상장폐지
                elif case == 4:
                    if any(word in company['title'] for word in ['상장폐지']):
                        ## 내용에 상장폐지 단어 찾아서 있으면 시장가 매수
                        signal = 'BUY'
                        case = "4, 상장폐지"
                    elif '공개매수' in company['title']:
                        if any(word in company['title'] for word in ['설명서', '신고서', '결과']):
                            break
                        else:
                            signal = 'HOLD'
                            case = "4, 공개매수"

                # 최대주주 대표이사
                elif case == 6:
                    if '변경' in company['title']:
                        '''
                        가격 2% 상승하면 매수
                        
                        - 2분 간 반응 없으면 매도
                        - 고점 대비 -2%면 손절  
                        '''
                        signal = 'HOLD'
                        case = "6, 변경"
                         
                # 합병  
                elif case == 7:
                    '''
                    합병은 알림
                    '''

                # 상호변경
                elif case == 8:
                    '''
                    상호변경 알림
                    '''

                # elif case == 9:
                #     '''
                #     알림 
                #     '''
                #     pass

                # 유상 무상
                elif case == 10:
                    '''
                    
                    '''
                    if '유상증자결정' in company['title']:
                        '''
                        공시내용안에 제3자배정증자 있을 경우 급등 가능성
                        '''
                        signal = 'HOLD'
                        case = '10, 유상증자결정'
                    elif '유상감자결정' in company['title']:
                        signal = 'BUY'
                        case = '10, 유상감자결정'
                    elif '무상' in company['title']:
                        case  = '10, 무상 30분간 정지'
                                    

                # 처분 소각
                elif case == 11:
                    '''
                    소각예정금액이 시가총액 대비 얼마인지 확인
                    '''
                    signal = 'HOLD'
                    case = '11, 소각,취득금액이 시총대비 4% 이상일 경우 BUY'
                send_message(company,signal,case)                   
                                   


## 띄어쓰기는 인식 못한다
## if want to check all word then just change any to all
def title_to_num(company_name):
        if any(word in company_name for word in ['주식분할결정']):
            return 1
        elif any(word in company_name for word in ['최대주주변경을수반하는주식양수도계약체결']):
            return 3
        elif any(word in company_name for word in ['공개매수', '자기주식취득', '자진상장폐지']):
            return 4
        elif any(word in company_name for word in ['최대주주변경', '대표이사변경']):
            return 6
        elif any(word in company_name for word in ['합병']):
            return 7    
        elif any(word in company_name for word in ['상호변경안내']):
            return 8
        elif any(word in company_name for word in []):
            return 9
        elif any(word in company_name for word in ['유상', '무상']):
            return 10
        elif any(word in company_name for word in ['자기주식취득결정', '주식소각결정']):
            return 11
        elif any(word in company_name for word in ['투자판단', '자율공시','주요사항보고']):
            return 2




if __name__ == '__main__':
    ## Telegram bot 설정
    bot_token = config.telegram_bot['bot_token']
    # our_channel_id = config.telegram_bot['our_channel_id']
    bot = telegram.Bot(token = bot_token)
    
    while True:
        try:
            """실전"""
            dart_list = request_dart_data()
            recent_1min_data = recent_data(dart_list)
            new_list = compare_data(recent_1min_data)
            print("will check :::: ", datetime.utcnow())
            new_algorithm(new_list)
            time.sleep(2)
            """테스트"""
            # new_list = [{'dc:creator':'테스트','title':'테스트-최대주주변경을수반하는주식양수도계약체결', 'link':'test'}]
            # new_algorithm(new_list)
            # time.sleep(2)
            continue
        except KeyboardInterrupt:
            print('\nexit with keyboard')
            break
        except:
            print("While Error")
            time.sleep(2)