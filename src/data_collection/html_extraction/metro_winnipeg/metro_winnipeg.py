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


def extract_heading(html_soup):
    """
    Extracts title of the article from content
    Input : Content in BeautifulSoup format
    Output : Title of the article
    """
    title = ""
    if html_soup.find('title') is not None:
        return html_soup.find('title').text.strip().split("|")[0]
    return title


def extract_date(html_soup):
    """
    Extracts date of the article from content
    Input : Content in BeautifulSoup format
    Output : Date of the article
    """
    if html_soup.find('meta', attrs = {'property':'article:published_time'}) is not None:
        html_date = html_soup.find('meta', attrs = {'property':'article:published_time'})["content"]
        html_date = datetime.datetime.strptime(html_date.split("T")[0], '%Y-%m-%d')
    else:
        print("Huston we have a problem!")
        html_date = "-"
    return html_date


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
    author = ""
    if html_soup.find('div', attrs = {"itemprop" : "author"}) is not None:
        temp_soup = html_soup.find('div', attrs = {"itemprop" : "author"})
        if temp_soup.find('meta', attrs = {"itemprop" : "name"}) is not None:
            author = temp_soup.find('meta', attrs = {"itemprop" : "name"})["content"].strip()
    return author


def extract_category(url):
    """
    Extracts category of the article from URL
    Input : URL
    Output : Category
    """
    if "/life/" in url:
        return "other"
    elif "/opinion/" not in url :
        return "regular"
    elif "/editorial/" in url or "/editorials/" in url:
        return "editorial"
    elif "/op-ed/" in url :
        return "oped"
    elif "/letters/"  in url :
        return "other"
    elif "/columnists/" in url :
        return "guest"
    else:
        return "other"


def main():
    """
    Reads the data file from the data/tagged/ directory from the path and returns saves content 
    for Washington Observer Reporter in csv format in the data/collected/ directory from the path
    """
    csv_data = pd.read_csv("data/tagged/ns-stories-full.csv")
    csv_data = csv_data[csv_data["Source"] == "Metro Winnipeg"]
    winnipeg_csv = pd.DataFrame(columns = ["URL","date","title","content","tag", "Editorial", "author"])
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
            winnipeg_csv = winnipeg_csv.append({"URL": url, "date": art_date, "title": title,"content": text,"tag": tag, "Editorial": category, "author": author}, ignore_index = True)
        except:
            err = err + 1
    winnipeg_csv.to_csv("data/collected/metro_winnipeg.csv", index=False)
    winnipeg_csv.to_excel("data/collected/metro_winnipeg.xlsx", index=False)
    winnipeg_csv.to_pickle("data/collected/metro_winnipeg.pkl")





#### Temporary functions
def category_assignement():
    """
    A Temporary Function that was implemented to reassign categories. 
    """
    winnipeg_metro_csv = pd.read_csv("data/collected/metro_winnipeg.csv")
    for i, row in winnipeg_metro_csv.iterrows():
        category = extract_category(row["URL"])
        winnipeg_metro_csv.loc[i, "Editorial"] = category
    winnipeg_metro_csv["content"] = winnipeg_metro_csv["content"].apply(lambda x : x.replace("/n",""))
    winnipeg_metro_csv.to_csv("data/collected/metro_winnipeg.csv", index=False)
    winnipeg_metro_csv.to_excel("data/collected/metro_winnipeg.xlsx", index=False)
    winnipeg_metro_csv.to_pickle("data/collected/metro_winnipeg.pkl")
