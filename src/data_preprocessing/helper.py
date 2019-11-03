import numpy as np
from text_processor import TextPreprocessing
from itertools import groupby
# sentiment analyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from afinn import Afinn
import pandas as pd
import spacy
import gensim
from textblob import TextBlob
nlp = spacy.load('en_core_web_sm')


def transform_to_word(name):
        try: 
            float(name)
            import inflect
            p = inflect.engine()
            name = p.number_to_words(int(name))
            return name
        except:
            return name

def int_to_string(article_text):
    import inflect
    import numpy as np
    """The workhorse of this feature extractor"""
    p = inflect.engine()
    return " ".join([transform_to_word(x) for x in article_text.split()])

def average_word_length(article_text):
    try:
        return np.mean([len(word) for word in article_text.split()])
    except:
        return len(str(article_text))
    
def text_preprocessing(article_text, stopwords = None):
    
    if stopwords is None:
        stop_words = ['um','a','the','uh','an']
    else:
        stop_words = stopwords
    return TextPreprocessing(article_text).apply_contractions().lower_case().remove_punctuations().process_html().remove_urls().decode_text().remove_stutterings().remove_short_words().stopwords_remove(stopwords = stop_words).lemmatize().remove_punctuations().text

def sentiment_from_vader(article_text):
    sent_scores = SentimentIntensityAnalyzer().polarity_scores(article_text)
    return sent_scores["neg"], sent_scores["neu"], sent_scores["pos"], sent_scores["compound"]

def sentiment_from_afinn(article_text):
    return Afinn().score(article_text)

def return_entities(x):

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