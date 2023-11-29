# text generation

In text generation we build a model trained on sequences like:

* prompt / answers
* text / text with blanks
* language 1 / language 2
* sequence n / sequence n + 1

The model would learn how to map the input and output and learn how to answer, complete text, translate...

The model is composed by an **encoder and a decoder**, we start from long-short-term-memory models and we evolve into transformers.

There are different procedures to **preprocess and parse** the text to be able to feed the data into the model.

## text preprocessing

We use this [text preprocessing routine](https://github.com/sabeiro/kotoba/kotoba/clean_text.py) to clean and simplify the text

* lowercase
* stemming - remove suffixes
* remove puctuation, double spaces
* clean hyperlinks
* remove stopwords

After we preprocessed the text we create a corpus using the remaning lemmas and choose a **vocabulary**. Usually the words for the vocabulary are chosen as the most frequent until a maximum vocabulary size.

## tokenization

For each model we select a maximum number of lemmas and create a token for each word depending on the occurency in the training data set. 

* set a lower occurence frequency
* vocabular size
* handle punctuation

A token can be a caracter, a word, a bag of words... To reduce the token dimension we can introduce semantic relationship between lemmas as per word2vec. 

The tokens need to be **reshaped** as the model needs, usually adding an additional dimension for batching.

We need to save a consistent function to preprocess the text, select the words for the vocabulary, tokenize and reshape the data.

## models

We use and compare different models.

Different models tried to learn natural language sequences starting with [long short term memory](https://github.com/sabeiro/kotoba/kotoba/text_gen_lstm.py) where we use two layers of LSTM of 256 characters and where the model learns the next character. Results are usually poor and lack of semantic consitency.

[Transformers](https://github.com/sabeiro/kotoba/kotoba/gen_text_gpt.py) focus on attention maps and learn flexibly the cross correlation of words and sequences. Transformers have a built in positional embedding that helps learning grammmar features. 

With [BERT](https://github.com/sabeiro/kotoba/kotoba/bert_transformer.py) we show an extended example of a BERT architecture with its [characteristic features](https://www.tensorflow.org/text/tutorials/transformer).

## generative results

We use the [routine](https://github.com/sabeiro/kotoba/example/text_translate.py) to load example files and test the different models.

## word2vec

in [word2vec](https://github.com/sabeiro/kotoba/kotoba/word2vec.py) we use a shallow neural network to understand similarity between lemmas and reduce text input dimensions. 

We analyze different documents and create 2-3 dimensional plots to show dimension reduction and clustering of words. In practive 3d are too few for an effective embedding of text.

![vec2d](../f/f_kotoba/vec2d_1.png "vect 2d")
_private conversations_

![vec2d](../f/f_kotoba/vec2d_4.png "vect 2d")
_private conversations_

![vec2d](../f/f_kotoba/vec2d_5.png "vect 2d")
_private conversations_

![vec2d](../f/f_kotoba/vec2d_7.png "vect 2d")
_private conversations_

A 3d representation shows a more complex structure

![vec3d](../f/f_kotoba/vec3d_2.png "vect 2d")
_private conversations_

![vec3d](../f/f_kotoba/vec3d_3.png "vect 2d")
_private conversations_




