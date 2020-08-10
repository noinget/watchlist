from flask import url_for, Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route('/test')
def test_url_for():
    print(url_for('/'))
    print(url_for('/user/name=noinget'))


@app.route('/user/<name>')
def user_page(name):
    from flask import escape
    return 'user page {}'.format(escape(name))
