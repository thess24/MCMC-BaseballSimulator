import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import urllib2
import unicodedata


os.chdir('C:\Users\Taylor\Desktop')
year = [2012,2013,2014,2015]
headers = {'User-agent': 'Mozilla/5.0'}



def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def get_player_link_list(typeofplayer):
    ''' gets link list of players for either batters or pitchers from the past year'''
    
    if typeofplayer =='batter':
        # this is a list of links for batters with stats from past 365 days
        plist = 'http://www.baseball-reference.com/leagues/daily.cgi?user_team=&bust_cache=&type=b&dates=lastndays&lastndays=365&level=mlb&franch=&stat=&stat_value=0'
    
    elif typeofplayer=='pitcher':
        # and the pitchers
        plist = 'http://www.baseball-reference.com/leagues/daily.cgi?user_team=&bust_cache=&type=p&dates=lastndays&lastndays=365&since=2012-07-10&fromandto=2015-07-01.2015-07-31&level=mlb&franch=&stat=&stat_value=0'
        
    else:
        raise Exception
        
    linklist = []
    baselink = 'http://www.baseball-reference.com'
    
    req= requests.get(plist)
    reqtext = req.text
    soup= BeautifulSoup(reqtext)
    
    table = soup.find('table', attrs={'id':'daily'})
    anchors = table.find_all('a')
    
    for a in anchors:
        url = str(baselink) + str(a.get('href'))
        linklist.append(url)
    
    return linklist[::2] # every other item in list



def get_redirected_url(url):
    '''player link redirects - we need redirected link to get player id'''
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    request = opener.open(url)
    return request.url


def get_player_ids(player_list):
    '''takes player link list and returns player id list'''
    playeridlist = []
    count = 0
    
    for b in player_list:
        redirect =  get_redirected_url(b)
        bid= redirect.split('/')[-1].split('.')[0]  # will output player id
        playeridlist.append(bid)
        count+=1
        print '{} - {}'.format(count, bid)
    
    playeridlist = filter(lambda a: a != 'player', playeridlist)
    return playeridlist



def get_stats_from_soup_table(soup,name,playerid,year,throws,bats,tablename,filename,tablerows = 2):
    ''' writes stats data to csv file from scraped data'''
    table = soup.find('table', attrs={'id':tablename})
    
    if table:
        if len(table.find_all('tr'))>2:
            for i in range(tablerows):
                try:
                    csvrow = [name,playerid,year,throws,bats]
                    row =  table.find_all('tr')[i+1].find_all('td')
                    for r in row:
                        csvrow.append(r.string)
                        
                    with open(filename, 'ab') as f:
                        writer = csv.writer(f)
                        writer.writerow(csvrow)
                except:
                    continue
                    


def get_basic_stats_from_soup(soup):
    ''' returns basic data on a player from scraped data '''
    
    name = soup.find('span', attrs={'itemprop':'name'}).string
    name = strip_accents(name)
    
    infobox = soup.find('div', attrs={'id':'info_box'})
    throwstring = str(infobox.find_all('p')[2])
    
    # throwing hand
    thrstart = re.search("Throws",throwstring)
    shortthrow = throwstring[thrstart.start():]
    
    if shortthrow.find("Right") >0:
        throws="Right"
    else:
        throws="Left"
        
    # batting hand
    batstart = re.search("Bats",throwstring)
    shortbat = throwstring[batstart.start():batstart.start()+22]  
    
    if shortbat.find("Right") >0:
        bats="Right"
    elif shortbat.find("Left") >0:
        bats="Left"
    else:
        bats='Switch'
    
    return name,throws,bats
    
    
    
def get_soup(player,year,playertype):
    ''' scrapes data for a given year for a player'''
    
    if playertype =='pitcher':
        site = 'http://www.baseball-reference.com/players/split.cgi?id='+str(player)+'&year='+str(year)+'&t=p'
    elif playertype =='batter':
        site = 'http://www.baseball-reference.com/players/split.cgi?id='+str(player)+'&year='+str(year)+'&t=b'
    else:
        raise Exception
        
    req= requests.get(site,headers=headers)
    reqtext = req.text
    soup= BeautifulSoup(reqtext)
    
    #this is the year, scraped from header
    webpage_year = int(soup.find('div', attrs={'id':'piData'}).find('h2').string[:4])  
    
    if webpage_year != year:
        raise Exception
    
    return soup
    


print 'Gathering list of pitchers...' 
pitcher_link_list = get_player_link_list('pitcher')
print '{} pitchers'.format(len(pitcher_link_list))

print 'Gathering list of batters...' 
batter_link_list = get_player_link_list('batter')
print '{} batters'.format(len(batter_link_list))

print 'Getting list of player id\'s from list of players' 
pitcher_ids = get_player_ids(pitcher_link_list)
batter_ids = get_player_ids(batter_link_list)

print 'Starting to scrape batter data...'
for b in batter_ids:
    print 'Scraping Batter: {}'.format(b)
    for y in year:
        try:
            soup = get_soup(b,y,'batter')
            print y
        except:
            continue
        
        try:
            name,throws,bats = get_basic_stats_from_soup(soup)
        except:
            continue
    
        get_stats_from_soup_table(soup, name, b, y, throws, bats,'plato','batters_stats.csv')
        get_stats_from_soup_table(soup, name, b, y, throws, bats,'hmvis','batters_stats.csv')
        get_stats_from_soup_table(soup, name, b, y, throws, bats,'power','batters_stats.csv',tablerows=3)
        
print 'Starting to scrape pitcher data...'
for p in pitcher_ids:
    print 'Scraping Pitcher: {}'.format(p)
    for y in year:
        try:
            soup = get_soup(p,y,'pitcher')
            print y
        except:
            continue
        
        try:
            name,throws,bats = get_basic_stats_from_soup(soup)
        except:
            continue
    
        get_stats_from_soup_table(soup,name,p,y,throws,bats,'plato','pitchers_stats.csv')
        get_stats_from_soup_table(soup,name,p,y,throws,bats,'hmvis','pitchers_stats.csv')
        
print 'Done!'