from django.shortcuts import render,redirect
import firebase_admin
import google
from firebase_admin import credentials
from firebase_admin import firestore
from hackyourlife_sch.firebase import FirestoreControlView
from .models import Notice
# Create your views here.


def notice_detail(request):
    return render(request, "notice_detail.html")


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
    notices = []

    notice_datas = db.collection('Notice').stream()

    for notice_data in notice_datas:
        notice = Notice.from_dict(notice_data.to_dict(),notice_data.id)
        notices.append(notice)

    return render(request,'notice.html',{'notices':notices})

