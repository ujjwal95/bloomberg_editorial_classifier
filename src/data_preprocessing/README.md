## Creating Features

Below are the features that would be created for running the ML models:

```article_length```: Length of the article

```heading_length```: Length of the title

```num_questions```: Number of questions marks in the article

```num exclamations```: Number of exclamation marks in the article

```article_sentiment```: Sentiment of the article using TextBlob. Range is [-1.00, 1.00] with -1.00 implying negative and 1.00 implying positive sentiment.

```article_subjectivity```: Subjectivity of the article using TextBlob. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.

```heading_sentiment```: Sentiment of the heading

```heading_subjectivity```: Subjectivity of the heading

```ENT_PERSON, ENT_NORP, ENT_ORG, ENT_LOCATION, ENT_PRODUCT, ENT_LANGUAGE, ENT_OTHERS```: Number of different named entities in the article. Refer to the EDA section for the description of the entities.

```POS_ADJ, POS_ADV, POS_PROPN, POS_NUM, POS_AUX```: Number of different parts-of-speech tags in the article. Refer to the EDA section for the description of the POS tags.


### Execution Instructions

Run the ```main(df)``` function in the create_features.py file with pandas dataframe as the input. The function return an updated dataframe with the new features added as columns.

```input```: Dataframe with atleast two columns: ```heading``` and ```article_text```
```output```: Dataframe with new features
