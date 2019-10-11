This folder contains the code used to scrape articles posted by Enid News.
Input: csv file containing url and category of articles
Output: csv file containing metadata of each article posted by Enid News

Few pointers:
-> Some urls were incorrect, so skipped those
-> Metadata collected: date, title, description, author, article content, news keywords
-> Reworked the category of articles using the rule:
   If 'guest' in article url, category= guest
   If 'opinion' in article url, category= editorial
   Else category= regular
