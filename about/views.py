from django.shortcuts import render

# Create your views here.

def about(request):
    return render(request, "about.html")

def history(request):
    return render(request, "history.html")

def staff(request):
    return render(request, "staff.html")