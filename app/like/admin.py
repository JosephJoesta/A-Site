from django.contrib import admin
from .models import *

# Register your models here.
class LikeCountAdmin(admin.ModelAdmin):
	list_display = ('content_type','content_object','liked_num')

class LikeRecordAdmin(admin.ModelAdmin):
	list_display = ('content_object','liked_time','user')

admin.site.register(LikeCount,LikeCountAdmin)
admin.site.register(LikeRecord,LikeRecordAdmin)