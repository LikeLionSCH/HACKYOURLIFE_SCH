from django.shortcuts import render,redirect

from firebase_admin import credentials
from firebase_admin import firestore

from datetime import datetime

from hackyourlife_sch.firebase import initialize_firebase
from .models import Report

def create_Report_view(request,assignment_id):

    # 리퀘스트의 메소드가 POST일 경우에만
    if (request.method=='POST'):
        
        # 파이어베이스 초기화
        db = initialize_firebase()

        # form 으로부터 값을 불러오는 코드
        repository_address = request.POST['repository_address']
        contents = request.POST['contents']

        # 현제 시간을 구해 정해진 타입으로 포멧
        now = datetime.now()
        time = format(str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ' ' + str(now.hour) + '시' + str(now.minute) + '분')
        print(time)

        # 새로운 레포트 객체 생성
        report = Report(assignment_id,'author',contents,repository_address,time,'체점중')

        # 파이어베이스와 연결 후 레포트 데이터 생성
        db.collection('Report').document().set(report.to_dict())

        # 리다이렉트
        return redirect('/')

    # 포스트가 아닐경우 report_create 페이지 렌더
    return render(request,'report_create.html', {'assignment_id':assignment_id})