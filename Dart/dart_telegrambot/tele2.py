import telegram
import config


if __name__ == '__main__':

    bot_token = config.telegram_bot['bot_token']
    id = config.telegram_bot["channel_id"]

    bot = telegram.Bot(token=bot_token)
    bot.sendMessage(chat_id=id, text='<b>(채권) 신흥국과 원화 자산에 드리울 단기적 시련: 좋았던 약달라의 강세 되돌림이 나타나고 있음. 건강한 성장을 위해서는 불가피함</b> \n<a href="http://app.fnguide.com/respresso/Contents/summary?kind=R500&no=72806&s=a">더 알아보기</a>'
                                    , parse_mode=telegram.ParseMode.HTML)


# 기타 파트 쓸대없이 들어오는거 제거해야함

