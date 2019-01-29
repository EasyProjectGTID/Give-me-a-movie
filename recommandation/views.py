from django.http import HttpResponse
from django.shortcuts import render
from recommandation.models import Series, KeyWords


def index(request):
    return render(request, 'index.html')

def listeSeries(request):
    liste_serie = Series.objects.all()

    return render(request, 'listeSerie.html', {'toto': liste_serie})

def detailSerie(request, id):
    serie = Series.objects.get(id=id)
    #listeDesMots = KeyWords.objects.filter(posting__series=serie.id)

    return render(request, 'detailsSerie.html', {'serie': serie})




