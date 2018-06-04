# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
import card
import utils

class CustomUserCreationForm(UserCreationForm):
	"""A form for creating new users. Includes all the required
    fields, plus a repeated password."""
	class Meta(UserCreationForm.Meta):
		model = CustomUser
		fields =  ('email','username')

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		import card
		
		if commit:
			user.save()
			lexicon = card.models.UserLexicon()
			lexicon.user=user
			lexicon.save()
		
		utils.initUserLexicon(lexicon)
		utils.initUserPlan(user)
		return user


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields =UserChangeForm.Meta.fields