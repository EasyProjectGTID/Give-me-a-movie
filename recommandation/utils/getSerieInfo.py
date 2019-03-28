import requests
from PTUT.settings import API_KEY

def getInfos(modeladmin, request, queryset):

    for serie in queryset:
        URL = 'http://www.omdbapi.com/?apikey=' + API_KEY + '&'
        r = requests.get(URL + 't=' + serie.real_name)
        serie.infos = r.json()
        serie.save()
        print(serie.real_name, r.json())


getInfos.short_description = "Télécharger les informations complémentaires pour les series selectionnées"

