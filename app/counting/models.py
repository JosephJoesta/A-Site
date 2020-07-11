from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Counting(models.Model):
	content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type','object_id')

	total_num = models.IntegerField(default=0)

class CountingDate(models.Model):
	content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type','object_id')

	date = models.DateField(default=timezone.now)
	total_num = models.IntegerField(default=0)

class CountingHelp():
	def record_num(self):

		content_type = ContentType.objects.get_for_model(self)

		counting,is_created = CountingDate.objects.get_or_create(date=timezone.now().date(),content_type=content_type,object_id=self.id)
		counting.total_num += 1
		counting.save()

		counting,is_created = Counting.objects.get_or_create(content_type=content_type,object_id=self.id)
		counting.total_num += 1
		counting.save()

		return counting.total_num

	def display_num(self):
		try:
			content_type = ContentType.objects.get_for_model(self)
			counting = Counting.objects.get(content_type=content_type,object_id=self.id)
		except:
			num = 0
		else:
			num = counting.total_num
		return num