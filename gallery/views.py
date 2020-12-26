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


def gallery_detail(request):
    # firebase initialize
    db = initialize_firebase()

    # template 으로 전달해줄 리스트 생성
    galleries = []

    # firebase 에 접근해 과제 목록들 불러옴
    gallery_datas = db.collection('Gallery').stream()

    # 값을 읽어와 하나씩 assignment_list 에 담는다
    for gallery_data in gallery_datas:
        gallery = Gallery.from_dict(gallery_data.to_dict(),gallery_data.id)
        galleries.append(gallery)

    # assignment_list 페이지 띄우고 과제 데이터 전달
    return render(request,'gallery_board_detail.html',{'galleries':galleries})
