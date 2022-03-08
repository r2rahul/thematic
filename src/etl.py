#%%
import numpy as np
import pandas as pd
import dask.bag as db
import random
import click
import logging
import requests
import yfinance as yf
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from textblob.blob import TextBlob
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
#Initialize global parameters
random.seed(1729)
logging.basicConfig(filename='logs/etl.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
words = set(nltk.corpus.words.words())
stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
stem_word = PorterStemmer()
#Additional Stop Words
add_stop = ["also", "date", "time", "company", "llc", "ltd"]
stop_words + add_stop
#%%
def get_stoxx50(data_path):
    url = "https://en.wikipedia.org/wiki/EURO_STOXX_50"
    #tstamp = pd.Timestamp.now().strftime("%Y%m%d")
    data_store = data_path + "thematic" + ".h5"
    response = requests.get(url)
    if response.status_code == 200:
        all_tables = pd.read_html(response.text)
        # convert list to dataframe
        df = pd.DataFrame(all_tables[3])
        with pd.HDFStore(data_store) as store:
            store.put("stoxx50", df)
        logging.info("Success getting the Stoxx50 Universe")
    else:
        logging.info("Error reading the web url code = {}".format(response.status_code))
    return(data_store)
#%%
def help_yfinance(symbol):
    logging.info("Starting Symbol {}".format(symbol))
    try:
        data = yf.Ticker(symbol)
    except Exception as e:
        logging.error("Error symbol {}".format(symbol), exc_info = True)
    return(data.info)

def get_bus_desc(data_store):
    with pd.HDFStore(data_store) as store:
        data = store["stoxx50"]
    symbols = data.Ticker.tolist()
    results = db.from_sequence(symbols).map(help_yfinance).compute()
    out = pd.DataFrame(results)
    with pd.HDFStore(data_store) as store:
        store.put("desc", out)
    return(out)
#%%
def clean_text(text):
    try:
        out = " ".join(w for w in nltk.wordpunct_tokenize(text) \
                    if w.lower() in words \
                    and w.lower() not in stop_words \
                    and len(w.lower()) > 2)
        out = out.strip().replace("\s+", "\s")
    except Exception as e:
        logging.debug("Could not lemmatize or stem {}".format(e))
        out = ""
    # Next lemmatize the text
    try:
        out = lemmatizer.lemmatize(out, pos = "a") 
        out = stem_word.stem(out)
    except Exception as e:
        logging.debug("Could not lemmatize or stem {}".format(e))
        out = ""
    return(out)

def create_wordcloud(text, fname = "data/wc.png", show = False):
    wordcloud = WordCloud(background_color = 'white').generate(text)
    wordcloud.to_file(fname)
    # Display the generated image:
    if show:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
    return(fname)

def get_analysis(data, data_store):
    data = data.dropna(subset=["symbol"])
    data = data.loc[:, ["symbol", "longBusinessSummary", "sector", "industry", "country"]]
    data["business_desc"] = data.longBusinessSummary.apply(clean_text)
    with pd.HDFStore(data_store) as store:
        store.put("analysis", data)
    return(data)
#%%   
@click.command(
    help='''Provide the data director like data/
    the code will write a data in the data director with
    thematic[timestamp].h5'''
)
@click.option("--path-files", default = "data/", help = "relative path to current working directory")
@click.option("--path-figs", default = "doc/figs/", help = "relative path to store figures")
def run_etl(path_files, path_figs):
    store_path = path_files
    curr_store = get_stoxx50(store_path)
    df = get_bus_desc(curr_store)
    data = get_analysis(df, curr_store)
    # Generate Word Cloud
    text = " ".join(data.business_desc.tolist())
    text = " ".join(w for w in text.split() if w != "company")
    text_nclean = " ".join(data.longBusinessSummary.tolist())
    path_wc_clean = path_figs + "wc_clean" + ".png"
    path_wc_nclean = path_figs + "wc_nclean" + ".png"
    create_wordcloud(text, path_wc_clean)
    create_wordcloud(text_nclean, path_wc_nclean)
    return None

if __name__ == "__main__":
    run_etl()