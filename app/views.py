from app import app, db, lm
from flask import render_template, flash, redirect, url_for, g, request, make_response
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import SignupForm, LoginForm
from models import User

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template(
        'index.html',
    )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Signed up successfully.', category='success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        flash('Logged in successfully.', category='success')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    resp = make_response(redirect(url_for('index')))
    return redirect(url_for('index'))