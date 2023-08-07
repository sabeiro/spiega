# text generation

Text generation consists in selecting a particular **tokenization/embedding** where we assign a token to a word after **preprocessing** and learn sequences paying particular attention to the relative position and importance between words.

## text preprocessing

We adapt the [text preprocessing routine](https://github.com/sabeiro/kotoba/kotoba/transformer_text.py) depending on the source and the language. In particular:

* lowercase
* stemming - remove suffixes
* remove puctuation, double spaces
* clean hyperlinks

## tokenization

For each model we select a maximum number of lemmas and create a token for each word depending on the occurency in the training data set. 

* set a lower occurence frequency
* vocabular size
* handle punctuation

## models

Different models tried to learn natural language sequences starting with [long short term memory](https://github.com/sabeiro/kotoba/kotoba/text_gen.py) where the linear sequence was built in in the neural network.

[Transformers](https://github.com/sabeiro/kotoba/kotoba/gen_text_gpt.py) focus on attention maps and learn flexibly the cross correlation of words and sequences. Transformers have a built in positional embedding that helps learning grammmar features. 

## word2vec

We analyze different 

## results


