from flask import Blueprint, render_template, request, session
from user import user_dao
import os
import sys
import requests

user_blue = Blueprint('user_blue', __name__)


client_id = "vMRLHcQLbp65AeICpwkI"
client_secret = "WSXIRzUvZ1"

@user_blue.route('/')
def user_login():
    html = render_template('user_login.html')
    return html


@user_blue.route('/user_join')
def user_join():
    html = render_template('user_join.html')
    return html

# 네이버 API 요청
# open(파일명 필요)
@user_blue.route('/face')
def face_url():
    url = "https://openapi.naver.com/v1/vision/face" // 얼굴감지
    #url = "https://openapi.naver.com/v1/vision/celebrity" // 유명인 얼굴인식
    files = {'image': open('YOUR_FILE_NAME', 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code
    if(rescode==200):
        print (response.text)
    else:
        print("Error Code:" + rescode)

    return "hello"
# @user_blue.route('/user_modify')
# def user_modify():
#     user_idx = session['user_idx']
#     result = user_dao.get_user_info(user_idx)
#
#     print(result)
#
#     html = render_template('user/user_modify.html', user_data=result)
#
#     return html
#
#
# @user_blue.route('/user_modify_pro', methods=['post'])
# def user_modify_pro():
#     #user_name = request.form['user_name']
#     user_id = request.form['user_id']
#     user_pw = request.form['user_pw1']
#     user_email = request.form['user_email']
#     user_phone = request.form['user_phone']
#
#     user_dao.update_user(user_id, user_pw, user_email, user_phone)   # 이름과 아이디는 업데이트 안해도되려나?
#
#     return 'OK'
#
#
@user_blue.route('/user_join_pro', methods=['post'])
def user_join_pro():
    # 파라미터 데이터 추출
    user_name = request.form['user_name']
    user_id = request.form['user_id']
    user_pw = request.form['user_pw1']
    user_email = request.form['user_email']
    user_phone = request.form['user_phone']

    #print(user_name)
    #print(user_id)
    #print(user_pw)
    #print(user_email)
    #print(user_phone)

    # 저장
    user_dao.add_user(user_name, user_id, user_pw, user_email, user_phone)

    return 'OK'


# 아이디 중복체크
@user_blue.route('/check_user_id', methods=['post'])
def ckeck_user_id():
    user_id = request.form['user_id']

    result = user_dao.check_user_id(user_id)
    return result

#
# # 로그인 처리
# @user_blue.route('/user_login_pro', methods=['post'])
# def user_login_pro() :
#     # 파라미터 추출
#     user_id = request.form['user_id']
#     user_pw = request.form['user_pw']
#     # 확인한다.
#     result = user_dao.check_login(user_id, user_pw)
#
#     if result == 'NO' :
#         return 'NO'
#     else :
#         session['login'] = 'YES'
#         session['user_idx'] = result
#         return 'YES'
#
#
# # 로그아웃 처리
# @user_blue.route('/user_logout')
# def user_logout():
#     session['login'] = 'NO'
#     html = render_template('index.html')
#     return html
# #    return None
#
#
# # 로그인했는지 확인 (게시판들어갈때 알림창)
# @user_blue.route('/login_check')
# def login_check():
#     print(session['login'])
#     if session['login'] == 'YES' :
#         return 'YES'
#     else :
#         return 'NO'
