from django.contrib.auth.forms import PasswordChangeForm


class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe Actuel'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nouveau Mot de passe'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmer votre mot de passe'})
