from django.shortcuts import render

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