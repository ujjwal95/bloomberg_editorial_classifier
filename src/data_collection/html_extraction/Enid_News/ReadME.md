This folder contains the code used to scrape articles posted by Enid News. <br>
Input: csv file containing url and category of articles <br>
Output: csv file containing metadata of each article posted by Enid News <br>
<br>
Few pointers: <br>
-> Some urls were incorrect, so skipped those <br>
-> Metadata collected: date, title, description, author, article content, news keywords <br>
-> Reworked the category of articles using the rule: <br>
   If 'guest' in article url, category= guest <br>
   If 'opinion' in article url, category= editorial <br>
   Else category= regular <br>
-> Used dates scraped from the articles 
