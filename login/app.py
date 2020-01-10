from flask import Flask, render_template, session
# from index import main
from user import user
# from board import board


app = Flask(__name__)
app.debug=True
# 세션 사용을 위한 secret key
app.secret_key = 'selkjfoiwejfoiwjfoijiofj'


# app.register_blueprint(main.main_blue)
app.register_blueprint(user.user_blue)
# app.register_blueprint(board.board_blue)


app.run(host='127.0.0.1', port=5000)
