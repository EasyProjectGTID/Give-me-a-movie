import os
import psycopg2
import pysrt
import re
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from nltk.corpus import stopwords
import operator
from collections import Counter
import time
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    cachedStopWords = stopwords.words("french") + stopwords.words("english") #Permet une optimisation sinon NLTK réouvre à chaque fois le fichier contenant les stopwords
conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")
cur = conn.cursor()


def getWords(text):
    return re.compile('\w+').findall(text)

def getKey(item):
    return item[1]

def insertWordCount(word, seriePk):

    cur.execute(
        "INSERT INTO recommandation_keywords (key) VALUES ('{}') returning id".format(word[0]))
    key_id = cur.fetchone()[0]
    cur.execute(
        "INSERT INTO recommandation_posting (number, keywords_id, series_id) VALUES ('{0}','{1}','{2}')".format(word[1],
                                                                                                             key_id,
                                                                                                             seriePk))
    conn.commit()


def insertSerie(serieName):
    cur = conn.cursor()

    cur.execute("INSERT INTO recommandation_series (name) VALUES ('{}') returning id".format(serieName))
    conn.commit()
    return cur.fetchone()[0]

def ExtractWordsAndCount(filepath, seriePk):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        subs = pysrt.open(filepath, encoding='iso-8859-1')
    list = []
    string = ''

    #Pour toutes les lignes dans le fichier de sous titre
    for nbLine in range(len(subs)):

        for word in getWords(subs[nbLine].text):
            list.append(word.lower())
            #string = string + ' ' + word # Recréer le text complet


    filtered_words = [word for word in list if word not in cachedStopWords] # Supprime les stopword
    d = Counter(' '.join(filtered_words).split()) # Créer un dictionnaire type mot:nb de fois présent


    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

    #print(sorted_d)
    list = set()
    
    for x in sorted_d:
        list.add(x)
    list_sorted = sorted(list, key=getKey)
    start = time.time()

    for word in list_sorted: #word type tuple avec ('word', 5)

        insertWordCount(word, seriePk)

    end = time.time()


def walk_sub(path, seriepk):
        ExtractWordsAndCount(path, seriepk)


if __name__ == '__main__':
    import time

    start = time.time()
    import multiprocessing

    for root in os.scandir("G:\Desktop\sous-titres"):
            seriepk = insertSerie(root.name)
            listpath = []
            for files in os.scandir(root):
                if str(files.name)[-4:] == '.zip':
                    pass
                else:
                    listpath.append("G:\Desktop\sous-titres\\" + root.name + '/' + files.name)


            ListOfProcesses = []
            Processors = 20  # n of processors you want to use
            # Divide the list of files in 'n of processors' Parts
            Parts = [listpath[i:i + Processors] for i in range(0, len(listpath), Processors)]

            for part in Parts:

                for f in part:

                    string = str(f)
                    p = multiprocessing.Process(target=walk_sub, args=(string, seriepk))
                    p.start()
                    ListOfProcesses.append(p)
                for p in ListOfProcesses:
                    p.join()
    end = time.time()
    print(end - start)