#!/usr/bin/env python3

''' 
SCRAPER
*****************************************************************************************************************
Handles the background scraping of account info
Each scpare function has been iteratively improved, just look for the one with the largest number 
i.e. get_something3() is better than get_something2() 

The strategy to get data has been:
    1.  call get_wikipedia_names on a whole bunch of pages (see list at bottom of scraper, 
        under if __name__='__main__'
    2.  once these names are in DB, call schema.remove_dup_celeb() to remove duplicates
    3.  with that subset, call get_instagram() & get_twitter() to get data every x minutes 

'''

import requests
import json
import time
from bs4 import BeautifulSoup
import re




def get_wikipedia_names(keyword):
    ''' 
    Gets [firstname, lastname, unixtime, sourceurl] from 
    a wikipedia input list page of names  
    try: keyword='List_of_American_film_actresse'
    '''
    endpoint = 'https://en.wikipedia.org/api/rest_v1/page/html/{}?redirect=false'.format(keyword)
    time.sleep(0.0051)  #to comply with Wikipedia's rate in case someone calls this recursively
    output = requests.get(endpoint).text
    soup = BeautifulSoup(output, 'html.parser')
    lines = soup.find_all(rel="mw:WikiLink")
    insertime = time.time()
    source = endpoint
    names = []
    for line in lines:
        try:
            lin = line.text.split(' ')
            lin.append(insertime)
            lin.append(source)
            names.append(lin) #,source,insertime)
        except:
            pass
    
    return names,len(names)



def get_instagram_data(url):
    ''' 
    Gets instagram data from a name-based URL
    Returns [posts, followers, following, photo_url] if everything went well
    Return False if something failed
    '''
    time.sleep(0.25)  #try and increase until they ban IP
                   #banned @ 0.05
    try: 
        output = requests.get(url).text
        soup = BeautifulSoup(output, 'html.parser')
        photo_url = str(soup.find(property="og:image")).split(' ')[1][9:-1]
        dataline = str(soup.find(property="og:description"))
        followers = str(re.findall(r'content="(.*?) Followers',dataline)[0])
        if followers[-1] == 'm':
            followers = float(followers[:-1])*1000000
        elif followers[-1] == 'k':
            followers = float(followers[:-1])*1000
        else:
            followers = float(followers)    
        following = int(re.findall(r'Followers, (.*?) Following,',dataline)[0])
        posts = int(re.findall(r'Following, (.*?) Posts',dataline)[0])
        return [posts, followers, following, photo_url]
    except:
        return False


def get_instagram_data2(url):
    ''' 
    Gets instagram data from a name-based URL
    Returns [posts, followers, following, photo_url(HD),verifiedstatus] if everything went well
    Return False if something failed
    '''
    time.sleep(0.25)  #try and increase until they ban IP
                      #banned @ 0.05
    try:
        output = requests.get(url).text
        soup = BeautifulSoup(output, 'html.parser')
        photo_url = str(soup.find(property="og:image")).split(' ')[1][9:-1]
        desc_line = str(soup.find(property="og:description"))
        dataline = str(soup.find_all(type="text/javascript")[3])
        followers = float(re.findall(r'"count":(.*?)}',dataline)[0])
        following = float(re.findall(r'"count":(.*?)}',dataline)[1])
        photo_url_hd = str(re.findall(r'"profile_pic_url_hd":"(.*?)"',dataline)[0])
        posts = str(re.findall(r'Following, (.*?) Posts',desc_line)[0])
        if len(posts) > 3:
            posts = float("".join(posts.split(',')))
        
        if photo_url_hd:
            photo = photo_url_hd
        else:
            photo = photo_url
        status = str(re.findall(r'"is_verified":(.*?),',dataline)[0])
                


        return [int(posts), followers, int(following), photo, status]
    except:
        return False



def get_instagram_data3(url):
    ''' 
    Gets instagram data from a name-based URL
    Returns [posts, followers, following, photo_url(HD),verifiedstatus] if eve$
    Return False if something failed
    '''
    time.sleep(0.20)  #try and increase until they ban IP
                      #banned @ 0.05
    try:
    #if True:
        ### GET user info totals
        output = requests.get(url).text
        soup = BeautifulSoup(output, 'html.parser')
        photo_url = str(soup.find(property="og:image")).split(' ')[1][9:-1]
        desc_line = str(soup.find(property="og:description"))
        dataline = str(soup.find_all(type="text/javascript")[3])
        followers = float(re.findall(r'"count":(.*?)}',dataline)[0])
        following = float(re.findall(r'"count":(.*?)}',dataline)[1])
        photo_url_hd = str(re.findall(r'"profile_pic_url_hd":"(.*?)"',dataline)[0])
        posts = str(re.findall(r'Following, (.*?) Posts',desc_line)[0])
        insta_user_id = int(re.findall(r'"owner":{"id":"(.*?)"',dataline)[0])
        if len(posts) > 3:
            posts = float("".join(posts.split(',')))

        if photo_url_hd:
            photo = photo_url_hd
        else:
            photo = photo_url
        status = str(re.findall(r'"is_verified":(.*?),',dataline)[0])

        ### Trying to get POSTS info
        post_comments = re.findall(r'"comments":{"count":(.*?)}',dataline)
        post_likes = re.findall(r'"likes":{"count":(.*?)}',dataline)        
        post_imgs = re.findall(r'"thumbnail_src":"(.*?)"',dataline)        
        post_codes = re.findall(r'"code":"(.*?)"',dataline)        
        post_dates = re.findall(r'"date":(.*?),',dataline)        
        post_caption = re.findall(r'"caption":"(.*?)"',dataline)        
                

        posts_dict = {}
        if len(post_codes) > 0:
            for i in range(len(post_codes)):
                try:
                    posts_dict[post_codes[i]] = [post_dates[i],post_likes[i],post_comments[i],post_caption[i],post_imgs[i],time.time()]
                except:
                    pass


        return [int(posts), followers, int(following), photo, status,insta_user_id],posts_dict
    except:
        return False,False



def get_twitter_data(url):
    ''' 
    Gets TWITTER data from a name-based URL
    Returns [posts, followers, following, photo_url(HD),verifiedstatus] if eve$
    Return False if something failed
    '''
    time.sleep(0.20)  #try and increase until they ban IP
    try:
    #if True:
        ### GET user info totals
        output = requests.get(url).text
        soup = BeautifulSoup(output, 'html.parser')
        photo_url = re.findall(r'class="ProfileAvatar-image " src="(.*?)"',str(soup.find_all('img')))[0]
        profile_link = re.findall(r'href="(.*?)"',str(soup.find_all(class_="ProfileCardMini-screenname")))

        dataline = str(soup.find(class_="ProfileNav"))

        twitter_id = re.findall(r'data-user-id="(.*?)"',dataline)[0]
        metrics = re.findall(r'data-count=(.*?) data-is-compact=',dataline)
        followers = metrics[2][1:-1]
        tweets = metrics[0][1:-1]
        following = metrics[1][1:-1]
        likes = metrics[3][1:-1]

        account = str(soup.find(class_="ProfileHeaderCard-name"))
        status_text = str(re.findall(r'span class="Icon Icon(.*?)"',account))
        if status_text.find('hidden') == '-1':
            status = 'u'
        else:
            status = 'v'

        created_on_text = str(soup.find(class_="ProfileHeaderCard-joinDateText js-tooltip u-dir"))
        created_on = str(re.findall(r'title="(.*?)"',created_on_text)[0])

        outside_link_text = str(soup.find(class_="ProfileHeaderCard-urlText u-dir"))
        outside_link = str(re.findall(r'title="(.*?)"',outside_link_text)[0])

        return [int(tweets),int(followers), int(following), int(likes), photo_url, status,twitter_id,created_on,outside_link]
    except:
        return False






''' FROM A PREVIOUS PROLEM, HERE AS EXAMPLE IN CASE
def get_quote(ticker_symbol):
    time.sleep(0.25)  #in case there's a rate limiter
    quote_endpoint = 'http://dev.markitondemand.com/MODapis/Api/v2/Quote/json?symbol={}'.format(ticker_symbol)
    full_json = json.loads(requests.get(quote_endpoint).text)  #write error handler to control for one o$
    quote = {}
    quote['Name'] = full_json['Name']
    quote['Symbol'] = full_json['Symbol']
    quote['LastPrice'] = full_json['LastPrice']
    quote['Change'] = full_json['Change']
    quote['ChangePercent'] = full_json['ChangePercent']
    quote['MarketCap'] = full_json['MarketCap']
    quote['Volume'] = full_json['Volume']
    quote['ChangeYTD'] = full_json['ChangeYTD']
    quote['ChangePercent'] = full_json['ChangePercent']
    quote['High'] = full_json['High']
    quote['Low'] = full_json['Low']
    quote['Open'] = full_json['Open']
    return quote
'''


if __name__ == '__main__':
    #print(endpoint)
    #time.sleep(1)
    #keyword = 'List_of_Harper%27s_Bazaar_US_cover_models'
    #print(get_wikipedia_names(keyword))
    #out = get_instagram_data2('https://www.instagram.com/ZooeyDeschanel')
    #out = get_instagram_data3('https://www.instagram.com/EmilyDeschanel')
    out = get_twitter_data('https://www.twitter.com/MileyCyrus')
    print(out)
    #pass
