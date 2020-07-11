# this is article urls.py

from django.urls import path
from .views import *

urlpatterns = [
	path('',homepage,name='article_home'),
	path('<int:article_id>/',articlepage,name='article_article'),
	path('type/<int:type_id>',typepage,name='article_type'),
	path("date/<int:year>-<int:month>",datepage,name='article_date'),
]