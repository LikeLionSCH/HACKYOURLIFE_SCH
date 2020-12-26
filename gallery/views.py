from django.shortcuts import render,redirect
import firebase_admin
import google
from firebase_admin import credentials
from firebase_admin import firestore
from hackyourlife_sch.firebase import initialize_firebase
from .models import Gallery

# Create your views here.
def gallery_main(request):
    return render(request, "gallerymain.html")

def gallery_board(request):
    return render(request, "th_gallery_board.html")

def gallery_detail(request):
    return render(request, "gallery_board_detail.html")


def gallery_create(request):
    if request.method == 'POST':
        # firebase initialize
        db = initialize_firebase()

        contents = request.POST['contents']
        created_at = request.POST['created_at']
        title = request.POST['title']
        image_url = request.POST['image_url']
        place = request.POST['place']

        # 과제 객체 생성
        new_gallery = Gallery(contents, created_at, title, image_url, place)

        # firebase 에 데이터 생성
        db.collection('Gallery').document().set(new_gallery.to_dict())

        # redirect
        return redirect('gallery_board')

    # POST가 아닐 경우 assignment create 페이지 띄움
    return render(request, 'gallery_create.html')

