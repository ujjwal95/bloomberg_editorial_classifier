# Processing Data Module
This module prepares the data for input into ensemble machine learning models and neural network models. The following functions are carried out by the moduls, with the corresponding sub-modules mentioned:

1. Data assembly (data_assembler.py) - Combines the various data sources together from the data folder (present in the drive), and provides a unified data to the rest of the modules and sub-modules.

2. Train-test splits (data_features_part1.py) - Carries out a temporal train-test split, which ensures that the test dataset is in the future, to check that the model is robust to future datasets in production.

3. Undersampling (data_features_part1.py) - Due to a severe imbalance in the training data, it undersamples the training data such that for each target=1 in the data, there is an equivalent target= 0 in the data from the same day and data source. If sufficient target= 0 is not available, a lookback and lookforward is used to enusre that there are a minimum number of target= 0 available.

4. General- purpose feature extraction (data_features_part1.py)- The following features


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
