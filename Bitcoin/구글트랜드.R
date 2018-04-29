rm(list=ls())
setwd('C:/Users/Jin/Desktop/Bitcoin')
library('xts')
ICO <- read.csv('ico.data.csv', header=T, stringsAsFactors = FALSE)
trend = read.csv('BTC.csv')
trend.C = as.data.frame(trend[,2])
rownames(trend.C) = trend[,1]
trend.z = xts(trend.C, order.by = as.Date(trend[,1]))

bit.function = function(trend.z = trend.z, ICO = ICO ) {
  for (i in 1: nrow(ICO)) {
    if (ICO[i,15] == "") { NA
    } else if (identical((which((ICO[i,15] < time(trend.z)) & (time(trend.z) < ICO[i,16])) - 4), numeric(0))) {NA
    } else if (identical((which((ICO[i,15] < time(trend.z)) & (time(trend.z) < ICO[i,16])) + 4), numeric(0))) {NA  
    } else {
      btc = trend.z[first(which((ICO[i,15] < time(trend.z)) & (time(trend.z) < ICO[i,16])) - 4):
                last(which((ICO[i,15] < time(trend.z)) & (time(trend.z) < ICO[i,16])) + 4),1]
      colnames(btc) = c("Trend INDEX of Cryptocoin")
      
        if (ICO[i,8]== "#N/A") {
        NA 
      } else {
        setwd('C:/Users/Jin/Desktop/Bitcoin/Trend.Cryptocoin')
        Asset = paste(ICO[i,8],  ",", ICO[i,9], ".jpeg",  sep="")
        png(Asset)
        par(mar = c(5,5,2,5)) 
        plot.zoo(x = btc[,1], xlab = "Days", ylab = "Trend INDEX of Cryptocoin", 
                 col = "darkblue", lwd="3", main = "The effect of Ico on Cryptocoin Trend", xaxt = "n")
        axis(1, at = time(btc), labels = format(time(btc[,0]), "%Y-%m-%d"), tck = 0.01)
        abline(v = as.Date(ICO[i,15]), lty = 3, lwd = 2, col = "darkred")
        abline(v = as.Date(ICO[i,16]), lty = 3, lwd = 2, col = "darkred")
        dev.off()
        Asset2 = paste(ICO[i,8],  ",", ICO[i,9], ".csv",  sep="")
        btc2 = as.data.frame(btc)
        write.csv(btc2, Asset2)
      }}
  }
}

bit.function(trend.z = trend.z, ICO = ICO)
