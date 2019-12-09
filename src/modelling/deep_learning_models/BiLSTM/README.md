Models implemented:
1. BiLSTM 
2. BiLSTM with attention
3. Multi - input BiLSTM

The general model architecture used is BiLSTM layer with 64 hidden units. The
BiLSTM layer has been regularised by using dropout (p=0.2) & recurrent dropout (p=0.1)
on hidden layers. The next layer used is a global Max pooling layer. It is followed by a dense layer
of 64 units with ‘relu’ activation. Next, a dropout layer with dropout percentage p=0.5 is used.
Dropout helps improve model generalizability & prevent model overfitting. The last layer is a Dense
layer with softmax activation to give a probabilistic output score for article classification.

To improve on the BiLSTM model we have incorporated word level attention. It is observed that different words & sentences in a document are differentially informative. Attention uses context to discover when a sequence of tokens is relevant rather than simply filtering for sequence of tokens taken out of context. It can be that for an editorial article the model pays more attention to words like why, don't, lie, all, etc. which convey strong emotions of the author. Words like both, guys, democracy, die, etc. are given a lower score as they are more generic and don't give any strong opinions of the author.

A Multi-input BiLSTM model was developed. The 2 inputs to the model are article heading & text. Both input sources were trained separately on the general model architecture. The results were concatenated & the final vector passed through a dense layer with softmax activation function to predict the final class probabilities.