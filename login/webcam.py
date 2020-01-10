# https://icandooit.tistory.com/100
# 웹캠을 이용하여 동영상처럼 처리하기
# https://pinkwink.kr/1136
# 사진에 추가처리하기  , 정보, 네모박스
import cv2
import os
import datetime
import sys
import requests

client_id = "vMRLHcQLbp65AeICpwkI"
client_secret = "WSXIRzUvZ1"
now = datetime.datetime.now().strftime("%d_%H-%M-%S")
path = os.path.dirname(__file__)
# 현재 디렉토리 경로를 시작으로 지정
filename = str(now) + '.png'
fullpath = os.path.join(path, filename)
print(path)
print(fullpath)
print(filename)

#url = "https://openapi.naver.com/v1/vision/celebrity" // 유명인 얼굴인식
url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지

#비디오의 개수만큼 객체 생성
cap = cv2.VideoCapture(0)

#카메라로부터 이미지 한장을 가져옴
ret, frame = cap.read()
# print(frame)
## 프레임 컬러 설정함
#gray = cv2.cvtColor(frame, cv2.IMREAD_COLOR)

## 윈도우 프레레임에 보임

cv2.imshow('frame', frame)

#아무키나 누르기 전까지 대기
# cv2.waitKey(0)

# 이미지 'fullpath'로 저장
cv2.imwrite(fullpath, frame)
# 네이버 API 연동
print(type(frame))  # numpy.ndarray
print(type(open(fullpath, 'rb')))
files = {'image': open(fullpath, 'rb')}
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
response = requests.post(url,  files=files, headers=headers)
rescode = response.status_code
if(rescode==200):
    print (response.text)
    # print (response.text)
    # data = json.loads(response.text)
    # faceCount = data['info']['faceCount']
    # print("감지된 얼굴 수는 {}입니다.".format(faceCount))
else:
    print("Error Code:" + rescode)

# 캠 리소스 해제
cap.release()
# 윈도우즈 해제
cv2.destroyAllWindows()

if os.path.isfile(fullpath):
    print("exist!")
    # os.remove(filename)
    # PermissionError: [WinError 32] 다른 프로세스가 파일을 사용 중이기 때문에 프로세스가 액세스 할 수 없습니다: '10_23-29-37.png'


# 네이버 api 쓰려면 파일 저장이 필요하다...  파일저장후 지우려고하는데 프로세스 선점중이라 못한다한다..(sync?)
# 시간이 너무 오래걸리는데
# 프레임 여러개 해보기
