from app import app
from flask import render_template

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template(
        'index.html',
    )

@app.route('/hello', methods=['GET', 'POST'])
@app.route('/hello/<user>', methods=['GET', 'POST'])
def hello(user = "guest"):
    return render_template(
        'hello.html',
        user=user,
    )
