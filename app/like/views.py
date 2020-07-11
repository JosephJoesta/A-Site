from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from .models import *

# Create your views here.

def SuccessResponse(liked_num):
	data = {}
	data['liked_num'] = liked_num

	data['status'] = 'SUCCESS'
	return JsonResponse(data)

def ErrorResponse(code,message):
	data = {}
	data['code'] = code
	data['message'] = message 

	data['status'] = 'ERROR'
	return JsonResponse(data)

def like_change(request):

	user = request.user
	if not user.is_authenticated:
		return ErrorResponse(400,'you have to login')

	content_type = request.GET.get('content_type')
	content_type = ContentType.objects.get(model=content_type)

	object_id = int(request.GET.get('object_id'))

	try:
		ModelClass = content_type.model_class()
		model_class = ModelClass.objects.get(id=object_id)
	except:
		return ErrorResponse(401,'like object is not existed')

	if request.GET.get('is_liked') == 'true':
		# like

		like_record,created = LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)

		if created:
			# have not liked
			like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
			like_count.liked_num += 1
			like_count.save()
			like_record.save()

			return SuccessResponse(like_count.liked_num)
		else:
			# have liked
			return ErrorResponse(402,'you have liked once')
	else:
		return ErrorResponse(403,'you have liked')