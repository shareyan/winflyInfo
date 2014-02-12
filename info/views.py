from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	return render(request,'home.html')

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