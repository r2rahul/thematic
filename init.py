#%%
import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import pandas_profiling as pp

from py.etl import clean_text, create_wordcloud
# %%
with pd.HDFStore("data/thematic_20220305.h5") as store:
    data = store["desc"]
data.head()
#%%
data = data.loc[:, ["symbol", "longBusinessSummary", "sector", "industry", "country"]]

# %%
data["business_desc"] = data.longBusinessSummary.apply(clean_text)
# %%
text = " ".join(data.business_desc.tolist())
text = " ".join(w for w in text.split() if w != "company")
text_nclean = " ".join(data.longBusinessSummary.tolist())
# %%
create_wordcloud(text)
# %%
create_wordcloud(text_nclean, "data/wc_notclean.png")
# %%
X = data.business_desc.tolist()
textfile = open("data/text_data.txt", "w")
for element in X:
    textfile.write(element + "\n")
textfile.close()
# %%
