import nltk
import nltk
import spacy
from nltk.corpus import wordnet as wn
from spacy.lang.en import English
from nltk.stem.wordnet import WordNetLemmatizer


nltk.download('wordnet')
nltk.download('stopwords')
spacy.load('en')
parser = English()
en_stop = set(nltk.corpus.stopwords.words('english'))

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)


def transcript_preprocessing(text):
    """

    :param text:
    :return:
    """
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens
