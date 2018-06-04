"""vocabulary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.views.generic.base import TemplateView
from card.views import addCustomizeWord,listCustomizeWord,deleteCustomizeWord,setPlan
#import auth
urlpatterns = [

    path('admin/', admin.site.urls),
   
    path('l_cust_word/', listCustomizeWord, name='list_all'),
    
    path('delete/<slug:slug>/', deleteCustomizeWord, name='delete'),
    #path('main/',addCustomizeWord, name='add_own'),
    path('main/',setPlan,name='home'),

    #path('',UploadWordsView.as_view(), name='home'),
    path('', TemplateView.as_view(template_name='home.html'), name='main'),

    #path(r'^uplaod/',UploadWords , name = 'upload'),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('account.urls')),
    re_path(r'^card/',include('card.urls')),
    


]
