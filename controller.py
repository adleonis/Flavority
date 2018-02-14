#!/usr/bin/env python3
''' 
CONTROLLER
**************************************************************************
Main site Controller.  Uses flask to throw templates, 


'''

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
import flask_login
import os


#import model
#import view
import datetime
import time
import orm

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = os.urandom(24)



@app.context_processor
def override_url_for():
    ''' 
    This code is by Eric Buckley from http://flask.pocoo.org/snippets/40/
    It updates your static files everytime the browser refreshes so styles are up to date, not busted by browser cache
    '''
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    ''' 
    This code is by Eric Buckley from http://flask.pocoo.org/snippets/40/
    It updates your static files everytime the browser refreshes so styles are up to date, not busted by browser cache
    '''
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/', methods=['GET', 'POST'])
def show_celebs():
    ''' 
    ..Main website page, shows list of celebs
    '''
    if request.method == 'GET':
        # This is an HTTP get request.
        (c,conn) = orm.do_connect()
        number = 1000
        data = orm.select_top_celeb_by_followers(c,[number])
        orm.dis_connect((c,conn))
        return render_template('index.html', message=number, data=data)
    else:
        if request.form['submit'] == 'login':
            return render_template('login.html', message='Please Login')
        elif request.form['submit'] == 'register':
            return redirect(url_for('register'))
        return

def tryit():
    (c,conn) = orm.do_connect()
    data = orm.select_top_celeb_by_followers(c,[10])
    print(data)
    orm.dis_connect((c,conn))






if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

