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
'''
class CustomizedLexiconForm(forms.Form):
	words = forms.FileField(validators=[validate_excel])
	class Meta:
   		model=CustomizedLexicon
   		fields=('user','words')
'''

class CustomizedWordForm(forms.Form):
	new_word=forms.CharField(label='输入单词',max_length=50,required=True) 
	new_meaning=forms.CharField(label='含义',max_length=200,required=True)
	new_phonetic=forms.CharField(label='音标',max_length=100,required=True)





