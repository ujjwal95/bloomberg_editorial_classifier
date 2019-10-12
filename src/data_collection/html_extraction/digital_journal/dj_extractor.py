
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time


def get_article(url):
    """
    Gets article content from URL
    Input : URL of article
    Output : Content in BeautifulSoup format
    """
        
    r = requests.get(url) 
    html_soup = BeautifulSoup(r.content, 'lxml')
    return html_soup
        
def get_author(html_soup):
    """
    Extracts Author of the article from content
    Input : Content in BeautifulSoup format
    Output : Author of the article
    """
    auth_text = html_soup.find('div', attrs = {"class" : "author"}).text.split("|")
    for i in auth_text:
        if 'By' in i:
            auth_text_split = i.split()
            auth_text_split = auth_text_split[auth_text_split.index('By')+1:auth_text_split.index('By')+3]
            auth_text_split = ' '.join(auth_text_split)
    return(auth_text_split)

def get_title(html_soup):
    """
    Extracts title of the article from content
    Input : Content in BeautifulSoup format
    Output : Title of the article
    """
    heading = html_soup.find('title').get_text()
    return heading

def get_content(html_soup):
    """
    Extracts text content of the article from content
    Input : Content in BeautifulSoup format
    Output : Text content of the article
    """
    text_above_image = html_soup.findAll('div', attrs = {"class" : "rs-content abstract"})
    if len(text_above_image) > 1:
        text_above_image = text_above_image[1].get_text()
    else:
        text_above_image = ''    
    text_below_image = html_soup.find('div', attrs = {"class" : "body"}).get_text()
    content = text_above_image + text_below_image
    
    return content

def get_tags(html_soup):
    """
    Extracts keywords of the article from content
    Input : Content in BeautifulSoup format
    Output : List of keywords of the article
    """
    
    tags = html_soup.findAll('a', attrs = {"class" : "tag"})
    all_tags = []
    for i in tags:
        all_tags.append(i.get_text())
    
    return all_tags


def main():
    """
    Reads the data file from the data/tagged/ directory from the path and returns saves content 
    for Digital Journal in csv format in the data/collected/ directory from the path
    """

df_links = pd.read_csv('data/tagged/ns-stories-full.csv', header=None)
df_links.columns = ['source', 'date', 'label', 'url']

df_dj = df_links[df_links['source'] == 'Digital Journal'].reset_index(drop=True)
df_dj['date'] = pd.to_datetime(df_dj['date'].apply(lambda x: x[:9]))

dj_csv = pd.DataFrame(columns = ["url","date","title", "author", "content","tag", "label"])
for i, row in tqdm(df_dj.iterrows()):
    try:
        url = row["url"]
        html_soup = get_article(url)
        title = get_title(html_soup)
        tag = get_tags(html_soup)
        content = get_content(html_soup)
        author = get_author(html_soup)
        dj_csv = dj_csv.append({"url": url, "date": row["date"], "title": title, "author": author, 
                                      "content": content,"tag": tag, 
                                      "label": row["label"]}, 
                                 ignore_index = True)
    except:
        print(i)
        time.sleep(10)
        try:
            url = row["url"]
            html_soup = get_article(url)
            title = get_title(html_soup)
            tag = get_tags(html_soup)
            content = get_content(html_soup)
            author = get_author(html_soup)
            dj_csv = dj_csv.append({"url": url, "date": row["date"], "title": title, "author": author, 
                                          "content": content,"tag": tag, 
                                          "label": row["label"]}, 
                                     ignore_index = True)
        except:
            continue
            
dj_csv.to_csv("digital_journal.csv", index=False)


if __name__ == "__main__":
    main()