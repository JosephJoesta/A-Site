# This is like urls.py 

from .views import *
from django.urls import path,include

urlpatterns = [
	path('like_change/',like_change,name='like_change'),
]