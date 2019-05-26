from django import forms


class ProfilForm(forms.Form):
	"""
	Pour la page de login
	"""
	username = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Compte utilisateur'}))

	email = forms.EmailField(
		widget=forms.TextInput(attrs={'class': "form-control", 'type': "text", 'placeholder': "Email"}))



