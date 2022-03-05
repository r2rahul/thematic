#%%
import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import pandas_profiling as pp

from etl import clean_text, create_wordcloud
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
# %%
create_wordcloud(text)
# %%
