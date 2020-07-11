import re

from .models import *
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
#448p

class LoginForm(forms.Form):
	username = forms.CharField(label='用户名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))
	password = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))
	def clean(self,request):
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = auth.authenticate(username=username,password=password)
		if user == None:
			return False,None

		return True,user

class RegisterForm(forms.Form):
	nickname = forms.CharField(max_length=15,label='昵称',widget=forms.TextInput(attrs={'onKeypress':'javascript:if(event.keyCode == 32)event.returnValue = false;','value':'','class':'form-control','placeholder':'请输入昵称(最多15位)'}))
	username = forms.CharField(min_length=6,max_length=25,label='用户名',widget=forms.TextInput(attrs={'onKeypress':'javascript:if(event.keyCode == 32)event.returnValue = false;','value':'','class':'form-control','placeholder':'请输入用户名(6-25位)'}))                  
	password = forms.CharField(min_length=6,label='密码',widget=forms.PasswordInput(attrs={'value':'','class':'form-control','placeholder':'请输入密码(最少6位)'}))
	password_again = forms.CharField(label='确认密码',widget=forms.PasswordInput(attrs={'value':'','class':'form-control','placeholder':'请再次输入密码'}))

	def clean(self,request):
		register_data = {}
		is_passed,nickname,wrong = self.clean_nickname(request)
		if is_passed == False:
			return False,wrong,None
		register_data['nickname'] = nickname

		is_passed,username,wrong = self.clean_username(request)
		if is_passed == False:
			return False,wrong,None
		register_data['username'] = username

		is_passed,password,wrong = self.clean_password(request)
		if is_passed == False:
			return False,wrong,None
		register_data['password'] = password

		return True,None,register_data
	def clean_nickname(self,request):
		nickname = request.POST.get('nickname')
		nickname_re = r'\s'
		if len(nickname) > 15:
			wrong = '昵称过长'
			return False,None,wrong

		if re.search(nickname_re,nickname) != None:
			wrong = '昵称不能存在空格'
			return False,None,wrong

		if Profile.objects.filter(nickname=nickname).exists():
			wrong = '昵称已存在'
			return False,None,wrong
		return True,nickname,None

	def clean_username(self,request):
		username = request.POST.get('username')
		username_re = r'[^0-9a-zA-Z]'
		if len(username) < 6 or len(username) > 25:
			wrong = '用户名不符规范'
			return False,None,wrong

		if re.search(username_re,username) != None:
			wrong = '用户名只能有字母和数字'
			return False,None,wrong

		if User.objects.filter(username=username).exists():
			wrong = '用户名已存在'
			return False,None,wrong
		return True,username,None

	def clean_password(self,request):
		password = request.POST.get('password')
		password_again = request.POST.get('password_again')

		if len(password) < 6:
			wrong = '密码不符规范'
			return False,None,wrong
		if password != password_again:
			print(password)
			print(password_again)
			wrong = '密码不一致'
			return False,None,wrong
		return True,password,None

class ChangeNickNameForm(forms.Form):
	new_nickname = forms.CharField(max_length=15,label='新昵称',widget=forms.TextInput(attrs={'value':'','class':'form-control','placeholder':'请输入新昵称'}))

class BindEmailForm(forms.Form):
	email = forms.CharField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}))
	verification_code = forms.CharField(label='验证码',required=False,max_length=6,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入验证码'}))

	def clean(self,request):
		print(request.POST)
		email = self.clean_email(request.session.get('email'))
		verification_code = self.clean_verification_code(request.POST.get('verification_code',''))
		if email==False:
			return False,'邮箱已经被绑定'
		if verification_code==False:
			return False,'验证码不能为空'
		try:
			int(verification_code)
		except:
			return False,'验证码不正确'

		if int(verification_code) != int(request.session.get('bind_email_code')):
			print(verification_code)
			print(request.session.get('bind_email_code'))
			return False,'验证码不正确'
		return True,email

	def clean_email(self,email):
		if User.objects.filter(email=email).exists() and email != '' :
			print(User.objects.filter(email=email))
			return False
		return email

	def clean_verification_code(self,verification_code):
		if verification_code == '':
			return False
		return verification_code

class ChangePasswordForm(forms.Form):
	old_password = forms.CharField(label='旧密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))
	new_password = forms.CharField(label='新密码',min_length=6,widget=forms.PasswordInput(attrs={'value':'','class':'form-control','placeholder':'请输入密码(最少6位)'}))
	new_password_again = forms.CharField(label='确认密码',widget=forms.PasswordInput(attrs={'value':'','class':'form-control','placeholder':'请再次输入密码'}))

	def clean(self,request):

		is_passed,password,wrong = self.clean_password(request)
		if is_passed == False:
			return False,wrong,None

		return True,None,password

	def clean_password(self,request):
		old_password = request.POST.get('old_password')
		new_password = request.POST.get('new_password')
		new_password_again = request.POST.get('new_password_again')

		if request.user.check_password(old_password):
			if len(new_password) < 6:
				wrong = '密码不符规范'
				return False,None,wrong
			if new_password != new_password_again:
				wrong = '密码不一致'
				return False,None,wrong
			return True,new_password,None
		else:
			wrong = '旧密码不正确'
			return False,None,wrong

class FindPasswordForm(forms.Form):
	email = forms.CharField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}))
	verification_code = forms.CharField(label='验证码',required=False,max_length=6,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入验证码'}))
	def clean(self,request):
		email = request.session.get('email')
		verification_code = request.POST.get('verification_code','')
		try:
			int(verification_code)
		except:
			return False,'验证码不正确',email

		if int(verification_code) != int(request.session.get('bind_email_code')):
			print(verification_code)
			print(request.session.get('bind_email_code'))
			return False,'验证码不正确',email
		return True,None,email