rm(list=ls())
library(rvest)
library(stringr)
library(dplyr)
library(tidyr)
library(knitr)
library(slackr)

url_news = 'http://dart.fss.or.kr/dsac001/mainY.do'
keyword = "주주"
slackr_setup(api_token = "xoxb-324459867104-L5ZLBTWl3DcGEdJxdPuYOL19", username = "jooji")



crawling_function = function(url_news){
    repeat {  
    news_data = read_html(url_news, encoding = 'UTF-8') #UTF-8
    head = news_data %>% html_nodes('td') %>% html_text()
    head = str_trim(head)
    
    news = data.frame(time = character(0), stock = character(0), head = character(0), date = character(0))
    
    for (i in 0:((length(head)/6)-1)) {
    news = bind_rows(news, data.frame(time = head[1+6*i], stock = head[2+6*i], head = head[3+6*i], date = head[5+6*i]))
    }
    
    print(news)
  
    if(length(grep(keyword, news$head)) > 0){ 
      print(news[grep(keyword, news$head),])
      news = news[grep(keyword, news$head),]
    for (j in 1:nrow(news)) {
      text = paste(as.character(news[j,])[1], as.character(news[j,])[2], as.character(news[j,])[3], as.character(news[j,])[4])
      text_slackr(text, channel = '#dart')
    }}
    Sys.sleep(10)
    }
}

crawling_function(url_news)




