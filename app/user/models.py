from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User,default=None,on_delete=models.CASCADE,related_name='profile',verbose_name='昵称')
	nickname = models.CharField(max_length=15,default=None)

	def __str__(self):
		return '<Profile: %s for %s >' % (self.nickname,self.user)

	def nickname_checkout(self,nickname):
		nickname = nickname.strip()
		if len(nickname) > 15:
			wrong = '昵称过长'
			return wrong,False

		if nickname == '':
			wrong = '昵称不能为空'
			return wrong,False
		else:
			if Profile.objects.filter(nickname=nickname).exists():
				wrong = '昵称已存在'
				return wrong,False
		return nickname,True