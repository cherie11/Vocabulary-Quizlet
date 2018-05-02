from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .forms import LexiconForm, CustomizedLexicon
from .models import Lexicon,Word,CustomizedLexicon,UserWordList,UserLexicon


class LexiconAdmin(UserAdmin):
    model = Lexicon
    add_form = LexiconForm

admin.site.register(Lexicon)
admin.site.register(Word)
admin.site.register(UserWordList)
admin.site.register(UserLexicon)


