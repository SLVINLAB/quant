rm(list=ls())
setwd('C:/Users/Jin/Desktop/Bitcoin')
library(ggthemes)
library(xts)
library(Quandl)
library(dplyr)
library(gridExtra)
library(PerformanceAnalytics)
library(ggplot2)
library(quantmod)


Data = Quandl("BCHARTS/BITSTAMPUSD", api_key="bwp6zzuZ41Rxypx7M-ju", type="xts")
Data1 = as.data.frame(Data)
Data1 = Data1[7]
colnames(Data1) = 'Price'

Data2 = Data1 %>%  mutate(Price1 = lag(Price))
Data2 = Data2 %>%  mutate(return = (log(Price/Price1)))
#Data2 = Data2 %>%  mutate(return = (Price/Price1 -1 ))

rownames(Data2) = rownames(Data1)
Data2$return[is.infinite(Data2$return)] = NA

ICO <- read.csv('ico.data.csv', header=T, stringsAsFactors = FALSE)
trend = read.csv('GTbitcoin.csv')

trend.C = as.data.frame(trend[,2])
rownames(trend.C) = trend[,1]
trend.z = xts(trend.C, order.by = as.Date(trend[,1]))

setwd('C:/Users/Jin/Desktop/Bitcoin/Event.BTC')
  
event = as.numeric()
  for (i in 1: nrow(ICO)) {
    if (ICO[i,15] == "") { NA
    } else {
      btc = trend.z[(which((ICO[i,15] == time(trend.z)))-7) :
                      (which((ICO[i,15] == time(trend.z)))+30) ,1]
      colnames(btc) = c("Trend INDEX of Bitcoin")
      btc = as.numeric(btc)
      event = cbind(event, btc)
      }}
     event = as.data.frame(apply(event, 1, mean))
     colnames(event) = "GoogleTrend.Index.of.Bitcoin"
     #write.csv(event, "Event.csv")
    
     
    event.r = as.numeric()
    for (i in 1: nrow(ICO)) {
       if (ICO[i,15] == "") { NA
       } else {
         btc = Data2$return[(which((ICO[i,15] == rownames(Data2)))-7) :
                         (which((ICO[i,15] == rownames(Data2)))+30)]
         btc = as.numeric(btc)
         mom = Data2$return[(which(ICO[i,15]==rownames(Data2))-7) :
                        (which(ICO[i,15]==rownames(Data2))-1)]
         mom = mean(mom, na.rm=T)
         btc = btc-mom
         event.r = cbind(event.r, btc)
       }}
     
     event.r = as.data.frame(apply(event.r, 1, mean, na.rm=T ))
     colnames(event.r) = "Daily.Return.of.Bitcoin"
     #write.csv(event.r, "Event.csv")  
     
     event.rr = as.numeric()
     for (i in 1:nrow(event.r)) {
     btc = Return.cumulative(event.r[1:i,])
     event.rr = rbind(event.rr, btc)
     }
     event.r = event.rr
     event.r = as.data.frame(event.r)
     colnames(event.r) = "Daily.Return.of.Bitcoin"
      
      P1 = ggplot(event, aes(x = -7:30, y = event$GoogleTrend.Index.of.Bitcoin)) + geom_line(colour="blue", size = 1) + geom_point() +
      theme_solarized_2()+
      ggtitle("Eventstudy of ICO for Bitcoin") +
      xlab("EventDay") +theme(axis.title.x=element_text(angle=0, face="italic", colour="darkblue",size=14)) + 
      ylab("GoogleTrend Index\n(Bitcoin)") + theme(axis.title.y=element_text(angle=90, face="italic", colour="darkblue",size=14)) +
      annotate("text", x = 0, y = 48, label="Start Day of ICO", size=5) + 
      geom_vline(xintercept = 0, colour="red", lty = 4, size = 1)
      
      P2 = ggplot(event.r, aes(x = -7:30, y = event.r$Daily.Return.of.Bitcoin)) + geom_line(colour="purple", size = 1) + geom_point() +   
      theme_solarized_2()+
      xlab("EventDay") +theme(axis.title.x=element_text(angle=0, face="italic", colour="darkblue",size=14)) + 
      ylab("Return\n(Bitcoin)") + theme(axis.title.y=element_text(angle=90, face="italic", colour="darkblue",size=14)) +
      annotate("text", x = 0, y = 0.012, label="Start Day of ICO", size=5) +
      geom_vline(xintercept = 0, colour="red", lty = 4, size = 1)
      
      grid.arrange(P1, P2, ncol = 1)      
 
      
      
      
#---------------------------------------------------------------------------
      
      rm(list=ls())
      
      library(ggthemes)
      library(xts)
      library(Quandl)
      library(dplyr)
      library(gridExtra)
      library(PerformanceAnalytics)
      library(ggplot2)
      
      setwd('C:/Users/Jin/Desktop/Bitcoin')
      
      Data = Quandl("BCHARTS/BITSTAMPUSD", api_key="bwp6zzuZ41Rxypx7M-ju", type="xts")
      Data1 = as.data.frame(Data)
      Data1 = Data1[7]
      colnames(Data1) = 'Price'
      Data2 = Data1 %>%  mutate(Price1 = lag(Price))
      Data2 = Data2 %>%  mutate(return = (log(Price/Price1)))
      
      #Data2 = Data2 %>%  mutate(return = (Price1/Price-1))
      rownames(Data2) = rownames(Data1)
      Data2$return[is.infinite(Data2$return)] = NA
      
      ICO <- read.csv('ico.data.csv', header=T, stringsAsFactors = FALSE)
      trend = read.csv('GTbitcoin.csv')
      trend.C = as.data.frame(trend[,2])
      rownames(trend.C) = trend[,1]
      trend.z = xts(trend.C, order.by = as.Date(trend[,1]))
      
      setwd('C:/Users/Jin/Desktop/Bitcoin/Event.BTC')
      event = as.numeric()
      for (i in 1: nrow(ICO)) {
        if (ICO[i,15] == "") { NA
        } else {
          btc = trend.z[(which((ICO[i,16] == time(trend.z)))-30) :
                          (which((ICO[i,16] == time(trend.z)))+7) ,1]
          colnames(btc) = c("Trend INDEX of Bitcoin")
          btc = as.numeric(btc)
          event = cbind(event, btc)
        }}
      event = as.data.frame(apply(event, 1, mean))
      colnames(event) = "GoogleTrend.Index.of.Bitcoin"
      #write.csv(event, "Event.csv")
      
      
      event.r = as.numeric()
      for (i in 1: nrow(ICO)) {
        if (ICO[i,15] == "") { NA
        } else {
          btc = Data2$return[(which((ICO[i,16] == rownames(Data2)))-30) :
                               (which((ICO[i,16] == rownames(Data2)))+7)]
          btc = as.numeric(btc)
          mom = Data2$return[(which(ICO[i,15]==rownames(Data2))-7) :
                               (which(ICO[i,15]==rownames(Data2))-1)]
          mom = mean(mom, na.rm=T)
          btc = btc-mom
          event.r = cbind(event.r, btc)
        }}
      
      event.r = as.data.frame(apply(event.r, 1, mean, na.rm=T ))
      #colnames(event.r) = "Daily.Return.of.Bitcoin"
      #write.csv(event.r, "Event.csv")  
      
      event.rr = as.numeric()
      for (i in 1:nrow(event.r)) {
        btc = Return.cumulative(event.r[1:i,])
        event.rr = rbind(event.rr, btc)
      }
      event.r = event.rr
      event.r = as.data.frame(event.r)
      colnames(event.r) = "Daily.Return.of.Bitcoin"
      
      P1 = ggplot(event, aes(x = -30:7, y = event$GoogleTrend.Index.of.Bitcoin)) + geom_line(colour="blue", size = 1) + geom_point() +
        theme_solarized_2()+
        ggtitle("Eventstudy of ICO for Bitcoin") +
        xlab("EventDay") +theme(axis.title.x=element_text(angle=0, face="italic", colour="darkblue",size=14)) + 
        ylab("GoogleTrend Index\n(Bitcoin)") + theme(axis.title.y=element_text(angle=90, face="italic", colour="darkblue",size=14)) +
        annotate("text", x = 0, y = 48, label="End Day of ICO", size=5) + 
        geom_vline(xintercept = 0, colour="red", lty = 4, size = 1)
      
      P2 = ggplot(event.r, aes(x = -30:7, y = event.r$Daily.Return.of.Bitcoin)) + geom_line(colour="purple", size = 1) + geom_point() +   
        theme_solarized_2()+
        xlab("EventDay") +theme(axis.title.x=element_text(angle=0, face="italic", colour="darkblue",size=14)) + 
        ylab("Return\n(Bitcoin)") + theme(axis.title.y=element_text(angle=90, face="italic", colour="darkblue",size=14)) +
        annotate("text", x = 0, y = 0.012, label="End Day of ICO", size=5) +
        geom_vline(xintercept = 0, colour="red", lty = 4, size = 1)
      
      grid.arrange(P1, P2, ncol = 1)      
      