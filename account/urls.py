from django.urls import path
from . import views
from django.views.generic.base import TemplateView
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('successful_signup/',TemplateView.as_view(template_name='registration/successful.html'), name='successful_signup')
]