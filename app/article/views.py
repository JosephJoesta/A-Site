from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum

from app.comment.forms import *
from app.comment.models import *

from app.user.forms import LoginForm

from .models import *

# Create your views here.
def homepage(request):
	articles = Article.objects.all()
	article_types = ArticleType.objects.all()

	pages = Paginator(articles,10)
	articles = pages.get_page(1)

	date_count = {}
	date_list = Article.objects.dates('created_time','month','DESC')
	for date in date_list:
		related_num = Article.objects.filter(created_time__year=date.year,created_time__month=date.month).count()
		date_count[date] = related_num

	message = {}
	message['articles'] = articles
	message['article_types'] = article_types

	message['date_count'] = date_count

	return render(request,'article/homepage.html',message)

def articlepage(request,article_id):
	article = Article.objects.get(id=article_id)
	content_type = ContentType.objects.get_for_model(Article)
	article.record_num()

	try:
		last_article = Article.objects.filter(id__lt=article_id).last()
	except:
		last_article = None

	try:
		next_article = Article.objects.filter(id__gt=article_id).first()
	except:
		next_article = None

	message = {}
	message['article'] = article
	message['last_article'] = last_article
	message['next_article'] = next_article
	message['login_form'] = LoginForm()

	message['comments'] = Comment.objects.filter(content_type=content_type,object_id=article_id,parent_comment=None).order_by('-comment_time')
	message['comment_form'] = CommentForm(initial={'content_type':'article','object_id':article_id,'reply_id':'0'})
	
	message['article_like'] = 1
	return render(request,'article/articlepage.html',message)

def typepage(request,type_id):
	article_type = get_object_or_404(ArticleType,id=type_id)
	article_types = ArticleType.objects.all()

	date_count = {}
	date_list = Article.objects.dates('created_time','month','DESC')
	for date in date_list:
		related_num = Article.objects.filter(created_time__year=date.year,created_time__month=date.month).count()
		date_count[date] = related_num

	message = {}
	message['article_type'] = article_type
	message['article_types'] = article_types

	message['date_count'] = date_count

	return render(request,'article/typepage.html',message)

def datepage(request,year,month):
	articles = Article.objects.filter(created_time__year=year,created_time__month=month)
	article_types = ArticleType.objects.all()

	pages = Paginator(articles,10)
	articles = pages.get_page(1)

	date_count = {}
	date_list = Article.objects.dates('created_time','month','DESC')
	for date in date_list:
		related_num = Article.objects.filter(created_time__year=date.year,created_time__month=date.month).count()
		date_count[date] = related_num

	message = {}
	message['articles'] = articles
	message['article_types'] = article_types

	message['date_count'] = date_count

	return render(request,'article/datepage.html',message)