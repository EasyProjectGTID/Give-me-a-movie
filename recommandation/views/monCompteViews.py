from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from recommandation.forms.PasswordChangeCustomForm import PasswordChangeCustomForm
from recommandation.forms.profileForm import ProfilForm

@login_required()
def profile(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = ProfilForm(request.POST)
        user.username = form['username']
        user.email = form['email']
        user
    else:

        form = ProfilForm(initial={'username':user.username,
                               'email':user.email,
                               })
    return render(request, 'editerProfile.html', {'form':form})


class ChangePassword(TemplateView):
    """
    Vue permettant le changement de mot de passe
    """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    def get(self, *args, **kwargs):
        passwordForm = PasswordChangeCustomForm(self.request.user)

        context = {'form': passwordForm}
        return render(self.request, 'changePassword.html', context)

    def post(self, request):
        passwordForm = PasswordChangeCustomForm(request.user, request.POST)
        if passwordForm.is_valid():
            passwordForm.save()
            update_session_auth_hash(request, passwordForm.user)
            messages.success(request, 'Votre mot de passe à été mis à jour !')
            return redirect('/profil')
        else:

            messages.error(request, passwordForm.errors)
            return (redirect('/profil/password'))
