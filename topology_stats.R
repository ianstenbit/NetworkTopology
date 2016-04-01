data <- read.csv('stats.csv')
# turn to variances to average
data$algorithm <- as.factor(data$algorithm)
data$sd_interference <- data$sd_interference^2
data$sd_hops <- data$sd_hops^2
data$sd_dist <- data$sd_dist^2
summary(data)

# break down by algorithm
algorithm1 <- data[which(data$algorithm == 1),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm1 <- aggregate(algorithm1, by=list(algorithm1$nodes, algorithm1$cluster), FUN=mean)
algorithm1$sd_interference <- sqrt(algorithm1$sd_interference)
algorithm1$sd_hops <- sqrt(algorithm1$sd_hops)
algorithm1$sd_dist <- sqrt(algorithm1$sd_dist)
algorithm1$nodes <- NULL
algorithm1$cluster <- NULL

algorithm2 <- data[which(data$algorithm == 2),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm2 <- aggregate(algorithm2, by=list(algorithm2$nodes, algorithm2$cluster), FUN=mean)
algorithm2$sd_interference <- sqrt(algorithm2$sd_interference)
algorithm2$sd_hops <- sqrt(algorithm2$sd_hops)
algorithm2$sd_dist <- sqrt(algorithm2$sd_dist)
algorithm2$nodes <- NULL
algorithm2$cluster <- NULL

algorithm3 <- data[which(data$algorithm == 3),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm3 <- aggregate(algorithm3, by=list(algorithm3$nodes, algorithm3$cluster), FUN=mean)
algorithm3$sd_interference <- sqrt(algorithm3$sd_interference)
algorithm3$sd_hops <- sqrt(algorithm3$sd_hops)
algorithm3$sd_dist <- sqrt(algorithm3$sd_dist)
algorithm3$nodes <- NULL
algorithm3$cluster <- NULL

algorithm4 <- data[which(data$algorithm == 4),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm4 <- aggregate(algorithm4, by=list(algorithm4$nodes, algorithm4$cluster), FUN=mean)
algorithm4$sd_interference <- sqrt(algorithm4$sd_interference)
algorithm4$sd_hops <- sqrt(algorithm4$sd_hops)
algorithm4$sd_dist <- sqrt(algorithm4$sd_dist)
algorithm4$nodes <- NULL
algorithm4$cluster <- NULL

algorithm5 <- data[which(data$algorithm == 5),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm5 <- aggregate(algorithm5, by=list(algorithm5$nodes, algorithm5$cluster), FUN=mean)
algorithm5$sd_interference <- sqrt(algorithm5$sd_interference)
algorithm5$sd_hops <- sqrt(algorithm5$sd_hops)
algorithm5$sd_dist <- sqrt(algorithm5$sd_dist)
algorithm5$nodes <- NULL
algorithm5$cluster <- NULL

algorithm6 <- data[which(data$algorithm == 6),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm6 <- aggregate(algorithm6, by=list(algorithm6$nodes, algorithm6$cluster), FUN=mean)
algorithm6$sd_interference <- sqrt(algorithm6$sd_interference)
algorithm6$sd_hops <- sqrt(algorithm6$sd_hops)
algorithm6$sd_dist <- sqrt(algorithm6$sd_dist)
algorithm6$nodes <- NULL
algorithm6$cluster <- NULL

algorithm7 <- data[which(data$algorithm == 7),c("nodes", "interference", "sd_interference", "hops", "sd_hops", "distance", "sd_dist", "totalTraffic", "cluster")]
algorithm7 <- aggregate(algorithm7, by=list(algorithm7$nodes, algorithm7$cluster), FUN=mean)
algorithm7$sd_interference <- sqrt(algorithm7$sd_interference)
algorithm7$sd_hops <- sqrt(algorithm7$sd_hops)
algorithm7$sd_dist <- sqrt(algorithm7$sd_dist)
algorithm7$nodes <- NULL
algorithm7$cluster <- NULL

source("http://michael.hahsler.net/SMU/EMIS7332/R/copytable.R")
copytable(algorithm1)
copytable(algorithm2)
copytable(algorithm3)
copytable(algorithm4)
copytable(algorithm5)
copytable(algorithm6)
copytable(algorithm7)


plot(algorithm1$nodes, algorithm1$interference, col=algorithm1$Group.2, pch=20, main="Interference for algorithm 1")
legend(x='topleft', legend=names(summary(algorithm1$Group.2)), col=algorithm1$Group.2, lwd=1, cex=.5)
# pairs(data[, c("nodes", "interference", "hops", "distance", "totalTraffic")], col=data$algorithm, pch=20)

#ploting
alg1 <- read.csv('1_NullAlgorithm.csv')
alg2 <- read.csv('2_TravisAlgo.csv')
alg3 <- read.csv('3_TravisExtended.csv')
alg4 <- read.csv('4_ErikFullyRecursive.csv')
alg5 <- read.csv('5_ErikSemiRecursive.csv')
alg7 <- read.csv('7_IanRecursive.csv')
alg8 <- read.csv('8_IanAlgo.csv')


random <- alg1[which(alg1$layout == 'R'),]
random <- rbind(random, alg2[which(alg2$layout == 'R'),])
random <- rbind(random, alg3[which(alg3$layout == 'R'),])
random <- rbind(random, alg4[which(alg4$layout == 'R'),])
random <- rbind(random, alg5[which(alg5$layout == 'R'),])
random <- rbind(random, alg7[which(alg7$layout == 'R'),])
random <- rbind(random, alg8[which(alg8$layout == 'R'),])

semi <- alg1[which(alg1$layout == 'SC'),]
semi <- rbind(semi, alg2[which(alg2$layout == 'SC'),])
semi <- rbind(semi, alg3[which(alg3$layout == 'SC'),])
semi <- rbind(semi, alg4[which(alg4$layout == 'SC'),])
semi <- rbind(semi, alg5[which(alg5$layout == 'SC'),])
semi <- rbind(semi, alg7[which(alg7$layout == 'SC'),])
semi <- rbind(semi, alg8[which(alg8$layout == 'SC'),])

clustered <- alg1[which(alg1$layout == 'C'),]
clustered <- rbind(clustered, alg2[which(alg2$layout == 'C'),])
clustered <- rbind(clustered, alg3[which(alg3$layout == 'C'),])
clustered <- rbind(clustered, alg4[which(alg4$layout == 'C'),])
clustered <- rbind(clustered, alg5[which(alg5$layout == 'C'),])
clustered <- rbind(clustered, alg7[which(alg7$layout == 'C'),])
clustered <- rbind(clustered, alg8[which(alg8$layout == 'C'),])ß

library(ggplot2)
ggplot(random, aes(x = nodes, y = throughput, colour = type, clarity, fill = type)) +
  #geom_line(size=1) +
  geom_bar(stat="identity", position="dodge") +
  ylab(label="Throughput") +
  xlab("Nodes") +
  scale_colour_manual(values=c("black", "black", "black", "black", "black", "black", "black") )


ggplot(semi, aes(x = nodes, y = throughput, colour = type, clarity, fill = type)) +
  #geom_line(size=1) +
  geom_bar(stat="identity", position="dodge") +
  ylab(label="Throughput") +
  xlab("Nodes") +
  scale_colour_manual(values=c("black", "black", "black", "black", "black", "black", "black") )

ggplot(clustered, aes(x = nodes, y = throughput, colour = type, clarity, fill = type)) +
  #geom_line(size=1) +
  geom_bar(stat="identity", position="dodge") +
  ylab(label="Throughput") +
  xlab("Nodes") +
  scale_colour_manual(values=c("black", "black", "black", "black", "black", "black", "black") )
