#!usr/bin/env python3

# Wrapper to handle I/O to from database

# REMEMBER TO OPEN A CURSOR FIRST TO PASS, THEN CLOSE
# ONLY THE CREATE DB function does that for you

# Functions Available
#    io_wrapper.
#             * do_connect()
#             * dis_connect()
#             * create_db(filename)

import traceback
import sqlite3
import datetime
import time
import collections


# CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
def do_connect():
    database = 'toppdog-01.01.db'
    conn = sqlite3.connect(database, check_same_thread=False)
    out = (conn.cursor(), conn)
    return out


# CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
def dis_connect(inn):
    try:
        conn = inn[1]
        c = inn[0]
        # conn.commit() ##remember this is off!!!
        c.close()
        conn.close()
        return True
    except:
        return False


# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD


def insert_celeb_data(c, data):
    ''' 
    INSERT DATA INTO TABLE CELEB
    data=[firstname,lastname,created_on,source,lastupdate,status]
    RETURNS created user ID if data correctly inserted, False if error
    ''' 
    try:
        c.execute(
            '''INSERT INTO celeb(
            firstname,
            lastname,
            created_on,
            source,
            lastupdate,
            status
            )
            VALUES(
            ?,
            ?,
            ?,
            ?,
            ?,
            ?);''', data)

        created_id = c.execute('SELECT MAX(id) FROM celeb;').fetchall()[0][0]
        return created_id
    except:
        return False



def select_celeb_data_by_id(c, id):
    ''' 
    SELECT DATA FROM TABLE CELEB BY ID
    data=[id,firstname,lastname,created_on,source,lastupdate,status]
    RETURNS data if correct, else return False
    '''
    try:
        data = c.execute('''SELECT * FROM 
                         celeb WHERE id=?;''', id).fetchall()[0]
        return data
    except:
        return False


def get_instagram_data(c,celeb_id):
    ''' 
    Gets instagram data by Celeb ID
    '''
    try:
        data = c.execute('''SELECT * FROM
                         instagram WHERE celeb_id=?;''', celeb_id).fetchall()[0]
        return data
    except:
        return False


def insert_instagram_data(c,data):
    ''' 
    Inserts instagram info for a specified user ID
    '''
    try:
        c.execute(
            '''INSERT INTO instagram(
            celeb_id,
            url,
            status,
            posts,
            followers,
            following,
            photo_url,
            lastupdate,
            insta_id)
            VALUES(
            ?,?,?,?,?,?,?,?,?);''', data)

        created_id = c.execute('SELECT MAX(id) FROM instagram;').fetchall()[0][0]
        print(">> DB.INSTAGRAM >> new row inserted >> ID:",created_id) 
        return created_id
    except: 
        return False



def update_instagram_data(c,data):
    ''' 
    Updates instagram info for a specified user ID
    data = [status,posts,followers,following,photo_url,lastupdate, celeb_id]
    id is primary key from celeb table
    '''
    #print('DATAIN:',data)
    try:
        print(data)
        c.execute('''UPDATE instagram SET
            status=?,
            posts=?,
            followers=?,
            following=?,
            photo_url=?,
            lastupdate=?,
            insta_id
            WHERE celeb_id=?;''',data)

        print(">> DB.INSTAGRAM >> row updated >> CELEB ID:",data[-1])
        return True
    except:
        return False


def select_top_celeb_by_followers(c, num):
    ''' 
    SELECT CELEBS with most Followers
    data=[id,firstname,lastname,created_on,source,lastupdate,status]
    RETURNS data if correct, else return False
    '''
    try:
        data = c.execute('''SELECT  firstname,
                                    lastname,
                                    instagram.followers,
                                    instagram.posts,
                                    instagram.following,
                                    instagram.photo_url
                            FROM celeb JOIN instagram ON 
                                    celeb.id=instagram.celeb_id
                            ORDER BY instagram.followers DESC LIMIT ?;''', num).fetchall()
        return data
    except:
        return False



def insert_instagram_posts_data(c,instagram_id,data):
    ''' 
    Inserts instagram post info for a specified instagram ID
    '''
    try:
        for key,values in data:
            c.execute(
            '''INSERT INTO instagram_posts(
            instagram_id,
            user_insta_id,
            post_date,
            post_likes,
            post_comments,
            post_caption,
            post_img_url,
            lastupdate)
            VALUES(
            ?,?,?,?,?,?,?,?);''', instagram_id, key,int(values[0]),int(values[1]),int(values[2]),values[3],values[4],int(values[5]))

        created_id = c.execute('SELECT MAX(id) FROM instagram_posts;').fetchall[0][0]
        print(">> DB.INSTAGRAM.POSTS >> new row inserted >> ID:",created_id)
        return created_id
    except:
        return False





















###### OLD ########## PREVIOUS PROBLEM ############## DISREGARD #####



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# UPDATED
def insert_users_data(c, data):
    # data=[balance, type, created_on]
    # INSERT DATA INTO TABLES
    # RETURNS created user ID if data correctly inserted, False if error
    try:
        c.execute(
            '''INSERT INTO users(
            balance,
            type,
            created_on
            )
            VALUES(
            ?,
            ?,
            ?
            );''', data)

        created_id = c.execute('SELECT MAX(id) FROM users;').fetchall()[0][0]
        return created_id
    except:  # TODO since the except is sometimes used in the model to check if users
        # already exist, catch various exceptions depending on code
        # print('An error has occured trying to insert data into the Users table of the DB')

        # print(traceback.format_exc())
        return False


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# NEW
def insert_secure_data(c, data):
    # data=[user_id,pass,last_login]
    # INSERT DATA INTO TABLES
    # RETURNS created key ID from SECURE table if data correctly inserted, False if error
    try:
        c.execute(
            '''INSERT INTO secure(
            user_id,
            pass,
            last_login
            )
            VALUES(
            ?,
            ?,
            ?
            );''', data)

        created_id = c.execute('SELECT MAX(id) FROM secure;').fetchall()[0][0]
        return created_id
    except:  # TODO since the except is sometimes used in the model to check if users
        # already exist, catch various exceptions depending on code
        # print('An error has occured trying to insert data into the Users table of the DB')

        # print(traceback.format_exc())
        return False


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# NEW
def get_secure_hash_for_user(c, ID):
    # INPUT ID is of type list... [ID]  <--- USER ID NOT SECURE TABLE ID
    # Returns: hash as a type<VARCHAR>
    #
    try:
        out = c.execute('''SELECT pass FROM secure WHERE user_id=?;''', ID).fetchall()[0][0]
        return out
    except:
        print('''    LOG >>  ORM >> An error has occured trying to get data in the
                SECURE table of the DB: get_secure_hash_for_user''')
        # print(traceback.format_exc())
        return False


# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# UPDATED
def insert_positions_data(c, data):
    # data=[user_id, ticker, amount, shares]
    # RETURNS newly created account ID if data correctly inserted, False if error
    try:
        c.execute(
            '''INSERT INTO positions(
                user_id,
                ticker,
                amount,
                shares
                )
                VALUES(
                ?,
                ?,
                ?,
                ?
                );''', data)

        created_id = c.execute('SELECT MAX(id) FROM positions;').fetchall()[0][0]
        return created_id
    except:
        print('''An error has occured trying to insert data into the
                Positions table of the DB''')
        print(traceback.format_exc())
        return False
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# NEW
def insert_transactions_data(c, data):
    # data=[user_id,position_id,buy_flag,shares,share_price,tstamp]
    # RETURNS newly created account ID if data correctly inserted, False if error
    try:
        c.execute(
            '''INSERT INTO trans(
                user_id,
                position_id,
                buy_flag,
                shares,
                share_price,
                ts
                )
                VALUES(
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
                );''', data)

        created_id = c.execute('SELECT MAX(id) FROM trans;').fetchall()[0][0]
        return created_id
    except:
        print('''An error has occured trying to insert data into the
                Trans table of the DB''')
        print(traceback.format_exc())
        return False


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT


# IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
# updated
def update_user_balance(c, data):
    # ID is the user id
    # data = [balance, id] (type:list)
    # RETURNS True if data correctly updated, False if error
    try:
        c.execute(
            '''UPDATE users SET
            balance=?
            WHERE
            ID=?;''', data)
        return True
    except:
        print('''An error has occured trying to update the balance in the
                Users table of the DB''', data[1])
        print(traceback.format_exc())
        return False


# IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

# UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU
# NEW
def update_position(c, data):
    # id is the table primary key  <-----position ID
    # data = [amount, shares, ticker]
    try:
        c.execute(
            '''UPDATE positions SET
            amount=?,
            shares=?
            WHERE
            ticker=?;''', data)
        print('    LOG >> ORM   >> Position Update OK')
        return True
    except:
        print('''An error has occured trying to update data in the
                Positions table of the DB, Position Ticker:''', data[2])
        print(traceback.format_exc())
        return False


# UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU


# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# UPDATED
def get_user_permission(c, ID):
    # INPUT ID is of type list... [ID]
    # Returns: permission level as a type<str>
    #
    try:
        return c.execute('SELECT type FROM users WHERE id=?;', ID).fetchall()[0][0]
    except:
        # print("An error has occured trying to get data in the USERS table of the DB: get_user_permission")
        # print(traceback.format_exc())
        dataout = 'unacredited'
        return dataout


# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS


# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# NEW - FLASK
def get_user_all(c, ID):
    # INPUT ID is of type list... [ID]
    # Returns: all user info for instantiation
    #
    try:
        return c.execute('SELECT * FROM users WHERE id=?;', ID).fetchall()[0]
    except:
        # print("An error has occured trying to get data in the USERS table of the DB: get_user_p$
        # print(traceback.format_exc())
        #dataout = 'unacredited'
        return None


# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS


# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# updated
def get_user_balance(c, ID):
    # INPUT ID is of type list... [ID]  <--- ACCOUNT ID not USER ID
    # Returns: balance as a type<float>
    #
    try:
        return c.execute('''SELECT balance FROM users WHERE id=?;''', ID).fetchall()[0][0]
    except:
        print('''An error has occured trying to get data in the
                USERS table of the DB: get_user_balance''')
        print(traceback.format_exc())
        return False


# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
# NEW
def get_positions(c, ID):
    # INPUT ID is of type list... [ID]  <--- USER ID
    # Returns: all open positions type<[list]>
    #
    try:
        ans = c.execute(
            '''SELECT ticker,shares,amount FROM positions WHERE user_id=? AND shares>0 GROUP BY ticker ORDER BY ticker;''',
            ID).fetchall()
        positions = {}
        for i in ans:
            positions[i[0]] = [i[1], i[2]]
        return positions
    except:
        print('''An error has occured trying to get data in the
                POSITIONS table of the DB: get_positions''')
        print(traceback.format_exc())
        return False


# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD


# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
# NEW
def get_position_id(c, ticker):
    # INPUT ticker is of type list... [ticker]  <---  position ticker
    # Returns: corresponding ID
    #
    try:
        ans = c.execute('''SELECT id FROM positions WHERE ticker=?;''', ticker).fetchall()[0][0]
        return ans
    except:
        print('''An error has occured trying to get data in the
                POSITIONS table of the DB: get_position_id''')
        print(traceback.format_exc())
        return False


# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD


# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
# NEW
def get_position_id_foruser(c, data):
    # INPUT ticker is of type list... [ticker]  <---  position ticker
    # user id is the user's id
    # Returns: corresponding ID
    # data = [ticker, userid]
    try:
        ans = c.execute('''SELECT id FROM positions WHERE ticker=? AND user_id=?;''', data).fetchall()[0][0]
        return ans
    except:
        print('''An error has occured trying to get data in the
                POSITIONS table of the DB: get_position_id''')
        print(traceback.format_exc())
        return False


# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# NEW
def get_transactions(c, ID):
    # INPUT ID is of type list... [ID]  <--- USER ID
    # Returns: all user transactions type<[list]>
    #
    try:
        ans = c.execute(
            '''SELECT id,position_id,buy_flag,shares,share_price,ts FROM trans WHERE user_id=? AND shares>0 ORDER BY ts;''',
            ID).fetchall()
        transactions = {}
        for i in ans:
            transactions[i[0]] = [i[1], i[2], i[3], i[4], i[5]]
        return transactions
    except:
        print('''An error has occured trying to get data in the
                TRANS table of the DB: get_transactions''')
        print(traceback.format_exc())
        return False


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def get_all_users(c, permission_level):
    # Permission level is of type list... [permission_level]  <--- ['Client'] or ['banker']
    # Returns: all user IDs of Clients type<[list]>
    #
    try:
        ans = c.execute('''SELECT id FROM users WHERE permission_level=? ORDER BY id;''', permission_level).fetchall()
        accounts = []
        for i in ans:
            accounts.append(i[0])
        return accounts
    except:
        print('''An error has occured trying to get data in the
                USERS table of the DB: get_all_users''')
        print(traceback.format_exc())
        return False


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# NEW -- SUPER USER FUNC ONLY
def sup_get_user_stats(c):
    # Returns: all user positions type<[list]>
    #
    try:
        ans = c.execute('''SELECT id,position_id,buy_flag,shares,share_price,ts
                         FROM trans WHERE user_id=? AND shares>0
                         ORDER BY ts;''', ID).fetchall()
        transactions = {}
        for i in ans:
            transactions[i[0]] = [i[1], i[2], i[3], i[4], i[5]]
        return transactions
    except:
        print('''An error has occured trying to get data in the
                TRANS table of the DB: get_transactions''')
        print(traceback.format_exc())
        return False


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT

# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# NEW -- SUPER USER FUNC ONLY
def sup_get_pnl(c):
    # Returns: all users, held amount, balance amount, pnl<[list]>
    #
    try:
        ans = c.execute('''SELECT * FROM sup_users_pnl
                         ORDER BY pnl DESC;''').fetchall()
        transactions = collections.OrderedDict()
        for i in ans:
            transactions[i[0]] = [i[1], i[2], i[3]]
        return transactions
    except:
        print('''An error has occured trying to get data in the
                SUP_USERS_PNL VIEW of the DB: sup_get_pnl''')
        print(traceback.format_exc())
        return False


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT


# UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU
# SUPER USER FUNC ONLY :  update AMOUNT row with new shareprice data
def sup_update_all_positions_amount(c, data):
    # data = [amount, id]   <--- ID is positions ID
    try:
        c.execute(
            '''UPDATE positions SET
            amount=?
            WHERE
            id=?;''', data)
        print('    LOG >> ORM   >> SUP >> Position Price Updated >> ID:', data[1])
        return True
    except:
        print('''An error has occured trying to update data in the
                Positions table of the DB, Position ID:''', data[1])
        print(traceback.format_exc())
        return False


# UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU


# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
# SUPERUSER FUNC ONLY
def sup_get_position_info(c, data):
    # data = [id]
    try:
        ans = c.execute('''SELECT ticker,shares FROM positions WHERE id=?;''', data).fetchall()[0]
        return ans
        # ans = (ticker, shares) tuple
    except:
        print('''An error has occured trying to get data in the
                POSITIONS table of the DB: sup_get_position_info''')
        print(traceback.format_exc())
        return False


# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD


# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
# SUPERUSER FUNC ONLY
def sup_get_positions_tablesize(c):
    # data = [id]
    try:
        ans = c.execute('''SELECT COUNT (*) FROM positions;''').fetchall()[0][0]
        return ans
        # ans = number of rows in positions table
    except:
        print('''An error has occured trying to get data in the
                POSITIONS table of the DB: sup_get_positions_tablesize''')
        print(traceback.format_exc())
        return False


# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD


if __name__ == '__main__':
    print(
        'Running this will create a new DB called stock.db, if necessary remove any old files called stock.db beforehand, are you sure?(Y/N)')
    in_put = input()
    if in_put.upper() == 'Y':
        # print('Name your database file(with extension):')
        # db_name = input()
        create_db('stock.db')
        create_secure_table('stock.db')
        dbviews.sup_users_balances()
        dbviews.sup_users_pnl()
    else:
        print('Goodbye')



