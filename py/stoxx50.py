
#%%
import pandas as pd # library for data analysis
import requests # library to handle requests
#%%
url = "https://en.wikipedia.org/wiki/EURO_STOXX_50"
response = requests.get(url)
print(response.status_code)
# %%
# %%
all_tables = pd.read_html(response.text)
# convert list to dataframe
df = pd.DataFrame(all_tables[3])
print(df.head())
# %%
df.to_hdf("data/thematic.h5", key = "stoxx50")
# %%
