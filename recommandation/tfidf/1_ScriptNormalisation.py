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
import unidecode
from nltk.stem.snowball import FrenchStemmer, EnglishStemmer

from PTUT.settings import DATABASES
from recommandation.tfidf.detectLanguage import detect_language


cachedStopWords = stopwords.words("french") + stopwords.words("english")

def getWords(text):
    return re.findall('\w+', text)

def getKey(item):
    return item[1]
#"""retourne à partir du dictionnaire corpus [mots - nboccurences ] et du maximum d'occurence
#dans ce même corpus un dictionnaire resultat[mot-tf} avec tf arrondi à 3 chiffres Ce dictionnaire est trié par ordre décroissant de tf"""
def calculTf(corpus, maxi):
    resultat = dict()
    for word, number in corpus.items():
        resultat[word] = (number, round(number / maxi, 4))
    #print(sorted(resultat.items(), key=operator.itemgetter(1), reverse=True))
    return resultat

def maxNB(corpus):
    return corpus[max(corpus, key=corpus.get)]




def read_srt_files(listSrt): #retourne un dictionnaire contenant en valeur un dictionnaire [mot-tf] et en clé le nombre
    #d'occurence du mot le plus cité dans le corpus
    corpus = collections.Counter()


    for episode in listSrt:
        #"""pour chaque fichier srt d'une série, on sépare chaque mot de ce srt,
        #on les stemme avant de regrouper les similaires et de les compter. ce regroupement est commun pour tous les srts"""
        #print(episode)

        subs = pysrt.open(episode, encoding='iso-8859-1')

        language = detect_language(subs.text[0:1000])
        if language == 'french':
            stemmer = FrenchStemmer()
        elif language == 'english':
            stemmer = EnglishStemmer()
        #stemmer = PorterStemmer()

        tokens = nltk.word_tokenize(subs.text)
        words = [stemmer.stem(unidecode.unidecode(w.lower())) for w in tokens if w.lower() not in cachedStopWords and len(w) > 2 and w.lower().isalpha()]

        words = [stemmer.stem(w.lower()) for w in tokens if w.lower() not in cachedStopWords and len(w) > 2 and w.lower().isalpha()]
        """words est une liste de mots stemmés pour un épisode"""
        #words = [w.lower() for w in tokens if w.lower() not in cachedStopWords and len(w) > 3 and w.lower().isalpha()]

        corpus.update(words)

    maxi = maxNB(corpus)


    corpusWithTf = calculTf(corpus, maxi)

    return {'corpus':corpusWithTf, 'lenCorpus':maxi} #maxi est le mot qui apparait le plus dans le corpus

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
    """le dictionnaire contient en clés le nom des répertoires contenu dans directory, la variable passsée en en-tête
    et en valeurs une liste contenant le chemin vers les srt"""
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


conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(DATABASES['default']['NAME'],
                                                                                DATABASES['default']['USER'],
                                                                                DATABASES['default']['HOST'],
                                                                                DATABASES['default']['PASSWORD']))
subs = walk_sub('/home/hadrien/Bureau/sous-titres/') # Ne pas oublier le slash a la fin

tot = 0
totals = time.time()
for key, value in subs.items():



    start = time.time()
    text = read_srt_files(value) #"""value est ici une liste de chemin vers les srt d'une série"""
    end = time.time()

    startbdd = time.time()

    insertInDatabase(key, text['corpus'], text['lenCorpus'])
    tot += 1
    endbdd = time.time()
    print('INSERT IN BDD:{0} READ SRT :{1} --- {2} / {3}'.format(endbdd - startbdd, end - start, tot, len(subs.items())))

fin = time.time()
print('TOTAL DU TRAITEMENT :', fin - totals)

