from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from parsel import Selector
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import csv


class Parser:
    def __init__ (self):
    	self.open_csv()
    	self.driver = webdriver.Chrome('C:/Users/User/Desktop/chromedriver.exe')
    	options = webdriver.ChromeOptions()
    	options.add_argument('headless')
    	self.newspaper_parser()
    
    def open_csv(self):
        self.file_name = ["sample-data.csv", "nyt-wpo-2016-sample.csv", "nyt-wpo-2017-sample.csv", "nyt-wpo-2018-sample.csv", "nyt-wpo-2019-sample.csv"]
        file = pd.read_csv(self.file_name[0])
        subframe = file["Source"]=="WPT"
        self.url_list = file[subframe]['URL']
        
        for i in range(1, len(self.file_name)):
        	file = pd.read_csv(self.file_name[i], header=None, names=["Number", "URL"], index_col="Number")
        	subframe = file[file["URL"].str.contains("http://www.washingtonpost.com/")]
        	self.url_list = self.url_list.append(subframe["URL"])
        
        self.url_list = list(set(self.url_list))
        

    def newspaper_parser (self, sleep_time=0):
        print("running newspaper_parser()...")
        writer = csv.writer(open('output.csv', mode='a'), delimiter=',')

        results = []
        count = 0

        for l in self.url_list:
       		self.driver.get(l)
       		time.sleep(5)
       		sel = Selector(self.driver.page_source)
       		try:
       			title = self.driver.find_element_by_xpath("//div[contains(@class, 'headline-flex-basis')]/h1").text.encode('utf-8')
       		except:
       			try:
       				title = self.driver.find_element_by_xpath("//div[contains(@class,'topper-headline')]/h1[@itemprop='headline']").text.encode('utf-8')
       			except:
       				title = None
       		
       		try:
	       		author_name = WebDriverWait(self.driver, 30).until(
	       			lambda x: x.find_elements_by_xpath("//a[@class='author-name']"))
	       		author_name = [a.text for a in author_name if a.text!='']
	       	except:
	       		try:
		       		author_name = WebDriverWait(self.driver, 30).until(
		       			lambda x: x.find_elements_by_xpath("//span[@class='author-name font-bold link blue hover-blue-hover']"))
		       		author_name = [a.text.encode('utf-8') for a in author_name if a.text!='']
		       	except:
		       		author_name = []		       			

       		publish_date = sel.xpath('//*[starts-with(@class, "display-date")]/text()').extract_first()
       		if publish_date is None:
       			publish_date = sel.xpath('//*[starts-with(@class, "author-timestamp")]/text()').extract_first()
       				
       		try:
       			text = self.driver.find_element_by_xpath("//div[contains(@class, 'article-body content-format-ans')]").text.encode('utf-8')
       		except:
       			try:
       				text = self.driver.find_element_by_xpath("//div[contains(@id, 'article-body')]").text.encode('utf-8')
       			except:
       				text = None

       		link = self.driver.current_url
       		
       		writer.writerow([title, publish_date, author_name, link, text])
       	return results

if __name__=="__main__":
    parser = Parser()