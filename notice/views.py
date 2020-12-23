from django.shortcuts import render

# Create your views here.

def notice_list(request):
    return render(request, "notice.html")

def notice_detail(request):
    return render(request, "notice_detail.html")

def faq(request):
    return render(request, "faq.html")