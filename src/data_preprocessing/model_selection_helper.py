## import libraries
import pandas as pd
import numpy as np
import datetime

def undersampling_balanced(unbalanced_data, lookback, lookforward, random_state, datetime_col, date_col, source_col, target, original_cols):
    unbalanced_data = unbalanced_data.sort_values(by = [source_col, datetime_col])
    data_zeros = unbalanced_data.loc[unbalanced_data[target] == 0]
    data_ones = unbalanced_data.loc[unbalanced_data[target] == 1]
    weights = data_ones.groupby([source_col, date_col]).url.agg(['count']).reset_index(drop = False)
    data_zeros = weights.merge(data_zeros, how = 'left', on = [source_col,date_col], suffixes=('_1', '_0'))
    data_zeros.drop_duplicates(inplace = True)
    sampled_zeros = pd.DataFrame(columns=data_zeros.columns)
    for i in weights.iterrows():
        source_name = i[1][source_col]
        creation_date = i[1][date_col]
        counts = i[1]['count']
        # print('ones count: ', counts)
        extracted_data = data_zeros.loc[(data_zeros.source_name == source_name) & (data_zeros[date_col]== creation_date)]

        if  extracted_data.shape[0] >= counts:
          # print('sampled data: ', extracted_data.sample(n = counts, random_state = random_state).shape[0])
            sampled_zeros = pd.concat([sampled_zeros,extracted_data.sample(n = counts, random_state = random_state)])
        else:
            extracted_data = data_zeros.loc[(data_zeros.source_name == source_name) & 
                                            (data_zeros[date_col]>= creation_date - datetime.timedelta(days = lookback)) & 
                                            (data_zeros[date_col]<= creation_date + datetime.timedelta(days = lookforward))]
            sampled_zeros = pd.concat([sampled_zeros,extracted_data.sample(n = counts, random_state = random_state)])
        
    return pd.concat([data_ones[original_cols], sampled_zeros[original_cols]], ignore_index= True)

# guarantees that test size is at least the size mentioned below, will be just over that size
def train_test_split(data, test_size, datetime_col, date_col, source_col, target, original_cols):
    def binarySearch (arr, l, r, x): 
        if r >= l: 
            mid = l + (r - l)//2
            if arr[mid] == x: 
                return mid 
            elif arr[mid] > x: 
                return binarySearch(arr, l, mid-1, x) 
            else: 
                return binarySearch(arr, mid + 1, r, x) 
        else: 
            return r

    date_counts = data.groupby([date_col]).url.agg(['count']).reset_index()
    date_counts['cumsum'] = date_counts['count'].cumsum()
    total = date_counts['count'].sum()
    train_sample_size = round(total * (1-test_size))
    index_to_split = binarySearch(date_counts['cumsum'].values, 0, date_counts['cumsum'].values.shape[0]-1, train_sample_size)
    date_to_split = date_counts.date[index_to_split]
    train, test = data.loc[data.date < date_to_split], data.loc[data.date >= date_to_split]
    
    return train, test

def main(complete_data, test_size = 0.2, lookback = 5, lookforward = 0, random_state = 42):
    
    ### variables -- make changes here only
    datetime_col = 'created_date'
    date_col = 'date'
    source_col = 'source_name'
    target_zero = ['regular', '0', 0]
    target_one = ['opinion', 'oped', 'guest', 'editorial', 'other', 2, '1', '2']
    target = 'label'
    
    complete_data.drop_duplicates(inplace = True)
    original_cols = complete_data.columns
    
    ## checks and data manipulation
    complete_data = complete_data.loc[~(complete_data[datetime_col].isna())]
    complete_data[datetime_col] = pd.to_datetime(complete_data[datetime_col], utc = True)
    complete_data[date_col] = complete_data[datetime_col].dt.date
    complete_data.sort_values(by = [source_col, datetime_col], inplace = True)
    
    ## define target variables clearly
#     complete_data.loc[complete_data.label.isin(target_zero), target] = 0
#     complete_data.loc[complete_data.label.isin(target_one), target] = 1
    
    train, test = train_test_split(complete_data, test_size, datetime_col, date_col, source_col, target, original_cols)
    
    undersampled_train = undersampling_balanced(train, lookback, lookforward, random_state, datetime_col, date_col, source_col, target, original_cols)
    
    return undersampled_train, test[original_cols]
#     return train[original_cols], test[original_cols]