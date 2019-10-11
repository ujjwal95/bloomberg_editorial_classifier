
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import warnings
warnings.filterwarnings('ignore')

bbg_data=pd.read_csv('Bloomberg_data.csv',header=None)
bbg_data.columns=['Source','Timestamp','Category','URL']
bbg_data.head()

Enid_News=bbg_data[(bbg_data['Source']=="Enid News")].reset_index(drop=True)

bad_url=[]
c=0
for url in Enid_News['URL']:
    r=requests.get(url)
    if r.status_code!=200:
        bad_url.append(url)
        print(url)

        
bad_url_frame=pd.DataFrame(columns=['URL'])
bad_url_frame['URL']=bad_url
bad_url_frame.to_csv('Enid_news_bad_url.csv')

bad_url=pd.read_csv('Enid_news_bad_url.csv')
bad_url.head(5)

Enid_News=bbg_data[(bbg_data['Source']=="Enid News")&(bbg_data['URL'].isin(bad_url['URL'])==False)].reset_index(drop=True)
Enid_News['Category'].value_counts()


def get_metadata(url):
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
        html_soup1 = html_soup.find('div', attrs = {"itemprop" : "articleBody"})
        try:
            soup = html_soup1.findAll('p')
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
    
    # return all the metadata
    return (content,date,title,author,keywords,description)


Enid_News['Content'],Enid_News['Date'],Enid_News['Title'],Enid_News['Author'],Enid_News['Keywords'],Enid_News['Description'] = zip(*Enid_News['URL'].apply(get_metadata))

Enid_news1=Enid_News.copy()
Enid_news1['ind']=Enid_news1['URL'].apply(lambda x: 'guest' if 'guest' in x else('opinion' if 'opinion' in x else 'regular'))
Enid_News['Category']=Enid_news1['ind']
Enid_News.to_csv('Bloomberg_Enid_News.csv')
