import numpy as np
import glob, os
import pandas as pd
import re
import time
from nltk.corpus import stopwords
from helper import int_to_string, average_word_length, text_preprocessing, sentiment_from_vader, sentiment_from_afinn
from sklearn.model_selection import train_test_split
# ignore warnings
import warnings
warnings.filterwarnings("ignore")
# import variables
data_location = '../data/combined_data.csv'
date_column = 'created_date'
article_text_column = 'article_text'
processed_text_column = 'preprocessed_text'
target = 'label'
target_zero = ['regular', '0']
target_one = ['opinion', 'oped', 'guest', 'editorial', 'other', 2, '1', '2']
output_location = '../data/'
random_state = 42
test_size = 0.2
# read input data
print("Reading Data...")
start = time.time() 
input_data = pd.read_csv(data_location)
print('Read Data!')
print('Time: ',time.time() - start)
# format date column
print("Formatting Data...")
start = time.time()
input_data[date_column] = pd.to_datetime(input_data[date_column])
input_data = input_data.loc[input_data[article_text_column].notnull()]

input_data.loc[input_data.label.isin(target_zero), target] = 0
input_data.loc[input_data.label.isin(target_one), target] = 1

X = input_data[[article_text_column]]
y = input_data[[target]]
print('Formatted Data!')
print('Time: ',time.time() - start)

print("Preprocessing Text Data...")
start = time.time()
X[processed_text_column] = X[article_text_column].apply(lambda x: text_preprocessing(x, stopwords = set(stopwords.words('english'))))
print('Preprocessed Text Data!')
print('Time: ',time.time() - start)

print("Converting Number to String...")
start = time.time()
X[processed_text_column] = X[processed_text_column].apply(int_to_string)
print('Converted Number to String!')
print('Time: ',time.time() - start)

print("Extracting Average Word Length...")
start = time.time()
X['avg_word_length'] = X[processed_text_column].apply(average_word_length)
print('Extracted Average Word Length!')
print('Time: ',time.time() - start)

print("Extracting VADER Sentiments ...")
start = time.time()
X['neg_vader'],  X['neu_vader'], X['pos_vader'], X['compound_vader'] = zip(*X[article_text_column].apply(sentiment_from_vader))
print('Extracted VADER Sentiments!')
print('Time: ',time.time() - start)

print("Extracting AFINN Sentiments ...")
start = time.time()
X['afinn'] = X[article_text_column].apply(sentiment_from_afinn)
print('Extracted AFINN Sentiments!')
print('Time: ',time.time() - start)

print("Splitting to Train/Test and Saving to "+output_location+" ...")
start = time.time()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size, random_state = random_state)

X_train.to_pickle(output_location + 'X_train.pkl')
X_test.to_pickle(output_location + 'X_test.pkl')
y_train.to_pickle(output_location + 'y_train.pkl')
y_test.to_pickle(output_location + 'y_test.pkl')
print('Saved to '+ output_location + '!')
print('Time: ',time.time() - start)