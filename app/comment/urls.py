# This is main urls.py 

from .views import *
from django.urls import path,include

urlpatterns = [
	path('update_comment/',update_comment,name='update_comment'),
]