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
from flashtext.keyword import KeywordProcessor
conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")
from nltk import word_tokenize
cachedStopWords = stopwords.words("french") + stopwords.words("english")
def getWords(text):
    return re.findall('\w+', text)

def getKey(item):
    return item[1]


def read_srt_files(listSrt):
    stemmer = FrenchStemmer()
    list = []
    string = ''
    somme = 0

    for episode in listSrt:

        subs = pysrt.open(episode, encoding='iso-8859-1')

        for ligne in range(len(subs)):
            for mot in getWords(subs[ligne].text):
                if len(mot) > 2:

                    list.append(mot.lower())
                    #string = string + ' ' + j

    filtered_words = []
    for word in list:
        if word not in cachedStopWords:
            filtered_words.append(stemmer.stem(word))

    d = Counter(' '.join(filtered_words).split())

    return d

def insertInDatabase(serie, d):
    cur = conn.cursor()
    cur.execute("INSERT INTO recommandation_series (name) VALUES ('{}') returning id".format(serie))
    conn.commit()
    serie_id = cur.fetchone()[0]

    for word, number in d.items():

        try:
            cur.execute(
                "INSERT INTO recommandation_keywords (key) VALUES ('{}') returning id".format(word))
            key_id = cur.fetchone()[0]
            conn.commit()
        except Exception as e:
            conn.rollback()
            cur.execute("SELECT k.id from recommandation_keywords as k where k.key='{}'".format(word))
            key_id = cur.fetchone()[0]


        cur.execute(
            "INSERT INTO recommandation_posting (number, keywords_id, series_id) VALUES ('{0}','{1}','{2}')".format(
                number, key_id, serie_id))
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

# totals = time.time()
for key, value in subs.items():

#      start = time.time()
       text = read_srt_files(value)
#      end = time.time()
#      print('read srt', end - start)
#      startbdd = time.time()
       insertInDatabase(key, text)
#      endbdd = time.time()
#      print('INSERT BDD', endbdd - startbdd)
#
# fin = time.time()
# print('total', end - start)
