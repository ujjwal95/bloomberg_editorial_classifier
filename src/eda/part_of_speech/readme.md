### Exploratory data analysis of different Parts of Speech in Regular and Non-Regular Articles

In this notebook, we will look at the distribution of different parts of speech in regular and non-regular articles. 

We would be looking at how many times different parts of speeches were used in an article. We first calulate a `Instance per article length` metric which evaluates the percentage of that POS appearing in the article. We then look at the distribution of `instance per article length` with the count of `articles` for both regular and non regular articles

To ensure that the distribution are comparable, we have undersampled the "Regular" class

Our general Hypothesis before this experiment is that the POS speech used in Regular and Non regular articles would be different

Let us first look at the different parts of speech detected. We use Spacy package from Python to conduct this experiment

**Different Parts of speech**

`ADJ` : adjective

`ADP` : adposition

`ADV` : adverb

`AUX` : auxiliary verb

`CONJ` : coordinating conjunction

`DET` : determiner

`INTJ` : interjection

`NOUN` : noun

`NUM` : numeral

`PART` : particle

`PRON` : pronoun

`PROPN` : proper noun

`PUNCT` : punctuation

`SCONJ` : subordinating conjunction

`SYM`: symbol

`VERB` : verb

`X` : other




