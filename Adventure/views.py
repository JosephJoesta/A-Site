from django.shortcuts import render,redirect
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType 
from app.counting.tool import *
from app.article.models import *

def homepage(request):
	content_type = ContentType.objects.get_for_model(Article)
	each_date,each_num = get_late_seven_days_num(content_type)

	six = each_num[5]
	seven = each_num[6]

	try:
		if seven > six:
			percent = format(100-(six/seven*100),'.4f')
		else:
			percent = format(100-(seven/six*100),'.4f')
	except:
		percent = 0.00

	article_ranking_weekly = cache.get('article_ranking_weekly')
	if article_ranking_weekly:
		pass
	else:
		article_ranking_weekly = get_num_ranking_weekly(content_type)
		cache.set('article_ranking_weekly',article_ranking_weekly,60)

	message = {}
	message['six'] = six
	message['seven'] = seven
	message['percent'] = percent
	message['each_date'] = each_date
	message['each_num'] = each_num
	message['article_ranking'] = get_num_ranking_yesterday(content_type)
	message['article_ranking_weekly'] = article_ranking_weekly

	return render(request,'homepage.html',message)
