from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from recommandation.forms.LoginForm import ConnexionForm
from recommandation.forms.RegisterForm import RegisterForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form
            user.username = form.cleaned_data["username"]
            user.password = form.cleaned_data["password1"]
            user.email = form.cleaned_data["email"]
            user.save()
            login(request, user)

        else:
            messages.add_message(request, messages.INFO, form.errors)

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def passwordRecovery(request):
    return render(request, 'password-recovery.html')