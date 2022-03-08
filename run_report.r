library(rmarkdown)
library(here)
library(glue)
wd <- glue("{here()}/doc/")
setwd(wd)
message(wd)
render("report.Rmd", 
knit_root_dir = wd,
output_dir = wd
)