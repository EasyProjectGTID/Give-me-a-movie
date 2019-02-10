from django.shortcuts import render
from recommandation.tfidf.searchTFIDF import search
from recommandation.models import Series, KeyWords, Posting


def index(request):
    return render(request, 'base.html')



def recherche(request):
    if request.method == 'POST':
        dataForm = request.POST
        words = dataForm['recherche']
        resultat = search(words)
        return render(request, 'formulaire.html', {'resultat': resultat})
    return render(request, 'formulaire.html')