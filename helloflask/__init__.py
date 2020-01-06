from flask import Flask, g, session
from flask import request, Response, make_response
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.debug = True  # 디버깅모드

# 127.0.0.1/index  -> URL
# /index -> URI

# COOKIE
# 고객의 브라우저에 심어놓는 정보
@app.route('/wc')
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response('Set cookie')
    res.set_cookie(key, val)
    session['token'] = '1231A'
    return make_response(res)

@app.route('/rc')
def rc():
    key = request.args.get('key') #token
    val = request.cookies.get(key)
    return "cookie['" + key + "'] = " + val + ", " + session.get('token')
# cookie

# session
# 세션 사용을 위한 secret key
app.config.update(
    SECRET_KEY='ASGDJKWBC12',
    SESSION_COOKIE_NAME='pyweb_flask_session',
    PERMANET_SESSION_LIFETIME=timedelta(10)
)
# 서버에 심어놓는 정  다른페이지에 들어가도 로그인이 되어있는지 알수있도록
@app.route('/setsess')
def setsess():
    session['token'] = '1231A'
    return "Session이 설정되었습니다!"

@app.route('/getsess')
def getsess():
    return session.get('token')
# session['token']이나 session.get('token')은 같은의미
# 다만 get을 쓰면 key값이 없을때 에러가 나지 않음

@app.route('/delsess')
def delsess():
    if session.get('token'):
        del session['token']
    return "Session이 삭제되었습니다!"
# session

@app.route('/rp')
def rp():
    #GET parameter 받기  URI에서 찾는다
    #q = request.args.get('q')

    #POST parameter 받기  헤더안에서 찾는다
    #q = request.form.get('p', 123)

    #GET or POST    둘다 찾아본다
    #q = request.values.get('v')
    # get이 post보다 빠르다. get으로 구현할 수 있는것은 get으로 구현하자
    # 굳이 뭔지 알면 values함수를 쓰지말자 ( 써도 괜찮음 )

    #parameters
    q = request.args.getlist('q') #같은 파라미터를 반복적으로 받을 때에는 list로 받는다

    return "q=%s" % str(q)

# 날짜를 포맷에 맞게 반환하는 이중함수
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans

@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)

@app.route("/res1")
def res1():
    custom_res = Response("Custom Response", 200, {'test':'ttt'})
    return make_response(custom_res)
    # 큰 파일이나 데이터를 스트링으로 만들어서 보낼때 사용

@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [ ('Content_type', 'text/plain'),('Content-Length', str(len(body)))]
        start_response('200 OK', headers)
        return [body]
    return make_response(application)

# @app.before_request  # 어떤 요청이 들어와도 거치고 진행한다.
# def before_request():
#     print("before_request!!!")
#     g.str = "한글"    # g는 플라스크의 전역변수 객체
# # application context ( 보내는 모든 유저의 데이터 )
# # session context (한 유저의 데이터 )

@app.route("/gg")
def helloworld2():
    return "Hello flask" + getattr(g, 'str', '111')

@app.route("/")
def helloworld():
    return "Hello Flask World"

'''
    @app.before_first_request  첫번째 리퀘스트 전에 실행해라
    @app.before_request  매번 리퀘스트 전에 실행해라
    @app.after_request
    @app.teardown_request  response가 끝나고나서( 돈 보내다가 제대로 안됐을때 처리해준다는 개념 )
    @app.teardown_appcontext  application context가 destory될때 추후

    @app.route('/test', defaults={'page' : 'index'})
    @app.route('/test/<page>')   page가 없으면 자동으로 index로 들어간다

    @app.route('/test', host='abc.com')  다른 주소도 여기로 불러온다
    @app.route('/test', redirect_to='/new_test')  리다이렉션
'''
