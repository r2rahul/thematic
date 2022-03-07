rule all:
    input:
        "doc/report.html"
        

rule etl:
    input:
        "data/"
        "doc/figs"
    output:
        "data/thematic.h5"
    script:
        "src/etl.py"

rule model:
    input:
        "data/thematic.h5"
    output:
        "data/dendrogram.svg"
        "data/forreport.csv"
    script:
        "src/model.py"

rule report:
    input:
        "data/dendrogram.svg"
        "data/forreport.csv"
    output:
        "doc/report.html"
    shell:
        Rscript.exe "doc/run_report.R"

onsuccess:
    print("Workflow finished, no error")