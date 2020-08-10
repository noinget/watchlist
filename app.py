# --------------------------------------------
# automatic re-load server if code changed.
# 1. pip install python-dotenv
# 2. create a file named '.flaskenv'
# 3. FLASK_ENV=development
# url: keyword, search 'I got a different idea:'
# https://stackoverflow.com/questions/16344756/auto-reloading-python-flask-app-upon-code-changes
# --------------------------------------------

import os
import sys

from flask import url_for, Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# ----------------------------------------
# DB setting for SQLLite3
# ----------------------------------------
WIN = sys.platform.startswith('win')

if WIN:  # 如果是 Windows 系統，使用三個斜線
    prefix = 'sqlite:///'
else:  # 否則使用四個斜線
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 關閉對模型修改的監控
# 在擴展類實例化前加載配置
db = SQLAlchemy(app)

# ----------------------------------------

name = '503 Edwin'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


class User(db.Model):  # 表名將會是 user（自動生成，小寫處理）
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名將會是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    title = db.Column(db.String(60))  # 電影標題
    year = db.Column(db.String(4))  # 電影年份


class Tide(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    height = db.Column(db.Float(6))  # 電影標題
    month = db.Column(db.String(4))  # 電影年份
    year = db.Column(db.String(4))  # 電影年份
    hour = db.Column(db.String(2))  # 電影年份


# ----------------------------------------------
# for adding your customized flask commands
# ----------------------------------------------

import click


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的兩個變量移動到這個函數內
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()  # 註冊為命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 設置選項
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判斷是否輸入了選項
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 輸出提示信息


@app.route('/')
def index():
    # == use the static variable
    # return render_template('index.html', name=name, movies=movies)
    user = User.query.first()  # 讀取用戶記錄
    movies = Movie.query.all()  # 讀取所有電影記錄
    tides = Tide.query.all()  # 讀取所有電影記錄
    return render_template('index.html', user=user, movies=movies, tides=tides)


@app.route('/test')
def test_url_for():
    print(url_for('/'))
    print(url_for('/user/name=noinget'))


@app.route('/user/<name>')
def user_page(name):
    from flask import escape
    return 'user page {}'.format(escape(name))
