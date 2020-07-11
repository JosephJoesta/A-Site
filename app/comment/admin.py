from django.contrib import admin
from .models import *

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
	list_display = ('id','content_object','user','text','comment_time')
	ordering = ('-comment_time',)
admin.site.register(Comment,CommentAdmin)