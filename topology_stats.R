data <- read.csv('stats.csv')
summary(data)
data$algorithm <- as.factor(data$algorithm)
algorithm1 <- data[which(data$algorithm == 1),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm1 <- aggregate(algorithm1, by=list(algorithm1$nodes, algorithm1$cluster), FUN=mean)

algorithm2 <- data[which(data$algorithm == 2),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm2 <- aggregate(algorithm2, by=list(algorithm2$nodes, algorithm2$cluster), FUN=mean)

algorithm3 <- data[which(data$algorithm == 3),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm3 <- aggregate(algorithm3, by=list(algorithm3$nodes, algorithm3$cluster), FUN=mean)

algorithm4 <- data[which(data$algorithm == 4),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm4 <- aggregate(algorithm4, by=list(algorithm4$nodes, algorithm4$cluster), FUN=mean)

algorithm5 <- data[which(data$algorithm == 5),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm5 <- aggregate(algorithm5, by=list(algorithm5$nodes, algorithm5$cluster), FUN=mean)

algorithm6 <- data[which(data$algorithm == 6),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm6 <- aggregate(algorithm6, by=list(algorithm6$nodes, algorithm6$cluster), FUN=mean)



plot(data$nodes, data$interference, col=data$algorithm, pch=20, main="Interference for different algorithms")
legend(x='topleft', legend=names(summary(data$algorithm)), col=data$algorithm, lwd=1, cex=.5)
pairs(data[, c("nodes", "interference", "hops", "distance", "totalTraffic")], col=data$algorithm, pch=20)
