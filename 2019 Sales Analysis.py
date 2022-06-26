#!/usr/bin/env python
# coding: utf-8

# In[173]:


import pandas as pd
import os
import matplotlib.pyplot as plt


# In[174]:


#Read 12 months of sales data (individual files) and put into single file.

df = pd.read_csv('./Sales_Data/Sales_April_2019.csv')

all_sales_data = pd.DataFrame()

filenames = []
for file in os.listdir('./Sales_Data/'):
    filenames.append(file)

for file in filenames:
    df = pd.read_csv('./Sales_Data/' + file)
    all_sales_data = pd.concat([all_sales_data, df])

all_sales_data.to_csv('all_sales_data.csv', index = False)


# In[175]:


#Read updated DF

sales_2019 = pd.read_csv('all_sales_data.csv')

sales_2019.head()


# In[176]:


#Cleaning data


# In[177]:


nan_df = sales_2019[sales_2019.isna().any(axis=1)]
nan_df.head(100)


# In[178]:


#found many Nan values. Dropping those here.
sales_2019 = sales_2019.dropna(how ='all')
sales_2019.head()


# In[179]:


sales_2019 = sales_2019[sales_2019['Order Date'].str[:2] != 'Or']
sales_2019


# In[180]:


#converting columns to correct type

sales_2019['Quantity Ordered'] = pd.to_numeric(sales_2019['Quantity Ordered'])
sales_2019['Price Each'] = pd.to_numeric(sales_2019['Price Each'])


# In[105]:


#adding additional columns for clarity/ease of use


# In[181]:


#adding month column

sales_2019['Month'] = sales_2019['Order Date'].str[:2]
sales_2019['Month'] = sales_2019['Month'].astype('int32')

sales_2019


# In[ ]:





# In[ ]:





# In[182]:


#We need to add a new column combining 'Quantity' with 'Price' to get the total $ Per sale.

sales_2019['Sales'] = (sales_2019['Price Each'] * sales_2019['Quantity Ordered'])
sales_2019.head()


# In[183]:


#What was the best month for sales in 2019? How much was earned that month?

sales_by_month = sales_2019.groupby('Month').sum()
sales_by_month.sort_values(by='Sales', ascending = False)

#answer: December


# In[184]:


months = range(1,13)

plt.bar(months, sales_by_month['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month in 2019')
plt.show()


# In[200]:


# Which city had the most sales in 2019?

def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

sales_2019['City'] = sales_2019['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

sales_2019


# In[204]:


sales_by_city = sales_2019.groupby('City').sum()
sales_by_city.sort_values(by='Sales', ascending = False)

#city with highest sales in 2019 was San Francisco.


# In[210]:


cities = [city for city, df in sales_2019.groupby('City')]

plt.bar(cities, sales_by_city['Sales'])
plt.xticks(cities, rotation = 'vertical')
plt.ylabel('Sales in USD ($)')
plt.xlabel('U.S. City')
plt.show()


# In[213]:


#What time should we show advertisements to maximize likelihood for sale?

sales_2019.head(2)


# In[216]:


#convert order date to datetime format

sales_2019['Order Date'] = pd.to_datetime(sales_2019['Order Date'])

sales_2019.head(2)


# In[220]:


#create a new hour and minute column to make analysis easier

sales_2019['Hour'] = sales_2019['Order Date'].dt.hour
sales_2019['Minute'] = sales_2019['Order Date'].dt.minute
sales_2019.head(3)


# In[262]:


sales_by_hour = sales_2019.groupby(['Hour']).count()['Order ID']


# In[261]:


sales_by_hour.plot()
plt.xticks(hours)
plt.ylabel('Number of Orders')
plt.grid()
plt.show()

#Peak ordering times are between 11am - 12pm and 7pm - 9pm
#May want to adjust advertising timing accordingly. Right before either of these time frames may produce better results. 


# In[274]:


#What products are most often sold together?

dup_orders = sales_2019[sales_2019['Order ID'].duplicated(keep = False )]

dup_orders['Grouped'] = dup_orders.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))


dup_orders = dup_orders[['Order ID', 'Grouped']].drop_duplicates()

dup_orders.head()


# In[279]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in dup_orders['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key, value in count.most_common(10):
    print(key, value)
    
#below are the most common items sold together. This could fuel promotional ideas to lure in more customers who may be interested in buying additional products


# In[301]:


#What were the most popular products in 2019?

most_pop_product = sales_2019.groupby('Product').sum()['Quantity Ordered']

most_pop_product



# In[312]:


most_pop_product.plot.bar()
plt.ylabel('Quantity Ordered')
plt.show()


# In[309]:


#triple A batteries are the highest sold item along with double a batteries, lightning charging cords etc. 


# In[ ]:




