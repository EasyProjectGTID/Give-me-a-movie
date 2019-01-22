# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 14:45:44 2019

@author: Hania
"""

import math
import fnmatch
import os
import time

import pysrt
import nltk
import nltk.corpus
import collections
from nltk.stem.snowball import FrenchStemmer
import pandas as pd
import numpy as np



stop_words = set(nltk.corpus.stopwords.words("french") + nltk.corpus.stopwords.words("english"))
stemmer = FrenchStemmer()


def word_count_for_srt_files2(listSrt):
    
    """ tworzmy pusty slownik-counter -- rodzaj slownika, w ktorym wartosci
        to liczby calkowite; struktura ta sluzy do zliczania """
    word_count = collections.Counter()

    for episode in listSrt:
        subs = pysrt.open(episode, encoding='iso-8859-1')
        for block in subs:
            ligne = block.text
            """ type(ligne) = str """
            tokens = nltk.word_tokenize(ligne)
            words = [stemmer.stem(token.lower()) for token in tokens if token.isalpha()]
            words = [w for w in words if w not in stop_words]

            word_count.update(words)
            print(word_count)
    return word_count


def word_count_for_srt_files(listSrt):
    word_count = collections.Counter()
    for episode in listSrt:
        subs = pysrt.open(episode, encoding='iso-8859-1')
        t = subs.text
        tokens = nltk.word_tokenize(t)
        words = [token.lower() for token in tokens if token.isalpha()]
        words = [w for w in words if w not in stop_words]
        word_count.update(words)
    return word_count



def process_series(series):

    no_documents_with_a_word = collections.Counter()
    tf = {}
    for seria, files in series.items():
        """ (seria) - key;
            (files) - value, ktore jest lista sciezek do plikow srt serii (seria) """
        if len(files) > 0:
            print(seria)
            wc = word_count_for_srt_files(files)
            print("word_count_for_srt_files...done")
        
            """ (wc) zlicza liczbe wystapien poszczegolnyc slow w dialogach serii (seria) """
            tf[seria] = term_freq(wc)
            """ obliczamy tf serii (seria) i zapamietujemy go w slowniku (tf) pod kluczem (seria) """
            word_set = wc.keys()
            """ pod (word_set) podstawiamy zbior kluczy/slow z licznika slow w serii """
            no_documents_with_a_word.update(word_set)
            """ ... i w liczniku (no_documents_with_a_word) zwiekszamy o jeden wartosc 
                przy kazdym slowie ze zbioru (word_set) """
    
    print("idf, weights...")

    total_no_documents = len(tf)            
    no_documents_with_a_word = pd.Series(no_documents_with_a_word)
    """ zamienilismy z Counter na Series, zeby ponizej mozna bylo robic operacje
        arytmetyczne """
    idf = np.log(total_no_documents / no_documents_with_a_word)
    
    weight = {}
    for seria in tf:
        (_tf, _idf) = pd.Series.align(tf[seria], idf, join='inner')
        weight[seria] = _tf * _idf
        """ prawie to samo, co 
            weight[seria] = tf[seria] * idf
            tyle ze ignorujemy wspolrzedne, ktorych nie ma w tf[seria]
            w przeciwnym razie, mielibysmy mnostwo wartosci NaN """
    
    print("done")
    
    return weight



def term_freq(word_count):
    tf = pd.Series(word_count)
    tf /= sum(word_count.values())
    return tf

def correlation(v1, v2):
    scalar_prod_v1_v2 = pd.Series.sum(v1 * v2)
    length_v1 = math.sqrt(pd.Series.sum(v1 * v1))
    length_v2 = math.sqrt(pd.Series.sum(v2 * v2))
    return scalar_prod_v1_v2 / (length_v1 * length_v2)
    

def correlation_matrix(w):
    m = { seria : {} for seria in w }
    for i in w:
        print(i)
        for j in w:
            if i in m[j]:
                m[i][j] = m[j][i]
            else:
                m[i][j] = correlation(w[i], w[j])
    return pd.DataFrame(m)


def serialize(w):
    print('Serialization...')
    for k, v in w.items():
        print(k)
        v.to_pickle(k + '.pkl')
    print('Done')


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
    word_count_for_srt_files2(value)

fin = time.time()
print('TOTAL DU TRAITEMENT :', fin - totals)