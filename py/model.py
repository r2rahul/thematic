
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
from sklearn.cluster import KMeans, MiniBatchKMeans
import logging
import sys
from time import time
# Display progress logs on stdout
logging.basicConfig(filename='logs/model.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
