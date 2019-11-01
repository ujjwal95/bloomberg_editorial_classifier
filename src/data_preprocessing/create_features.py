import pandas as pd
import numpy as np
import spacy
import gensim
from textblob import TextBlob
nlp = spacy.load('en_core_web_sm')

def return_entites(x):
    
    '''Helper function: Return Entities using NER'''
    entities_dict = {'PERSON': 0, 'NORP': 0, 'ORG': 0, 'LOCATION': 0, 'PRODUCT': 0, 'LANGUAGE': 0, 'OTHERS': 0}
    for entity in nlp(x).ents:
        if entity.label_ in ['FAC', 'GPE', 'LOC']:
            entities_dict['LOCATION'] +=1
        elif entity.label_ in entities_dict.keys():
            entities_dict[entity.label_] +=1
        else:
            entities_dict['OTHERS'] +=1
    return entities_dict['PERSON'], entities_dict['NORP'], entities_dict['ORG'], \
            entities_dict['LOCATION'], entities_dict['PRODUCT'], entities_dict['LANGUAGE'], entities_dict['OTHERS']

def return_pos(x):
    '''Helper function: Return POS'''
    pos_dict = {'ADJ': 0, 'ADV': 0, 'PROPN': 0, 'NUM': 0, 'AUX':0}
    for token in nlp(x):
        if token.pos_ in pos_dict.keys():
            pos_dict[token.pos_] +=1
    return pos_dict['ADJ'], pos_dict['ADV'], pos_dict['PROPN'], pos_dict['NUM'], pos_dict['AUX']

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
    entity_list = zip(*df['article_text'].map(return_entites))
    entity_list = list(entity_list)
    entity_list = pd.DataFrame(entity_list).transpose()
    entity_list.columns = ['ENT_PERSON', 'ENT_NORP', 'ENT_ORG', 'ENT_LOCATION', 'ENT_PRODUCT', 'ENT_LANGUAGE', 'ENT_OTHERS']
    df = pd.concat([df, entity_list], axis=1)
    
    '''Feature 5: Parts-of-Speech Tagging'''
    print('Creating Feature: Parts-of-Speech...')
    pos_list = zip(*df['article_text'].map(return_pos))
    pos_list = list(pos_list)
    pos_list = pd.DataFrame(pos_list).transpose()
    pos_list.columns = ['POS_ADJ', 'POS_ADV', 'POS_PROPN', 'POS_NUM', 'POS_AUX']
    df = pd.concat([df, pos_list], axis=1)
    
    return df