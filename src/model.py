
#%%
import numpy as np
import pandas as pd # library for data analysis
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import logging
import sys
from time import time
import click
import mlflow
#%%
# Display progress logs on stdout
logging.basicConfig(filename='logs/model.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
#%%
def plot_dendrogram(model, fname, **kwargs):
    '''
    Function adapted from https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html#sphx-glr-auto-examples-cluster-plot-agglomerative-dendrogram-py
    '''
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    plt.figure(facecolor = 'white')
    plt.figure(figsize = (40, 30), dpi = 100)
    dendrogram(linkage_matrix, **kwargs)
    plt.title("Business Description Dendogram")        
    plt.xlabel("Ticker Symbols")
    plt.savefig(fname)
    return None

def get_model(data):
    mlflow.sklearn.autolog()
    X = data.business_desc.tolist()
    hasher = HashingVectorizer(lowercase = False)
    vectorizer = make_pipeline(hasher, TfidfTransformer())
    X2 = vectorizer.fit_transform(X)
    # setting distance_threshold=0 ensures we compute the full tree.
    model = AgglomerativeClustering(distance_threshold = 0, n_clusters = None,\
        affinity = "l1", linkage = "average")
    with mlflow.start_run() as run:
        model = model.fit(X2.toarray())
        print("Logged data and model in run {}".format(run.info.run_id))
    return(model)

#%%   
@click.command(
    help='''Provide the data path'''
)
@click.option("--path-data", default = "data/thematic.h5", help = "relative path to the data")
@click.option("--fig-name", default = "data/dendrogram.svg", help = "relative path to the dendrogram")
@click.option("--wc-data", default = "data/forreport.csv", help = "relative path to the word cloud file")
def run_model(path_data, fig_name, wc_data):
    with pd.HDFStore(path_data) as store:
        data = store["analysis"]
    model = get_model(data)
    # Visualize the figure
    labels = data.symbol.tolist()
    plot_dendrogram(model, fig_name, labels = labels,\
        orientation = "top", leaf_rotation = 45)
    #For word cloud
    forwc = data.loc[data.symbol.isin(["DG.PA", "RI.PA", "ABI.BR", "CS.PA"])]
    forwc.to_csv(wc_data, index = False)
    return model
# %%
if __name__ == "__main__":
    model = run_model()
    