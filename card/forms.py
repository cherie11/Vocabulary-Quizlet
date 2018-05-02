#-*- coding: utf-8 -*-
from django import forms
from .models import Lexicon,CustomizedLexicon
from django.utils.translation import gettext
from django.core.exceptions import ValidationError
def validate_excel(value):
	if value.name.split('.')[-1] not in ['xls','xlsx']:
		raise ValidationError('Invalid File Type!Must be execel')


class LexiconForm(forms.Form):
	name=forms.CharField(max_length=200)
	lexicon = forms.FileField(validators=[validate_excel])
	class Meta:
   		model=Lexicon
   		fields=('name','lexicon')

class CustomizedLexiconForm(forms.Form):
	words = forms.FileField(validators=[validate_excel])
	class Meta:
   		model=CustomizedLexicon
   		fields=('user','words')


	'''
	def is_valid(self):

		if os.path.splitext(self.data['name'])[-1]!='.xls':
   			raise forms.ValidationError("Wrong Format!")
		return data
	'''
