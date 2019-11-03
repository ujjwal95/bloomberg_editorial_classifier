import numpy as np
import glob, os
import pandas as pd
import re
import time
from nltk.corpus import stopwords
from helper import int_to_string, average_word_length, text_preprocessing, sentiment_from_vader, sentiment_from_afinn
from sklearn.model_selection import train_test_split
from create_features_helper import main as create_text_feat_main
from model_selection_helper import main as train_test_and_undersample_main 
# ignore warnings
import warnings
warnings.filterwarnings("ignore")


# import variables -- make changes here
data_location = '../data/combined_data.csv'
date_column = 'created_date'
article_text_column = 'article_text'
processed_text_column = 'preprocessed_text'
heading_column = 'heading'
target = 'label'
target_zero = ['regular', '0']
target_one = ['opinion', 'oped', 'guest', 'editorial', 'other', 2, '1', '2']
output_location = '../data/'
random_state = 42
test_size = 0.1

# read input data
print("Reading Data...")
start = time.time() 
input_data = pd.read_csv(data_location)
print('Read Data!')
print('Time: ',time.time() - start)
# format date column
print("Formatting and Cleaning Data...")
start = time.time()
input_data.drop_duplicates(inplace = True)
input_data = input_data.dropna(subset=[date_column, heading_column, article_text_column], how='any')
input_data[date_column] = pd.to_datetime(input_data[date_column], utc = True)
input_data = input_data.loc[input_data[article_text_column].notnull()]

input_data.loc[input_data.label.isin(target_zero), target] = 0
input_data.loc[input_data.label.isin(target_one), target] = 1

# testing
# input_data = input_data[2000: 4000]
print('Formatted Data!')
print('Shape of complete data', input_data.shape)
print('Time: ',time.time() - start)

# splitting into train and test to speed up pipeline
print("Splitting into train-test...")
start = time.time()
complete_data = input_data
train, test = train_test_and_undersample_main(complete_data, test_size = test_size, lookback = 3, lookforward = 0, random_state = random_state)
print('Split into train-test!')
print('Train Size:',  train.shape)
print('Test Size:',  test.shape)
print('Time: ',time.time() - start)

print("Preprocessing Text Data...")
start = time.time()
train[processed_text_column] = train[article_text_column].apply(lambda x: text_preprocessing(x, stopwords = set(stopwords.words('english'))))
test[processed_text_column] = test[article_text_column].apply(lambda x: text_preprocessing(x, stopwords = set(stopwords.words('english'))))
print('Preprocessed Text Data!')
print('Time: ',time.time() - start)

print("Converting Number to String...")
start = time.time()
train[processed_text_column] = train[processed_text_column].apply(int_to_string)
test[processed_text_column] = test[processed_text_column].apply(int_to_string)
print('Converted Number to String!')
print('Time: ',time.time() - start)

print("Extracting Average Word Length...")
start = time.time()
train['avg_word_length'] = train[processed_text_column].apply(average_word_length)
test['avg_word_length'] = test[processed_text_column].apply(average_word_length)
print('Extracted Average Word Length!')
print('Time: ',time.time() - start)

print("Extracting VADER Sentiments ...")
start = time.time()
train['neg_vader'],  train['neu_vader'], train['pos_vader'], train['compound_vader'] = zip(*train[article_text_column].apply(sentiment_from_vader))
test['neg_vader'],  test['neu_vader'], test['pos_vader'], test['compound_vader'] = zip(*test[article_text_column].apply(sentiment_from_vader))
print('Extracted VADER Sentiments!')
print('Time: ',time.time() - start)

print("Extracting AFINN Sentiments ...")
start = time.time()
train['afinn'] = train[article_text_column].apply(sentiment_from_afinn)
test['afinn'] = test[article_text_column].apply(sentiment_from_afinn)
print('Extracted AFINN Sentiments!')
print('Time: ',time.time() - start)
input_data.to_pickle(output_location +'intermediate_x_1.pkl')

print("Extrating Text Features based on Sarang's work ...")
start = time.time()
train = create_text_feat_main(train)
test = create_text_feat_main(test)
print('Extracted text features!')
print('Time: ',time.time() - start)

print("Saving to "+output_location+" ...")
start = time.time()
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size, random_state = random_state)
X_train, y_train = train.loc[:, ~train.columns.isin([target])], train[[target]]
X_test, y_test = test.loc[:, ~test.columns.isin([target])], test[[target]]
print("X_train size:", X_train.shape)
print("y_train size:", y_train.shape)
print("X_test size:", X_test.shape)
print("y_test size:", y_test.shape)

X_train.to_pickle(output_location + 'X_train.pkl')
X_test.to_pickle(output_location + 'X_test.pkl')
y_train.to_pickle(output_location + 'y_train.pkl')
y_test.to_pickle(output_location + 'y_test.pkl')
print('Saved to '+ output_location + '!')
print('Time: ',time.time() - start)