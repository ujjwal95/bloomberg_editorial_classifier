The general model architecture used is LSTM layer with 64 hidden units. The
LSTM layer has been regularised by using dropout (p=0.2) & recurrent dropout (p=0.1)
on hidden layers. The next layer used is a global Max pooling layer. It is followed by a dense layer
of 64 units with ‘relu’ activation. Next, a dropout layer with dropout percentage p=0.5 is used.
Dropout helps improve model generalizability & prevent model overfitting. The last layer is a Dense
layer with softmax activation to give a probabilistic output score for article classification.