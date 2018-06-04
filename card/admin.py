from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .forms import LexiconForm, CustomizedLexicon
from .models import Lexicon,Word,CustomizedLexicon,CustomizedLexicon,UserLexicon,UserPlan


class LexiconAdmin(UserAdmin):
    model = Lexicon
    add_form = LexiconForm

#admin.site.register(Lexicon)
admin.site.register(Word)
admin.site.register(CustomizedLexicon)
admin.site.register(UserLexicon)

admin.site.register(UserPlan)


