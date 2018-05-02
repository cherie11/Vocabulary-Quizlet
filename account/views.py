from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('successful_signup')
    template_name = 'registration/signup.html'