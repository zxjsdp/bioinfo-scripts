setwd('WORKING_DIR')

library("FactoMineR")


d = read.csv("CSV_FILE", header=T)
rownames(d) <- ROW_NAMES

pdf(file='OUT_PDF_PATH')
res.pca <- PCA(d, quali.sup=GROUP_INDEX_LINE)
plotellipses(res.pca, GROUP_INDEX_LINE)
dev.off()

res.pca <- PCA(d, quali.sup=GROUP_INDEX_LINE)
png(file='OUT_PNG_PATH')
plotellipses(res.pca, GROUP_INDEX_LINE)
dev.off()
