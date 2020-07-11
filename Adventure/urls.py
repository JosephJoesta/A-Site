# This is main urls.py 

from django.contrib import admin
from django.urls import path,include
from app.user.views import *
from .views import *

urlpatterns = [
	path('',homepage,name='home'),
    path('admin/',admin.site.urls,name='admin'),

	path('user/',include('app.user.urls')),
	path('article/',include('app.article.urls')),
	path('comment/',include('app.comment.urls')),
	path('like/',include('app.like.urls')),
]