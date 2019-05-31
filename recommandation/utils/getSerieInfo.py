import requests
from django.conf.global_settings import STATIC_ROOT

from PTUT.settings import API_KEY, STATICFILES_DIRS, STATIC_URL


def getInfos(modeladmin, request, queryset):

    for serie in queryset:
        URL = 'http://www.omdbapi.com/?apikey=' + API_KEY + '&'
        r = requests.get(URL + 't=' + serie.real_name)
        serie.infos = r.json()
        serie.save()


        response = requests.get(serie.infos['Poster'])

        if response.status_code == 200:
            with open(STATIC_ROOT + 'posters/' + str(serie.name) + '.jpeg', 'wb') as f:
                f.write(response.content)
        serie.image_local = STATIC_URL + 'posters/' + str(serie.name) + '.jpeg'
        serie.save()



getInfos.short_description = "Télécharger les informations complémentaires pour les series selectionnées"

