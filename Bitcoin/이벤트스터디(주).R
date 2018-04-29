rm(list=ls())
setwd('C:/Users/Jin/Desktop/Bitcoin')
library('xts')
ICO <- read.csv('ico.data.csv', header=T, stringsAsFactors = FALSE)
trend = read.csv('BTC.csv')
trend.C = as.data.frame(trend[,2])
rownames(trend.C) = trend[,1]
trend.z = xts(trend.C, order.by = as.Date(trend[,1]))

  setwd('C:/Users/Jin/Desktop/Bitcoin/Event.BTC')
  event = as.numeric()
  for (i in 1: nrow(ICO)) {
    if (ICO[i,15] == "") { NA
    } else {
      btc = trend.z[(first(which((ICO[i,16] <= time(trend.z))))-4) :
                      (first(which((ICO[i,16] <= time(trend.z))))+4) ,1]
      colnames(btc) = c("Trend INDEX of Bitcoin")
      btc = as.numeric(btc)
      event = cbind(event, btc)
    }}
  event = as.data.frame(apply(event, 1, mean))
  colnames(event) = "GoogleTrend.Index.of.Bitcoin"
  write.csv(event, "Event.csv")
  
  library(ggplot2)
  png("Eventstudy of ICO.png")      
  ggplot(event, aes(x = -4:4, y = event$GoogleTrend.Index.of.Bitcoin)) + geom_line(colour="blue", size = 1) + geom_point() + 
    ggtitle("Eventstudy of ICO for Bitcoin") +
    xlab("EventDay") +theme(axis.title.x=element_text(angle=0, face="italic", colour="darkblue",size=14)) + 
    ylab("GoogleTrend Index\n(Bitcoin)") +theme(axis.title.y=element_text(angle=90, face="italic", colour="darkblue",size=14)) +
    geom_vline(xintercept = 0, colour="red", lty = 4, size = 1)
  dev.off()
  





