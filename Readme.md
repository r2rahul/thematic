# Introduction
The repository is the analysis repository for the case study [Finding peer stocks using business description of a company](https://rpubs.com/r2rahul/874302)

# Executing the code
 There are three ways to execute the code. 
 ### Native Python
 1. Step 1: execute the code ``` python py/etl.py --path-files "data/" --path-figs "doc/figs/" ```
 2. Step 2: Step 1 will create a time stamped data file in the data directory (example data is given in data directory) ``` python py/model.py --path-data "data/thematic_20220306.h5""```
   
### SnakeMake
[Snakemake](https://snakemake.readthedocs.io/en/stable/index.html) user can just type in ```snakemake --cores 1``` from command shell. Please note Rscript and Python should be in path

### Mlflow

[Mlflow](https://www.mlflow.org/) users can just type ```mlflow run .```

# Schema thematic.h5

|  key |  data |
|---|---|
| stoxx50  | Euro Stoxx50 Universe  |
|  desc | Yahoo finance data  |
| analysis  | Analysis data  |
