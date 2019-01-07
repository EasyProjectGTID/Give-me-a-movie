import os
import re

import psycopg2
import pysrt
from nltk.corpus import stopwords
import asyncio


def getWords(text):
    return re.compile('\w+').findall(text)

async def analyseFile(filename, series=None):
    subs = pysrt.open(filename, encoding='iso-8859-1')
    list = []
    string = ''
    for i in range(len(subs)):
        for j in getWords(subs[i].text):
            list.append(j.lower())
            string  = string + ' ' + j
    #nltk.download('stopwords')
    filtered_words =  [word for word in list if word not in stopwords.words('french')]
    import operator
    from collections import Counter
    d = Counter(' '.join(filtered_words).split())
    # create a list of tuples, ordered by occurrence frequency
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    # print all entries that occur more than once
    for x in sorted_d:
        if x[1] > 5:
            print(x)
            pass
            """keyword = KeyWords.objects.create(key=x[0])
            Posting.objects.create(number=x[1], keywords=keyword, series=series)"""

async def pars():
    for root in  os.scandir("G:\Desktop\sous-titres"):
        for files in os.scandir(root):

            if str(files.name)[-4:] == '.zip':
                pass
            else:

                """serie = Series.objects.create(name=files.name).save()
                serie = Series.objects.get(name=files.name)"""
                await analyseFile("G:\Desktop\sous-titres\\" + root.name + '/' + files.name)

loop = asyncio.get_event_loop()
loop.run_until_complete(pars())
loop.close()