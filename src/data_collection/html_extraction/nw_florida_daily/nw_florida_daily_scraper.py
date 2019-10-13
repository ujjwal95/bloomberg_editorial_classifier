import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse

## helper functions ----
### check url of blog for multiple types of links
def check_blogs_url(url):
    if "blogs.nwfdailynews.com" in url:
        return True
    else:
        return False

### check whether page is 404
def check_404(soup):
    try :
        error_text = soup.find('section', attrs = {'class': 'section-general'}).find('div', attrs = {'class', 'inner'}).h2.text 
        if error_text == "Page Not Found":
            return True
        else:
            return False
    except:
        return False

### find heading
def find_heading(soup, url):
    if check_blogs_url(url):
        return soup.find('h1', attrs = {'class': 'entry_title'}).a.text
    else:
        return soup.find('h1', attrs = {'class':'headline'}).text

### format date from unstandardized to standardized format
def format_date(unformatted_date):
    try:
        return datetime.strptime(unformatted_date, '%b %d, %Y at %I:%M %p')
    except:
        return unformatted_date

### find creation of article date
def find_created_date(soup, url):
    if check_blogs_url(url):
        return datetime.strptime(soup.find('div', attrs = {'class': 'post_meta'}).time['datetime'][:-6], '%Y-%m-%dT%H:%M:%S')
    else: 
        created_date = soup.find('span', attrs = {'class': 'article-meta-date'}).text.replace(u'\xa0', u' ')
        return format_date(created_date)

### find updation of article date
def find_updated_date(soup, url):
    if check_blogs_url(url):
        return np.nan
    else:
        updated_date = soup.find('span', attrs = {'class': 'article-meta-updated'}).text.replace(u'\xa0', u' ')
        return format_date(updated_date)

### find author byline
def find_author(soup, url):
    if check_blogs_url(url):
        return soup.find('span', attrs = {'class': 'by-author'}).find('a', attrs = {'rel':'author'}).text
    else:
        author_unformatted = soup.find('span', attrs = {'class': 'byline-item'}).text
        return author_unformatted.replace(u'\r', u' ').replace(u'\r', u' ').replace(u'\t', u' ').strip()

### find body of article
def find_article_body(soup, url):
    if check_blogs_url(url):
        return soup.find('div', attrs = {'class':'entry_content'})
    else:
        return soup.find('div', attrs = {'class' :'article-body'})

### using body of article, find text of article
def find_article_text(article_body):
    article_text = []
    article_text.extend([y.text for y in article_body.findAll('p')])
    return ' '.join(article_text).strip()

### using body of article, find all the hyperlinks in the body 
def find_hyperlinks(article_body):
    article_links = []
    article_links.extend([y['href'] for y in article_body.findAll('a')])
    return article_links


## main nw florida news scraper
def nw_fl_daily_scraper(x):
    ## the following function is the main function to scrape data from NW Florida Daily
    # find url
    URL = x['url']
#     print(URL)
    if x.name%100 == 1:
        print("%dst URL: %s"% (x.name, URL))
    # request url
    r = requests.get(URL) 
    # soup = BeautifulSoup(r.content, 'html5lib')
    soup = BeautifulSoup(r.content, 'lxml')
    # check 404
    if not check_404(soup):
        # find heading
        x['heading'] = find_heading(soup, URL)
        x['created_date'] = find_created_date(soup, URL)
        x['updated_date'] = find_updated_date(soup, URL)
        x['author'] = find_author(soup, URL)
        article_body = find_article_body(soup, URL)
        x['article_text'] = find_article_text(article_body)
        x['article_links'] = find_hyperlinks(article_body)
    else:
        x['heading'] = np.nan
        x['created_date'] = np.nan
        x['updated_date'] = np.nan
        x['author'] = np.nan
        x['article_text'] = np.nan
        x['article_links'] = np.nan
    return x