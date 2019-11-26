A Multi-input BiLSTM model was developed. The 2 inputs to the model are article heading &
text. Both input sources were trained separately on the general model architecture.
The results were concatenated & the final vector passed through a dense layer with softmax
activation function to predict the final class probabilities.