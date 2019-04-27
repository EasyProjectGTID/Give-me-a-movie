import nltk
from nltk.corpus import stopwords
import operator
from collections import Counter
import time
from nltk.stem.snowball import FrenchStemmer, EnglishStemmer
from nltk import word_tokenize

from PTUT.settings import DATABASES
nltk.download('stopwords')
nltk.download('punkt')


cachedStopWords = stopwords.words("french") + stopwords.words("english")
print(cachedStopWords)

def _calculate_languages_ratios(text):
    """
    Calculate probability of given text to be written in several languages and
    return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}

    @param text: Text whose language want to be detected
    @type text: str

    @return: Dictionary with languages and unique stopwords seen in analyzed text
    @rtype: dict
    """

    languages_ratios = {}

    '''
    nltk.wordpunct_tokenize() splits all punctuations into separate tokens

    >>> wordpunct_tokenize("That's thirty minutes away. I'll be there in ten.")
    ['That', "'", 's', 'thirty', 'minutes', 'away', '.', 'I', "'", 'll', 'be', 'there', 'in', 'ten', '.']
    '''

    tokens = nltk.wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements)  # language "score"

    return languages_ratios


# ----------------------------------------------------------------------
def detect_language(text):
    """
    Calculate probability of given text to be written in several languages and
    return the highest scored.

    It uses a stopwords based approach, counting how many unique stopwords
    are seen in analyzed text.

    @param text: Text whose language want to be detected
    @type text: str

    @return: Most scored language guessed
    @rtype: str
    """

    ratios = _calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)

    return most_rated_language

text= 'je le ferait bien un jour'


language = detect_language(text)
if language == 'french':
    stemmer = FrenchStemmer()
elif language == 'english':
    stemmer = EnglishStemmer()

tokens = nltk.word_tokenize(text)

tokens = nltk.word_tokenize(text)

words = [stemmer.stem(w.lower()) for w in tokens if w.lower() not in cachedStopWords and len(w) > 2 and w.lower().isalpha()]


print(words)