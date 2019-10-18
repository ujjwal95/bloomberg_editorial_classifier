import numpy as np
from text_processor import TextPreprocessing
from itertools import groupby
# sentiment analyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from afinn import Afinn

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
