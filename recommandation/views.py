import time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import os
import pysrt
import re
import nltk
from nltk.corpus import stopwords
from recommandation.forms.uploadForm import UploadFileForm
from recommandation.models import Series, Posting, KeyWords





def view_serie(request):
    posting = Posting.objects.filter(series=5)

    return HttpResponse(str(len(posting)))

def getWords(text):
    return re.compile('\w+').findall(text)


def analyseFile(filename, series=None):

    subs = pysrt.open(filename, encoding='iso-8859-1')
    list = []
    string = ''
    for i in range(len(subs)):
        for j in getWords(subs[i].text):
            list.append(j.lower())
            string  = string + ' ' + j

    cachedStopWords = stopwords.words("french") + stopwords.words("english")
    #nltk.download('stopwords')
    filtered_words = [word for word in list if word not in cachedStopWords]


    import operator
    from collections import Counter

    d = Counter(' '.join(filtered_words).split())

    # create a list of tuples, ordered by occurrence frequency
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    #client = MongoClient('localhost', 27017)

    #post = {"title" : series.name,
            #"keywords": subs.text}
    #db = client.serie
   # db.Serie.insert_one(post)

    # print all entries that occur more than once
    for x in sorted_d:
        if x[1] > 2:
            #enelever les doublons
            keyword = KeyWords.objects.create(key=x[0])
            Posting.objects.create(number=x[1], keywords=keyword, series=series)


def handle_uploaded_file(f):
    with open('C:/Users/hhout/PycharmProjects/PTUT/' + f.name, 'wb+') as destination:

        for chunk in f.chunks():
            destination.write(chunk)

@require_http_methods(["GET","POST"])
def upload(request):
    start = time.time()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            try:
                serie = Series.objects.create(name=request.FILES['file'].name).save()
                serie = Series.objects.get(name=request.FILES['file'].name)
                analyseFile(request.FILES['file'].name, serie)
            except:
                return HttpResponse('ERROR')

            return HttpResponse('upload OK')
    else:
        for root in os.scandir("G:\Desktop\sous-titres"):
            for files in os.scandir(root):

                if str(files.name)[-4:] == '.zip':
                    pass
                else:

                    serie = Series.objects.create(name=files.name).save()
                    serie = Series.objects.get(name=files.name)
                    analyseFile("G:\Desktop\sous-titres\\" + root.name + '/' + files.name, series=serie)


               
        form = UploadFileForm()
    end = time.time()
    print(end - start)

    return render(request, 'upload.html', {'form': form})


