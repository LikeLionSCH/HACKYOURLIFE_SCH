from django.shortcuts import render,redirect

from firebase_admin import credentials
from firebase_admin import firestore

from datetime import datetime

from hackyourlife_sch.firebase import initialize_firebase
from .models import Report

"""
레포트를 등록 해주는 함수
@param : request, 등록할 레포트에 해당하는 과제의 id
@return : 래포트 등록하는 페이지 (report_create.html) 페이지 렌더링
"""
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


"""
레포트의 목록을 과제별로 나눠서 띄워주는 함수
@param : request, 해당하는 과제의 id
@return : report_list.html 렌더링, 해당하는 과제 목록들 전달
"""
def read_Report_list_view(request, assignment_id): 
    
    # 파이어 베이스 초기화
    db = initialize_firebase()

    # 파이어베이스에서 assignment_id 값이 매개변수로 불로온 과제의 id값과 일치하는 것만 가져오는 쿼리문
    datas = db.collection('Report').where('assignment_id','==',assignment_id).stream()

    reports = []

    # 템플릿으로 전달을 위해 불러온 데이터를 객체로 변환하여 전달할 리스트 생성
    for data in datas:
        report = Report.from_dict(data.to_dict(),data.id)
        reports.append(report)

    # report_list.html 페이지 렌더링, 과제 목록 전달
    return render(request,"report_list.html",{'reports':reports})



def get_Report_detail_view(request,report_id):
    pass

def update_Report_view(request,report_id):
    pass

def delete_Report(request,report_id):
    pass
