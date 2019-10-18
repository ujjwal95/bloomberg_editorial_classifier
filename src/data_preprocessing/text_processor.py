import nltk
import re
from bs4 import BeautifulSoup

class TextPreprocessing:
    def __init__(self,text):
        self.__text = text
    
    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, text):
        self.__text = text
    
    @text.deleter
    def text(self):
        del self.__text
        
    def lower_case(self, to_lower = True):
        text = self.__text
        if to_lower:
            text = ' '.join([ word.strip().lower() for word in text.split()])
        
        self.__text = text
        return self
    
    def process_html(self):
        text = self.__text
        text = BeautifulSoup(text, 'lxml').get_text()
        self.__text = text
        return self
    
    def remove_urls(self, remove_urls = True):
        text = self.__text
        if remove_urls:
            text = re.sub('http?://[A-Za-z0-9./]+','',text)
            text = re.sub('https?://[A-Za-z0-9./]+','',text)       
        self.__text = text
        return self
    
    def decode_text(self):
        text = self.__text
        try:
            text = text.decode("utf-8-sig").replace(u"\ufffd", "?")
        except:
            text = text
        self.__text = text
        return self
    
    def stopwords_remove(self, stopwords = nltk.corpus.stopwords.words('english')):
        text = self.__text
        if stopwords:
            text = " ".join([word for word in text.split() if word not in stopwords])
        self.__text = text
        return self

    def tokenize(self, tokenizer= nltk.tokenize.WordPunctTokenizer()):
        text = self.__text
        if tokenizer:
            text = tokenizer.tokenize(text)
            text = (" ".join(text)).strip()
        self.__text = text
        return self

    def lemmatize(self, lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()):
        text = self.__text
        if lemmatizer:
            text = ' '.join([lemmatizer.lemmatize(word, 'v') for word in text.split()])
        self.__text = text
        return self
    
    def stem(self, stemmer):
        text = self.__text
        # mostly stemmers are stemmer = nltk.stem.PorterStemmer()
        if stemmer:
            text = ' '.join([stemmer.stem(word) for word in text.split()])
        self.__text = text
        return self
        
    def remove_short_words(self, remove = True):
        text = self.__text
        if remove:
            text = ' '.join([w for w in text.split() if len(w)>2])
        self.__text = text
        return self
    
    def apply_contractions(self):
        contractions = { "ain't": "am not / are not", "aren't": "are not / am not", "can't": "cannot", "can't've": "cannot have", "'cause": "because",
                        "could've": "could have", "couldn't": "could not", "couldn't've": "could not have", "didn't": "did not", "doesn't": "does not",
                        "don't": "do not", "hadn't": "had not", "hadn't've": "had not have", "hasn't": "has not", "haven't": "have not", "he'd": "he had / he would", 
                        "he'd've": "he would have", "he'll": "he shall / he will", "he'll've": "he shall have / he will have", "he's": "he has / he is", 
                        "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how has / how is", "i'd": "I had / I would", 
                        "i'd've": "I would have", "i'll": "I shall / I will", "i'll've": "I shall have / I will have", "i'm": "I am", "i've": "I have", 
                        "isn't": "is not", "it'd": "it had / it would", "it'd've": "it would have", "it'll": "it shall / it will", "it'll've": "it shall have / it will have",
                        "it's": "it has / it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have", "mightn't": "might not",
                        "mightn't've": "might not have", "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not",
                        "needn't've": "need not have", "o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not",
                        "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she had / she would", "she'd've": "she would have", "she'll": "she shall / she will", 
                        "she'll've": "she shall have / she will have", "she's": "she has / she is", "should've": "should have", "shouldn't": "should not", 
                        "shouldn't've": "should not have", "so've": "so have", "so's": "so as / so is", "that'd": "that would / that had", "that'd've": "that would have",
                        "that's": "that has / that is", "there'd": "there had / there would", "there'd've": "there would have", "there's": "there has / there is",
                        "they'd": "they had / they would", "they'd've": "they would have", "they'll": "they shall / they will", "they'll've": "they shall have / they will have",
                        "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we had / we would", "we'd've": "we would have",
                        "we'll": "we will", "we'll've": "we will have", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what shall / what will",
                        "what'll've": "what shall have / what will have", "what're": "what are", "what's": "what has / what is", "what've": "what have", 
                        "when's": "when has / when is", "when've": "when have", "where'd": "where did", "where's": "where has / where is", "where've": "where have",
                        "who'll": "who shall / who will", "who'll've": "who shall have / who will have", "who's": "who has / who is", "who've": "who have",
                        "why's": "why has / why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", 
                        "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would", "y'all'd've": "you all would have",
                        "y'all're": "you all are", "y'all've": "you all have", "you'd": "you had / you would", "you'd've": "you would have", "you'll": "you shall / you will",
                        "you'll've": "you shall have / you will have", "you're": "you are", "you've": "you have" }
        
        text = self.__text
        for word in text.split():
            if word.lower() in contractions:
                text = text.replace(word, contractions[word.lower()])
        self.__text = text
        return self
    
    def remove_stutterings(self):
        from itertools import groupby 
        text = self.__text
        text = ' '.join([i[0] for i in groupby(text.split())])
        self.__text = text
        return self
    
    def remove_punctuations(self):
        import string
        text = self.__text
        text = text.translate(str.maketrans('', '', string.punctuation))
        self.__text = text
        return self