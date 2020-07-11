from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from .forms import *
from .models import *
import json
 
 
def default(obj):
	if isinstance(obj,bytes):
		return str(obj, encoding='utf-8')
	return obj

def update_comment(request):
	data = {}
	message = {}
	wrong = False
	referer = request.META.get('HTTP_REFERER')

	if request.POST.get('text').strip():
		text = request.POST.get('text').strip()
	else:
		message['wrong'] = '评论不能为空'
		wrong = True

	try:
		content_type = ContentType.objects.get(model=request.POST.get('content_type')).model_class()
		content_object = content_type.objects.get(id=request.POST.get('object_id'))
	except:
		wrong = True
		message['wrong'] = '评论对象不存在'

	if request.user.is_authenticated:
		user = request.user
	else:
		wrong = True
		message['wrong'] = '你还未登陆'

	if wrong:
		data['status'] = 'ERROR'
		data['error'] = list(comment_form.errors.values())[0][0]
	else:
		comment = Comment()
		comment.user = user


		try:
			comment.parent_comment = Comment.objects.get(id=request.POST.get('reply_id'))
			comment.reply_object = comment.parent_comment.user
				
			if comment.parent_comment.root_comment == None:
				comment.root_comment = comment.parent_comment
			else:
				comment.root_comment = comment.parent_comment.root_comment
		except:
			comment.parent_comment = None
			comment.root_comment = None
			comment.reply_object = None 

		comment.text = text
		comment.content_object = content_object
		comment.save()

		data['status'] = 'SUCCESS'
		data['username'] = default(comment.user.profile.nickname) 
		data['comment_time'] = default(comment.comment_time)
		data['text'] = default(comment.text)
		
		try:
			data['parent_id'] = comment.parent_comment.id
			data['reply_user'] = comment.reply_object.username
		except:
			data['parent_id'] = 0
			data['reply_user'] = None

		data['id'] = comment.id

		if request.POST.get('content_type') == 'article':
			if content_object.author.email != '':
				path = content_object.get_path
				email = content_object.author.email
				send_mail(
					'有人评论你的文章',
					'有人评论你的文章\n%s' % path,
					'70055052@qq.com',
					[email],
					fail_silently=False,
				)
		else:
			if comment.reply_object.email != '':
				path = content_object.root_comment.reply_object.get_path()
				email = content_object.author.email
				send_mail(
					'有人回复你的评论',
					'有人回复你的评论\n%s' % path,
					'70055052@qq.com',
					[email],
					fail_silently=False,
				)
	return JsonResponse(data)