from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView





class Profile(TemplateView):
    def get(self, request):


        return (redirect('/'))
