rm(list=ls())
library(rvest)
library(stringr)
library(dplyr)
library(tidyr)
library(KoNLP)
library(knitr)
library(tm)

library(wordcloud)
library(RColorBrewer)
library(qgraph)

setwd('C:/Users/Jin/Desktop/Project/Slackopenapi')
useNIADic(which_dic = c("woorimalsam", "insighter"), category_dic_nms = "economic", backup = T)


data_list = list()
stock_list = list()

for (j in 1:500) {
  url_news = 'http://finance.naver.com/research/company_list.nhn?&page='
  url_news = paste0(url_news, j)
  news_data = read_html(url_news, encoding = 'cp949') #UTF-8
  # news_data
  head = news_data %>% html_nodes('div#newarea') %>% html_nodes('tr') %>% html_nodes('td') %>% html_nodes('a')  %>% html_text()
  #head
  data = head[1:(length(head)-17)]
  data[data==""] = NA
  data = na.omit(data)
  
  stock = data[seq(from = 1, to = length(data), by=2 )]
  if (length(stock)>30) {
    stock = stock[-31]  
  }
  
  head_report = data[seq(from = 2, to = length(data), by=2 )]
  head_report = str_trim(head_report)
  if (length(head_report)>30) {
    head_report = head_report[-31]  
  }
  head_report
  
  data_list[[j]] = head_report
  stock_list[[j]] = stock
}

# Word Cloud
rawword = data_list %>% unlist() %>% extractNoun() %>% unlist()
rawword[nchar(rawword)==1] = NA
rawdata = rawword %>% na.omit() %>% table()
head(sort(rawdata, decreasing = TRUE), 40)
rawdata = as.data.frame(rawdata, stringsAsFactors = F)
str(rawdata)

pal = brewer.pal(12,"Paired")

wordcloud(words = rawdata$.,  # 단어
          freq = rawdata$Freq,   # 빈도
          min.freq = 50,          # 최소 단어 빈도
          max.words = 150,       # 표현 단어 수
          random.order = F,      # 고빈도 단어 중앙 배치
          rot.per = .1,          # 회전 단어 비율
          scale = c(8, 1),     # 단어 크기 범위
          colors = pal)          # 색깔 목록


data_create = function(data_list, stock_list) {
data2 = data.frame()
for (i in 1:length(data_list)) {
  data_L = data.frame(unlist(data_list[[i]]))
  data_S = data.frame(unlist(stock_list[[i]]))
  data = bind_cols(data_S, data_L)
  data2 = bind_rows(data2, data)
}
return(data2)
}

data_ = data_create(data_list, stock_list)
colnames(data_) = c("stock", "forecast")
data_$score = 0

pos_word = c("성장", "개선", "기대", "안정", "회복", "상승", "매력", "확대", "기대감", "배당", "호조", "서프라이즈", "저평가", "정상화", "턴어라운드", "반등", "수혜", "성장세", "긍정", "촤고", "고성장", "흑자", "상향", "해소", "저점")
nag_word= c("부진", "우려", "불확실", "하락", "하회", "부담", "과도", "감소", "쇼크", "악재", "축소", "하향")

score_function = function(data_){
for (pos in pos_word){
  for (i in 1:nrow(data_) ) {
    if( grepl(pos, data_[i,2]) ) {
      data_[i,3] =  (data_[i,3]+1) }
  }
}

for (nag in nag_word){
  for (i in 1:nrow(data_) ) {
    if( grepl(nag, data_[i,2]) ) {
      data_[i,3] =  (data_[i,3]-1) }
  }
}

data_$score[which(data_$score>1)] = 1
data_$score[which(data_$score<(-1))] = (-1)

return(data_)}

data_ = score_function(data_)
table(data_$score)

data_all = data_ %>% group_by(stock) %>% summarize(sum(score))
data_all %>% head()
summary(data_all$`sum(score)`)



# Q-graph
string = paste(unlist(SimplePos22(unlist(data_list))))
head(string)


# NOUN
noun = str_match_all(string, "[가-힣]+/[N][C]|[가-힣]+/[N][Q]+")%>% unlist()
noun = str_replace_all(noun,"/[N][C]","") %>% str_replace_all("/[N][Q]","") %>%unlist()
noun = Corpus(VectorSource(noun)) #tm

myTdmNC<-TermDocumentMatrix(noun,control = list(removePunctuation=T,removeNumbers=T,weighting=weightBin))
Encoding(myTdmNC$dimnames$Terms)= "UTF-8"
findFreqTerms(myTdmNC, lowfreq=10)

# 제대로 작동했다면 extractnoun함수를 통해 얻은 결과값과 대충 비슷한 형태의 결과가 나온다.
mtNC<-as.matrix(myTdmNC) #행렬(matrix)로 변환하는 게 상관성 분석의 핵심이다.
mtrowNC<-rowSums(mtNC)

mtNC.order<-mtrowNC[order(mtrowNC,decreasing=T)]
freq.wordsNC<-sample(mtNC.order[mtNC.order>30],25)
freq.wordsNC<-as.matrix(freq.wordsNC)
freq.wordsNC 

co.matrix<-freq.wordsNC %*% t(freq.wordsNC)

qgraph(co.matrix,
       labels=rownames(co.matrix),
       diag=FALSE,
       layout='spring', 
       vsize=log(diag(co.matrix)*2))



# AD 
#  str_match_all(tt,"[가-힣]+/[P][V]+|[가-힣]+/[P][X]+|[가-힣]+/[P][A]+|[가-힣]+/[M][A]+")%>%unlist()
#  PNM<-str_replace_all(alldta2,"/[P][V]","") %>%
#  str_replace_all("/[P][A]","") %>%
#  str_replace_all("/[M][A]","") %>%
#  str_replace_all("/[P][X]","") %>% unlist() 

