import time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from recommandation.models import Series, Posting, KeyWords



def index(request):
    return HttpResponse('coucou')


