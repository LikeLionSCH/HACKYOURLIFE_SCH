from django.shortcuts import render

# Create your views here.

def study(request):
    return render(request, "study.html")

def hackathon(request):
    return render(request, "hackathon.html")

def ideathon(request):
    return render(request, "ideathon.html")

def etc(request):
    return render(request, "etc.html")