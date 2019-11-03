import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import time
# ignore warnings
import warnings
warnings.filterwarnings("ignore")

## define variables
data_location = '../data/'
max_feat = 1000
article_text_column = 'article_text'
pure_text_cols = ['article_text', 'preprocessed_text']
output_location = '../data/'

# read input data
print("Reading Data...")
start = time.time() 
X_train = pd.read_pickle(data_location + 'X_train.pkl')
X_test = pd.read_pickle(data_location + 'X_test.pkl')
y_train = pd.read_pickle(data_location + 'y_train.pkl')
y_test = pd.read_pickle(data_location + 'y_test.pkl')
print('Read Data!')
print('Time: ',time.time() - start)

def article_transformer(transformer, train, test, article_text_column, transformer_name):
    start = time.time()
    train_transformer = transformer.fit_transform(train[article_text_column])
    train_transformer = pd.DataFrame(train_transformer.toarray(), 
                                     columns=[transformer_name+x for x in transformer.get_feature_names()], 
                                     index=train.index)
    
    test_transformer = transformer.transform(test[article_text_column])
    test_transformer = pd.DataFrame(test_transformer.toarray(), 
                                    columns=[transformer_name+x for x in transformer.get_feature_names()], 
                                    index=test.index)
    print(transformer_name + " finished!")
    print('Time: ',time.time() - start)
    
    return train_transformer, test_transformer, transformer

### feature engineers
## count vectorizer
### word level
ngram_count_word = CountVectorizer(ngram_range=(1, 3), 
                                   analyzer='word', 
                                   token_pattern=r'\w{1,}', 
                                   stop_words='english', 
                                   max_features=max_feat)
### char level
ngram_count_char = CountVectorizer(ngram_range=(1, 2), 
                                   analyzer='char', 
                                   max_features=max_feat)
## tf idf vectorizer
### word level
tf_idf_word = TfidfVectorizer(ngram_range=(1, 3), 
                              analyzer='word', 
                              token_pattern=r'\w{1,}', 
                              stop_words='english',
                              max_features=max_feat)
### char level
tf_idf_char = TfidfVectorizer(ngram_range=(1, 2), 
                              analyzer='char', 
                              max_features=max_feat)

X_train_ngram_word, X_test_ngram_word, ngram_count_word =  article_transformer(transformer= ngram_count_word,
                                                                               train = X_train,
                                                                               test = X_test, 
                                                                               article_text_column= article_text_column,
                                                                               transformer_name="ngram_word_")

X_train_ngram_char, X_test_ngram_char, ngram_count_char =  article_transformer(transformer= ngram_count_char,
                                                                               train = X_train,
                                                                               test = X_test, 
                                                                               article_text_column= article_text_column,
                                                                               transformer_name="ngram_char_")

X_train_tfidf_word, X_test_tfidf_word, tf_idf_word =  article_transformer(transformer= tf_idf_word,
                                                                          train = X_train,
                                                                          test = X_test, 
                                                                          article_text_column= article_text_column,
                                                                          transformer_name="tf_idf_word_")

X_train_tfidf_char, X_test_tfidf_char, tf_idf_char =  article_transformer(transformer= tf_idf_char,
                                                                          train = X_train,
                                                                          test = X_test, 
                                                                          article_text_column= article_text_column,
                                                                          transformer_name="tf_idf_char_")

# final unscaled datasets
X_train_final = pd.concat([X_train.loc[:, ~X_train.columns.isin(pure_text_cols)], 
                           X_train_ngram_word, 
                           X_train_ngram_char, 
                           X_train_tfidf_word, 
                           X_train_tfidf_char], axis = 1)

X_test_final = pd.concat([X_test.loc[:, ~X_test.columns.isin(pure_text_cols)], 
                          X_test_ngram_word, 
                          X_test_ngram_char, 
                          X_test_tfidf_word, 
                          X_test_tfidf_char], axis = 1)

# final scaling datasets
start = time.time()
std_scaler = StandardScaler()
X_train_scaled = std_scaler.fit_transform(X_train_final)
X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train_final.columns)

X_test_scaled = std_scaler.transform(X_test_final)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test_final.columns)
print("Data Scaled!")
print('Time: ',time.time() - start)

# save to output_location
start = time.time()
X_train_scaled.to_pickle(output_location + 'X_train_scaled.pkl')
X_test_scaled.to_pickle(output_location + 'X_test_scaled.pkl')
print('Saved to '+ output_location + '!')
print('Time: ',time.time() - start)
