from flask import render_template, flash, redirect, url_for, send_file
from app import app, db
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, WeighInForm
from app.models import User, WeighIn
from app.processing import get_weight_bf_graph, copy_filelike_to_file
from werkzeug.utils import secure_filename

import os, time

def has_no_empty_params(rule): # for use with site-map route
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_anonymous:
        flash('You must log in to use app.')
        return redirect(url_for('login'))
    return render_template('index.html', title='Home')

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
    if current_user.is_anonymous:
        flash('You must log in to add weigh-in.')
        return redirect(url_for('login'))
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
    graph_obj = get_weight_bf_graph(user_id=current_user.id)
    graph_filename = secure_filename(str(current_user.id) + '-' + time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time())) + '.png')
    with open(os.path.join('app', 'static', 'graph', graph_filename), "wb") as outfile:
        copy_filelike_to_file(src=graph_obj, dest=outfile)
    return render_template('graph.html',img_src=url_for('static',filename=('graph/'+graph_filename)),title='Curren Weight Graph')

@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return render_template('site_map.html', title='Site Map', links=links)