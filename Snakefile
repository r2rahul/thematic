rule all:
    input:
        "doc/report.html"
        

rule etl:
    input:
        path_files="data/",
        path_figs="doc/figs"
    output:
        "data/thematic.h5"
    script:
        "src/etl.py --path-files {input.path_files} --path-figs {input.path_figs}"

rule model:
    input:
        data_store="data/thematic_20220306.h5",
        fig_name="data/dendrogram.svg",
        wc_data="data/forreport.csv",
    output:
        "data/dendrogram.svg"
        "data/forreport.csv"
    script:
        "src/model.py --path-data {input.data_store} --fig-name {input.fig_name} --wc-data {input.wc_data}"

rule report:
    input:
        "data/dendrogram.svg",
        "data/forreport.csv",
    output:
        "doc/report.html"
    shell:
        "Rscript.exe run_report.r"

onsuccess:
    print("Workflow finished, no error")