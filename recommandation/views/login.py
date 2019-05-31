from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from recommandation.forms.LoginForm import ConnexionForm
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            if request.COOKIES.get('cookies-state', None) == 'accepted':
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user:
                    token, created = Token.objects.get_or_create(user=user)
                    # Crée le token pour les apps react et l'insert en session
                    request.session['token'] = str(token)

                    login(request, user)
                    return redirect('/')
                else:
                    print(form.errors)
            else:
                messages.add_message(request, messages.INFO, 'Vous devez accepter les notre politiques sur l\'utilisation des cookies pour continuer')

    form = ConnexionForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def logout_user(request):
    logout(request)

    return HttpResponseRedirect('/')

def politique(request):
    return render(request, 'privacy.html')