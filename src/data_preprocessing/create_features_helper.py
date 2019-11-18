import spacy 
nlp = spacy.load('en_core_web_sm')
from textblob import TextBlob
from helper import return_entities, return_pos
def main(df):
        
    '''Deleting rows which have article text and heading missing'''
    df = df.dropna(subset=['heading', 'article_text'])
    
    '''Feature 1: Number of words in the heading and the article'''
    print('Creating Feature: Article Length...')
    df['article_length'] = df['article_text'].apply(lambda x: len(nlp(x)))
    print('Creating Feature: Heading Length...')
    df['heading_length'] = df['heading'].apply(lambda x: len(nlp(x)))
    
    '''Feature 2: Number of exclamation and question marks in the sentence'''
    print('Creating Feature: Number of Question...')
    df['num_questions'] = df['article_text'].apply(lambda x: x.count('?'))
    print('Creating Feature: Number of Exclamation...')
    df['num_exclamations'] = df['article_text'].apply(lambda x: x.count('!'))
    
    '''Feature 3: Sentiment Analysis - Heading and Article'''
    print('Creating Feature: Article Sentiment...')
    df['article_sentiment'] = df['article_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    print('Creating Feature: Article Subjectivity...')
    df['article_subjectivity'] = df['article_text'].apply(lambda x: TextBlob(x).sentiment.subjectivity)

    print('Creating Feature: Heading Sentiment...')
    df['heading_sentiment'] = df['heading'].apply(lambda x: TextBlob(x).sentiment.polarity)
    print('Creating Feature: Heading Subjectivity...')
    df['heading_subjectivity'] = df['heading'].apply(lambda x: TextBlob(x).sentiment.subjectivity)
    
    '''Feature 4: Named Entity Recognition'''
    print('Creating Feature: Named Entity Recognition...')
    df['ENT_PERSON'], df['ENT_NORP'], df['ENT_ORG'], df['ENT_LOCATION'], df['ENT_PRODUCT'], df['ENT_LANGUAGE'], df['ENT_OTHERS'] = zip(*df['article_text'].apply(return_entities))
#     entity_list = zip(*df['article_text'].map(return_entites))
#     entity_list = list(entity_list)
#     entity_list = pd.DataFrame(entity_list).transpose().set_index(df.index)
#     entity_list.columns = ['ENT_PERSON', 'ENT_NORP', 'ENT_ORG', 'ENT_LOCATION', 'ENT_PRODUCT', 'ENT_LANGUAGE', 'ENT_OTHERS']
#     df = pd.concat([df, entity_list], axis=1)
    
    '''Feature 5: Parts-of-Speech Tagging'''
    print('Creating Feature: Parts-of-Speech...')
    df['POS_ADJ'], df['POS_ADV'], df['POS_PROPN'], df['POS_NUM'], df['POS_AUX'] = zip(*df['article_text'].apply(return_pos))
#     pos_list = list(pos_list)
#     pos_list = pd.DataFrame(pos_list).transpose().set_index(df.index)
#     pos_list.columns = ['POS_ADJ', 'POS_ADV', 'POS_PROPN', 'POS_NUM', 'POS_AUX']
#     df = pd.concat([df, pos_list], axis=1)
    
    return df