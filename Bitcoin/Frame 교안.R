library(dplyr)
library(PerformanceAnalytics)
rm(list=ls())
setwd('C:/Users/Jin/Desktop/Bitcoin')
sample = read.csv('교안.csv', header = TRUE, stringsAsFactors = F, na.strings = NA)
sample[sample == ""] = NA


sample = sample %>% group_by(Name) %>%  mutate(EPS1 = lag(EPS, 1))
sample = sample %>% group_by(Name) %>%  mutate(EPS2 = lag(EPS, 2))


E = list()
for (i in 1:6) {
year =paste0('201',i) 
output = sample %>% group_by(Name) %>%  filter(EPS > EPS1, EPS1 > EPS2, Year == year, BPS > 10000)
A = as.data.frame(output$Symbol)
A = t(A)
setwd('C:/Users/Jin/Desktop/Revenue Surprises and Bond/Data')

SR = read.csv("StockReturn.csv")
SR = SR[1:(nrow(SR)-1),]
Date = SR[,1]
SR = SR[,2:ncol(SR)]
rownames(SR) = Date
B = SR[,which(colnames(SR) %in% A)]
C = B[grep(year, rownames(B))+90,]
D = as.data.frame(apply(C, 1, mean, na.rm=T))

E[[i]] = D/100 }

port = as.numeric()

for (i in 1:6) {
port = rbind(port, E[[i]])
}

colnames(port) = 'EPS증가하는기업'
charts.PerformanceSummary(port)

# 1) 패키지    
# 2) 시계열 데이터와 패널데이터    
# 3) 금융 데이터를 어떻게 다룰 것인가? 에 대한 논의    
# 4) 백테스팅 자동화를 통하여 다양한 전략을 수립하고 비교 및 발전시킬 것
































