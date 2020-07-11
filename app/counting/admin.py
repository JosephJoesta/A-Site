from django.contrib import admin
from .models import *

# Register your models here.
class CountingAdmin(admin.ModelAdmin):
	list_display = ('content_type','object_id','content_object','total_num')

class CountingDateAdmin(admin.ModelAdmin):
	list_display = ('content_object','date','total_num')

admin.site.register(Counting,CountingAdmin)
admin.site.register(CountingDate,CountingDateAdmin)