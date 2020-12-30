from django.shortcuts import render,redirect

from firebase_admin import credentials
from firebase_admin import firestore
import google

from datetime import datetime
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from hackyourlife_sch.firebase import FirestoreControlView, SignInRequiredView
from .models import Report, My_report_data
from assignments.models import Assignment

"""
레포트를 등록 해주는 함수
@param : request, 등록할 레포트에 해당하는 과제의 id
@return : 래포트 등록하는 페이지 (report_create.html) 페이지 렌더링
"""
@SignInRequiredView()
@FirestoreControlView
def create_Report_view(request, db, assignment_id):

    # 유저 정보 불러옴
    uid = request.POST['uid']

    # 파이어베이스에서 매개변수로 불러온 과제, 레포트의 데이터 불러옴
    try:
        assignment_data = db.collection('Assignment').document(assignment_id).get()
        reports = db.collection('Report').where('assignment_id','==',assignment_id).where('author_uid','==',uid).get()
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exception.NotFound:
        print('report not found')

    if current_user['permission'] == 'manager':
        raise PermissionDenied

    # 내가 제출한 과제가 있는지 없는지 확인
    if len(reports) >= 1:
        my_report = Report.from_dict(reports[0].to_dict(),reports[0].id)

        # 레포트 데이터, 과제의 제목, id
        output_datas = {
            'report':my_report,
            'assignment_title':assignment_data.to_dict()['title'],
            'assignment_id':assignment_data.id,
        }
    
        # report_update 렌더링, output datas
        return render(request,'report_update.html',output_datas)

    # 해당 과제의 제목 추출
    assignment_title = assignment_data.to_dict()['title']

    # 리퀘스트의 메소드가 POST일 경우에만
    if request.method=='POST':

        # request.POST 에 레포 주소랑 컨텐츠가 포함되어 있을 경우
        if 'repository_address' and 'contents' in request.POST:

            # form 으로부터 값을 불러오는 코드
            repository_address = request.POST['repository_address']
            contents = request.POST['contents']

            # 새로운 레포트 객체 생성
            report = Report(assignment_id,uid,current_user['username'],contents,repository_address,firestore.SERVER_TIMESTAMP,'미채점','')

            # 파이어베이스와 연결 후 레포트 데이터 생성
            db.collection('Report').document().set(report.to_dict())

            # 리다이렉트
            # 유저 타입 나뉘 경우 수정 해야함
            return redirect('my_list')

    output_datas = {
        'assignment_id':assignment_id,
        'assignment_title':assignment_title,
    }

    # 포스트가 아닐경우 report_create 페이지 렌더
    return render(request,'report_create.html', output_datas)


"""
레포트의 목록을 과제별로 나눠서 띄워주는 함수
@param : request, 해당하는 과제의 id
@return : report_list.html 렌더링, output datas
"""
@SignInRequiredView()
@FirestoreControlView
def read_Report_list_view(request, db, assignment_id):

    uid = request.POST['uid']

    # 파이어베이스에서 매개변수로 불러온 과제의 데이터 불러옴
    try:
        assignment_data = db.collection('Assignment').document(assignment_id).get()
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exception.NotFound:
        print('report not found')
    
    if current_user['permission'] == 'member':
        raise PermissionDenied

    # 해당 과제의 제목 추출
    assignment_title = assignment_data.to_dict()['title']

    # 파이어베이스에서 레포트 데이터를 작성일 순서대로 정렬하여 불러오는 쿼리문
    # 공식 문서에는 db.collection().where().order_by() 가 되는 것으로 나와 있지만 우리 프로젝트에선 불가 이유는 모름 ㅠ
    report_datas = db.collection('Report').order_by('submit_date', direction=firestore.Query.DESCENDING).stream()

    # 유저들의 데이터도 불러옴
    user_datas = db.collection('User').stream()

    not_scored_report_list = []
    scoring_complete_report_list = []
    not_submitted_report_list = []
    report_list = []

    # 템플릿으로 전달을 위해 불러온 데이터를 객체로 변환하여 전달할 리스트 생성
    for report_data in report_datas:

        report_dict = report_data.to_dict()

        # 불러온 과제 아이디와 매개변수의 과제 아이디가 같을 경우만 객체를 생성하여 append
        if report_dict['assignment_id'] == assignment_id:
            report = Report.from_dict(report_dict,report_data.id)

            # 제출 상태가 채점중일 경우 미채점 리스트에 추가
            if report.submit_status == '미채점':
                not_scored_report_list.append(report)

            # 제출 상태가 채점 완료일 경우 채점 완료 리스트에 추가
            elif report.submit_status == '채점완료':
                scoring_complete_report_list.append(report)


    # 모든 유저의 목록을 불러와 그에 해당하는 객채를 미제출 상태로 생성
    # 코드 리펙토링 필요
    for user_data in user_datas:
        count = 0

        for report in not_scored_report_list:
            if user_data.to_dict()['uid'] == report.author_uid:
                count+=1

        for report in scoring_complete_report_list:
            if user_data.to_dict()['uid'] == report.author_uid:
                count+=1

        if count == 0 and user_data.to_dict()['permission'] == 'member':
            not_submitted_report_list.append(Report(assignment_id,user_data.to_dict()['uid'],user_data.to_dict()['username'],None,None,None,"미제출",''))

    report_list = not_scored_report_list + scoring_complete_report_list + not_submitted_report_list

    if request.method == 'POST':

        if 'filter' in request.POST:

            filter_type = request.POST['filter']
            print(filter_type)

            # 미채점 일 경우 미채점된 리스트만 추가
            if filter_type == "not_scored":
                report_list = not_scored_report_list

            # 채점 완료 일 경우 채점 완료인 리스트만 추가
            elif filter_type == "scoring_complete":
                report_list = scoring_complete_report_list

            # 제출이 안됐을 경우 미제출인 아이들만 추가
            elif filter_type == "not_submitted":
                report_list = not_submitted_report_list
            
            # 그 외에 전체 리스트를 원하면 모든 리스트를 합친다
            else:
                report_list = not_scored_report_list + scoring_complete_report_list + not_submitted_report_list


    # 페이지 네이터
    paginator = Paginator(report_list,5)
    page = int(request.GET.get('page',1))
    reports = paginator.get_page(page)

    # 레포트 데이터들, 해당 과제의 Id, 해당 과제의 제목
    output_datas = {
        'reports':reports,
        'assignment_id':assignment_data.id,
        'assignment_title':assignment_title,
    }

    # report_list.html 페이지 렌더링, output_datas
    return render(request,"report_list.html",output_datas)


"""
레포트의 디테일 뷰를 보여주는 함수
@param : request, 보여줄 레포트의 id
@return : report_detail.html 렌더링, output datas
"""
@SignInRequiredView()
@FirestoreControlView
def get_Report_detail_view(request, db, assignment_id, report_id):

    uid = request.POST['uid']

    # 매개변수의 id 값으로 파이어베이스에서 해당하는 데이터를 불러옴
    try:
        report_data = db.collection('Report').document(report_id).get()
        assignment_data = db.collection('Assignment').document(assignment_id).get()
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exception.NotFound:
        print('report not found')

    # 해당 과제의 제목 추출
    assignment_title = assignment_data.to_dict()['title']

    # 불러온 데이터로 레포트 객체 생성
    report = Report.from_dict(report_data.to_dict(),report_data.id)

    # 내가 쓴 거 이면 수정 가능 안되면 불가
    if uid == report.author_uid:
        access = True
    else:
        access = False

    # 이 글을 보는 사람이 메니저 이면 채점 페이지로 보냄
    if current_user['permission'] == 'manager':
        permission = 'manager'
    else:
        permission = 'member'

    # 레포트 목록, 해당하는 과제의 제목
    output_datas = {
        'report' : report,
        'assignment_title' : assignment_title,
        'assignment_id' : assignment_data.id,
        'access' : access,
        'permission' : permission,
    }

    # 레포트 데테일 페이지 렌더링, output datas
    return render(request,'report_detail.html',output_datas)


"""
제출한 과제를 수정하는 함수
@param : request, 수정할 레포트의 id
@return : report_update.html 렌더링, 수정한 레포트의 디테일 페이지로 리다이렉트
"""
@SignInRequiredView()
@FirestoreControlView
def update_Report_view(request, db, assignment_id, report_id):

    uid = request.POST['uid']

    # 매개변수의 id 값으로 파이어베이스에서 해당하는 데이터를 불러옴
    try:
        report_data = db.collection('Report').document(report_id).get()
        assignment_data = db.collection('Assignment').document(assignment_id).get()
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exception.NotFound:
        print('report not found')

    if report_data.to_dict()['author_uid'] != uid:
        raise PermissionDenied

    # 파이어베이스에서 불러온 데이터로 객체 생성
    report = Report.from_dict(report_data.to_dict(),report_data.id)

    # 과제의 제목 추출
    assignment_title = assignment_data.to_dict()['title']

    if (request.method == 'POST'):

        if 'repository_address' and 'contents' in request.POST:

            # form 으로부터 값을 불러오는 코드
            repository_address = request.POST['repository_address']
            contents = request.POST['contents']

            # 현제 시간을 불러와 지정 형식으로 포멧팅
            now = datetime.now()
            time = now.strftime('%Y-%m-%d %H:%M')

            # 파이어베이스에 접속하여 입력된 값으로 수정
            db.collection('Report').document(report_id).update({
                'repository_address' : repository_address,
                'contents' : contents,
            })

            # 수정 한 레포트의 디테일 페이지로 리다이렉트
            return redirect('report_detail',assignment_id,report_id)

    # 레포트 데이터, 과제의 제목
    output_datas = {
        'report':report,
        'assignment_title':assignment_title,
        'assignment_id':assignment_data.id,
    }
    
    # report_update 렌더링, output datas
    return render(request,'report_update.html',output_datas)


"""
학생이 제출한 과제를 채점하고 커멘트를 남기는 페이지
@param : request, 해당 과제 Id, 레포트의 id
@return : render
"""
@SignInRequiredView()
@FirestoreControlView
def scoring_Report_view(request,db, assignment_id, report_id):

    uid = request.POST['uid']

    # 매개변수의 id 값으로 파이어베이스에서 해당하는 데이터를 불러옴
    try:
        report_data = db.collection('Report').document(report_id).get()
        assignment_data = db.collection('Assignment').document(assignment_id).get()
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exception.NotFound:
        print('report not found')

    if current_user['permission'] != 'manager':
        raise PermissionDenied # 권한 없음

    # 파이어베이스에서 불러온 데이터로 객체 생성
    report = Report.from_dict(report_data.to_dict(),report_data.id)

    # 과제의 제목 추출
    assignment_title = assignment_data.to_dict()['title']

    # request 의 메소드가 POST 일 경우
    if request.method == 'POST':

        if 'comment' in request.POST:

            # 커멘트 값 불러옴
            comment = request.POST['comment']
            
            # 불러온 커멘트로 레포트에 커멘트 추가, 상태를 채점 완료로 변경
            db.collection('Report').document(report_id).update({
                'comment' : comment,
                'submit_status' : '채점완료',
            })

            # 수정한 레포트의 디테일 페이지로 이동
            return redirect('report_detail',assignment_id,report_id)

    # 레포트 데이터, 과제의 제목
    output_datas = {
        'report':report,
        'assignment_title':assignment_title,
        'assignment_id':assignment_data.id,
    }

    # report scoring 페이지 렌더링, output datas 전달
    return render(request,'report_scoring.html',output_datas)


"""
레포트를 삭제하는 함수
@param : request, 삭제할 레포트의 id
@return : 리스트 페이지로 리다이렉트
"""
@SignInRequiredView()
@FirestoreControlView
def delete_Report(request, db, assignment_id, report_id):

    uid = request.POST['uid']

    try:
        report = db.collection('Report').document(report_id).get()
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exception.NotFound:
        print('report not found')

    if report.to_dict()['author_uid'] != uid:
        raise PermissionDenied 

    # 파이어베이스에서 삭제할 데이터를 불러와 삭제
    db.collection('Report').document(report_id).delete()

    # 여기도 수정 필요 
    # 리스트 페이지로 리다이렉트
    return redirect('my_list')


@SignInRequiredView()
@FirestoreControlView
def my_report_page(request, db):
    
    uid = request.POST['uid']

    try:
        report_datas = db.collection('Report').where('author_uid','==',uid).stream()
        assignment_datas = db.collection('Assignment').order_by('timestamp',direction=firestore.Query.DESCENDING).stream()
        user = db.collection('User').where('uid','==',uid).get()
        current_user = user[0].to_dict()
    except google.cloud.exception.NotFound:
        print('report not found')

    datas = []
    for assignment_data in assignment_datas:

        assignment = Assignment.from_dict(assignment_data.to_dict(),assignment_data.id)
        report_datas = db.collection('Report').where('author_uid','==',uid).stream()

        is_checked = 0
        for report_data in report_datas:
            report = Report.from_dict(report_data.to_dict(),report_data.id)
            print('report: '+report.assignment_id)
            print('assignment: ' + assignment.assignment_id)
            if report.assignment_id == assignment.assignment_id:
                datas.append(My_report_data(assignment.title,assignment.deadline,'제출완료',report.submit_date,report.report_id,assignment.assignment_id))
                is_checked += 1

        if is_checked == 0:
            print('asdasd')
            datas.append(My_report_data(assignment.title,assignment.deadline,'미제출',None,None,assignment.assignment_id) )

    # 페이지 네이터
    paginator = Paginator(datas,5)
    page = 1
    if request.method == 'POST':
        if 'page' in request.POST:
            page = int(request.POST['page'])
            print(page)
    data_list = paginator.get_page(page)

    return render(request,'my_report_list.html',{'username':current_user['username'],'datas':data_list})



