import datetime
from django.utils import timezone
from django.db.models import Sum
from .models import * 
from app.article.models import *

def get_late_seven_days_num(content_type):
	today = timezone.now().date()
	each_num = []
	each_date = []
	for delta in range(6,-1,-1):
		date = today - datetime.timedelta(days=delta)
		each_date.append(date.strftime('%m/%d'))

		date_objects = CountingDate.objects.filter(content_type=content_type,date=date)
		total_num = date_objects.aggregate(Sum('total_num'))

		each_num.append(total_num['total_num__sum'] or 0)

	return each_date,each_num

def get_num_ranking_yesterday(content_type):
	today = timezone.now().date()
	yesterday = today - datetime.timedelta(days=1)
	article_ranking = CountingDate.objects.filter(content_type=content_type,date=yesterday).order_by('-total_num')

	return article_ranking

def get_num_ranking_weekly(content_type):
	today = timezone.now().date()
	seven_day = today - datetime.timedelta(days=7)
	article_ranking = Article.objects.filter(counting__date__gt=seven_day).values('id','title').annotate(total_num = Sum('counting__total_num')).order_by('-total_num')

	return article_ranking