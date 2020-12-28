from django.shortcuts import render,redirect

import firebase_admin
import google
from firebase_admin import credentials
from firebase_admin import firestore
from hackyourlife_sch.firebase import FirestoreControlView

from django.core.paginator import Paginator

from .models import Notice

# Create your views here.

@FirestoreControlView
def notice_detail(request, db, notice_id):
    try:
        data = db.collection('Notice').document(notice_id).get()
    except google.cloud.exceptions.NotFound:
        print('Not Found')

    notice = Notice.from_dict(data.to_dict(), data.id)
    print(data.to_dict())

    return render(request, "notice_detail.html", {'notice':notice})


def faq(request):
    return render(request, "faq.html")


@FirestoreControlView
def notice_create(request,db):
    if request.method == 'POST':
        contents = request.POST['contents']
        date = request.POST['date']
        title = request.POST['title']
        file = request.POST['file']
        image = request.POST['image']


        new_notice = Notice(contents, date, title, file, image)

        db.collection('Notice').document().set(new_notice.to_dict())

        return redirect('notice_list')

    return render(request, 'notice_create.html')


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

    return render(request,'notice.html',{'notices':notices})

