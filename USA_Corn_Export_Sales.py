import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# 1. Web Scraping
source = requests.get("https://apps.fas.usda.gov/export-sales/myfiaug.htm").text
soup = BeautifulSoup(source, 'lxml')

pre = soup.find('pre')
start_text = 'CORN - UNMILLED'
end_text = 'OPTIONAL ORIGIN'

page_text = pre.text.strip()
start_position = page_text.find(start_text)
end_position = page_text.find(end_text)
table_text = page_text[start_position:end_position]
lines = table_text.splitlines()
lines = lines[10:-2] # select the countries part


# 2. Data Manipulating
country = [l.split(':')[0] for l in lines]
numbers = [l.split(':')[-1] for l in lines]

ex_2017 = []
ex_2018 = []

for n in numbers:
    if len(n) == 0: # to exclude the empty '' in numbers
        pass
    elif len(n) == 80: # to exclude the dash line '---------'
        pass
    else:
        x = n.split()
        ex_2018.append(x[-2])
        ex_2017.append(x[-1])

country = [c.strip() for c in country] # use .strip() to remove the spaces in text

new_country = []
for c in country:
    if len(c) == 0:
        pass
    elif len(c) == 80:
        pass
    else:
        new_country.append(c)

df1 = pd.DataFrame(new_country)
df1.rename(columns={0:'Country'}, inplace=True)
df2 = pd.DataFrame(ex_2017)
df2.rename(columns={0:'2017'}, inplace=True)
df3 = pd.DataFrame(ex_2018)
df3.rename(columns={0:'2018'}, inplace=True)

df = pd.concat([df1['Country'], df2['2017'], df3['2018']], axis=1)
df.set_index('Country', inplace=True)

df['2017'] = pd.to_numeric(df['2017'], errors='coerce') 
 #By setting errors=’coerce’, you’ll transform the non-numeric values into NaN.
df['2018'] = pd.to_numeric(df['2018'], errors='coerce')


top5_2017 = df.sort_values(['2017'], ascending=False).drop(index={
    'TOTAL KNOWN', 'WESTERN HEMISPHERE', 'OTHER ASIA AND OCEANIA'})['2017'].head()
top5_2018 = df.sort_values(['2018'], ascending=False).drop(index={
    'TOTAL KNOWN', 'WESTERN HEMISPHERE', 'OTHER ASIA AND OCEANIA'})['2018'].head()

top5_2017.rename({'KOR REP':'KOREA', 'COLOMB':'COLOMBIA'}, inplace=True)
top5_2018.rename({'KOR REP':'KOREA', 'COLOMB':'COLOMBIA'}, inplace=True)

labels2017 = top5_2017.index.to_list()
export2017 = top5_2017.to_list()
total2017 = df.loc['TOTAL KNOWN']['2017']
perc2017 = []
for e in export2017:
    e = round((e/total2017)*100,2)
    perc2017.append(e)

labels2018 = top5_2018.index.to_list()
export2018 = top5_2018.to_list()
total2018 = df.loc['TOTAL KNOWN']['2018']
perc2018 = []
for e in export2018:
    e = round((e/total2018)*100,2)
    perc2018.append(e)

# 4. Annotations

def autolabel(rects): # for single-year graph
    for rect in rects:
        width = rect.get_width()
        ax.annotate('{}%'.format(width),
                    xy=(width, rect.get_y()),
                    xytext=(20,10),
                    textcoords='offset points',
                    ha='center', va='bottom')

def autolabel_MT(rects): # for single-year graph, unit in 1000MT
    for rect in rects:
        width = rect.get_width()
        ax.annotate('{}'.format(width),
                    xy=(width, rect.get_y()),
                    xytext=(25,10),
                    textcoords='offset points',
                    ha='center', va='bottom')


def autolabel_2(rects): # for two-years graph
    for rect in rects:
        width = rect.get_width()
        ax.annotate('{}%'.format(width),
                    xy=(width, rect.get_y() + rect.get_height()/2),
                    xytext=(25,-5),
                    textcoords='offset points',
                    ha='center', va='bottom')  

def autolabel_2_MT(rects): # for two-years graph, unit in 1000MT
    for rect in rects:
        width = rect.get_width()
        ax.annotate('{}'.format(width),
                    xy=(width, rect.get_y() + rect.get_height()/2),
                    xytext=(25,-5),
                    textcoords='offset points',
                    ha='center', va='bottom')  

# 3. Visualisation by Matplotlib

"""
# for 2017, unit in %
y = np.arange(len(labels2017))
width = 0.35

fig, ax = plt.subplots(figsize=(18,8))
rects1 = ax.barh(y, perc2017, width, label='2017', alpha=0.8)
ax.set_title('2017 USA Corn Export Sales top 5 countries', fontsize=25)
ax.set_xlabel('Export Sales (%)')
ax.set_yticks(y)
ax.set_yticklabels(labels2017, fontsize=15)
autolabel(rects1)
"""
"""
# for 2017, unit in 1000MT
y = np.arange(len(labels2017))
width = 0.35

fig, ax = plt.subplots(figsize=(18,8))
rects1 = ax.barh(y, export2017, width, label='2017', alpha=0.8)
ax.set_title('2017 USA Corn Export Sales top 5 countries', fontsize=25)
ax.set_xlabel('Export Sales (1000MT)')
ax.set_yticks(y)
ax.set_yticklabels(labels2017, fontsize=15)
autolabel_MT(rects1)
"""


"""
# for 2018, unit in %
y = np.arange(len(labels2018))
width = 0.35

fig, ax = plt.subplots(figsize=(18,8))
rects2 = ax.barh(y, perc2018, width, label='2018', alpha=0.8, color='r')
ax.set_title('2018 USA Corn Export Sales top 5 countries', fontsize=25)
ax.set_xlabel('Export Sales (%)')
ax.set_yticks(y)
ax.set_yticklabels(labels2018, fontsize=15)
autolabel(rects2)
"""
"""
# for 2018, unit in 1000MT
y = np.arange(len(labels2018))
width = 0.35

fig, ax = plt.subplots(figsize=(18,8))
rects2 = ax.barh(y, export2018, width, label='2018', alpha=0.8, color='r')
ax.set_title('2018 USA Corn Export Sales top 5 countries', fontsize=25)
ax.set_xlabel('Export Sales (1000MT)')
ax.set_yticks(y)
ax.set_yticklabels(labels2018, fontsize=15)
autolabel_MT(rects2)
"""

"""
# for 2017 & 2018, unit in %
y = np.arange(len(labels2018))
width = 0.35

fig, ax = plt.subplots(figsize=(18,8))
rects3 = ax.barh(y+width/2, perc2017, width, label='2017', alpha=0.8)
rects4 = ax.barh(y-width/2, perc2018, width, label='2018', alpha=0.8)
ax.set_title('2017 & 2018 USA Corn Export Sales top 5 countries', fontsize=25)
ax.set_xlabel('Export Sales (%)')
ax.set_yticks(y)
ax.set_yticklabels(labels2018, fontsize=15)
ax.legend(loc='upper right', prop={'size':15})
autolabel_2(rects3)
autolabel_2(rects4)
"""
"""
# for 2017 & 2018, unit in 1000MT
y = np.arange(len(labels2018))
width = 0.35

fig, ax = plt.subplots(figsize=(18,8))
rects3 = ax.barh(y+width/2, export2017, width, label='2017', alpha=0.8)
rects4 = ax.barh(y-width/2, export2018, width, label='2018', alpha=0.8)
ax.set_title('2017 & 2018 USA Corn Export Sales top 5 countries', fontsize=25)
ax.set_xlabel('Export Sales (1000MT)')
ax.set_yticks(y)
ax.set_yticklabels(labels2018, fontsize=15)
ax.legend(loc='upper right', prop={'size':15})
autolabel_2_MT(rects3)
autolabel_2_MT(rects4)
"""

"""
# Make Example graph for Medium article
y = np.arange(len(labels2018))
width = 0.35

fig, ax = plt.subplots(figsize=(18,8))
rects3 = ax.barh(y+width/2, export2017, width, label='2017', alpha=0.8)
rects4 = ax.barh(y-width/2, export2018, width, label='2018', alpha=0.8)
ax.set_title('matplotlib.pyplot.barh()', fontsize=25)
ax.set_xlabel('Width', fontsize=20)
ax.set_yticks(y)
ax.set_ylabel('y', fontsize=20)
"""

