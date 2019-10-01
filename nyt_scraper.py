## import packages
import requests
from bs4 import BeautifulSoup

## function for scraping article from website
def nyt_scraper(x):
    # find url
    URL = x['article_link']
    print(URL)
    
    # request url
    r = requests.get(URL) 
    # soup = BeautifulSoup(r.content, 'html5lib')
    soup = BeautifulSoup(r.content, 'lxml')
    
    # find heading
    if soup.find('h1', attrs = {'itemprop':'headline'}) is not None:
        x["heading"] = soup.find('h1', attrs = {'itemprop':'headline'}).span.text
    else:
        x["heading"] = soup.find('h1', attrs = {'class':'edye5kn2'}).text
    
    # find topic, it is available on the html of the page
    if soup.find('a', attrs = {'class':'css-nuvmzp'}) is not None:
        x["topic"] = soup.find('a', attrs = {'class':'css-nuvmzp'}).text
    else:
        x["topic"] = "Not available"
        
    # if front heading exists, extract image and caption 
    try:
        x['front_heading_image'] = soup.find('div', attrs = {'class': 'css-bsn42l'}).img['itemid']
        x['front_image_caption'] = soup.find('figcaption', attrs = {'itemprop': 'caption description'}).span.text
    except:
        pass
    
    # find author
    if soup.find('span', attrs = {'class': 'last-byline'}) is not None:
        x['author'] = soup.find('span', attrs = {'class': 'last-byline'}).text
    else:
        x["author"] = "Not available"
        
    # find time of publishing of article
    if soup.find('time') is not None:
        x['datetime'] = soup.find('time', attrs = {'class': 'e16638kd0'})['datetime']
    else:
        x["datetime"] = "Not available"
    
    # find article text, all images hyperlinks, any hyperlinks in articles, if youtube videos exist
    article_text = []
    images_dict = dict()
    article_links = []
    youtube_videos = []
    
    rows = soup.find('section', attrs = {'itemprop': 'articleBody'})
    # find youtube videos if they exist
    youtube_videos.extend([y['src'] for y in rows.findAll('iframe', attrs={'title':'YouTube Video'})])
    # find all article text
    article_text.extend([y.text for y in rows.findAll('p')])
    # find links in articles
    article_links.extend([y['href'] for y in rows.findAll('a')])
    # find images hyperlinks and the captions if they exist
    [images_dict.update({y['src']:"Not available"}) if not y.has_attr('item_id') else (images_dict.update({y['itemid']:"Not available"}) if not y.has_attr('alt') else images_dict.update({y['itemid']:y["alt"]})) for y in rows.findAll('img')]
    
    x['article'] = ' '.join(article_text)
    x['hyperlinks'] = article_links
    x['images_in_article'] = images_dict
    x['youtube_videos'] = youtube_videos

    return x