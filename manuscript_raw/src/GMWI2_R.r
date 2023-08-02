library(ggplot2)
library(ggpubr)
library(reshape2)
library(vegan)
library(ggfortify)
#Figure 1
fig1a<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig1a.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F,row.names = 1)
#age
hist(as.numeric(fig1a$Age),xlab = "Age (years)",ylab = "Sample count",main = "")
mean(fig1a$Age,na.rm = T)
#sex
fig1a$Sex[is.na(fig1a$Sex)] <- "NA"
data_sex<-data.frame(table(fig1a$Sex))
colnames(data_sex)<-c("category","count")
data_sex$fraction <- data_sex$count / sum(data_sex$count)
data_sex$ymax <- cumsum(data_sex$fraction)
data_sex$ymin <- c(0, head(data_sex$ymax, n=-1))
data_sex$labelPosition <- (data_sex$ymax + data_sex$ymin) / 2
data_sex$label <- paste0(data_sex$category, ": ", data_sex$count)
plot_sex<-ggplot(data_sex, aes(ymax=ymax, ymin=ymin, xmax=4, xmin=3, fill=category)) +
  geom_rect() +
  geom_label(x=3.5, aes(y=labelPosition, label=label), size=4,color="black") +
  scale_fill_brewer(palette=4) +
  coord_polar(theta="y") +
  xlim(c(2, 4)) +
  theme_void() +
  theme(legend.position = "none")
plot_sex+scale_fill_manual(values=c("#FFCC66", "#66CCCC", "#CCCCCC"))
#geography
fig1a$Continent[is.na(fig1a$Continent)] <- "NA"
data_geo<-data.frame(table(fig1a$Continent))
colnames(data_geo)<-c("category","count")
data_geo$fraction <- data_geo$count / sum(data_geo$count)
data_geo$ymax <- cumsum(data_geo$fraction)
data_geo$ymin <- c(0, head(data_geo$ymax, n=-1))
data_geo$labelPosition <- (data_geo$ymax + data_geo$ymin) / 2
data_geo$label <- paste0(data_geo$category, ": ", data_geo$count)
plot_geo<-ggplot(data_geo, aes(ymax=ymax, ymin=ymin, xmax=4, xmin=3, fill=category)) +
  geom_rect() +
  geom_label(x=4, aes(y=labelPosition, label=label), size=4,color="black") +
  scale_fill_brewer(palette=4) +
  coord_polar(theta="y") +
  xlim(c(2, 4)) +
  theme_void() +
  theme(legend.position = "none")
plot_geo+scale_fill_manual(values=c("#FF6633", "#FFCC00", "#0066CC","#CCCCCC","#009933","#33CCCC","#996699"))
#
#fig.1b
fig1b_data<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig1b_relab.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F,row.names = 1)
fig1b_metadata<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig1b_metadata.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F)
fig1b_data[fig1b_data <= 0.00001] <- 0
fig1b_data1<-fig1b_data
fig1b_data1[fig1b_data1 > 0] <- 1
res.pca <- prcomp(fig1b_data1, scale = F)
fig1b_pca_plot <- autoplot(res.pca,
                          data = fig1b_metadata,
                          loadings.colour = "black",
                          colour = 'Phenotype',loadings = TRUE,frame = TRUE, frame.type = 'norm')
fig1b_pca_plot + scale_fill_manual(values = c("#66CCFF","#FF6666")) + scale_color_manual(values = c("#66CCFF","#FF6666"))+theme_bw()
set.seed(10)
adonis2(fig1b_data~Phenotype,data = fig1b_metadata)
#fig.1c
fig1c_data<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig1c.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F)
ggplot(data = fig1c_data, aes(x = Rank, y = Coefficient,color = Group), show.legend = F) +
  scale_color_manual(values=c("#FFCC33","#66CC33","#CCCCCC")) +
  geom_point() +theme_bw()
#fig.1d
library(ggpubr)
fig1d_data<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig1d.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F,row.names = 1)
p_GMWI2<-ggplot(fig1d_data, aes(x=Health_status, y=GMWI2, fill=Health_status)) +
  geom_violin(trim=FALSE)+geom_boxplot(width=0.1,fill="white")
p_GMWI2+scale_fill_manual(values=c("#3399CC","#FF6699"))+theme(axis.text=element_text(size=12,face="bold"),axis.title=element_text(size=12,face="bold"))+labs(x = "",y="GMWI2")+rremove("legend")+stat_compare_means()+theme_bw()
p_GMWI<-ggplot(fig1d_data, aes(x=Health_status, y=GMWI, fill=Health_status)) +
  geom_violin(trim=FALSE)+geom_boxplot(width=0.1,fill="white")
p_GMWI+scale_fill_manual(values=c("#3399CC","#FF6699"))+theme(axis.text=element_text(size=12,face="bold"),axis.title=element_text(size=12,face="bold"))+labs(x = "",y="GMWI")+rremove("legend")+stat_compare_means()+theme_bw()
p_shannon<-ggplot(fig1d_data, aes(x=Health_status, y=Shannon_Diversity, fill=Health_status)) +
  geom_violin(trim=FALSE)+geom_boxplot(width=0.1,fill="white")
p_shannon+scale_fill_manual(values=c("#3399CC","#FF6699"))+theme(axis.text=element_text(size=12,face="bold"),axis.title=element_text(size=12,face="bold"))+labs(x = "",y="Shannon's index")+rremove("legend")+stat_compare_means()+theme_bw()
p_richness<-ggplot(fig1d_data, aes(x=Health_status, y=Species_Richness, fill=Health_status)) +
  geom_violin(trim=FALSE)+geom_boxplot(width=0.1,fill="white")
p_richness+scale_fill_manual(values=c("#3399CC","#FF6699"))+theme(axis.text=element_text(size=12,face="bold"),axis.title=element_text(size=12,face="bold"))+labs(x = "",y="Species richness")+rremove("legend")+stat_compare_means()+theme_bw()
p_simpson<-ggplot(fig1d_data, aes(x=Health_status, y=Simpson_Diversity, fill=Health_status)) +
  geom_violin(trim=FALSE)+geom_boxplot(width=0.1,fill="white")
p_simpson+scale_fill_manual(values=c("#3399CC","#FF6699"))+theme(axis.text=element_text(size=12,face="bold"),axis.title=element_text(size=12,face="bold"))+labs(x = "",y="Simpson's index")+rremove("legend")+stat_compare_means()+theme_bw()
#fig.1e
fig1e_data<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig1e.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F,row.names = 1)
fig1e_plot<-ggboxplot(fig1e_data, x = "Phenotype", y = "GMWI2",
                 fill = "Phenotype",
                 title = "",
                 short.panel.labs = FALSE,outlier.shape=NA,xlab = "", ylab = "GMWI2",order = c("Healthy","MS","Ankylosing spondylitis","Rheumatoid arthritis","Ulcerative colitis","NAFLD","Type 2 diabetes","Crohn's Disease","Graves’ disease","Colorectal cancer","Liver Cirrhosis","Atherosclerotic cardiovascular disease"))
fig1e_plot+scale_fill_manual(values=c("#3399CC","#99CCCC","#FFFFCC","#CCCCFF","#FF6666","#99CCCC","#FFCC66","#CCCC66","#FFCCCC","#CCCCCC","#CCFFCC","#FFFF66"))+labs(x = "",y="GMWI2")+theme_bw()+theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1))+rremove("legend")+stat_compare_means(label = "p.signif", method = "wilcox.test", ref.group = "Healthy" )
#fig1f
fig1f_data<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig1f.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F,row.names = 1)
par(mar = c(5, 4, 4, 4) + 0.25)
hist(fig1f_data$GMHI2,col = "red",breaks = 12,xlim = c(-6,6),yaxt='n',xlab = '',ylab = '',ylim = c(0,2000),main = "")
axis(4)
mtext("Number of samples",side = 4,line = 3)
par(new=T)
healthy_freq<-data.frame(table(cut(fig1f_data$GMHI2[fig1f_data$Health_status=="Healthy"], breaks=seq(-6, 6, 1))))
nonhealthy_freq<-data.frame(table(cut(fig1f_data$GMHI2[fig1f_data$Health_status=="Nonhealthy"], breaks=seq(-6, 6, 1))))
df<-data.frame(healthy_freq,nonhealthy_freq)
df$percentage_H<-round((df$Freq/(df$Freq+df$Freq.1)),digits = 2)
df$percentage_D<-round((df$Freq.1/(df$Freq+df$Freq.1)),digits = 2)
df$total_count<-df$Freq+df$Freq.1
df$diff<-df$percentage_H-df$percentage_D
plot(df$diff, type="l", col="black", pch="o", lty=0.1, ylim=c(0,1),xaxt='n',yaxt='n',xlab = '',ylab = '')
axis(2, seq(0, 1, by = 0.1), seq(0, 1, by = 0.1), las = 2)
par(new=T)
plot(df$percentage_H, type="o", col="#3399CC", pch=19, lty=1,xaxt='n',yaxt='n',xlab = "",ylab = "",main="")
par(new=T)
plot(df$percentage_D, type="o", col="#FF6699", pch=19, lty=1,xaxt='n',yaxt='n',xlab = '',ylab = '')
par(new=T)
hist(fig1f_data$GMHI, col=rgb(0, 1, 0, 0.2),breaks = 12,xlim = c(-6,6),yaxt='n',xlab = '',ylab = '',ylim = c(0,2000),main = "")
par(new=T)
healthy_freq<-data.frame(table(cut(fig1f_data$GMHI[fig1f_data$Health_status=="Healthy"], breaks=seq(-6, 6, 1))))
nonhealthy_freq<-data.frame(table(cut(fig1f_data$GMHI[fig1f_data$Health_status=="Nonhealthy"], breaks=seq(-6, 6, 1))))
df1<-data.frame(healthy_freq,nonhealthy_freq)
df1$percentage_H<-round((df1$Freq/(df1$Freq+df1$Freq.1)),digits = 2)
df1$percentage_D<-round((df1$Freq.1/(df1$Freq+df1$Freq.1)),digits = 2)
df1$total_count<-df1$Freq+df1$Freq.1
df1$diff<-df1$percentage_H-df1$percentage_D
par(new=T)
axis(2, seq(0, 1, by = 0.1), seq(0, 1, by = 0.1), las = 2)
par(new=T)
plot(df1$percentage_H, type="o", col="#99CC99", pch=19, lty=1,xaxt='n',yaxt='n',xlab = "",ylab = "",main="")
par(new=T)
plot(df1$percentage_D, type="o", col="#FF9933", pch=19, lty=1,xaxt='n',yaxt='n',xlab = 'GMWI/GMWI2 bins',ylab = 'Proportion of samples')
legend(x=1,y=0.65, c("GMWI2", "GMWI"), fill=c("red", "#CCFFCC"),cex = 0.7)
legend(x=1,y=0.5, legend=c("GMWI2_H", "GMWI2_NH","GMWI_H","GMWI_NH"), col=c("#3399CC", "#FF6699","#99CC99","#FF9933"), lty=1, cex=0.5)
#fig.1g
fig1g_data<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig1g.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F)
fig1g_data$bal_acc<-fig1g_data$bal_acc*100
par(mar = c(5, 4, 4, 4) + 0.25)
plot(fig1g_data$cutoff,fig1g_data$bal_acc, type="l", col="#336699", pch="o", lty=1,xlab = "GMWI2 magnitude",ylab = "Balanced training set accuracy (%)",main="")
par(new=T)
plot(fig1g_data$cutoff,fig1g_data$samples_retained, type="l", col="#FF9933", pch="o", xaxt='n',yaxt='n',lty=1,xlab = "",ylab = "",main="")
axis(4)
legend("right", legend=c("Balanced training set accuracy", "Number of retained samples"), col=c("#336699","#FF9933"), lty=1,cex = 0.7)
mtext("Number of retained samples",side = 4,line = 3)
#fig1h
fig1h_data<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig1h.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F)
fig1h_data1<-melt(fig1h_data,id.vars = c("Group","magnitude"),measure.vars = c("Healthy","Nonhealthy"))
fig1h_data1$Group<-factor(fig1h_data1$Group,levels = c("Training (GMWI)","Training (GMWI2)","LOOCV (GMWI2)","10-fold CV (GMWI2)"))
ggplot(fig1h_data1, aes(fill=variable, y=value, x=factor(magnitude))) + 
  geom_bar(position="dodge", stat="identity")+scale_fill_manual(values=c("#3399CC", "#FF6699"))+labs(x = "GMWI/GMWI2 magnitude threshold", y="Prediction accuracy (%)",fill = "Phenotype")+facet_wrap(Group~ ., scales="free",ncol = 4)
######################################################################################################################################################################################################################################################
#FIGURE 2:
######################################################################################################################################################################################################################################################
#fig2a
fig2a_data<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig2a.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F)
par(mar = c(5, 4, 4, 4) + 0.25)
fig2a_data$rank<-seq(1,54,1)
fig2a_data1<-melt(fig2a_data[,c(3:5)],id.vars = "rank")
colnames(fig2a_data1)[3]<-"counts"
fig2a_data2<-dcast(fig2a_data1, variable~rank)
row.names(fig2a_data2)<-fig2a_data2$variable
barplot(as.matrix(fig2a_data2[,-1]))
barplot(as.matrix(fig2a_data2[,-1]),
        main = "",
        xlab = "Rank of study", ylab = "ISV accuracy per study (%)",
        col = c("#3399CC", "#FF6699"),
        beside = FALSE,yaxt='n',ylim = c(0,1000))
axis(4)
mtext("Number of samples",side = 4,line = 3)
par(new=T)
plot(fig2a_data$balanced_accuracy, type="o", col="steelblue", pch="o", lty=1,xaxt='n',yaxt='n',xlab = "",ylab = "",main="",ylim = c(0,1))
axis(2)
legend(x=40,y=1, legend=c("# of Healthy samples", "# of Nonhealthy samples"), fill = c("#3399CC","#FF6699"))
#fig2b
#Daniel use your python script
#fig2c
fig2c_data<-read.csv("/Users/m184679/Documents/GMHI-2/Data_for_figures/figure_data/final/fig2c.csv", sep = ",", header = TRUE,na.strings=c("","NA"),check.names = F)
my_comparisons <- list( c("Effect_Baseline", "Effect_6mo"),c("NoEffect_Baseline", "NoEffect_6mo"))
my_comparisons1 <- list( c("Donor","Effect_Baseline"),c("Donor","NoEffect_Baseline"))
plot2<-ggboxplot(fig2c_data, x = "group", y = "shannon_index",
                 color = "black",
                 fill = "group",
                 add = "point",title = "",
                 short.panel.labs = FALSE,outlier.shape=NA,xlab = "", ylab = "GMWI2",order = c("Donor","Effect_Baseline","Effect_6mo","NoEffect_Baseline","NoEffect_6mo"))
plot2+scale_fill_manual(values=c("#FFFFCC","#009933","#333399","#009933","#333399"))+geom_line(aes(group = subjectID))+rremove('legend')+stat_compare_means(comparisons = my_comparisons,paired = T,method.args = list(alternative="less"))+stat_compare_means(comparisons = my_comparisons1,label.y = c(3, 3.5),method.args = list(alternative="greater"))
#fig2d
#Daniel use your python script
#fig2e
#Daniel use your python script
#fig2f
#Daniel use your python script

