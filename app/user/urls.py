# This is user urls.py 

from .views import *
from django.urls import path,include

urlpatterns = [
	path('',userpage,name='user_info'),
   	path('login/',loginpage,name='login'),
	path('logout/',logoutpage,name="logout"),
	path('register/',registerpage,name='register'),
	path('alertlogin/',alertlogin,name='alertlogin'),
	path('change_nickname/',changenicknamepage,name='change_nickname'),
	path('bind_email/',bindemailpage,name='bind_email'),
	path('send_verification_code/',send_verification_code,name='send_verification_code'),
	path('change_password/',changepasswordpage,name='change_password'),
	path('find_password/',findpasswordpage,name='find_password'),
	path('send_verification_code_s/',send_verification_code_s,name='send_verification_code_s'),
]