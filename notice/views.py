from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied

import firebase_admin
import google
from firebase_admin import credentials
from firebase_admin import firestore
from hackyourlife_sch.firebase import FirestoreControlView, SignInRequiredView

from django.core.paginator import Paginator

from .models import Notice

# Create your views here.
@SignInRequiredView(readable = True)
@FirestoreControlView
def notice_detail(request, db, notice_id):
    
    try:
        data = db.collection('Notice').document(notice_id).get()
        notice_datas = db.collection('Notice').order_by('date',direction=firestore.Query.DESCENDING).stream()
    except google.cloud.exceptions.NotFound:
        print('Not Found')

    permission = ''

    if request.method == 'POST':

        uid = request.POST['uid']

        try:
            user = db.collection('User').where('uid','==',uid).get()
        except google.cloud.exceptions.NotFound:
            print('Not Found')

        if len(user) >= 1:
            current_user = user[0].to_dict()

            if current_user['permission'] == 'manager':
                permission = 'manager'
            else:
                permission = 'member'

    notice = Notice.from_dict(data.to_dict(), data.id)

    notices = []

    prev_notice = None
    next_notice = None

    count = 0
    for notice_data in notice_datas:
        new_notice = Notice.from_dict(notice_data.to_dict(),notice_data.id)
        notices.append(new_notice)
        count += 1

    i=0
    for _notice in notices:
        if _notice.date == notice.date:
            if i > 0:
                prev_notice = notices[i-1]
            if i < (count - 1):
                next_notice = notices[i+1]
        i+=1

    output_datas = {
        'notice':notice,
        'prev_notice':prev_notice,
        'next_notice':next_notice,
        'permission': permission,
    }    

    return render(request, "notice_detail.html", output_datas)

def faq(request):
    return render(request, "faq.html")


@SignInRequiredView()
@FirestoreControlView
def notice_create(request, db):
    uid = request.POST['uid']

    try:
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exceptions.NotFound:
        print('report not found')

    if current_user['permission'] != 'manager':
        raise PermissionDenied # 권한 없음

    if request.method == 'POST':
        if 'contents' and 'date' and 'title' and 'file' and 'filename' and 'image' and 'imagename' in request.POST:
            author = current_user['username']
            contents = request.POST['contents']
            date = request.POST['date']
            title = request.POST['title']
            file = request.POST['file']
            filename = request.POST['filename']
            image = request.POST['image']
            imagename = request.POST['imagename']

            new_notice = Notice(contents, date, title, file, filename, image, imagename, author)

            db.collection('Notice').document().set(new_notice.to_dict())

            return redirect('notice_list')

    return render(request, 'notice_create.html')

@SignInRequiredView(readable = True)
@FirestoreControlView
def notice_list(request, db):
    notice_list = []

    notice_datas = db.collection('Notice').order_by('date', direction=firestore.Query.DESCENDING).stream()

    for notice_data in notice_datas:
        notice = Notice.from_dict(notice_data.to_dict(),notice_data.id)
        notice_list.append(notice)

    # 페이지 네이터
    paginator = Paginator(notice_list,5)
    page = int(request.GET.get('page',1))
    notices = paginator.get_page(page)

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

    return render(request,'notice.html',{'notices':notices, 'permission':permission})


@SignInRequiredView()
@FirestoreControlView
def notice_delete(request, db, notice_id):
    uid = request.POST['uid']

    try:
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exeption.NotFound:
        print('report not found')

    if current_user['permission'] != 'manager':
        raise PermissionDenied # 권한 없음

    db.collection('Notice').document(notice_id).delete()

    return redirect('notice_list')


@SignInRequiredView()
@FirestoreControlView
def notice_update(request, db, notice_id):

    uid = request.POST['uid']

    try:
        notice_data = db.collection('Notice').document(notice_id).get()
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exceptions.NotFound:
        print('Not Found')

    if current_user['permission'] != 'manager':
        raise PermissionDenied # 권한 없음

    notice = Notice.from_dict(notice_data.to_dict(), notice_data.id)

    if request.method == 'POST':
        if 'contents' and 'date' and 'title' and 'file' and 'filename' and 'image' and 'imagename' in request.POST:
            contents = request.POST['contents']
            date = request.POST['date']
            title = request.POST['title']
            file = request.POST['file']
            filename = request.POST['filename']
            image = request.POST['image']
            imagename = request.POST['imagename']

            db.collection('Notice').document(notice_id).update({
                'contents': contents,
                'date': date,
                'title': title,
                'file': file,
                'filename': filename,
                'image': image,
                'imagename': imagename,
            })

            return redirect('notice_detail', notice_id)

    # POST 가 아닐 경우 update 창 띄워줌
    return render(request, 'notice_update.html', {'notice': notice})

def faq(request):
    return render(request, "faq.html")