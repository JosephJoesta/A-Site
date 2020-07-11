from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.http import JsonResponse

# Create your models here.
class Comment(models.Model):
	comment_time = models.DateTimeField(auto_now_add=True)

	content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type','object_id')

	text = models.TextField()
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	root_comment = models.ForeignKey('self',null=True,related_name='replys',on_delete=models.CASCADE)
	parent_comment = models.ForeignKey('self',null=True,on_delete=models.CASCADE)                  
	reply_object = models.ForeignKey(User,null=True,related_name='reply_set',on_delete=models.CASCADE)

	def __str__(self):
		return self.text
