# French Word Embeddings
French Word Embeddings from series subtitles.

The current repository includes three versions of word embeddings :

  1. [Word2Vec](https://code.google.com/archive/p/word2vec/) by Google
  2. [GloVe](https://nlp.stanford.edu/projects/glove/) by Stanford NLP
  3. [FastText](https://fasttext.cc/) by Facebook's AI Research - FAIR
 
All these models are trained using [Gensim](https://radimrehurek.com/gensim/) software's built-in functions.

Currently, the vocabulary is about 25k words based on subtitles after the preproccessing phase. 

The vocabulary is clean and contains simple and meaningful words.

**This work is still under development.**
___
# Reproduction 

To reproduce the Word Embeddings, one must pre-process the files after scraping `sous-titres.eu`. This website is the source of data used in this project. The current pre-processing scripts aren't well made, because the files in the website do not follow a specific naming protocol. Thus, only the scraping file is provided. 

In future work, I will create a pre-processing script that gathers the whole data with minimum possible issues and errors.

## Scraping

To launch the scraping script, all you have to do is setting up the environment which includes the following packages :

  1. [Requests](https://anaconda.org/anaconda/requests) for HTTP requests 
  2. [BeautifulSoup](https://anaconda.org/anaconda/beautifulsoup4) for simple Scraping requests

I'm using Anaconda Distribution, if you need any specific instruction for the installation, pleace refer to this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-16-04) by DigitalOcean for Linux as a guide to get the environment set up. 

You may need to install other packages, but usually packages like `zipfile` and `time` come with Anaconda Distribution and you won't need to install them. Otherwise, To install the packages in Anaconda, please refer to the urls in the previous packages list. The following command is generally the most used one :

	conda install -c anaconda <package>

The command line to launch the scraper script is simply the following : 


	python scraper.py --serie <serie_name>

You may leave series_name empty. To get more series, please refer to the website. This scraper doesn'ts pull all the series, only the provided ones are scraped. This helps get specific text data for a specific problem to avoid using biased data. For our project, I scraped family series like 'How I Met Your Mother'.

## Word Embeddings Models

The file `data.txt`, in [Data](https://github.com/Ismailhachimi/WordEmbeddings_fr/blob/master/Data) repository, is the result of a pre-processing phase of a list of series. Currently, it includes 7xx.xxx sentences. There is more available data, but still under pre-processing to make sure it's clean.

I'm using the file mentioned above, to build Word2Vec, GloVe and FastText language models to have a numerical presentation of words or in other words, Word Embeddings.

As it may be clear that GloVe isn't doing good as Word2Vec or FastText, the problem may lie in the fact that data isn't as big as needed to train the model. The file `data.txt` will be filled with more data in the future.

To reproduce the models, change hyperparameters, parameters or whatever you need, you can refer to the notebooks in the current directory. The notebooks are using the following packages : 

  1. [Gensim](https://anaconda.org/anaconda/gensim) A Topic Modeling library that includes a complete implementation of Word2Vec and FastText
  2. [glove-python](https://github.com/maciejkula/glove-python) A librarie for GloVe in python

To Install glove-python, you may use the following command line :

	pip install glove_python
___
## Intention Model

In this section, I use a pretrained FastText model to train an intention model for Sequence-to-Class (Seq2Class). In case you need the pretrained models, you can download them via this [LINK](https://www.dropbox.com/sh/7rt459ivnydpl0u/AAAOelXsVJjHjk1ZrNVhX6TTa?dl=0). You may as well train your the FastText model and use it in this part.

**Please make sure you download all the files to avoid getting errors**

The data used for this model is under the [POC](https://github.com/Ismailhachimi/WordEmbeddings_fr/blob/master/POC_data) repository. POC stands for Proof of Concept. The data is hand-maded and includes Input data `X` as a bunch of text sequences with a target `Y` which is a service label. This model maps an input request to a specific related website (Google, Youtube, LinkedIn, Booking, Amazon).

`Intention-Seq2Class` notebook contains the full implementation of the **Seq-to-Class with Intention** architecture.

To get a global view of the architecture, you may refer to this [image](https://github.com/Ismailhachimi/WordEmbeddings_fr/blob/master/images/seq2class_architecture.png) in the current repository.

Finally, `utils.py` contains a number of functions that are used in the word embeddings as in the intention model notebooks.
___
# License
This work is licensed under the [MIT License](LICENSE).
