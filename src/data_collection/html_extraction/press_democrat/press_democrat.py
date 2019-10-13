import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import time
import csv

class Press_Democrat:
	def __init__(self):
		data_file = pd.read_csv('datafile.csv')
		self.sub_file=data_file[(data_file['Source']=="Press Democrat")].reset_index(drop=True)
		self.parse_data()

	def parse_data(self):
		ctr = -1
		writer = csv.writer(open('output_press_dem.csv', mode='a'), delimiter=',')
		for i, row in (self.sub_file.iterrows()):
			if i>2168:
				link = row['URL']
				ctr+=1
				r = requests.get(link)
				
				if r.status_code!=200:
					print(ctr)
					continue

				soup = BeautifulSoup(r.content, 'lxml')
				title=''
				date= ''
				author=''
				text=''
				keyword = ''

				time.sleep(3)
				try:
					title = soup.find('meta',attrs={"property":"og:title"})["content"].encode('utf-8')
				except:
					print('Title not found at ', ctr)

				try: 
					date = soup.find('meta',attrs={"property":"og:updated_time"})["content"]
					date = date.split("T")[0].encode('utf-8')
				except:	
					print('Date not found at ', ctr)

				try:
					author = soup.find('div', attrs = {"class":"byline-author bc-author"}).text.split("AND")
					author = ','.join(author).encode('utf-8')
				except:
					print('Author not found at ', ctr)

				try:
					keyword = soup.find('meta',attrs={"property":"bt:keywords"})["content"].encode('utf-8')
				except:
					print('Keyword not found at ', ctr)

				try:
					text = soup.find('div', attrs={"class":"story-content"}).get_text().encode('utf-8')
					print(len(text))
				except:
					print('Text not found at ', ctr)
				
				print(title)#, date, author, keyword, text)
				try:
					writer.writerow([title, date, row['Type'], author, keyword, link, text])
				except:
					print(ctr)

				time.sleep(5)

if __name__=="__main__":
	p = Press_Democrat()