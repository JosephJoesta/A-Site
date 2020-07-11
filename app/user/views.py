from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from random import randint

from .forms import * 
from .models import *
#https://v.huya.com/play/349553732.html
def userpage(request):
	return render(request,'user/user_info.html')

def alertlogin(request):
	data = {}
	login_form = LoginForm(request.POST)
	login_form.is_valid()
	is_valid,login_form = login_form.authenticate(request)
	print(is_valid,login_form)
	if is_valid:
		data['status'] = 'SUCCESS'

		user = login_form['user']
		auth.login(request,user)
	else:
		data['status'] = 'ERROR'
	return JsonResponse(data)

def loginpage(request):
	path = request.META.get('HTTP_REFERER')
	if not request.user.is_authenticated:
		if request.method == 'POST':
			login_form = LoginForm(request.POST)

			is_valid,user = login_form.clean(request)
			if is_valid:
				auth.login(request,user)

				data = {}
				data['status'] = 'SUCCESS'
				return JsonResponse(data)

			data = {}
			data['wrong'] = '用户名或密码错误'
			data['status'] = 'ERROR'
			return JsonResponse(data)
		else:
			login_form = LoginForm()

		message = {}
		message['login_form'] = login_form
		return render(request,'user/login.html',message)
	else:
		return redirect(reverse('user_info'))

def logoutpage(request):
	path = request.META.get('HTTP_REFERER')
	print(request.user.is_authenticated)
	if request.user.is_authenticated:
		logout(request)

		return redirect(path,request.GET.get(path,reverse('home')))
	else:
		return redirect(request.GET.get(path,reverse('home')))


def registerpage(request):
	if not request.user.is_authenticated:
		path = request.META.get('HTTP_REFERER')
		if request.method == 'POST':
			print(request.POST)

			register_form = RegisterForm()
			is_passed,wrong,register_data = register_form.clean(request)
			if is_passed:
				user = User()
				user.username = register_data['username']
				user.set_password(register_data['password'])
				user.save()

				user = auth.authenticate(username=register_data['username'],password=register_data['password'])
				auth.login(request,user)

				profile = Profile()
				profile.user = user
				profile.nickname = register_data['nickname']
				profile.save()

				data = {}
				data['status'] = 'SUCCESS'
				return JsonResponse(data)
			else:
				data = {}
				data['status'] = 'ERROR'
				data['wrong'] = wrong
				return JsonResponse(data)

		else:
			register_form = RegisterForm()

		message = {}
		message['register_form'] = register_form
		return render(request,'user/register.html',message)
	else:
		return redirect(reverse('home'))

def changenicknamepage(request):
	if request.user.is_authenticated:
		# 已登陆
		message  = {}
		path = request.META.get('HTTP_REFERER')
		if request.method == 'POST':	
			# POST
			nickname = request.POST.get('new_nickname')
			profile = request.user.profile

			nickname,is_passed = profile.nickname_checkout(nickname)
			if is_passed:
				# passed
				profile.nickname = nickname
				profile.save()

				return redirect(reverse('user_info'))
			else:
				# failed
				message['wrong'] = nickname

		# GET
		message['page_title'] = '用户|修改昵称'
		message['panel_title'] = '修改昵称'
		message['form'] = ChangeNickNameForm()
		message['submit_text'] = '修改'

		return render(request,'form.html',message)

	else:
		return redirect(reverse('home'))

def bindemailpage(request):
	if request.user.is_authenticated and request.user.email == '':
		# 已登陆
		message  = {}
		path = request.META.get('HTTP_REFERER')
		if request.method == 'POST':	
			# POST
			form = BindEmailForm(request.POST)
			if form.is_valid:
				email = request.POST.get('email')
				verification_code = request.POST.get('verification_code')
				is_passed,email = form.clean(request)
				if is_passed:

					request.user.email = email
					request.user.save()

					data = {}
					data['STATUS'] = 'SUCCESS'
					return JsonResponse(data)
				else:
					data = {}
					data['status'] = 'ERROR'
					data['wrong'] = email
					return JsonResponse(data)
		else:
			# GET
			message['page_title'] = '用户|绑定邮箱'
			message['panel_title'] = '绑定邮箱'
			message['form'] = BindEmailForm()
			message['submit_text'] = '绑定'

			return render(request,'user/bind_email.html',message)
	else:
		return redirect(reverse('home'))

def send_verification_code(request):
	email = request.GET.get('email','')
	data = {}

	verification_code = randint(100000,999999)
	print(verification_code)
	request.session['bind_email_code'] = verification_code
	request.session['email'] = email
	send_mail(
		'绑定邮箱',
		'验证码：%s' % verification_code,
		'70055052@qq.com',
		[email],
		fail_silently=False,
	)
	data['status'] = 'SUCCESS'
	return JsonResponse(data)

def changepasswordpage(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = ChangePasswordForm()
			is_passed,wrong,password = form.clean(request)
			if is_passed:
				request.user.set_password(password)
				request.user.save()

				auth.login(request,request.user)

				data = {}
				data['STATUS'] = 'SUCCESS'
				return JsonResponse(data)
			else:
				data = {}
				data['status'] = 'ERROR'
				data['wrong'] = wrong
				return JsonResponse(data)			
		else:
			# GET
			data = {}

			data['page_title'] = '用户|修改密码'
			data['panel_title'] = '修改密码'
			data['form'] = ChangePasswordForm()
			data['submit_text'] = '修改'

			return render(request,'user/change_password.html',data)
	else:
		return redirect(reverse('home'))

def findpasswordpage(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			data = {}
			form = FindPasswordForm()
			is_passed,wrong,email = form.clean(request)
			if is_passed:
				user = User.objects.get(email=email)
				password = str(randint(1000000,9999999))
				user.set_password(password)
				user.save()

				data['status'] = 'SUCCESS'
				data['wrong'] = '密码已经重置: ' + password
			else:
				data['status'] = 'ERROR'
				data['wrong'] = wrong
			return JsonResponse(data)
		else:
			data = {}

			data['page_title'] = '用户|重置密码'
			data['panel_title'] = '重置密码'
			data['form'] = FindPasswordForm()
			data['submit_text'] = '提交'
			return render(request,'user/find_password.html',data)
	else:
		return redirect(reverse('user_info'))

def send_verification_code_s(request):
	email = request.GET.get('email','')
	data = {}
	print(User.objects.filter(email=email))
	if User.objects.filter(email=email).exists() != 0:
		verification_code = randint(100000,999999)
		print(verification_code)
		request.session['bind_email_code'] = verification_code
		request.session['email'] = email
		send_mail(
			'绑定邮箱',
			'验证码：%s' % verification_code,
			'70055052@qq.com',
			[email],
			fail_silently=False,
		)
		data['status'] = 'SUCCESS'
	else:
		data['status'] = 'ERROR'
	return JsonResponse(data)