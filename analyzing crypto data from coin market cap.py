#!/usr/bin/env python
# coding: utf-8

# ### Project details.
# in this project I tried to automate the process of extracting real time data using coin_market_cap_API. And perform exploratory data analysis on the extracted data.

# In[47]:


# testing coinmarket_cap API 

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'500',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'a4373e3f-f98b-403b-8887-9989d5a673bb',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# In[48]:


import pandas as pd
data_df = pd.json_normalize(data["data"])


# In[49]:


data_df
# doesnot show all the columns 


# In[50]:


# to show all the columns 

pd.set_option('display.max_columns',None)
data_df


# In[3]:


import os 

def run_api():
    global data_df
    from requests import Request, Session
    from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
    import json

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'20',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'a4373e3f-f98b-403b-8887-9989d5a673bb',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    # avoid duplicating values in the script. 
    data_df = pd.json_normalize(data['data'])
    data_df['timestamp'] = pd.to_datetime('now')
    data_df
   
    # below script will let us store the whole data frame in a csv file format. 
    if not os.path.isfile(r"C:\Users\hp\Documents\cryto api data\Cypto_data2.csv"):
        data_df.to_csv(r"C:\Users\hp\Documents\cryto api data\Cypto_data2.csv", header = "column_names")
    else:
        data_df.to_csv(r"C:\Users\hp\Documents\cryto api data\Cypto_data2.csv", mode = "a", header = False)
        


        


# In[6]:


from time import time 
from time import sleep
for i in range(2):
    run_api()
    print("execution done")
    sleep(60) # api will run after every 1 minute
exit()


# In[51]:


# formating the data in a more understandable form

data_df.style.format({"max_supply": "{:.5f}"})
data_df.style.format({"circulating_supply": "{:.5f}"})
data_df


# In[52]:


data_df2 = data_df.rename(columns={'quote.USD.last_updated':'time_stamp'})


# In[53]:


# changing the position of the timestamp

sixth_col = data_df2.pop('time_stamp')
data_df2.insert(6, 'time_stamp', sixth_col)
data_df2


# ## above we have 3 matrics:
# 
# market dominance = the measure of the quallity of a token relative to its competition
# 
# dilluted market cap = market cap when all of the tokens have been mined or released
# 
# market cap = current overall value of the token in fiat

# In[12]:


# sorting the data to so as to make it more understandable

data_df3 = data_df.groupby('name', sort=False)[[  'quote.USD.market_cap', 'quote.USD.market_cap_dominance','quote.USD.fully_diluted_market_cap']].mean()


# In[13]:


data_df3.head(15)


# In[14]:


data_df2['token_price'] = data_df2['quote.USD.market_cap']/data_df2['circulating_supply'] 
tokenPrice = data_df2.pop('token_price')
data_df2.insert(3, 'token_price', tokenPrice)
data_df3 = data_df2.head(15)
data_df3


# In[15]:


data_df4 = data_df3[['name', 'token_price']]


# In[16]:


data_df5 = data_df4.transpose()
data_df5


# ### A plot to show the comparison between crypto currencies

# In[17]:


ax = data_df4.plot.bar(figsize=(12, 5), legend=False)
ax.set_xlabel("name")
ax.set_ylabel('token_price')


# #### Becuase of the high price of the bitcoin we can't analyze the others so we decide to drop it 

# In[18]:


# don't touch it 
data_df5.drop(data_df5.columns[[0]], axis = 1, inplace = True)


# In[106]:


data_df5


# In[19]:


data_df6 = data_df5.transpose()
data_df6


# #### to know about the token prices excluding bitcoin. 

# In[21]:


import seaborn as sns

sns.set(rc={'figure.figsize':(12,5)})

sns.barplot(x= data_df6['name'], y=data_df6['token_price']/1000, data=data_df6)


# In[22]:


data_df7 = data_df6.drop(1)


# In[23]:


sns.set(rc={'figure.figsize':(12,5)})

sns.barplot(x= data_df7['name'], y=data_df7['token_price']/1000, data=data_df7)


# # now we'll analyze the performance of the Meme_Coins vs Legit_Coins
# 
# for this experiment we'll look into the performance of some Meme coins and compare it with the performance of the Legit_coins
# 
# The matrix of measure that we'll take is " PERCENT CHANGE" that occurs in the price of a coin during a period of the ninety days.
# 
# Selected Coins are:
# 
# Meme coins: 1) Dogecoin, 2) Shiba Inu
# 
# Legit coins: 1) Bitcoin, 2) Ethereum, 3) Polkadot, 4) Solana

# In[240]:


data_df10 = data_df.groupby('name', sort=False)[['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_90d']].mean()


# In[25]:


data_df10


# In[26]:


data_df11 = data_df10.head(20)


# In[27]:


data_df11.rename(columns={'quote.USD.percent_change_1h' : '1H',
                           'quote.USD.percent_change_24h' :'24H', 
                           'quote.USD.percent_change_7d' :'7D',
                           'quote.USD.percent_change_30d' :'30D',
                               'quote.USD.percent_change_90d' :'90D'}, inplace = True) 


# In[ ]:





# In[28]:


data_df11


# In[29]:


# this returns a series and hence we will need to convert that series into a data frame

data_df12 = data_df11.stack()
data_df12


# In[155]:


data_df12.count()


# In[156]:


data_df12.to_frame(name='values')


# In[100]:


data_df13 = data_df12.reset_index()
data_df13


# ### Let's look at the collective performance of all the coins over the past 90 Days

# In[101]:


data_df13['values'] = data_df13[0]
data_df14 = data_df13.drop(columns=[0])
data_df14


# ### A plot to show the overall performance of the crypto market in the past 90 days 
# 

# In[32]:


# plot to show the overall performance of all the coins. 

sns.catplot(x= "level_1", y="values", hue="name", data=data_df14, kind = "point", height=5, aspect=2)


# In[33]:


data_df11


# ## look at the performace of BNB in past 90 days

# In[103]:


pd.set_option('display.max_columns',None)
data_df14


# In[154]:


data_df15 = data_df14.loc[data_df14['name'] == 'Bitcoin']
data_df15


# In[107]:


import seaborn as sns


# In[155]:


sns.lineplot(x= data_df15['level_1'], y= data_df15['values'], color='green')


# In[119]:


data_dfDC = data_df14.loc[data_df14['name'] == 'Dogecoin']


# In[120]:


data_dfDC


# In[152]:


sns.lineplot(x= data_dfDC['level_1'], y= data_dfDC['values'], color='red')


# In[143]:


import matplotlib.pyplot as plt 


# In[169]:


plt.plot(data_df15['level_1'], data_df15['values'], label= "bitcoin", color='green')
plt.plot(data_dfDC['level_1'], data_dfDC['values'], label= "dogecoin", color = "red")


plt.xlabel = 'TIME'
plt.ylabel = 'PRICE'
plt.legend()
plt.show()


# In[159]:


data_dfSOL = data_df13.loc[data_df13['name'] == 'Solana']
data_dfSOL


# In[161]:


data_dfDOT = data_df13[data_df13['name'] == 'Polkadot']
data_dfDOT


# In[165]:


data_dfSHIB = data_df14[data_df14['name'] == 'Shiba Inu']
data_dfSHIB


# In[168]:


plt.plot(data_df15['level_1'], data_df15['values'], label= "bitcoin", color='green')
plt.plot(data_dfDC['level_1'], data_dfDC['values'], label= "dogecoin", color = "red")
plt.plot(data_dfDOT['level_1'], data_dfDOT['values'], label= "DOT", color = "black")
plt.plot(data_dfSOL['level_1'], data_dfSOL['values'], label= "SOL", color = "blue")
plt.plot(data_dfSHIB['level_1'], data_dfSHIB['values'], label= "SHIB", color = "orange")

plt.xlabel = 'TIME'
plt.ylabel = 'PRICE'
plt.legend()
plt.show()


# 
# #### from the above exploratory data anlysis of the crypto market, we can say that meme coins proved to be better at performing than the legit coins like BIT, SOL, DOT
# 

# In[ ]:




