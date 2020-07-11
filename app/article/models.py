from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from ..counting.models import *
from django.urls import reverse
# Create your models here.
class ArticleType(models.Model):
	type_name = models.CharField(max_length=12)

	def __str__(self):
		return self.type_name

class Article(models.Model,CountingHelp):
	title = models.CharField(max_length=60)
	content = RichTextField()
	author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='articles')
	article_type = models.ForeignKey(ArticleType,on_delete=models.CASCADE,related_name='articles')
	created_time = models.DateTimeField(auto_now_add=True)
	counting = GenericRelation(CountingDate) 

	def __str__(self):
		return self.title

	def get_path(self):
		return reverse('article_article',kwargs={'<int:article_id>':self.id})