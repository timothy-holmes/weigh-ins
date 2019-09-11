from flask import render_template, flash, redirect, url_for, send_file
from app import app, db
from flask_login import current_user, login_user
from app.forms import LoginForm, WeighInForm
from app.models import User, WeighIn
from app.processing import get_weight_bf_graph

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_anonymous:
        flash('You must log in to use app.')
        return redirect(url_for('login'))
    return render_template('index.html', title='Home')
    
@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/add-weigh-in', methods=['GET', 'POST'])
def add_weighin():
    form = WeighInForm()
    if form.validate_on_submit():
        w = WeighIn(
            user_id = current_user.id,
            weight = form.weight.data,
            bf = form.bf.data,
            date = form.wdate.data,
            time = form.wtime.data
        )
        db.session.add(w)
        db.session.commit()
        flash('Weigh-in added: {}'.format(w))
        return redirect(url_for('index'))
    return render_template('add_weighin.html', title='Add Weigh-in', form=form)
    
@app.route('/graph-weight')
def graph_weight():
    if current_user.is_anonymous:
        flash('You must log in to see graphs.')
        return redirect(url_for('login'))
    graph_obj = get_weight_bf_graph(user_id=1)
    return send_file(graph_obj,attachment_filename='plot.png',mimetype='image/png')