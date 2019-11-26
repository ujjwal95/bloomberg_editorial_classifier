To improve on the BiLSTM model we have incorporated word level attention here.

It is observed that different words & sentences in a document are differentially informative. Attention uses context to discover
when a sequence of tokens is relevant rather than simply filtering for sequence of tokens taken out of context.



It can be that for an editorial article the model pays more attention to words like why, don't, lie, all, etc. which convey strong emotions of the author. Words like both, guys, democracy, die, etc. are given a lower score as they are more generic and don't give any strong opinions of the author.





