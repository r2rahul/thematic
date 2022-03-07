library(rmarkdown)
library(here)
library(glue)
wd <- glue("{here()}/doc/")
render("report.Rmd", 
knit_root_dir = wd,
output_dir = wd
)