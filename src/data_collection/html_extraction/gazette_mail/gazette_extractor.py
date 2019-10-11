import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import pandas as pd 


def get_article(url):
    """
    Gets article content from URL
    Input : URL of article
    Output : Content in BeautifulSoup format
    """
    r = requests.get(url) 
    html_soup = BeautifulSoup(r.content, 'lxml')
    return html_soup


def extract_date(html_soup):
    """
    Extracts date of the article from content
    Input : Content in BeautifulSoup format
    Output : Date of the article
    """
    if html_soup.find('time', attrs = {'class':'asset-date'}) is not None:
        html_date = html_soup.find('time', attrs = {'class':'asset-date'}).text.strip()
        html_date = datetime.datetime.strptime(html_date, '%b %d, %Y')
    elif html_soup.find('time', attrs = {'class':'tnt-date'}) is not None:
        html_date = html_soup.find('time', attrs = {'class':'tnt-date'}).text.strip()
        html_date = datetime.datetime.strptime(html_date, '%b %d, %Y')
    elif html_soup.find('time', attrs = {'class':'text-muted'}) is not None:
        html_date = html_soup.find('time', attrs = {'class':'text-muted'}).text.strip()
        html_date = datetime.datetime.strptime(html_date, '%b %d, %Y')
    else:
        html_date = datetime.datetime.today()
    return html_date


def extract_category(url):
    """
    Extracts category of the article from URL
    Input : URL
    Output : Category
    """
    if "/opinion/" not in url :
        return "regular"
    elif "/editorial/" in url:
        return "editorial"
    elif "/op_ed_commentaries/" in url :
        return "oped"
    elif "/letter_to_editor/"  in url or "/letters_to_editor/"  in url or "/readers_vent/"  in url:
        return "other"
    elif "/columnists/" in url or "guest" in url or "/daily_mail_opinion/" in url:
        return "guest"
    else:
        return "other"


def extract_heading(html_soup):
    """
    Extracts title of the article from content
    Input : Content in BeautifulSoup format
    Output : Title of the article
    """
    if html_soup.find('meta', attrs = {"name" : "title"}) is not None:
        return html_soup.find('meta', attrs = {"name" : "title"})["content"].strip()
    elif html_soup.find('title') is not None:
        main_title = html_soup.find('title').text.split("|")
        title =  main_title[0].strip()
    return title


def extract_keywords(html_soup):
    """
    Extracts keywords of the article from content
    Input : Content in BeautifulSoup format
    Output : Comma seperated keywords of the article
    """
    if html_soup.find('meta', attrs = {"name" : "news_keywords"}) is not None:
        return html_soup.find('meta', attrs = {"name" : "news_keywords"})["content"].strip()


def extract_content(html_soup):
    """
    Extracts text content of the article from content
    Input : Content in BeautifulSoup format
    Output : Text content of the article
    """
    text = ''
    if html_soup.findAll('div', attrs = {"itemprop" : "articleBody"}) is not None:
        temp_soup = html_soup.find('div', attrs = {"itemprop" : "articleBody"})
        soup = temp_soup.findAll('p')
        for s in soup:
            text = text + ' ' + s.text
    else:
        temp_soup = html_soup.findAll('p')
        for s in temp_soup:
            text = text + ' ' + s.text
    return text.strip()


def extract_author(html_soup):
    """
    Extracts Author of the article from content
    Input : Content in BeautifulSoup format
    Output : Author of the article
    """
    if html_soup.find('meta', attrs = {"name" : "author"}) is not None:
        author = html_soup.find('meta', attrs = {"name" : "author"})["content"].strip()
        if author: return author
    if html_soup.find('meta', attrs = {"name" : "twt-author-name"}) is not None:
        return html_soup.find('meta', attrs = {"name" : "twt-author-name"})["content"].strip()
    return ""


def main():
    """
    Reads the data file from the data/tagged/ directory from the path and returns saves content 
    for Washington Observer Reporter in csv format in the data/collected/ directory from the path
    """
    csv_data = pd.read_csv("data/tagged/ns-stories-full.csv")
    csv_data = csv_data[csv_data["Source"] == "Gazette-Mail"]
    gazette_csv = pd.DataFrame(columns = ["URL","date","title","content","tag", "Editorial", "author"])
    err = 0
    for i, row in csv_data.iterrows():
        if i % 50 == 0 :
            print(i)
        try:
            url = row["URL"]
            html_soup = get_article(url)
            art_date = extract_date(html_soup)
            title = extract_heading(html_soup)
            tag = extract_keywords(html_soup)
            text = extract_content(html_soup)
            author = extract_author(html_soup)
            category = extract_category(url)
            gazette_csv = gazette_csv.append({"URL": url, "date": art_date, "title": title,"content": text,"tag": tag, "Editorial": category, "author": author}, ignore_index = True)
        except:
            err = err + 1
    gazette_csv.to_csv("data/collected/gazette_mail.csv", index=False)



#### Temporary functions
def category_assignement():
    """
    A Temporary Function that was implemented to reassign categories. 
    """
    gazzette_csv = pd.read_csv("data/collected/gazette_mail.csv")
    for i, row in gazzette_csv.iterrows():
        category = extract_category(row["URL"])
        gazzette_csv.loc[i, "Editorial"] = category
    gazzette_csv.to_csv("data/collected/gazette_mail.csv", index=False)


