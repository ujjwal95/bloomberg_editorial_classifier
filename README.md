# Bloomberg Editorial Classifier

### Faculty Mentor
- Smaranda Muresan (Data Science Institute)

### Industry Mentors
- Daniel Preotiuc-Pietro (Bloomberg)
- Kai-Zhan Lee (Bloomberg)

### Team Members: 
- Aastha Joshi - aj2839@columbia.edu
- Ameya Karnad - ak4251@columbia.edu
- Nirali Shah - nss2173@columbia.edu
- Sarang Gupta - sg3637@columbia.edu
- Ujjwal Peshin - up2138@columbia.edu

## Project details

### Abstract
The main objective of our project is building a classifier that would be able to predict whether a
news article is an editorial. It was motivated by the need to improve on the editorial tab of the
Bloomberg terminal. This would remove the reliance on news sources to provide such
information. Our dataset was heavily imbalanced towards regular news articles, with an average
of every 10th article being non-regular. An analysis of NER and POS was performed and there
was a difference in distributions for each class, so, these features were included in our linear
models. The training dataset was undersampled and contained 6386 articles. The testing was
performed on two datasets, test (3436), and external test (1385), with the external test being a
dataset from another news source. On the test set, XLNet performed the best, and on the
external test set, BERT was the best model. Logistic regression performed very well and hence,
we would recommend using Logistic Regression in production.

### Motivation

Hundreds of thousands of news stories are published daily across the world and most make their way into the Bloomberg Terminal. A significant portion of these news stories are subjective editorial and opinion content written by staffers or individual contributors with the goal of providing a personal point of view, insight or persuading the readers on a certain issue, while others are regular reports filed by ground reporters. 

### Select Models

- Linear Models: Logistic Regression, Decision Trees, Gradient Boosting, Random Forest
- LightGBM
- RNN Models: Long Short-Term Memory, Bidirectional LSTM, BiLSTM with Attention
- BERT: Bidirectional Encoder Representations from Transformers
- XLNet

### Conclusion

BERT and XLNET are the best performing models. However, Logistic Regression has
comparable performance and does not lose out on explainability. Hence, we would recommend
using Logistic Regression in production.

## Directory 

- doc - contains the two reports for the project
- src - contains the source code for the project 
