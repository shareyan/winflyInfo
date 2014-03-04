from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from info.models import downloadCount

# Create your views here.
def index(request):
	if downloadCount.objects.count() == 0:
		myCount = 0
	else:
		myCount = downloadCount.objects.all()[0].count
	return render(request,'home.html',{'downloadCount':myCount})

def getStarted(request):
	return render(request,'getStarted.html')

def manual(request):
	return render(request,'manual.html')

def license(request):
	return render(request,'license.html')

def about(request):
	return render(request,'about.html')

def sitemap(request):
	sitemapData = open("sitemap.xml", "rb").read()
	return HttpResponse(sitemapData,content_type='application/xml')

def download(request):
	if downloadCount.objects.count() == 0:
		#no downloadCount record yet
		myCount = downloadCount()
		myCount.count = 1
		myCount.save()
	else:
		myCount = downloadCount.objects.all()[0]
		myCount.count += 1
		myCount.save()
	return HttpResponseRedirect('http://pcloud.shareyan.cn/downloads/latest')