import fnmatch
import os
import psycopg2
import pysrt
import re
from nltk.corpus import stopwords
import operator
from collections import Counter
import time
from nltk.stem.snowball import FrenchStemmer
import nltk
from PTUT.settings import DATABASES

conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password=''".format(DATABASES['default']['NAME'], DATABASES['default']['USER'], DATABASES['default']['HOST'] ))

cachedStopWords = stopwords.words("french") + stopwords.words("english")


def getWords(text):
    return re.findall('\w+', text)

def getKey(item):
    return item[1]

def calculTf(corpus, lenCorpus):
    resultat = dict()
    for word, number in corpus.items():
        resultat[word] = (number, number / lenCorpus)
    return resultat

def lenCorpus(corpus):
    len = 0
    for word in corpus:
        len = len +corpus[word]
    return len

def read_srt_files(listSrt):
    stemmer = FrenchStemmer()
    list = []

    for episode in listSrt:
        subs = pysrt.open(episode, encoding='iso-8859-1')
        for ligne in range(len(subs)):
            for mot in getWords(subs[ligne].text):
                if len(mot) > 2:
                    list.append(mot.lower())


    filtered_words = []
    for word in list:
        if word not in cachedStopWords:
            filtered_words.append(stemmer.stem(word))

    corpus = Counter(' '.join(filtered_words).split())
    l = lenCorpus(corpus)
    print(len(corpus))
    corpusWithTf = calculTf(corpus, l)
    print(len(corpusWithTf))
    return {'corpus':corpusWithTf, 'lenCorpus':l}

def insertInDatabase(serie, corpus, lenCorpus):

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO recommandation_series (name, max_keyword_nb) VALUES ('{0}', '{1}') returning id".format(serie,
                                                                                                             lenCorpus))
    conn.commit()
    serie_id = cur.fetchone()[0]

    for word, value in corpus.items():
        try:
            cur.execute(
                "INSERT INTO recommandation_keywords (key) VALUES ('{}') returning id".format(word))
            key_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO recommandation_posting (number, keywords_id, series_id, tf) VALUES ('{0}','{1}','{2}', '{3}')".format(
                    value[0], key_id, serie_id, value[1]))
            conn.commit()
        except Exception as e:
            conn.rollback()
            cur.execute("SELECT k.id from recommandation_keywords as k where k.key='{}'".format(word))
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

subs = walk_sub('/home/hadrien/Bureau/sous-titres/') # Ne pas oublier le slash a la fin
tot = 0
totals = time.time()
for key, value in subs.items():
    if key =='bones':
        print(key)
        print(value)
    # start = time.time()
    # text = read_srt_files(value)
    # end = time.time()
    #
    # startbdd = time.time()
    # insertInDatabase(key, text['corpus'], text['lenCorpus'])
    # tot += 1
    # endbdd = time.time()
    # print('INSERT IN BDD:{0} READ SRT :{1} --- {2} / {3}'.format(endbdd - startbdd, end - start, tot, len(subs.items())))

fin = time.time()
print('TOTAL DU TRAITEMENT :', fin - totals)
