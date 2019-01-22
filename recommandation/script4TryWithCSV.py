import fnmatch
import os
from pprint import pprint

import psycopg2
import pysrt
import re
from nltk.corpus import stopwords
import operator
from collections import Counter, OrderedDict
import time
from nltk.stem.snowball import FrenchStemmer
from nltk import word_tokenize
import csv
cachedStopWords = stopwords.words("french") + stopwords.words("english")
conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")

def getWords(text):
    return re.findall('\w+', text)


def getKey(item):
    return item[1]


def calculTf(corpus, lenCorpus):
    resultat = dict()
    for word, number in corpus.items():
        resultat[word] = (number, number / lenCorpus)
    return resultat

def maxNB(corpus):
    return corpus[max(corpus, key=corpus.get)]

def lenCorpus(corpus) -> int:
    len = 0
    for word in corpus:
        len = len + corpus[word]
    return len


def read_srt_files(listSrt: list) -> Counter:
    stemmer = FrenchStemmer()
    list = []

    for episode in listSrt:
        subs = pysrt.open(episode, encoding='iso-8859-1')
        for ligne in range(len(subs)):
            for mot in getWords(subs[ligne].text):
                if len(mot) > 2:
                    list.append(mot.lower())
                    # string = string + ' ' + j

    filtered_words = []

    for word in list:
        if word not in cachedStopWords:
            filtered_words.append(stemmer.stem(word))
            #filtered_words.append(word)

    corpus = Counter(' '.join(filtered_words).split())
    maxi = maxNB(corpus)
    corpusWithTf = calculTf(corpus, maxi)

    return {'corpus':corpusWithTf, 'lenCorpus':maxi}


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

def stockInMemory(serieName: str, serieID: int, corpus: Counter, lenCorpus: int):
    try:
        keywordID = int(sorted(dict_keyword.values())[-1])
        postingID = int(sorted(dict_posting.keys())[-1])
        print(postingID)
    except Exception  as e:
        print(e)
        keywordID = 0
        postingID = 0
    dict_serie[serieID] = serieName
    for word, value in corpus.items():

        if dict_keyword.get(word):
            keyID = dict_keyword.get(word)
            postingID += 1
            dict_posting[postingID] = (value[0],value[1], keyID, serieID,)
        else:
            keywordID += 1
            postingID += 1
            dict_keyword[word] = keywordID
            dict_posting[postingID] = (value[0],value[1], keywordID, serieID, )


subs = walk_sub('/home/hadrien/Bureau/sous-titres/') # Ne pas oublier le slash a la fin
conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")
dico = dict()
start = time.time()
dict_keyword = OrderedDict()
dict_posting = OrderedDict()
dict_serie = dict()
serieID = 0
tot = 0
totals = time.time()
for serieName, value in subs.items():
    start = time.time()
    text = read_srt_files(value)
    end = time.time()

    dico[serieName] = text
    serieID += 1
    startbdd = time.time()
    stockInMemory(serieName, serieID, text['corpus'], text['lenCorpus'])
    tot += 1
    endbdd = time.time()

    print('INSERT BDD :{0} READ SRT :{1} --- {2} / {3} --- {4}'.format(endbdd - startbdd, end - start, tot, len(subs.items()), serieName))


with open('series.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dict_serie.items():
       writer.writerow([key, value]) # key = PK, value = serieName
    csv_file.close()
with open('posting.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)

    for key, value in dict_posting.items():

        writer.writerow([key, value[0], value[1], value[2], value[3]]) # key->PK value[0]->number , value[1] -> keywords_id, value[2] -> serie_id, value[1]->tf
    csv_file.close()
with open('keywords.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dict_keyword.items():
       writer.writerow([value, key])
    csv_file.close()


cur = conn.cursor()
f = open('series.csv')
cur.copy_from(f, 'recommandation_series', sep=",")
conn.commit()


cur = conn.cursor()
f = open('keywords.csv')
cur.copy_from(f, 'recommandation_keywords', sep=",")
conn.commit()


cur = conn.cursor()
f = open('posting.csv')
cur.copy_from(f, 'recommandation_posting', sep=",")
conn.commit()
conn.close()

fin = time.time()
print('Longueur de la table posting',len(dict_posting.keys()))
print('TOTAL DU TRAITEMENT :', fin - totals)


