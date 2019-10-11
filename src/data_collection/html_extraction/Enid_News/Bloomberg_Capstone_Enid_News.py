#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import warnings
warnings.filterwarnings('ignore')


# In[2]:


bbg_data=pd.read_csv('Bloomberg_data.csv',header=None)
bbg_data.columns=['Source','Timestamp','Category','URL']
bbg_data.head()


# In[ ]:


Enid_News=bbg_data[(bbg_data['Source']=="Enid News")].reset_index(drop=True)


# In[ ]:


bad_url=[]
c=0
for url in Enid_News['URL']:
    print(c)
    c=c+1
    r=requests.get(url)
    if r.status_code!=200:
        bad_url.append(url)
        print(url)


# In[ ]:


bad_url_frame=pd.DataFrame(columns=['URL'])
bad_url_frame['URL']=bad_url
bad_url_frame.to_csv('Enid_news_bad_url.csv')


# In[3]:


bad_url=pd.read_csv('Enid_news_bad_url.csv')
bad_url.head(5)


# In[4]:


Enid_News=bbg_data[(bbg_data['Source']=="Enid News")&(bbg_data['URL'].isin(bad_url['URL'])==False)].reset_index(drop=True)
Enid_News.head()
print(len(Enid_News))


# In[ ]:


len(bad_url)


# In[5]:


Enid_News['Category'].value_counts()


# In[ ]:


c=0
def get_metadata(url):
    global c
    print(c)
    c=c+1
    r = requests.get(url) 
    html_soup = BeautifulSoup(r.content, 'lxml')
    text = ''
    date= ''
    title=''
    author=''
    keywords=''
    description=''
    
    #To access article content
    if html_soup.findAll('div', attrs = {"itemprop" : "articleBody"}) is not None:
        temp_soup = html_soup.find('div', attrs = {"itemprop" : "articleBody"})
        try:
            soup = temp_soup.findAll('p')
            for s in soup:
                text = text + ' ' + s.get_text()
        except:
            print(url)
    else:
        print('Content')
    content=text.replace(u"\xa0","")# to remove latin space
    
    
    #To acess article date
    if html_soup.find('meta',attrs={"itemprop":"dateCreated"}) is not None:
        date=html_soup.find('meta',attrs={"itemprop":"dateCreated"})["content"]
        date=date.split("T")[0]
    else:
        print("Date")
    
    
    #To acess the title   
    if html_soup.find('meta',attrs={"property":"og:title"})is not None:
        title=html_soup.find('meta',attrs={"property":"og:title"})["content"]
        if "|" in title:
            title=title.split("|")[0]
    else:
        print("Title")
    title=title.replace(u"\xa0","")
    print(title)
    
    #To acess the author
    if html_soup.find('meta',attrs={"name":"author"}) is not None:
        author=html_soup.find('meta',attrs={"name":"author"})["content"]
        if "|" in author:
            author=author.split("|")[0]
    else:
        print("author")
    author=author.replace(u"\xa0","")
    
    
    #To access keywords
    if html_soup.find('meta',attrs={"name":"news_keywords"}) is not None:
        keywords=html_soup.find('meta',attrs={"name":"news_keywords"})["content"]
    else:
        print("Keywords")
    keywords=keywords.replace(u"\xa0","")
    
    
    #To access general description of the article
    if html_soup.find('meta',attrs={"name":"description"}) is not None:
        description=html_soup.find('meta',attrs={"name":"description"})["content"]
    else:
        print("Description")
    description=description.replace(u"\xa0","") 
    
    
    return (content,date,title,author,keywords,description)


# In[ ]:


Enid_News['Content'],Enid_News['Date'],Enid_News['Title'],Enid_News['Author'],Enid_News['Keywords'],Enid_News['Description'] = zip(*Enid_News['URL'].apply(get_metadata))


# In[35]:


Enid_news1=Enid_News.copy()


# In[36]:


Enid_news1['ind']=Enid_news1['URL'].apply(lambda x: 'guest' if 'guest' in x else('opinion' if 'opinion' in x else 'regular'))


# In[38]:


Enid_News['Category']=Enid_news1['ind']


# In[39]:


Enid_News.head()


# In[40]:


Enid_News.to_csv('Bloomberg_Enid_News.csv')


# In[ ]:




