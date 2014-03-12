from django.shortcuts import render
from django.http import HttpResponse
import json

templateDir = 'favourite/templates/'
# Create your views here.
def Record(request):
	if 'targetList' not in request.session:
		targetList = []
		request.session['targetList'] = json.dumps([])
	else:
		targetList = json.loads(request.session['targetList'])
	return render(request,templateDir+'favRecord.html',{'targetList':targetList})

def add(request):
	if request.method != 'POST':
		return HttpResponse(json.dumps({'message':'Error','reason':'wrong request method'}),content_type='application/json')
	if 'targetList' not in request.session:
		request.session['targetList'] = json.dumps([])
	targetList = json.loads(request.session['targetList'])
	target = request.POST['target']
	if target not in targetList:
		targetList.append(target)
		request.session['targetList'] = json.dumps(targetList)
	return HttpResponse(json.dumps({'message':'OK'}),content_type='application/json')

def delete(request):
	if request.method != 'POST':
		return HttpResponse(json.dumps({'message':'Error','reason':'wrong request method'}),content_type='application/json')
	if 'targetList' not in request.session:
		request.session['targetList'] = json.dumps([])
	targetList = json.loads(request.session['targetList'])
	target = request.POST['target']
	if target not in targetList:
		return HttpResponse(json.dumps({'message':'Error',reason:'notFound'}),content_type='application/json')
	#del target from targetList
	targetList.remove(target)
	request.session['targetList'] = json.dumps(targetList)
	return HttpResponse(json.dumps({'message':'OK'}),content_type='application/json')
	