"""Servidor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from ProyectoNFC import viewsets
from rest_framework.urlpatterns import format_suffix_patterns
admin.autodiscover()


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', admin.site.urls),
    url(r'^rest_registro/$', viewsets.RegistroViewSet),
    url(r'^rest_usuario/$', viewsets.UsuarioViewSet),
    url(r'^rest_sala/$', viewsets.SalaViewSet),

]
urlpatterns = format_suffix_patterns(urlpatterns)
