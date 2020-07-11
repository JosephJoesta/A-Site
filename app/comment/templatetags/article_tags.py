from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import *

register = template.Library()

@register.simple_tag
def test():
	return 0
