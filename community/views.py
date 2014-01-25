from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from community.models import myUser,post,comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import time

# Create your views here.
templateDir = 'community/templates/'

def loginUser(request):
	if request.method != 'POST':
		return HttpResponse(json.dumps({'message':'Error','reason':'wrong request method'}),content_type='application/json')
	logout(request)
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user != None:
		login(request, user)
		return HttpResponse(json.dumps({'message':'OK','user':{'name':user.username,'id':user.pk}}),content_type='application/json')
	else:
		return HttpResponse(json.dumps({'message':'Error','reason':'error'}),content_type='application/json')
	
def register(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		if len(User.objects.filter(username=username)) != 0:
			return HttpResponse(json.dumps({'message':'Error','reason':'nameRepeat'}),content_type='application/json')
		user = User.objects.create_user(username, "%.0f"%time.time()+'@test.com', password)
		comUser = myUser()
		comUser.user = user
		comUser.type = 'local'
		comUser.oaId = 0
		comUser.save()
		userInfo = {};
		userInfo['name'] = comUser.user.username
		userInfo['id'] = comUser.user.pk
		return HttpResponse(json.dumps({'message':'OK','user':userInfo}),content_type='application/json')
	else:
		return HttpResponse(json.dumps({'message':'Error','reason':'wrong request method'}))
	
	
def community(request):
	#get latest posts
	res = getLatestPost(0,0)
	return render(request,templateDir +'community.html',
			   {'postList':res['postList'],
				'totalNum':res['totalNum'],
				})

def getPost(request):
	beginId = request.POST['beginId']
	endId = request.POST['endId']
	res = getLatestPost(beginId,endId)
	res['message'] = 'OK'
	return HttpResponse(json.dumps(res),content_type='application/json')

	
def newPost(request):
	if request.method != "POST":
		return HttpResponse(json.dumps({'message':'Error','reason':'wrong request method'}),content_type='application/json')
	content = request.POST['content']
	topic = request.POST['topic']
	myPost = post()
	if request.user.is_authenticated():
		comUser = myUser.objects.get(user=request.user)
		myPost.author = comUser
	myPost.content = json.dumps({'topic':topic,'content':content})
	myPost.save()
	return HttpResponse(json.dumps({'message':'OK','newPost':myPost.getInfo()}),content_type='application/json')


def getLatestPost(beginId,endId):
	totalPost = post.objects.all().order_by('-time')
	totalNum = totalPost.count()
	if beginId == 0 and endId == 0:
		postList = []
		newPostList = []
		targetList = totalPost[:10]
		for mypost in targetList:
			postList.append(mypost.getInfo())
		return {'postList':postList,'newPostList':newPostList,'totalNum':totalNum}
	beginPost = post.objects.get(pk=beginId)
	endPost = post.objects.get(pk=endId)
	targetNewPost = totalPost.filter(time__gt=beginPost.time)
	targetOldPost = totalPost.filter(time__lt=endPost.time)
	postList = []
	newPostList = []
	for mypost in targetNewPost:
		newPostList.append(mypost.getInfo())
	for mypost in targetOldPost:
		postList.append(mypost.getInfo())
	return {'postList':postList,'newPostList':newPostList,'totalNum':totalNum}

def getPageList(totalNum,pageNum,pageItemsNum=10):
	totalNum = int(totalNum)
	pageNum = int(pageNum)
	pageItemsNum = int(pageItemsNum)
	if totalNum%pageItemsNum == 0:
		totalPageNum = totalNum/pageItemsNum
	else:
		totalPageNum = totalNum/pageItemsNum + 1
	pageList = []
	if totalPageNum <= (9+pageNum):
		if totalPageNum<10:
			pageList = range(1,totalPageNum+1)
		else:
			pageList = range(totalPageNum-10,totalPageNum+1)
	else:
		pageList = range(pageNum-1-(pageNum-1)%10+1,pageNum-1-(pageNum-1)%10+1+10)
	startNum = (pageNum-1)*pageItemsNum
	endNum = pageNum*pageItemsNum
	return {'pageList':pageList,'startNum':startNum,'endNum':endNum,'totalPageNum':totalPageNum}


def sendComment(request):
	if request.method != "POST":
		return HttpResponse(json.dumps({'message':'Error','reason':'wrong request method'}),content_type='application/json')
	content = request.POST['content']
	targetId = request.POST['target']
	targetPost = post.objects.filter(pk=targetId)
	if len(targetPost) == 0:
		return HttpResponse(json.dumps({'message':'Error','reason':'target post not exist'}),content_type='application/json')
	targetPost = targetPost[0]
	newComment = comment()
	newComment.post = targetPost
	targetPost.commentNum += 1
	targetPost.save()
	newComment.content = content
	if request.user.is_authenticated():
		newComment.author = myUser.objects.get(user=request.user)
	newComment.save()
	return HttpResponse(json.dumps({'message':'OK'}),content_type='application/json')

def getComments(request):
	if request.method != 'POST':
		return HttpResponse(json.dumps({'message':'Error','reason':'wrong request method'}),content_type='application/json')
	beginId = int(request.POST['beginId'])
	endId = int(request.POST['endId'])
	targetId = request.POST['target']
	targetPost = post.objects.filter(pk=targetId)
	if len(targetPost) == 0:
		return HttpResponse(json.dumps({'message':'Error','reason':'target post not exist'}),content_type='application/json')
	targetPost = targetPost[0]
	if beginId == 0 and endId == 0:
		targetPost.viewCount += 1
		targetPost.save()
	res = getLatestComments(beginId,endId,targetPost)
	print res
	return HttpResponse(json.dumps({'message':'OK','commentList':res['commentList'],'totalNum':res['totalNum'],'newCommentList':res['newCommentList'],}),content_type='application/json')
	
	
	
def getLatestComments(beginId,endId,post):
	beginId = int(beginId)
	endId = int(endId)	
	totalComments = comment.objects.filter(post=post).order_by('-time')
	totalNum = totalComments.count()
	if beginId == 0 and endId == 0:
		commentList = []
		newComment = []
		targetList = totalComments[:10]
		for mycomment in targetList:
			commentList.append(mycomment.getInfo())
		return {'commentList':commentList,'newCommentList':newComment,'totalNum':totalNum}
	#get the latest news
	beginComment = comment.objects.get(pk=beginId)
	endComment = comment.objects.get(pk=endId)
	targetNewComment = totalComments.filter(time__gt=beginComment.time)
	targetOldComment = totalComments.filter(time__lt=endComment.time)[:10]
	commentList = []
	newComment = []
	for mycomment in targetNewComment:
		newComment.append(mycomment.getInfo())
	for mycomment in targetOldComment:
		commentList.append(mycomment.getInfo())
	res = {}
	res['commentList'] = commentList
	res['newCommentList'] = newComment
	res['totalNum'] = totalNum
	return res

@csrf_exempt
def logoutUser(request):
	if request.method != "POST":
		return HttpResponse(json.dumps({'message':'Error','reason':'wrong request method'}),content_type='application/json')
	logout(request)
	return HttpResponse(json.dumps({'message':'OK'}),content_type='application/json')