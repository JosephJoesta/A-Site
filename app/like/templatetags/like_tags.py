from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import *

register = template.Library()

@register.simple_tag
def get_like_num(obj):
	content_type = ContentType.objects.get_for_model(obj)
	like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=obj.id)
	return like_count.liked_num
