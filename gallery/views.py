from django.shortcuts import render,redirect
import firebase_admin
import google
from firebase_admin import credentials
from firebase_admin import firestore
from hackyourlife_sch.firebase import FirestoreControlView
from .models import Gallery


def gallery_main(request):
    return render(request, "gallerymain.html")


def gallery_board(request):
    return render(request, "th_gallery_board.html")


@FirestoreControlView
def gallery_create(request,db):
    if request.method == 'POST':
        contents = request.POST['contents']
        created_at = request.POST['created_at']
        title = request.POST['title']
        image_url = request.POST['image_url']
        place = request.POST['place']
        ordinal_num = request.POST['ordinal_num']
        event = request.POST['event']

        new_gallery = Gallery(contents, created_at, title, image_url, place, ordinal_num, event)

        db.collection('Gallery').document().set(new_gallery.to_dict())

        return redirect('gallery_board')

    return render(request, 'gallery_create.html')


@FirestoreControlView
def gallery_idea_detail(request, db):
    galleries = []

    gallery_datas = db.collection('Gallery').stream()

    for gallery_data in gallery_datas:
        gallery = Gallery.from_dict(gallery_data.to_dict(),gallery_data.id)
        galleries.append(gallery)

    return render(request,'gallery_idea_detail.html',{'galleries':galleries})


@FirestoreControlView
def gallery_hacka_detail(request, db):
    galleries = []

    gallery_datas = db.collection('Gallery').stream()

    for gallery_data in gallery_datas:
        gallery = Gallery.from_dict(gallery_data.to_dict(),gallery_data.id)
        galleries.append(gallery)

    return render(request,'gallery_hacka_detail.html',{'galleries':galleries})


@FirestoreControlView
def gallery_session_detail(request, db):
    galleries = []

    gallery_datas = db.collection('Gallery').stream()

    for gallery_data in gallery_datas:
        gallery = Gallery.from_dict(gallery_data.to_dict(),gallery_data.id)
        galleries.append(gallery)

    return render(request,'gallery_session_detail.html',{'galleries':galleries})


@FirestoreControlView
def gallery_other_detail(request, db):
    galleries = []

    gallery_datas = db.collection('Gallery').stream()

    for gallery_data in gallery_datas:
        gallery = Gallery.from_dict(gallery_data.to_dict(),gallery_data.id)
        galleries.append(gallery)

    return render(request,'gallery_other_detail.html',{'galleries':galleries})


@FirestoreControlView
def gallery_delete(requset, db, gallery_id):
    db.collection('Gallery').document(gallery_id).delete()

    return redirect('gallery_detail')


@FirestoreControlView
def gallery_update(request, db, gallery_id):
    try:
        gallery_data = db.collection('Gallery').document(gallery_id).get()
    except google.cloud.exeption.NotFound:
        print('Not Found')

    gallery = Gallery.from_dict(gallery_data.to_dict(), gallery_data.id)

    if request.method == 'POST':
        contents = request.POST['contents']
        created_at = request.POST['created_at']
        title = request.POST['title']
        image_url = request.POST['image_url']
        place = request.POST['place']
        ordinal_num = request.POST['ordinal_num']
        event = request.POST['event']

        db.collection('Gallery').document(gallery_id).update({
            'contents': contents,
            'created_at': created_at,
            'title': title,
            'image_url': image_url,
            'place': place,
            'ordinal_num': ordinal_num,
            'event': event,
        })

        return redirect('gallery_detail')

    # POST 가 아닐 경우 update 창 띄워줌
    return render(request, 'gallery_update.html', {'gallery': gallery})