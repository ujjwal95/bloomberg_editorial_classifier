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
    auth_text = html_soup.find('span', attrs = {"class" : "author"}).get_text()
    return(auth_text)

def get_title(html_soup):
    """
    Extracts title of the article from content
    Input : Content in BeautifulSoup format
    Output : Title of the article
    """
    heading = html_soup.find('title').get_text().split('|')[0]
    return heading

def get_content(html_soup):
    """
    Extracts text content of the article from content
    Input : Content in BeautifulSoup format
    Output : Text content of the article
    """
    html_soup.find('figure').extract()
    content = html_soup.find('div', attrs = {"class" : "entry-content"}).get_text()
    return content


def main():
    """
    Reads the data file from the data/tagged/ directory from the path and returns saves content 
    for Digital Journal in csv format in the data/collected/ directory from the path
    """
    df_links = pd.read_csv('data/tagged/ns-stories-full.csv', header=None)
    df_links.columns = ['source', 'date', 'label', 'url']

    df_nj = df_links[df_links['source'] == 'NJSpotlight'].reset_index(drop=True)
    df_nj['date'] = pd.to_datetime(df_nj['date'].apply(lambda x: x[:9]))
    
    nj_csv = pd.DataFrame(columns = ["url","date","title", "author", "content", "label"])
    for i, row in tqdm(df_nj.iterrows()):
        try:
            url = row["url"]
            html_soup = get_article(url)
            title = get_title(html_soup)
            content = get_content(html_soup)
            author = get_author(html_soup)
            nj_csv = nj_csv.append({"url": url, "date": row["date"], "title": title, "author": author, 
                                          "content": content,
                                          "label": row["label"]}, 
                                     ignore_index = True)
        except:
            print(i)
            time.sleep(10)
            try:
                url = row["url"]
                html_soup = get_article(url)
                title = get_title(html_soup)
                content = get_content(html_soup)
                author = get_author(html_soup)
                nj_csv = nj_csv.append({"url": url, "date": row["date"], "title": title, "author": author, 
                                              "content": content,
                                              "label": row["label"]}, 
                                         ignore_index = True)
            except:
                continue
                
    nj_csv.to_csv('NJSpotlight.csv', index=False)


if __name__ == "__main__":
    main()

