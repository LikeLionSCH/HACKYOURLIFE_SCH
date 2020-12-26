from django.shortcuts import render

# Create your views here.
def gallery_main(request):
    return render(request, "gallerymain.html")

def gallery_board(request):
    return render(request, "th_gallery_board.html")

def gallery_detail(request):
    return render(request, "gallery_board_detail.html")

def gallery_create(request):
    return render(request, "test.html")