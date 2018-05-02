from django.urls import path,re_path
from . import views

from django.views.generic.base import TemplateView
urlpatterns = [
    #path('<int:pk>',TemplateView.as_view(template_name='flashcard/card.html'), name='card'),
    path('',TemplateView.as_view(template_name='flashcard/card.html'), name='card'),
    path('<slug:slug>/<int:known>/',views.detail,name="lexicon"),
    path('quiz/<slug:slug>/<int:id>/',views.take_quiz,name="quiz"),
]