import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class RegisterForm(UserCreationForm):
	"""
	Formulaire permettant à un particulier de s'inscrire
	"""

	username = forms.RegexField(
		regex=r"^[^`~!#$%^&*()={}\[\]|\\:;“’<,>?๐฿]*$",
		widget=forms.TextInput(
			attrs={
				"class": "form-control",
				"type": "text",
				"placeholder": "Nom utilisateur",
			}
		),
	)



	email = forms.EmailField(
		max_length=250,
		widget=forms.TextInput(
			attrs={"class": "form-control", "type": "text", "placeholder": "Email"}
		),
	)
	password1 = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				"class": "form-control",
				"type": "password",
				"placeholder": "Mot de passe",
			}
		)
	)

	password2 = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				"class": "form-control",
				"type": "password",
				"placeholder": "Confirmer votre mot de passe",
			}
		)
	)


	class Meta:
		model = User

		fields = ("username", "password1", "password2", "email")
