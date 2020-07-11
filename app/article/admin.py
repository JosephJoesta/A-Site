from django.contrib import admin
from .models import *

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title','created_time','article_type','display_num')
	ordering = ('-created_time',)

class ArticleTypeAdmin(admin.ModelAdmin):
	list_display = ('id','type_name')
	ordering = ('id',)

admin.site.register(Article,ArticleAdmin)
admin.site.register(ArticleType,ArticleTypeAdmin)