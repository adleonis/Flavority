#!/usr/bin/env python3
''' 
CONTROLLER
**************************************************************************
Main site Controller.  Uses flask to throw templates, 


'''

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from flask_bootstrap import Bootstrap
import flask_login
import os


#import model
#import view
import datetime
import time
import orm
import scraper

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = os.urandom(24)
Bootstrap(app)

@app.template_filter('BMk')
def translate_followers(s):
    if s > 999999999:
        return str(round(s/1000000000,1))+'B'
    elif s > 999999:
        return str(round(s/1000000,1))+'M'
    elif s > 999:
        return str(round(s/1000,1))+'k'
    else:
        return s

@app.template_filter('ctime')
def timectime(s):
    return time.ctime(float(s)) # datetime.datetime.fromtimestamp(s)


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
        #data = orm.select_top_celeb_by_followers(c,[number]) #Just Instagram
        data = orm.select_top_celeb_by_followers2(c,[number])  #Instagram+Twitter
        orm.dis_connect((c,conn))
        return render_template('index-cards-3.html', message=number, data=data)
    else:
        celeb_firstname = request.form['searchfirstname']
        celeb_lastname = request.form['searchlastname']
        (c,conn) = orm.do_connect()      
        exists = orm.select_celeb_data_by_name(c,celeb_firstname,celeb_lastname)
        orm.dis_connect((c,conn))
        if exists:    #celeb found
            return redirect(url_for(ranked_list(exists)))
        else:                   #person not found in DB
            (c,conn) = orm.do_connect()      
            new_id = orm.insert_celeb_data(c,[celeb_firstname, celeb_lastname,time.time(), 'user input',time.time(), 'u'])
            conn.commit()
            print('NEW CELEBR ID:',new_id)
            url = 'http://www.instagram.com/'+celeb_firstname+celeb_lastname
            scrape,posts = scraper.get_instagram_data3(url)
            instagram_id = orm.insert_instagram_data(c,[int(new_id),url,scrape[4],scrape[0],\
                        scrape[1],scrape[2],scrape[3],time.time(),scrape[5]])
            conn.commit()
            print('NEW INSTA ID:',instagram_id)
            orm.dis_connect((c,conn))
            time.sleep(5)
            show_celeb_info(int(new_id))

@app.route('/<celeb_id>', methods=['GET', 'POST'])
def show_celeb_info(celeb_id):
    ''' 
    ..Show details of celeb
    '''
    if request.method == 'GET':
        # This is an HTTP GET request.
        print('CELEB-ID:',celeb_id)
        (c,conn) = orm.do_connect()
        celeb_data = orm.return_celeb_info(c,[int(celeb_id)])
        posts_data = orm.return_instagram_posts_info(c,[int(celeb_id)])
        orm.dis_connect((c,conn))
        return render_template("details-cards.html", celeb_data=celeb_data,posts_data=posts_data)
    else:
        pass



@app.route('/ranked_list', methods=['GET', 'POST'])
def ranked_list(celeb_id):
    ''' 
    ..Show details of celeb in ranked list
    '''
    if request.method == 'GET':
        return redirect(url_for(show_celebs))


def tryit():
    (c,conn) = orm.do_connect()
    data = orm.select_top_celeb_by_followers(c,[10])
    print(data)
    orm.dis_connect((c,conn))






if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

