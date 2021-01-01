from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied
import firebase_admin
import google
from firebase_admin import credentials
from firebase_admin import firestore
from hackyourlife_sch.firebase import FirestoreControlView,SignInRequiredView
from .models import Gallery


def gallery_main(request):
    return render(request, "gallerymain.html")

@SignInRequiredView(readable = True)
@FirestoreControlView
def gallery_board(request, db, generation):
    galleries = []
    thums = [0,0,0,0]

    permission = ''
    if request.method == 'POST':
    
        uid = request.POST['uid']

        try:
            user = db.collection('User').where('uid','==',uid).get()
        except google.cloud.exceptions.NotFound:
            print('Not Found')
            
        if len(user)>=1:

            current_user = user[0].to_dict()

            if current_user['permission'] == 'manager':
                permission = 'manager'
            else:
                permission = 'member'


    gallery_datas = db.collection('Gallery').stream()

    for gallery_data in gallery_datas:
        gallery = Gallery.from_dict(gallery_data.to_dict(), gallery_data.id)
        galleries.append(gallery)

    for gallery in galleries:
        if gallery.event == 'ideathon':
            thums[0] = gallery.image_url
        elif gallery.event == 'hackathon':
            thums[1] = gallery.image_url
        elif gallery.event == 'session':
            thums[2] = gallery.image_url
        elif gallery.event == 'other':
            thums[3] = gallery.image_url

        print(gallery.image_url)
    

    return render(request, 'th_gallery_board.html', {'galleries': galleries, 'idea':thums[0], 'hacka':thums[1], 'session':thums[2], 'other':thums[3],'permission':permission, 'generation':generation})

@SignInRequiredView()
@FirestoreControlView
def gallery_create(request,db, generation):

    uid = request.POST['uid']

    try:
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exceptions.NotFound:
        print('Not Found')

    if current_user['permission'] == 'member':
        raise PermissionDenied

    if request.method == 'POST':

        if 'conetents' and 'date' and 'title' and 'image_url' and 'place' and 'ordinal_num' and 'event' in request.POST:

            contents = request.POST['contents']
            date = request.POST['date']
            title = request.POST['title']
            image_url = request.POST['image_url']
            place = request.POST['place']
            ordinal_num = request.POST['ordinal_num']
            event = request.POST['event']

            new_gallery = Gallery(contents, firestore.SERVER_TIMESTAMP , date, title, image_url, place, ordinal_num, event)

            db.collection('Gallery').document().set(new_gallery.to_dict())

            return redirect('gallery_board', generation)

    return render(request, 'gallery_create.html', {'generation':generation})


@SignInRequiredView(readable = True)
@FirestoreControlView
def gallery_detail(request, db, generation, keyword):

    permission = ''
    if request.method == 'POST':
    
        uid = request.POST['uid']

        try:
            user = db.collection('User').where('uid','==',uid).get()
        except google.cloud.exceptions.NotFound:
            print('User Not Found')
            
        if len(user)>=1:

            current_user = user[0].to_dict()

            if current_user['permission'] == 'manager':
                permission = 'manager'
            else:
                permission = 'member'

    galleries = []

    gallery_datas = db.collection('Gallery').order_by('created_at',direction=firestore.Query.DESCENDING).stream()

    for gallery_data in gallery_datas:
        gallery = Gallery.from_dict(gallery_data.to_dict(),gallery_data.id)
        galleries.append(gallery)
        print(gallery.image_url)

    return render(request,'gallery_detail.html',{'galleries':galleries,'permission':permission})


# @SignInRequiredView(readable = True)
# @FirestoreControlView
# def gallery_idea_detail(request, db):

#     permission = ''
#     if request.method == 'POST':
    
#         uid = request.POST['uid']

#         try:
#             user = db.collection('User').where('uid','==',uid).get()
#         except google.cloud.exceptions.NotFound:
#             print('User Not Found')
            
#         if len(user)>=1:

#             current_user = user[0].to_dict()

#             if current_user['permission'] == 'manager':
#                 permission = 'manager'
#             else:
#                 permission = 'member'

#     galleries = []

#     gallery_datas = db.collection('Gallery').order_by('created_at',direction=firestore.Query.DESCENDING).stream()

#     for gallery_data in gallery_datas:
#         gallery = Gallery.from_dict(gallery_data.to_dict(),gallery_data.id)
#         galleries.append(gallery)
#         print(gallery.image_url)

#     return render(request,'gallery_idea_detail.html',{'galleries':galleries,'permission':permission})

# @SignInRequiredView(readable = True)
# @FirestoreControlView
# def gallery_hacka_detail(request, db):

#     permission = ''
#     if request.method == 'POST':
    
#         uid = request.POST['uid']

#         try:
#             user = db.collection('User').order_by('created_at',direction=firestore.Query.DESCENDING).where('uid','==',uid).get()
#         except google.cloud.exceptions.NotFound:
#             print('Not Found')
            
#         if len(user)>=1:

#             current_user = user[0].to_dict()

#             if current_user['permission'] == 'manager':
#                 permission = 'manager'
#             else:
#                 permission = 'member'

#     galleries = []

#     gallery_datas = db.collection('Gallery').stream()

#     for gallery_data in gallery_datas:
#         gallery = Gallery.from_dict(gallery_data.to_dict(),gallery_data.id)
#         galleries.append(gallery)

#     return render(request,'gallery_hacka_detail.html',{'galleries':galleries,'permission':permission})

# @SignInRequiredView(readable = True)
# @FirestoreControlView
# def gallery_session_detail(request, db):

#     permission = ''
#     if request.method == 'POST':
    
#         uid = request.POST['uid']

#         try:
#             user = db.collection('User').where('uid','==',uid).get()
#         except google.cloud.exceptions.NotFound:
#             print('Not Found')
            
#         if len(user)>=1:

#             current_user = user[0].to_dict()

#             if current_user['permission'] == 'manager':
#                 permission = 'manager'
#             else:
#                 permission = 'member'

#     galleries = []

#     gallery_datas = db.collection('Gallery').order_by('created_at',direction=firestore.Query.DESCENDING).stream()

#     for gallery_data in gallery_datas:
#         gallery = Gallery.from_dict(gallery_data.to_dict(),gallery_data.id)
#         galleries.append(gallery)

#     return render(request,'gallery_session_detail.html',{'galleries':galleries,'permission':permission})

# @SignInRequiredView(readable=True)
# @FirestoreControlView
# def gallery_other_detail(request, db):

#     permission = ''
#     if request.method == 'POST':
    
#         uid = request.POST['uid']

#         try:
#             user = db.collection('User').where('uid','==',uid).get()
#         except google.cloud.exceptions.NotFound:
#             print('Not Found')
            
#         if len(user)>=1:

#             current_user = user[0].to_dict()

#             if current_user['permission'] == 'manager':
#                 permission = 'manager'
#             else:
#                 permission = 'member'

#     galleries = []

#     gallery_datas = db.collection('Gallery').order_by('created_at',direction=firestore.Query.DESCENDING).stream()

#     for gallery_data in gallery_datas:
#         gallery = Gallery.from_dict(gallery_data.to_dict(),gallery_data.id)
#         galleries.append(gallery)

#     return render(request,'gallery_other_detail.html',{'galleries':galleries,'permission':permission})

@SignInRequiredView()
@FirestoreControlView
def gallery_delete(requset, db, gallery_id):

    uid = request.POST['uid']

    try:
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exceptions.NotFound:
        print('Not Found')

    if current_user['permission'] == 'member':
        raise PermissionDenied

    db.collection('Gallery').document(gallery_id).delete()

    return redirect('gallery_board')

@SignInRequiredView()
@FirestoreControlView
def gallery_update(request, db, gallery_id):

    uid = request.POST['uid']

    try:
        gallery_data = db.collection('Gallery').document(gallery_id).get()
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exeption.NotFound:
        print('Not Found')

    if current_user['permission'] == 'member':
        raise PermissionDenied

    gallery = Gallery.from_dict(gallery_data.to_dict(), gallery_data.id)

    if request.method == 'POST':

        if 'contents' and 'date' and 'title' and 'image_url' and 'placa' and 'ordinal_num' and 'event' in request.POST:
            contents = request.POST['contents']
            date = request.POST['date']
            title = request.POST['title']
            image_url = request.POST['image_url']
            place = request.POST['place']
            ordinal_num = request.POST['ordinal_num']
            event = request.POST['event']

            db.collection('Gallery').document(gallery_id).update({
                'contents': contents,
                'date': date,
                'title': title,
                'image_url': image_url,
                'place': place,
                'ordinal_num': ordinal_num,
                'event': event,
            })

            return redirect('gallery_board')

    # POST 가 아닐 경우 update 창 띄워줌
    return render(request, 'gallery_update.html', {'gallery': gallery})