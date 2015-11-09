# This is template for python
# PARAMETERS TO BE CHANGED:
#    - W-ORKING_DIR:  os.getcwd()
#    - C-SV_FILE   :  1_sample.csv
#    - G-ROUP_VECTOR
#    - O-UT_PDF_FILE
#    - O-UT_PNG_FILE

setwd('WORKING_DIR')

library(devtools)
library(ggbiplot)

d <- read.csv('CSV_FILE', header=TRUE)
d.pca <- prcomp(d, scale. = TRUE)
d.class <- c(GROUP_VECTOR)


pdf(file='OUT_PDF_FILE')
ggbiplot(d.pca, obs.scale = 1, var.scale = 1,  groups = d.class, ellipse = TRUE, circle = TRUE) +  scale_color_discrete(name = '') +  theme(legend.direction = 'horizontal', legend.position = 'top')
dev.off()

png(file='OUT_PNG_FILE',  bg="transparent" )
ggbiplot(d.pca, obs.scale = 1, var.scale = 1,  groups = d.class, ellipse = TRUE, circle = TRUE) +  scale_color_discrete(name = '') +  theme(legend.direction = 'horizontal', legend.position = 'top')
dev.off()
