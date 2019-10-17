This file contains the code used to visualize the data collected(news articles scraped).<br>
<br>
- The first plot in the code shows the imbalance across various categories of data. The number of regular articles in our dataset is <br>
much more than editorials. This suggests that we need to either downsample the regular articles or upsample the editorials.
- The second plot shows a plot of the number of words in articles across all sources. This plot is used while preprocessing data to <br>
remove articles that are either too short or too long. Very few articles were more than 2000 words long.
- The third plot has subplots with each subplot showing the distribution of word count for each news source in the dataset. Since <br>
the second plot had a word count range between 0 and 16000 words, this plot was used to figure out which news source had the tendency <br>
of publishing lengthy articles. As can be seen in the plot, New York Times generally publishes articles which are longer than the <br>
median word count obtained in the previous plot.
