from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import format

# Create your models here.

class myUser(models.Model):
	user = models.OneToOneField(User,blank=True,null=True)
	type = models.CharField(max_length=20)
	oaId = models.IntegerField()
	
class post(models.Model):
	time = models.DateTimeField(auto_now_add=True, blank=True)
	author = models.ForeignKey(myUser,related_name='postAuthor',blank=True,null=True)
	content = models.TextField()
	viewCount = models.IntegerField(default=0)
	commentNum = models.IntegerField(default=0)
	def getInfo(self):
		info = {}
		info['time'] = format(self.time, 'U')
		if self.author != None:
			info['author'] = {'name':self.author.user.username,'id':self.author.user.pk}
		else:
			info['author'] = {'name':'','id':'None'}
		info['content'] = self.content
		info['viewCount'] = self.viewCount
		info['commentNum'] = self.commentNum
		info['id'] = self.pk
		return info
	
class comment(models.Model):
	post = models.ForeignKey(post,related_name='comment_target')
	time = models.DateTimeField(auto_now_add=True, blank=True)
	content = models.TextField()
	author = models.ForeignKey(myUser,related_name='commentAuthor',null=True,blank=True)
	def getInfo(self):
		info = {}
		info['post'] = self.post.pk
		info['time'] = format(self.time, 'U')
		info['content'] = self.content
		if self.author != None:
			info['author'] = {'name':self.author.user.username,'id':self.author.user.pk}
		else:
			info['author'] = {'name':'','id':'None'}
		info['id'] = self.pk
		return info