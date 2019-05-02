import collections
import fnmatch
import operator
import os
import nltk
import psycopg2
import pysrt
import re
from nltk.corpus import stopwords
import time
from nltk.stem import PorterStemmer
from nltk.stem.snowball import FrenchStemmer, EnglishStemmer

from PTUT.settings import DATABASES

cachedStopWords = stopwords.words("french") + stopwords.words("english")


def getWords(text):
    return re.findall('\w+', text)

def getKey(item):
    return item[1]

def calculTf(corpus, maxi):
    resultat = dict()
    for word, number in corpus.items():
        resultat[word] = (number, round(number / maxi, 3))
    print(sorted(resultat.items(), key=operator.itemgetter(1), reverse=True))
    return resultat

def maxNB(corpus):
    return corpus[max(corpus, key=corpus.get)]




def read_srt_files(listSrt):
    corpus = collections.Counter()


    for episode in listSrt:
        #print(episode)

        subs = pysrt.open(episode, encoding='iso-8859-1')
        # language = detect_language(subs.text[0:1000])
        # if language == 'french':
        #     stemmer = FrenchStemmer()
        # elif language == 'english':
        #     stemmer = EnglishStemmer()
        # else:
        stemmer = PorterStemmer()

        tokens = nltk.word_tokenize(subs.text)

        words = [stemmer.stem(w.lower()) for w in tokens if w.lower() not in cachedStopWords and len(w) > 2 and w.lower().isalpha()]

        #words = [w.lower() for w in tokens if w.lower() not in cachedStopWords and len(w) > 3 and w.lower().isalpha()]

        corpus.update(words)


    maxi = maxNB(corpus)
    print('maxi', maxi)

    corpusWithTf = calculTf(corpus, maxi)

    return {'corpus':corpusWithTf, 'lenCorpus':maxi}

def insertInDatabase(serieName, corpus, lenCorpus):

    cur = conn.cursor()
    cur.execute("INSERT INTO recommandation_series (name, max_keyword_nb) VALUES ('{0}', '{1}') returning id".format(serieName, lenCorpus))
    conn.commit()
    serie_id = cur.fetchone()[0]

    for word, value in corpus.items():
        # try:
        key_id =cur.execute(
            "INSERT INTO recommandation_keywords (key) VALUES ('{0}') ON CONFLICT (key) DO UPDATE set key='{0}' returning id".format(word))

        key_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO recommandation_posting (number, keywords_id, series_id, tf) VALUES ('{0}','{1}','{2}', '{3}')".format(
                value[0], key_id, serie_id, value[1]))
    conn.commit()


def walk_sub(directory):
    """ Parcours du dossier de sous titres retourne un dictionnaire"""
    seriesPath = dict()
    for root in os.scandir(directory):

        listPath = []
        for racine, dir, files in os.walk(directory + root.name):

            for basename in files:
                if fnmatch.fnmatch(basename, '*.srt'):
                    filename = os.path.join(racine, basename)
                    listPath.append(filename)

            seriesPath[root.name] = listPath
    return seriesPath


conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password=''".format(DATABASES['default']['NAME'], DATABASES['default']['USER'], DATABASES['default']['HOST'] ))
subs = walk_sub('/home/hadrien/Bureau/sous-titres/') # Ne pas oublier le slash a la fin

tot = 0
totals = time.time()
for key, value in subs.items():



    start = time.time()
    text = read_srt_files(value)
    end = time.time()

    startbdd = time.time()

    insertInDatabase(key, text['corpus'], text['lenCorpus'])
    tot += 1
    endbdd = time.time()
    print('INSERT IN BDD:{0} READ SRT :{1} --- {2} / {3}'.format(endbdd - startbdd, end - start, tot, len(subs.items())))

fin = time.time()
print('TOTAL DU TRAITEMENT :', fin - totals)

