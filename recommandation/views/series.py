from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from recommandation.models import Series, KeyWords, Posting

@login_required(login_url='/login')
def listeSeries(request):
    liste_serie = Series.objects.all()

    return render(request, 'listeSerie.html', {'toto': liste_serie})

def detailSerie(request, id):
    serie = Series.objects.get(id=id)
    listeDesMots = Posting.objects.filter(series=id).select_related('keywords')
    return render(request, 'detailsSerie.html', {'serie': serie, 'listeDesMots':listeDesMots})



