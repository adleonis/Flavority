#!usr/bin/env python3

''' 
SCHEMA
*********************************************************************************
Main script to create DB

'''

import traceback
import sqlite3
import datetime
import time
import collections

########################################################
def create_db(filename):
    ''' 
    Main function to create the sqlite3 database 
    '''
    import sqlite3

    try:
        # Open Connection
        conn = sqlite3.connect(filename)
        c = conn.cursor()

        # CREATE TABLE
        c.execute(
            """CREATE TABLE celeb(
                  id           INTEGER PRIMARY KEY AUTOINCREMENT,
                  firstname    VARCHAR,
                  lastname     VARCHAR,
                  created_on   INTEGER,
                  source       VARCHAR,
                  lastupdate   FLOAT,
                  status       VARCHAR);""")

        c.execute(
            """CREATE TABLE twitter(
                  id           INTEGER PRIMARY KEY AUTOINCREMENT,
                  celeb_id     INTEGER,
                  url          VARCHAR,
                  status       VARCHAR,
                  followers    INTEGER,
                  posts        INTEGER,
                  lastupdate   FLOAT);""")

        c.execute(
            """CREATE TABLE facebook(
                  id           INTEGER PRIMARY KEY AUTOINCREMENT,
                  celeb_id     INTEGER,
                  url          VARCHAR,
                  status       VARCHAR);""")

        c.execute(
            """CREATE TABLE instagram(
                  id           INTEGER PRIMARY KEY AUTOINCREMENT,
                  celeb_id     INTEGER,
                  url          VARCHAR,
                  status       VARCHAR,
                  posts        INTEGER,
                  followers    FLOAT,
                  following    INTEGER,
                  photo_url    VARCHAR,
                  lastupdate   FLOAT);""")

        c.execute(
            """CREATE TABLE instagram_posts(
                  id           INTEGER PRIMARY KEY AUTOINCREMENT,
                  instagram_id INTEGER,
                  user_insta_id INTEGER,
                  post_date    INTEGER,
                  post_likes   INTEGER,
                  post_comments INTEGER,
                  post_caption VARCHAR,
                  post_img_url VARCHAR,
                  lastupdate   FLOAT);""")


        # Commit & Close
        conn.commit()
        c.close()
        conn.close()

        print('    Database', filename, 'was created successfuly')

    except:
        print('Some error occured in function(create_db), call your programmer')
        print(traceback.format_exc())

#******************************************************************************

def remove_dup_celeb(filename):
    ''' 
    Removes duplicate names in celeb table:
    where firstname && lastname match
    '''
    try:
        # Open Connection
        conn = sqlite3.connect(filename)
        c = conn.cursor()
       
        # Get Table Count before removing anything
        pre_total = c.execute(
            """SELECT count(*) FROM celeb;""").fetchall()[0][0]


        # DELETE DUPLICATES
        c.execute(
            """DELETE FROM celeb
               WHERE ID NOT IN
               (
               SELECT MIN(id)
               FROM celeb
               GROUP BY firstname,lastname
               );""")

        # Commit
        conn.commit()
        
        # Get Table count after removal
        post_total = c.execute(
            """SELECT count(*) FROM celeb;""").fetchall()[0][0]

        # Close
        c.close()
        conn.close()

        print(pre_total-post_total, ' duplicates removed')
        print(post_total, ' unique entries currently in DB')

    except:
        print('Some error occured in function(remove_dup_celeb), call your programmer')
        print(traceback.format_exc())






if __name__=='__main__':
    #create_db('toppdog-01.01.db')
    #remove_dup_celeb('toppdog-01.01.db')
