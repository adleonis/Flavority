#!/usr/bin/env python3

''' 
DBLoader
*****************************************************************************************************************
Main routine to load names into DB from various sources 
'''

import scraper, orm

import csv
import datetime 
import time

def load_wikipedia_names(keywords):
    ''' 
    Function which loads wikipedia names into DB
    '''
    success = []
    for keyword in keywords:
        (names, length) = scraper.get_wikipedia_names(keyword)
        id = []
        (c,conn) = orm.do_connect()
        for name in names:
            name.append(name[2]) #add last updated as created_on (for frst time around)
            name.append('u') #add last updated as created_on (for frst time around)
            current_id = orm.insert_celeb_data(c, name) #inserts data & appends ID to list
            id.append(current_id)
            conn.commit()
        orm.dis_connect((c,conn))
        success.append([len(id),length, keyword])    
    
    with open('db_insert_log001.txt', 'a') as f:
        f.write(str(datetime.datetime.now())+'\n')
        f.write('##########################################################################\n')
        for suc in success:
            f.write('{} names out of {} were written from {}\n'.format(suc[0],suc[1],suc[2]))
    

def insert_instagram_info(start,end):
    ''' 
    Gets names from the DB, and tries to get instagram info for that name
    start, end are the primary key IDs in the celeb table
    '''
    counter = 0
    upcounter = 0
    (c,conn) = orm.do_connect()
    for i in range(start,end):
        data = []
        #print('i:',i)
        out = orm.select_celeb_data_by_id(c,[i])
        #print('out:',out)
        if out != False:   #ID exists in celeb table
            #check if celeb already has been scraped
            temp = orm.get_instagram_data(c,[i])
            #print('temp:',temp)
            if temp == False:  #Celeb never been scraped
                url = 'https://www.instagram.com/{}{}'.format(out[1],out[2])
                scrape_result = scraper.get_instagram_data2(url)
                #print('ScrapeResult:',scrape_result[-1])
                #print('ScrapeResult:',scrape_result[-1])
                status = 'u'
    
                if scrape_result != False:     #If scraping worked
                    if scrape_result[-1] == 'true':  #if instagram marked as VERIFIED
                        status = 'v'
                    data.append(i)
                    data.append(url)
                    data.append(status)  # u  = unverified
                    data.append(scrape_result[0])
                    data.append(scrape_result[1])
                    data.append(scrape_result[2])
                    data.append(scrape_result[3])
                    data.append(time.time())
                    orm.insert_instagram_data(c,data)  #insert into DB            
                    conn.commit()
                    counter += 1
                    print('>> DBloader >> Created Instagram info for',out[1],out[2])
                else:                        #If scraping failed
                    data.append(i)            #insert anyway so that 
                    data.append(url)          #we don't scrape it over and over
                    data.append('f')  # u=unverified  f=failed
                    data.append(0)
                    data.append(0)
                    data.append(0)
                    data.append('None')
                    data.append(time.time())
                    orm.insert_instagram_data(c,data)  #insert into DB
                    conn.commit()
                    counter += 1
                    print('>> DBloader >> Scraping failed for',out[1],out[2])
            else:                       #already scraped, update fields
                updata = []
                url = 'https://www.instagram.com/{}{}'.format(out[1],out[2])
                scrape_result = scraper.get_instagram_data2(url)
                print('ScrapeResult:',scrape_result)
                status = 'u'
                if scrape_result != False:     #If scraping worked
                    if scrape_result[-1] == 'true':  #if instagram marked as VERIFIED
                        status = 'v'
                    updata.append(status)
                    updata.append(scrape_result[0])
                    updata.append(scrape_result[1])
                    updata.append(scrape_result[2])
                    updata.append(scrape_result[3])
                    updata.append(time.time())
                    updata.append(temp[0]) #instagram row ID
                    ins = orm.update_instagram_data(c,updata)  #insert into DB
                    conn.commit()
                    upcounter += 1
                    print('>> DBloader >> Updated Instagram info for',out[1],out[2])
                else:                        #If scraping failed
                    pass #don't update anything
        else: #ID not found in celeb table
            print('>> DBloader >> Unable to load name from DB')
        
    orm.dis_connect((c,conn))
    return counter, upcounter



def insert_instagram_info2(start,end):
    ''' 
    Gets names from the DB, and tries to get instagram info for that name
    also now gets the first few posts info and puts that into instagram_posts DB
    start, end are the primary key IDs in the celeb table
    '''
    counter = 0
    upcounter = 0
    (c,conn) = orm.do_connect()
    for i in range(start,end):
        data = []
        out = orm.select_celeb_data_by_id(c,[i])
        if out != False:   #ID exists in celeb table
            #check if celeb already has been scraped
            temp = orm.get_instagram_data(c,[i])
            if temp == False:  #Celeb never been scraped
                url = 'https://www.instagram.com/{}{}'.format(out[1],out[2])
                (scrape_result,posts_result) = scraper.get_instagram_data3(url)
                status = 'u'

                if scrape_result != False:     #If scraping worked
                    if scrape_result[-2] == 'true':  #if instagram marked as VERIFIED
                        status = 'v'
                    data.append(i)
                    data.append(url)
                    data.append(status)  # u  = unverified
                    data.append(scrape_result[0])
                    data.append(scrape_result[1])
                    data.append(scrape_result[2])
                    data.append(scrape_result[3])
                    data.append(time.time())
                    data.append(scrape_result[4])
                    instagram_id = orm.insert_instagram_data(c,data)  #insert into DB
                    orm.insert_instagram_posts_data(c,instagram_id,posts_results)
                    conn.commit()
                    counter += 1
                    print('>> DBloader >> Created Instagram info for',out[1],out[2])
                else:                        #If scraping failed
                    data.append(i)            #insert anyway so that
                    data.append(url)          #we don't scrape it over and over
                    data.append('f')  # u=unverified  f=failed
                    data.append(0)
                    data.append(0)
                    data.append(0)
                    data.append('None')
                    data.append(time.time())
                    data.append(0)
                    orm.insert_instagram_data(c,data)  #insert into DB
                    conn.commit()
                    counter += 1
                    print('>> DBloader >> Scraping failed for',out[1],out[2])
            else:                       #already scraped, update fields
                updata = []
                url = 'https://www.instagram.com/{}{}'.format(out[1],out[2])
                scrape_result,posts_results = scraper.get_instagram_data3(url)
                status = 'u'
                if scrape_result != False:     #If scraping worked
                    if scrape_result[-1] == 'true':  #if instagram marked as VERIFIED
                        status = 'v'
                    updata.append(status)
                    updata.append(scrape_result[0])
                    updata.append(scrape_result[1])
                    updata.append(scrape_result[2])
                    updata.append(scrape_result[3])
                    updata.append(time.time())
                    updata.append(str(scrape_result[5]))
                    updata.append(temp[0]) #instagram row ID
                    passfail = orm.update_instagram_data(c,updata)  #insert into DB
                    orm.insert_instagram_posts_data(c,updata[-1],posts_results)
                    conn.commit()
                    upcounter += 1
                    print('>> DBloader >> Updated Instagram info for',out[1],out[2])
                else:                        #If scraping failed
                    pass #don't update anything
        else: #ID not found in celeb table
            print('>> DBloader >> Unable to load name from DB')
    orm.dis_connect((c,conn))
    return counter, upcounter


def get_and_insert_instagram_info_by_id(c,conn,data):
    ''' 
    Takes a list of celebs and their data, scrapes instagram to update, and saves to DB
    Data should be the output of orm.select_top_celeb_by_followers() or similar output
    '''
    upcounter = 0
    reset_counter = 0
    for line in data:
        updata = []
        url = 'https://www.instagram.com/{}{}'.format(line[2],line[3])
        scrape_result,posts_results = scraper.get_instagram_data3(url)
        status = 'u'
        if scrape_result != False:     #If scraping worked
            if scrape_result[-2] == 'true':  #if instagram marked as VERIFIED
                status = 'v'                    
            updata.append(url)
            updata.append(status)
            updata.append(scrape_result[0])
            updata.append(scrape_result[1])
            updata.append(scrape_result[2])
            updata.append(scrape_result[3])
            updata.append(time.time())
            updata.append(str(scrape_result[5]))
            updata.append(line[0]) #instagram row ID
            passfail = orm.update_all_instagram_data(c,updata)  #insert into DB
            orm.insert_instagram_posts_data(c,updata[-1],posts_results)
            conn.commit()
            upcounter += 1
            print('>> DBloader >> Updated Instagram info for',line[2],line[3], 'ID:',line[0])
        else:                        #If scraping failed
            orm.reset_instagram_stats_by_id(c,line[0])
            reset_counter += 1
    return upcounter, reset_counter


def update_instagram_slice(from_celeb_rank,to_celeb_rank):
    ''' 
    Updates the instagram info from the top of the list down ranked by # followers
    Ex: to update the top 50 celebs, (0,49)
        to update the next 50, (50,100)
    '''
    (c,conn) = orm.do_connect()
    data = orm.select_top_celeb_by_followers(c, [to_celeb_rank])
    out = get_and_insert_instagram_info_by_id(c,conn,data[from_celeb_rank:])
    orm.dis_connect([c,conn])
    print('Celebs updated:',out[0], 'Celebs reset:',out[1])





def get_and_insert_twitter_info_by_id(c,conn,data):
    ''' 
    Takes a list of celebs and their data, scrapes twitter to update, and saves to DB
    Data should be the output of orm.select_top_celeb_by_followers() or similar output
    '''
    upcounter = 0
    reset_counter = 0
    for line in data:
        updata = []
        url = 'https://www.twitter.com/{}{}'.format(line[2],line[3])
        scrape_result = scraper.get_twitter_data(url)
        if scrape_result != False:     #If scraping worked
            updata.append(line[0])
            updata.append(url)
            updata.append(scrape_result[5])
            updata.append(scrape_result[0])
            updata.append(scrape_result[1])
            updata.append(scrape_result[2])
            updata.append(scrape_result[3])
            updata.append(scrape_result[4])
            updata.append(time.time())
            passfail = orm.insert_twitter_data(c,updata)  #insert into DB
            conn.commit()
            upcounter += 1
            print('>> DBloader >> Inserted TWITTER info for',line[2],line[3], 'ID:',line[0])
        else:                        #If scraping failed
            #orm.reset_instagram_stats_by_id(c,line[0])
            reset_counter += 1
    return upcounter, reset_counter


def insert_twitter_slice(from_celeb_rank,to_celeb_rank):
    ''' 
    Updates the instagram info from the top of the list down ranked by # followers
    Ex: to update the top 50 celebs, (0,49)
        to update the next 50, (50,100)
    '''
    (c,conn) = orm.do_connect()
    data = orm.select_top_celeb_by_followers(c, [to_celeb_rank])
    out = get_and_insert_twitter_info_by_id(c,conn,data[from_celeb_rank:])
    orm.dis_connect([c,conn])
    print('Celebs updated:',out[0], 'Celebs reset:',out[1])







if __name__ == "__main__":

    
    
    #input = ['List_of_American_film_actresses','List_of_American_television_actresses']
    #inputs = ['List_of_Harper%27s_Bazaar_US_cover_models',\
    #           'List_of_Allure_cover_models',
    #            'List_of_Harper%27s_Bazaar_Brazil_cover_models',
    #            'List_of_Marie_Claire_cover_models',
    #            'List_of_Vogue_(US)_cover_models']
    
    #inputs = ['Forbes_Celebrity_100',\
    #            'List_of_film_and_television_directors',\
    #            'List_of_female_film_and_television_directors',
    #            'The_World%27s_Billionaires',\
    #            'List_of_people_from_New_York_(state)',
    #            'List_of_people_from_Alabama']
    
    ''' 
    inputs = ['List_of_YouTubers',\
              'List_of_people_from_Alaska',\
              'List_of_people_from_Arizona',\
              'List_of_people_from_Arkansas',\
              'List_of_people_from_California',\
              'List_of_people_from_Colorado',\
              'List_of_people_from_Connecticut',\
              'List_of_people_from_Delaware',\
              'List_of_people_from_Florida',\
              'List_of_people_from_Georgia',\
              'List_of_people_from_Hawaii',\
              'List_of_people_from_Idaho',\
              'List_of_people_from_Illinois',\
              'List_of_people_from_Indiana',\
              'List_of_people_from_Iowa',\
              'List_of_people_from_Kansas',\
              'List_of_people_from_Kentucky',\
              'List_of_people_from_Lousiana',\
              'List_of_people_from_Maine',\
              'List_of_people_from_Maryland',\
              'List_of_people_from_Massachusetts',\
              'List_of_people_from_Michigan',\
              'List_of_people_from_Minnesota',\
              'List_of_people_from_Mississippi',\
              'List_of_people_from_Missouri',\
              'List_of_people_from_Montana',\
              'List_of_people_from_Nebraska',\
              'List_of_people_from_Nevada',\
              'List_of_people_from_New_Hampshire',\
              'List_of_people_from_New_Jersey',\
              'List_of_people_from_New_Mexico',\
              'List_of_people_from_North_Carolina',\
              'List_of_people_from_North_Dakota',\
              'List_of_people_from_Ohio',\
              'List_of_people_from_Oklahoma',\
              'List_of_people_from_Oregon',\
              'List_of_people_from_Pennsylvania',\
              'List_of_people_from_Rhode_Island',\
              'List_of_people_from_South_Carolina',\
              'List_of_people_from_South_Dakota',\
              'List_of_people_from_Tennessee',\
              'List_of_people_from_Texas',\
              'List_of_people_from_Utah',\
              'List_of_people_from_Vermont',\
              'List_of_people_from_Virginia',\
              'List_of_people_from_Washington',\
              'List_of_people_from_West_Virginia',\
              'List_of_people_from_Wisconsin',\
              'List_of_people_from_Wyoming']
    ''' 

    #load_wikipedia_names(inputs)
    
    #b = insert_instagram_info2(10000,34237)
    #b = insert_instagram_info(960,5295)
    #print(b)

    #
    update_instagram_slice(0,1000)
    #insert_twitter_slice(1001,30000)
