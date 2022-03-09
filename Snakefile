rule all:
    input:
        "data/thematic.h5",
        "data/dendrogram.svg",
        "data/forreport.csv",
        "doc/report.html",


rule etl:
    input:
        script = "src/etl.py",
        path_files="data/",
        path_figs="doc/figs",
    output:
        "data/thematic.h5",
    shell:
        "python {input.script} --path-files {input.path_files} --path-figs {input.path_figs}"
        

rule model:
    input:
        script = "src/model.py",
        data_store="data/thematic.h5",
        fig_name="data/dendrogram.svg",
        wc_data="data/forreport.csv",
    output:
        "data/dendrogram.svg",
        "data/forreport.csv",
    shell:
        "python {input.script} --path-data {input.data_store} --fig-name {input.fig_name} --wc-data {input.wc_data}"
        

rule report:
    input:
        "data/dendrogram.svg",
        "data/forreport.csv",
    output:
        "doc/report.html",
    shell:
        "Rscript.exe run_report.r"


onsuccess:
    print("Workflow finished, no error")
