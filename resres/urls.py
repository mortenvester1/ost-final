"""resres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/{{ docs_version }}/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^DEVprint', views.DEVprint, name = 'DEVprint'),
    url(r'^signup', views.signup, name = 'signup'),
    url(r'^userlogin', views.userlogin, name = 'userlogin'),
    url(r'^userlogout', views.userlogout, name = 'userlogout'),
    url(r'^userpage', views.userpage, name = 'userpage'),
    url(r'^createresource',views.createresource, name = 'createresource'),
    url(r'^viewresource',views.viewresource, name = 'viewresource'),
    url(r'^viewresource(?P<rid>[0-9]+)$',views.viewresource),
    url(r'^viewtags',views.viewtags, name = 'viewtags'),
    url(r'^admin/', admin.site.urls),
]
