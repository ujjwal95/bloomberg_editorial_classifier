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

Californian=bbg_data[(bbg_data['Source']=="Californian")].reset_index(drop=True)
Californian.head()
print(len(Californian))

bad_url=[]
c=0
for url in Californian['URL']:
    print(c)
    c=c+1
    r=requests.get(url)
    if r.status_code!=200:
        bad_url.append(url)
        print(url)

len(bad_url)
bad_url_frame=pd.DataFrame(columns=['URL'])
bad_url_frame['URL']=bad_url
bad_url_frame.to_csv('Californian_bad_url.csv')

bad_url=pd.read_csv('Californian_bad_url.csv')
bad_url.head()

Californian=bbg_data[(bbg_data['Source']=="Californian")&(bbg_data['URL'].isin(bad_url['URL'])==False)].reset_index(drop=True)
Californian.head()

Californian['Category'].value_counts()

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
    bad_url=[]
    ind=0
    
    #To acess the author
    if html_soup.find('meta',attrs={"name":"author"}) is not None:
        author=html_soup.find('meta',attrs={"name":"author"})["content"]
        if "|" in author:
            author=author.split("|")[0]
        if author=='':
            if html_soup.findAll('div', attrs = {"itemprop" : "articleBody"}) is not None:
                temp_soup = html_soup.find('div', attrs = {"itemprop" : "articleBody"})
                try:
                    soup = temp_soup.findAll('p')
                    author=soup[-1].get_text()
                    ind=1
                    words=author.split(" ")
                    if len(words)>5:
                        author=''
                        ind=0
                except:
                    print('Author missing!')
    else:
        print("author")
    author=author.replace(u"\xa0","")
    print(author)
    
    #To access article content
    if html_soup.findAll('div', attrs = {"itemprop" : "articleBody"}) is not None:
        temp_soup = html_soup.find('div', attrs = {"itemprop" : "articleBody"})
        try:
            soup = temp_soup.findAll('p')
            if ind==1:
                soup=soup[:-1]
            for s in soup:
                text = text + ' ' + s.get_text()
        except:
            temp_soup = html_soup.find('div', attrs = {"class" : "main-content-wrap"})
            try:
                temp_soup.findAll('p')
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
    
    if content=='':
        content=description
        
    return (content,date,title,author,keywords,description)
    
    
Californian['Content'],Californian['Date'],Californian['Title'],Californian['Author'],Californian['Keywords'],Californian['Description'] = zip(*Californian['URL'].apply(get_metadata))
Californian1=Californian[Californian['Title']!='404 Error']
Californian1.reset_index(drop=True)

Californian=Californian1.copy()
Californian1['ind']=Californian1['URL'].apply(lambda x: 'guest' if 'guest' in x else('opinion' if 'opinion' in x else 'regular'))
Californian['Category']=Californian1['ind']
Californian.to_csv('Bloomberg_Californian.csv')
