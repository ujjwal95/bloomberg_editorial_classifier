## import packages
import pandas as pd
import numpy as np
from glob import glob
import warnings

pd.options.mode.chained_assignment = None  # default='warn'

def read_all_csvs(csv_locations):
    '''
    Read csvs from all locations and return them as a dict, where keys are previous folder locations and values are dataframes.
    Concatenates the dataframes when the keys are the same 
    Input: 
            csv_locations(list): contains list of all csv locations
    Output:
            base_data(dict): Dictionary of all dataframes            
    '''
    ## find the parent directory names
    parent_dicts = [[i.split('/')[-2] for i in j] for j in csv_locations]
    
    base_data = dict()
    for i,j in zip(parent_dicts, csv_locations):
        for k, l in zip(i, j):
            ## excluding Washington Post as it has some issues in reading that data
            if k in ['Washington Post']:
                continue
#             print(k, l)
            if not (k in base_data):
                base_data[k] = pd.read_csv(l, encoding='utf-8')
            else:
                base_data[k] = pd.concat([base_data[k], pd.read_csv(l)])
    
    return base_data

def date_formatter(column, format = None):
    '''
    Converts a DataFrame Series to a DateTime format for unification
    Input:
            column(series): contains series with datetime which will be converted
            format(string): if the format cannot be directly selected, give your own data format
    Output:
            formatted datetime series(series) 
    '''
    return pd.to_datetime(column, format = format)

def select_col_names(df, col_names = ['source_name', 'url', 'created_date', 'tag', 'heading', 'author', 'article_text', 'label']):
    '''
    selects the columns given.
    Input:
            df(DataFrame): Input dataframe
            col_names(list): Columns to be selected
    Output:
            selected columns of dataframe
    '''
    return df[col_names]

def news_source_formatter(df, news_source_name = None, rename_dict = None, col_names = None, date_format = None):
    '''
    Format News Source DataFrame according to the following rules:
        1. If news source name is provided, will make a new column filled with the news source name
        2. If rename dictionary is provided, will rename the columns according to the dictionary
        3. If the date format is provided, will format the datetime column accroding to the format, or will try to derive the format if the format is not provided
    '''
    if news_source_name is not None:
        df['source_name'] = news_source_name
    if rename_dict is not None:
        df.rename(columns=rename_dict, 
                  inplace=True)
    if col_names is not None:
        df = select_col_names(df, col_names)
    else:
        df = select_col_names(df)
    if date_format is None:
        df['created_date'] = date_formatter(df['created_date'])
    else:
        df['created_date'] = date_formatter(df['created_date'], format = date_format)
    return df

if __name__ == "__main__":
    ## assuming that all the data is kept in a directory 1 level above the current directory
    data_dir = "../data/"
    # define column names of unified DataFrame
    col_names = ['source_name', 'url', 'created_date', 'tag', 'heading', 'author', 'article_text', 'label']
    # Combined data file name
    combined_data_file_name = 'combined_data.csv'
    
    data_directories = glob(data_dir + "collected/*")
    # find all the data file locations
    all_data_dirs = [glob(i + "/*") for i in data_directories]
    news_sources = [[i.split('/')[-2] for i in j] for j in all_data_dirs]
    # generate a dict containing all DataFrames
    base_data = dict()
    base_data = read_all_csvs(all_data_dirs)
    print("Read Data!")
    ## special formatting in order to find tags of news source article
    base_data['Northwest Florida Daily']['tag'] = base_data['Northwest Florida Daily']['url'].str.split('/').str[3]
    # formatting for northwest florida daily
    base_data['Northwest Florida Daily'] = news_source_formatter(base_data['Northwest Florida Daily'])
    print("Formatted for Northwest Florida Daily!")
    # formatting for Gazette Mail
    gazette_mail_renamer = {'URL': 'url',
                        'date': 'created_date',
                        'title': 'heading',
                        'content': 'article_text',
                        'Editorial':'label'}
    base_data['Gazette-mail'] = news_source_formatter(base_data['Gazette-mail'], news_source_name='Gazette-mail', rename_dict=gazette_mail_renamer)
    print("Formatted for Gazette Mail!")
    # formatting for Washington Observer Post
    washington_obs_post_renamer = {'URL': 'url',
                                   'date': 'created_date',
                                   'title': 'heading',
                                   'content': 'article_text',
                                   'Editorial':'label'}
    base_data['Washington Observer Report']= news_source_formatter(base_data['Washington Observer Report'], news_source_name='Washington Observer Report', rename_dict= washington_obs_post_renamer)
    print("Formatted for Washington Observer Report!")
    # formatting for Californian
    californian_renamer = {'URL': 'url',
                       'Source':'source_name',
                       'Date': 'created_date',
                       'Title': 'heading',
                       'Content': 'article_text',
                       'Category':'label',
                       'Keywords':'tag',
                       'Author':'author'}
    base_data['Californian'] = news_source_formatter(base_data['Californian'], rename_dict=californian_renamer)
    print("Formatted for Californian!")
    # formatting for New York Times
    base_data['New York Times'].loc[base_data['New York Times']['datetime'].str.contains('Not ava'), 'datetime'] = np.nan
    base_data['New York Times']['datetime'] = base_data['New York Times']['datetime'].str[:-6]
    nyt_renamer = {'article_link': 'url',
               'datetime': 'created_date',
               'topic': 'tag',
               'article': 'article_text'}
    base_data['New York Times']= news_source_formatter(base_data['New York Times'], news_source_name='New York Times', rename_dict= nyt_renamer, date_format='%Y-%m-%dT%H:%M:%S')
    print("Formatted for New York Times!")
    # formatting for Enid News
    enid_news_renamer = {'Source': 'source_name',
                         'URL': 'url',
                         'Date': 'created_date',
                         'Keywords': 'tag',
                         'Title': 'heading',
                         'Author': 'author',
                         'Content':'article_text',
                         'Category':'label'}
    base_data['Enid News']= news_source_formatter(base_data['Enid News'], rename_dict= enid_news_renamer)
    print("Formatted for Enid News!")
    # formatting for NJSpotlight
    njspotlight_renamer = {'date': 'created_date',
                           'title': 'heading',
                           'content':'article_text'}
    base_data['NJSpotlight']['tag'] = np.nan
    base_data['NJSpotlight']= news_source_formatter(base_data['NJSpotlight'], news_source_name='NJSpotlight', rename_dict= njspotlight_renamer)
    print("Formatted for NJSpotlight!")
    # formatting for Digital Journal
    digital_journal_renamer = {'date': 'created_date',
                           'title': 'heading',
                           'content':'article_text'}
    base_data['Digital Journal']= news_source_formatter(base_data['Digital Journal'], news_source_name='Digital Journal', rename_dict= digital_journal_renamer)
    print("Formatted for Digital Journal!")
    # formatting for Press Democrat
    base_data['Press Democrat']['source_name'] = 'Press Democrat'
    base_data['Press Democrat']['heading'] = base_data['Press Democrat']['heading'].str[2:-1]
    base_data['Press Democrat']['created_date'] = base_data['Press Democrat']['created_date'].str[2:-1]
    base_data['Press Democrat']['author'] = base_data['Press Democrat']['author'].str[2:-1]
    base_data['Press Democrat']['tag'] = base_data['Press Democrat']['tag'].str[2:-1]
    base_data['Press Democrat']['article_text'] = base_data['Press Democrat']['article_text'].str[4:-1]

    base_data['Press Democrat'] = news_source_formatter(base_data['Press Democrat'], news_source_name='Press Democrat')
    print("Formatted for Press Democrat!")    
    # combining dataframes
    combined_data = pd.concat(base_data.values(), ignore_index=True)
    print("Combined Data!")
    combined_data.to_csv(data_dir + combined_data_file_name, index = False)
    print("Saved to " + data_dir + combined_data_file_name + "!")