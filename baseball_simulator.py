# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import division
import numpy as np
import itertools
import pandas as pd
import os
from teams import *
import matplotlib.pyplot as plt




# Settings
gamelog = False
logtofile = True
use_parkfactor = True


sim_number = 1000
park_factors = {'Red Sox':1.047,'Rockies':1.045,'Giants':1.041,'Orioles':1.04,'Cubs':1.039,'Angels':1.037,'Diamondbacks':1.025,'Royals':1.021,'White Sox':1.017,'Marlins':1.016,'Indians':1.015,'Cardinals':1.013,'Dodgers':1.013,'Rangers':1.012,'Yankees':1.011,'Tigers':1.002,'Astros':0.998,'Pirates':0.997,'Phillies':0.991,'Reds':0.985,'Nationals':0.981,'Mariners':0.974,'Twins':0.974,'Rays':0.972,'Brewers':0.971,'Mets':0.966,'Braves':0.962,'Blue Jays':0.957,'Athletics':0.949,'Padres':0.939}
league_obpa = .3165
league_obpa_samehand = .30
league_obpa_opphand = .33
league_bb_percent = .24734
league_hr_percent = .07289
league_hbp_percent = .00899  # hbp given onbase
league_ko_percent = .2029  # k per pa
homefield_advantage = 0 #.03

missing_batters = []
points_dict = {}
score_dict={}
win_dict={}
no_hand_list=[]

batter_points = np.array([3,5,8,10,2,2,2,0,2,5,-2])  # in same order as batter class
pitcher_points = np.array([-.6,-.6,-.6,-2,2.25,2,0,0,4,2.5,0]) # in same order as pitcher class


teamdict = {'Red Sox':[Red_Sox_Batters,Red_Sox_Pitchers],'Rockies':[Rockies_Batters,Rockies_Pitchers],'Giants':[Giants_Batters,Giants_Pitchers],'Orioles':[Orioles_Batters,Orioles_Pitchers],'Cubs':[Cubs_Batters,Cubs_Pitchers],'Angels':[Angels_Batters,Angels_Pitchers],'Diamondbacks':[Diamondbacks_Batters,Diamondbacks_Pitchers],'Royals':[Royals_Batters,Royals_Pitchers],'White Sox':[White_Sox_Batters,White_Sox_Pitchers],'Marlins':[Marlins_Batters,Marlins_Pitchers],'Indians':[Indians_Batters,Indians_Pitchers],'Cardinals':[Cardinals_Batters,Cardinals_Pitchers],'Dodgers':[Dodgers_Batters,Dodgers_Pitchers],'Rangers':[Rangers_Batters,Rangers_Pitchers],'Yankees':[Yankees_Batters,Yankees_Pitchers],'Tigers':[Tigers_Batters,Tigers_Pitchers],'Astros':[Astros_Batters,Astros_Pitchers],'Pirates':[Pirates_Batters,Pirates_Pitchers],'Phillies':[Phillies_Batters,Phillies_Pitchers],'Reds':[Reds_Batters,Reds_Pitchers],'Nationals':[Nationals_Batters,Nationals_Pitchers],'Mariners':[Mariners_Batters,Mariners_Pitchers],'Twins':[Twins_Batters,Twins_Pitchers],'Rays':[Rays_Batters,Rays_Pitchers],'Brewers':[Brewers_Batters,Brewers_Pitchers],'Mets':[Mets_Batters,Mets_Pitchers],'Braves':[Braves_Batters,Braves_Pitchers],'Blue Jays':[Blue_Jays_Batters,Blue_Jays_Pitchers],'Athletics':[Athletics_Batters,Athletics_Pitchers],'Padres':[Padres_Batters,Padres_Pitchers]}



batterpath= str('C:\Users\Taylor\Desktop\\baseball\Batters-Weighed gt30ab.csv')
pitcherpath= str('C:\Users\Taylor\Desktop\\baseball\Pitchers-Weighed.csv')
os.chdir('C:\Users\Taylor\Desktop\\baseball\Scores')

    
dfpitcher = pd.read_csv(pitcherpath)
dfbatter = pd.read_csv(batterpath)   
allpitcherslist = list(dfpitcher['Name'])

##### TOOLS  #####
def expavg(batter,pitcher,league):
    p1 = batter*pitcher/league
    p2 = ((1-batter)*(1-pitcher))/(1-league)
    return p1/(p1+p2)

def zeroper(playerdata):
    return len([i for i in list(playerdata) if i<1])/len(playerdata) 
    
    
def graph(player,height=.2,binnum=18,prange=(0,40)):
    playerdata = prelimdf[player]
    plt.ylim(ymax=height)
    playerdata.hist(bins=binnum,range=prange,normed=True)
    print 'Skewness: %s' % (playerdata.skew())
    print 'Mean: %s' % (playerdata.mean())
    print 'Std: %s' % (playerdata.std())
    print 'Zero Percent: %s' % (zeroper(playerdata))
 


##### OBJECTS #####
class Player(object):
    def __init__(self,name):
        self.name = name
         
class Batter(Player):
    def __init__(self,name,hand,obp,rightobp,leftobp,sper,dper,tper,hrper,bbper,koper,hbpper,sbpg,hrperright,bbperright,koperright,hrperleft,bbperleft,koperleft):
        Player.__init__(self,name)
        self.atbats = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.bb = 0
        self.hr = 0
        self.hp = 0
        self.runs = 0
        self.rbis = 0
        self.sb = sbpg
        self.ko = 0
        self.cs = 0
        self.hand = hand
        self.baseobp = obp
        self.rightobp = rightobp
        self.leftobp = leftobp
        self.singleper = sper
        self.doubleper = dper
        self.tripleper = tper
        self.hrper = hrper
        self.bbper = bbper
        self.koper = koper
        self.hbpper = hbpper
        
        self.hrperright =hrperright
        self.bbperright =bbperright
        self.koperright =koperright
        self.hrperleft =hrperleft
        self.bbperleft =bbperleft
        self.koperleft =koperleft
        
        
    def points(self):
        singles = self.singles
        doubles = self.doubles
        triples = self.triples
        hr = self.hr
        bb = self.bb
        rbis = self.rbis
        runs = self.runs
        ko = self.ko
        hp = self.hp
        sb = self.sb
        cs = self.cs
        
        stats = np.array([singles,doubles,triples,hr,bb,rbis,runs,ko,hp,sb,cs])
        return np.sum(stats*batter_points)
        
    def points_print(self):
        print str(self.points())+" - "+str(self.name)
        
    def stats(self):
        print self.name
        print ""
        print str(self.atbats) + "  At Bats"
        print str(self.singles) + "  Singles"
        print str(self.doubles) + "  doubles"
        print str(self.triples) + "  triples"
        print str(self.bb) + "  bb"
        print str(self.hr) + "  hr"
        print str(self.hp) + "  hp"
        print str(self.runs) + "  runs"
        print str(self.rbis) + "  rbis"
        print str(self.ko) + "  kos"
        print ""
        
    def reset_stats(self):
        self.atbats = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.bb = 0
        self.hr = 0
        self.hp = 0
        self.runs = 0
        self.rbis = 0
        self.ko = 0
        self.cs = 0
        
class Pitcher(Player):
    def __init__(self,name,hand, obpa, rightobpa, leftobpa, hrper, bbper,bfmax,koper,hbpper,hrperright,bbperright,koperright,hrperleft,bbperleft,koperleft):
        Player.__init__(self,name)
        self.hand = hand
        self.bbi = 0
        self.ha = 0
        self.hb = 0
        self.er = 0
        self.ip = 0
        self.k = 0
        self.l = 0
        self.s = 0
        self.w = 0
        self.cg = 0
        self.bs = 0
        
        self.bfmax = bfmax

        self.hrper = hrper
        self.bbper = bbper 
        self.obpa = obpa
        self.rightobpa = rightobpa
        self.leftobpa = leftobpa
        self.koper = koper
        self.hbpper = hbpper
        self.hrperright =hrperright
        self.bbperright =bbperright
        self.koperright =koperright
        self.hrperleft =hrperleft
        self.bbperleft =bbperleft
        self.koperleft =koperleft
  
    def points(self):
        bbi = self.bbi
        ha = self.ha
        hb = self.hb
        er = self.er
        ip = self.ip
        k = self.k
        l = self.l
        s = self.s
        w = self.w
        cg = self.cg
        bs = self.bs
        
        stats = np.array([bbi,ha,hb,er,ip,k,l,s,w,cg,bs])

        return np.sum(stats*pitcher_points)

    def points_print(self):
        print str(self.points())+" - "+str(self.name)     
        
    def stats(self):
        print self.name
        print ""
        print str(self.bbi) + "  batters walked"
        print str(self.ha) + "  hits against"
        print str(self.er) + "  runs allowed"
        print str(self.ip) + "  innings pitched"
        print str(self.k) + "  strikeouts"
        print str(self.l) + "  loses"
        print str(self.s) + "  saves"
        print str(self.w) + "  wins"
        print ""
 
    def reset_stats(self):
        self.bbi = 0
        self.ha = 0
        self.hb = 0
        self.er = 0
        self.ip = 0
        self.k = 0
        self.l = 0
        self.s = 0
        self.w = 0
        self.cg = 0
        self.bs = 0     
        
class Team(object):
    def __init__(self,name,batters,pitchers):
#        self.runs = 0
        self.name = name
        self.batters = batters
        self.pitchers = pitchers
        self.currentpitcher = pitchers[0]
        self.pitchnumber = 0
        self.reliever_in = 0
        self.closer_in = 0
        self.batting_iter = itertools.cycle(self.batters)
    
    def lineup(self):
        lup=[]
        for b in self.batters:
            lup.append(b.name)
        return lup

    def runs(self):
        runs = 0
        for b in self.batters:
            runs+=b.runs
        return runs
        
    def pitcher_lineup(self):
        lup=[]
        for p in self.pitchers:
            lup.append(p.name)
        return lup

    def team_stats(self):
        for b in self.batters:
            b.stats()
        for p in self.pitchers:
            p.stats()
            
    def team_points(self):
        for b in self.batters:
            b.points_print()
        for p in self.pitchers:
            p.points_print()   
            
    def pts_dict(self):
        for b in self.batters:
            # dont add batting points for pitchers
            if self.pitchers[0].name == b.name:
                pass
            else:
                points_dict[b.name].append(b.points())
        for p in self.pitchers:
            points_dict[p.name].append(p.points())  

    def reset_stats(self):
        for b in self.batters:
            b.reset_stats()
        for p in self.pitchers:
            p.reset_stats()
            
        self.currentpitcher = self.pitchers[0]
        self.pitchnumber = 0
        self.reliever_in = 0
        self.closer_in = 0
        self.batting_iter = itertools.cycle(self.batters)
        

class Game(object):
    '''object with logic to simulate game -- MCMC'''
    def __init__(self,home,away):
        self.first = None
        self.second = None
        self.third = None
        self.inning = 1
        self.half = 'top'
        self.outs = 0
        self.hometeam = home
        self.awayteam = away
        
    def print_score(self):
        print str(self.hometeam.runs()) + " " + str(self.hometeam.name)
        print str(self.awayteam.runs()) + " " + str(self.awayteam.name)
        
    def clear_bases(self):
        self.first = None
        self.second = None
        self.third = None
        
    def bases(self):
        if self.first:
            first = self.first.name
        else: first='No One'
            
        if self.second:
            second = self.second.name
        else: second='No One'

        if self.third:
            third = self.third.name
        else: third='No One'
            
        return "First: " +first+ ",  Second:  " +second+",  Third:  "+third 
        
    def single(self,batter,pitcher):
        
        if gamelog: print batter.name + " hit a single"
        
        if self.third:
            rand = np.random.random()
            if rand<=.001:
                self.outs+=1
                if gamelog: print str(self.third.name)+" got thrown out after being on third"
                self.third = None
            elif rand<=.01:
                pass
            else:
                self.third.runs+=1
                batter.rbis+=1
                pitcher.er+=1
                if gamelog: print str(self.third.name)+" scored from third"
                self.third = None
        
        if self.second:
            rand = np.random.random()
            if rand<=.036:
                self.outs+=1
                if gamelog: print str(self.second.name)+" got thrown out after being on second"
                self.second = None
            elif rand<=.048:
                pass
            elif self.third:
                # cant move to 3rd or home but want to, redo
                self.single(batter,pitcher)
            elif rand<=.347:
                self.third = self.second
                self.second = None
            else:
                self.second.runs+=1
                batter.rbis+=1
                pitcher.er+=1
                if gamelog: print str(self.second.name)+" scored from second"
                self.second = None               
        
        if self.first:
            rand = np.random.random()
            if rand<=.021:
                self.outs+=1
                if gamelog: print str(self.first.name)+" got thrown out after being on first"
                self.first=None
            elif self.second:
                self.single(batter,pitcher)
            elif rand<=.673:
                self.second = self.first
                self.first = None
            elif rand<=98.6:
                self.third = self.first
                self.first = None
            else:
                self.first.runs+=1
                batter.rbis+=1
                pitcher.er+=1
                if gamelog: print str(self.first.name)+" scored from first"
                self.first = None 
                    
        self.first = batter
        batter.singles+=1

 
    def double(self,batter,pitcher):
        
        if gamelog: print batter.name + " hit a double"

        if self.third:
            self.third.runs+=1
            if gamelog: print str(self.third.name)+" scored from third"
            self.third = None
            pitcher.er+=1
            batter.rbis+=1
        
        if self.second:
            rand = np.random.random()
            if rand<=.001:
                self.outs+= 1
                if gamelog: print str(self.second.name)+" got thrown out after being on second"
                self.second = None
            elif rand<=.016:
                self.third=self.second
                self.second=None
            else:
                self.second.runs += 1
                if gamelog: print str(self.second.name)+" scored from second"
                self.second = None
                pitcher.er+=1
                batter.rbis+=1
        
        if self.first:
            rand = np.random.random()
            if rand<=.031:
                self.outs+=1
                if gamelog: print str(self.first.name)+" got thrown out after being on first"
                self.first = None
            elif self.third:
                self.double(batter,pitcher)
            elif rand<=.567:
                self.third=self.first
                self.first=None
            else:
                self.first.runs+=1
                batter.rbis+=1
                pitcher.er+=1
                if gamelog: print str(self.first.name)+" scored from first"
                self.first=None
            
        self.second = batter
        batter.doubles+=1
        
  
    def triple(self,batter,pitcher):
        
        if gamelog: print batter.name + " hit a triple" 
        
        if self.third:
            self.third.runs+= 1
            if gamelog: print str(self.third.name)+" scored from third"
            self.third = None
            pitcher.er+=1
            batter.rbis+=1
        
        if self.second:
            self.second.runs += 1
            if gamelog: print str(self.second.name)+" scored from second"
            self.second = None
            pitcher.er+=1
            batter.rbis+=1
        
        if self.first:
            self.first.runs += 1
            if gamelog: print str(self.first.name)+" scored from first"
            self.first = None
            pitcher.er+=1
            batter.rbis+=1
            
        self.third = batter
        batter.triples+=1
        
           
        
    def homerun(self,batter,pitcher):
        
        if gamelog: print batter.name + " hit a homerun" 
        
        if self.third:
            self.third.runs+= 1
            if gamelog: print str(self.third.name)+" scored from third"
            pitcher.er+=1
            batter.rbis+=1
        
        if self.second:
            self.second.runs += 1
            if gamelog: print str(self.second.name)+" scored from second"
            pitcher.er+=1
            batter.rbis+=1
        
        if self.first:
            self.first.runs += 1
            if gamelog: print str(self.first.name)+" scored from first"
            pitcher.er+=1
            batter.rbis+=1
            
        batter.runs+=1
        batter.hr+=1
        batter.rbis+=1
        pitcher.er+=1
        
        self.clear_bases()
 
    def walk(self,batter,pitcher):
        
        if gamelog: print batter.name + " walked" 
        
        if self.third:
            self.third.runs+=1
            pitcher.er+=1
            batter.rbis+=1
        if self.second:
            self.third = self.second
        if self.first:
            self.second = self.first
            
        self.first = batter
        batter.bb+=1
        pitcher.bbi+=1
 

    def pitcher_sub(self,pitchingteam,battingteam):
        if pitchingteam.pitchnumber > pitchingteam.currentpitcher.bfmax and pitchingteam.reliever_in==0:
            # sub in the reliever
            if gamelog: print str(pitchingteam.pitchnumber)+"    "+str(pitchingteam.currentpitcher.bfmax)
            if gamelog: print str(pitchingteam.pitchers[1].name)+" is coming in to relieve "+ str(pitchingteam.currentpitcher.name)
            pitchingteam.currentpitcher = pitchingteam.pitchers[1]
            pitchingteam.reliever_in = 1
        
        pitchscore = pitchingteam.runs()
        batscore = battingteam.runs()
        diff = pitchscore - batscore
        
        if diff>=0 and diff<=3:
            close_game=True
        else:
            close_game=False
        
        if self.inning == 9 and close_game and pitchingteam.closer_in==0:
            if gamelog: print str(pitchingteam.pitchers[-1].name)+" is coming in to close "
            pitchingteam.currentpitcher = pitchingteam.pitchers[-1]
            pitchingteam.closer_in = 1
            
            
    def calc_hit(self,batter,pitchingteam, park_factor, advantage):
        pitcher = pitchingteam.currentpitcher

        ## assign hand of switch hitter for this at bat
        if batter.hand =="Switch" and pitcher.hand =="Right":
            batter.hand="Left"
        if batter.hand =="Switch" and pitcher.hand =="Left":
            batter.hand="Right"
            
            
        ## choose what batter obp to use based on pitcher hand
        if pitcher.hand =="Right" and batter.rightobp != 0:
            batterobp = batter.rightobp
        elif pitcher.hand == "Left" and batter.leftobp != 0:
            batterobp = batter.leftobp
        else:
            if gamelog: print "***  Pitcherhand not found:   "+str(pitcher.name)
            batterobp = batter.baseobp

        ## choose what pitcher obpa to use based on batters hand
        if batter.hand =="Right" and pitcher.rightobpa != 0:
            pitcherobpa = pitcher.rightobpa
        elif batter.hand == "Left" and pitcher.leftobpa != 0:
            pitcherobpa = pitcher.leftobpa
        else:
            if gamelog: print "***  Batterhand not found:   "+str(batter.name)
            pitcherobpa = pitcher.obpa

        ## choose what pitcher hrper to use based on batters hand
        if batter.hand =="Right" and pitcher.hrperright != 0:
            pitcherhrper = pitcher.hrperright
        elif batter.hand == "Left" and pitcher.hrperleft != 0:
            pitcherhrper = pitcher.hrperleft
        else:
            if gamelog: print "***  Hrper by hand not found:   "+str(batter.name)
            pitcherhrper = pitcher.hrper

        ## choose what pitcher bbper to use based on batters hand
        if batter.hand =="Right" and pitcher.bbperright != 0:
            pitcherbbper = pitcher.bbperright
        elif batter.hand == "Left" and pitcher.bbperleft != 0:
            pitcherbbper = pitcher.bbperleft
        else:
            if gamelog: print "***  BBper by hand not found:   "+str(batter.name)
            pitcherbbper = pitcher.bbper

        ## choose what pitcher koper to use based on batters hand
        if batter.hand =="Right" and pitcher.koperright != 0:
            pitcherkoper = pitcher.koperright
        elif batter.hand == "Left" and pitcher.koperleft != 0:
            pitcherkoper = pitcher.koperleft
        else:
            if gamelog: print "***  KOper by hand not found:   "+str(batter.name)
            pitcherkoper = pitcher.koper

        ## choose what batter hrper to use based on pitchers hand
        if pitcher.hand =="Right" and batter.hrperright != 0:
            batterhrper = batter.hrperright
        elif pitcher.hand == "Left" and batter.hrperleft != 0:
            batterhrper = batter.hrperleft
        else:
            if gamelog: print "***  Hrper by hand not found or switch:   "+str(batter.name)
            batterhrper = batter.hrper

        ## choose what batter bbper to use based on pitchers hand
        if pitcher.hand =="Right" and batter.bbperright != 0:
            batterbbper = batter.bbperright
        elif pitcher.hand == "Left" and batter.bbperleft != 0:
            batterbbper = batter.bbperleft
        else:
            if gamelog: print "***  BBper by hand not found or switch:   "+str(batter.name)
            batterbbper = batter.bbper

        ## choose what batter koper to use based on pitchers hand
        if pitcher.hand =="Right" and batter.koperright != 0:
            batterkoper = batter.koperright
        elif pitcher.hand == "Left" and batter.koperleft != 0:
            batterkoper = batter.koperleft
        else:
            if gamelog: print "***  KOper by hand not found or switch:   "+str(batter.name)
            batterkoper = batter.koper
            
            ## choose what league obpa to use based on both hands
        if batter.hand =="Right" and pitcher.hand =="Right":
            league_obpa_hand = league_obpa_samehand
        elif batter.hand == "Left" and pitcher.hand == "Left":
            league_obpa_hand = league_obpa_samehand
        elif batter.hand =="Right" and pitcher.hand =="Left":
            league_obpa_hand = league_obpa_opphand
        elif batter.hand == "Left" and pitcher.hand == "Right":
            league_obpa_hand = league_obpa_opphand
        else:
            league_obpa_hand = league_obpa    
            
        onbaseper = expavg(batterobp, pitcherobpa, league_obpa_hand)*park_factor*advantage
        rand = np.random.random()
        if rand>onbaseper:
            koper = expavg(batterkoper,pitcherkoper,league_ko_percent)
            if rand<=koper+onbaseper:
                pitcher.k+= 1
                batter.ko+= 1
            
            self.outs+=1
            if gamelog: print str(self.outs) + " Outs --" + str(batter.name) +" got out"
        else:
            hrper = expavg(batterhrper,pitcherhrper,league_hr_percent)
            bbper = expavg(batterbbper,pitcherbbper,league_bb_percent)
            otherper = 1-hrper-bbper
            singleper = otherper*batter.singleper
            doubleper = otherper*batter.doubleper
            tripleper = otherper*batter.tripleper
            
            rand = np.random.random()  
            
            if rand <= hrper:
                pitcher.ha+=1
                self.homerun(batter,pitcher)
            elif rand <= hrper + bbper and rand >hrper:
                self.walk(batter,pitcher)
            elif rand <= hrper + bbper + singleper and rand >hrper + bbper:
                pitcher.ha+=1
                self.single(batter,pitcher)
            elif rand <= hrper + bbper + singleper + doubleper and rand >hrper + bbper + singleper:
                pitcher.ha+=1
                self.double(batter,pitcher)
            elif rand <= hrper + bbper + singleper + doubleper + tripleper and rand >hrper + bbper + singleper + doubleper:
                pitcher.ha+=1                
                self.triple(batter,pitcher)
            else:
                if gamelog: print "something went wrong when batting--this should never happen"
             
            

    def simulate_inning(self):
        self.outs = 0
        self.clear_bases()  
        self.half = 'top'
        batting_team = self.awayteam
        pitching_team = self.hometeam
        if use_parkfactor: park_factor = park_factors[self.hometeam.name]
        else: park_factor = 1
        
        homebat_iter = self.hometeam.batting_iter
        awaybat_iter = self.awayteam.batting_iter

        if gamelog:
            print ""
            print str(self.half) +" of the "+ str(self.inning)+" ........."
            print str(batting_team.name)+ " are batting"
            print "Score: " +str(self.awayteam.runs())+" away, "+str(self.hometeam.runs())+" home"
        
        while (self.outs < 3):
            self.pitcher_sub(pitching_team,batting_team)
            batter = awaybat_iter.next()
            batter.atbats+=1
            pitching_team.pitchnumber+=3.5
            self.calc_hit(batter, pitching_team, park_factor,1-homefield_advantage)
        
        pitching_team.currentpitcher.ip+=1
        
        self.outs = 0
        self.clear_bases()
        self.half = 'bottom'  
        batting_team = self.hometeam
        pitching_team = self.awayteam      

        if self.inning ==9 and self.hometeam.runs() > self.awayteam.runs():
            if gamelog: print "Game over, home team winning going into bottom of the 9th"
            return True
            
        if gamelog:
            print ""
            print str(self.half) +" of "+ str(self.inning)
            print str(batting_team.name)+ " are batting"
            print "Score: " +str(self.awayteam.runs())+" away, "+str(self.hometeam.runs())+" home"
        
        while (self.outs < 3):
            self.pitcher_sub(pitching_team,batting_team)
            batter = homebat_iter.next()
            batter.atbats+=1
            pitching_team.pitchnumber+=3.5
            self.calc_hit(batter, pitching_team, park_factor,1+homefield_advantage)
        
        pitching_team.currentpitcher.ip+=1
        
            
    def continue_game(self):
        if self.inning<9:
            return True
        elif self.inning>9 and self.hometeam.runs() != self.awayteam.runs():
            if self.hometeam.runs()>self.awayteam.runs():
                self.hometeam.pitchers[0].w+=1
                self.awayteam.pitchers[0].l+=1
            else:
                self.hometeam.pitchers[0].l+=1
                self.awayteam.pitchers[0].w+=1
            return False
        elif self.inning == 30:
            print "inning 30, somethings wrong!"
            return False
        else:
            return True  #teams are tied
        
        
    def simulate_game(self):
        while (self.continue_game()):
            self.simulate_inning()
            self.inning+=1
        print " "
        print ".....Game Over....."
        if gamelog: 
            self.print_score()
            print " "
            self.hometeam.team_points()
            self.awayteam.team_points()
            
    def update_points_dict(self):
        gamename = str(self.hometeam.name)+ "-" +str(self.awayteam.name)
        win_dict.update({})
        self.hometeam.pts_dict()
        self.awayteam.pts_dict()
        score_dict[self.hometeam.name].append(self.hometeam.runs())
        score_dict[self.awayteam.name].append(self.awayteam.runs())
        if self.hometeam.runs()>self.awayteam.runs():
            win_dict[gamename].append(1)
        else:
            win_dict[gamename].append(0)


 
def build_team(name,batters,pitchers):

    batterlist = []
    pitcherlist = []
    
    if gamelog: print "build is starting..."
    for batter in batters:
        #error handling if player not found or if stats very bad
        if gamelog:print batter
        try:
            playerrow =  dfbatter.loc[dfbatter['Name'] == batter]
            hrper = playerrow.iat[0,5]
        except IndexError:
            batterstring = '%s - %s' %(name,batter)
            if batter in allpitcherslist:
                playerrow =  dfbatter.loc[dfbatter['Name'] == 'Pitcher']
                missing_batters.append(batterstring+' (P)')
            elif batter in poor_batter_list:
                playerrow =  dfbatter.loc[dfbatter['Name'] == 'Poor Batter']
                missing_batters.append(batterstring+' (poor batter)')
            else:
                playerrow =  dfbatter.loc[dfbatter['Name'] == 'Average Batter']
                missing_batters.append(batterstring)
                  
        hrper = playerrow.iat[0,5]
        bbper = playerrow.iat[0,6]
        sper = playerrow.iat[0,7]
        dper = playerrow.iat[0,8]
        tper = playerrow.iat[0,9]
        koper = playerrow.iat[0,10]
        hbpper = playerrow.iat[0,11]
        sbpg = playerrow.iat[0,11]
        obp = playerrow.iat[0,33]
        rightobp = playerrow.iat[0,34]
        leftobp = playerrow.iat[0,35]
        hand = playerrow.iat[0,36]
        
        koperright = playerrow.iat[0,41]
        koperleft = playerrow.iat[0,44]
        hrperright = playerrow.iat[0,39]
        hrperleft = playerrow.iat[0,42]
        bbperright = playerrow.iat[0,40]
        bbperleft = playerrow.iat[0,43]
        
#        if not hand=="Right" and not hand=='Left' and not hand=="Switch":
#            no_hand_list.append(batter)
            
        batterlist+=[Batter(batter,hand,obp,rightobp,leftobp,sper,dper,tper,hrper,bbper,koper,hbpper,sbpg,hrperright,bbperright,koperright,hrperleft,bbperleft,koperleft)] # make this instanciate batter class instead
        
    for pitcher in pitchers:
        #error handling if player not found or if stats very bad
        if gamelog: print pitcher
        playerrow =  dfpitcher.loc[dfpitcher['Name'] == pitcher]
        hrper = playerrow.iat[0,5]
        bbper = playerrow.iat[0,6]
        hbpper = playerrow.iat[0,7]
#        bfmax = playerrow.iat[0,8]
        bfmax = np.random.uniform(low=95,high=110)
        koper = playerrow.iat[0,9]
        obpa = playerrow.iat[0,10]
        rightobpa = playerrow.iat[0,11]
        leftobpa = playerrow.iat[0,12]
        hand = playerrow.iat[0,13]
        koperright = playerrow.iat[0,16]
        koperleft = playerrow.iat[0,19]
        hrperright = playerrow.iat[0,14]
        hrperleft = playerrow.iat[0,17]
        bbperright = playerrow.iat[0,15]
        bbperleft = playerrow.iat[0,18]
        
        if not hand=="Right" and not hand=='Left':
            no_hand_list.append(pitcher+" (P)")
            
        pitcherlist+=[Pitcher(pitcher,hand,obpa,rightobpa,leftobpa,hrper,bbper,bfmax,koper,hbpper,hrperright,bbperright,koperright,hrperleft,bbperleft,koperleft)] 
            
    team = Team(name,batterlist,pitcherlist)
    return team






def run_simulation(homename,awayname):
    # creates dictionary to get ready for dataframe
    homebatters = teamdict[homename][0]
    homepitchers = teamdict[homename][1]
    
    awaybatters = teamdict[awayname][0]
    awaypitchers = teamdict[awayname][1]
    
    allplayers = homebatters+homepitchers+awaybatters+awaypitchers
    
    hometeam = build_team(homename,homebatters,homepitchers)
    awayteam = build_team(awayname,awaybatters,awaypitchers)
    
    gamename = str(hometeam.name)+ "-" +str(awayteam.name)
    win_dict.update({gamename:[]})
    score_dict.update({hometeam.name:[],awayteam.name:[]})

    
    for p in allplayers:
        points_dict.update({p:[]})
       
    for i in range(sim_number):

        game = Game(hometeam,awayteam)
        game.simulate_game()
        game.update_points_dict()

        hometeam.reset_stats()
        awayteam.reset_stats()

        print "Game "+str(i)+" :  "+homename+" - "+awayname
        
#        import pdb; pdb.set_trace()
        
        
#    finaldf = pd.DataFrame(points_dict)
#    
#    print finaldf.describe()
#    if logtofile:
#        filename = homename+"-"+awayname+".csv"
#        finaldf.to_csv(filename)

poor_batter_list = ['Cole Figueroa','Curt Casali','Nick Ahmed','Zelous Wheeler','Adam Duvall','Jesus Sucre']





run_simulation("Giants",'Dodgers')
run_simulation("Angels",'Tigers')  
run_simulation("Rockies",'Pirates')
run_simulation("Braves",'Padres')
run_simulation("Rangers",'Athletics')
run_simulation("Brewers",'Mets')
run_simulation("Astros",'Marlins')
run_simulation("Royals",'Indians')
run_simulation("Twins",'White Sox')   
run_simulation("Rays",'Red Sox')
run_simulation("Phillies",'Diamondbacks')
run_simulation("Cubs",'Cardinals')   
run_simulation("Yankees",'Blue Jays') 
run_simulation("Reds",'Nationals')
run_simulation("Mariners",'Orioles')




# take out placeholder players used in place of prospects to remove errors from small at bat sample size
if 'Average Batter' in points_dict:
    del points_dict['Average Batter']
if 'Poor Batter' in points_dict:
    del points_dict['Poor Batter']
if 'Pitcher' in points_dict:
    del points_dict['Pitcher']

winpers = pd.DataFrame(win_dict).mean()
scores = pd.DataFrame(score_dict)
avscores = scores.mean()

prelimdf = pd.DataFrame(points_dict).fillna(value=0)  # matrix of pts for each game simulated - all players
prelim_desc =  prelimdf.describe().transpose() # descriptive stats on players - all players
toptwohundredlist = list(prelim_desc.sort('mean',ascending=False).head(200).index) # list of 200 players w highest means

prelim_zeroper = prelimdf.apply(zeroper)
prelim_desc['Zero Point %'] = prelim_zeroper

finaldf = prelimdf[toptwohundredlist] # points each game for top 200 players
final_desc =  finaldf.describe().transpose() # descriptive stats on players - top 200
corr_matrix =  finaldf.corr().fillna(value=0)  # correlation matrix - top 200

final_zeroper = finaldf.apply(zeroper)
final_desc['Zero Point %'] = final_zeroper


if logtofile:
    final_desc.to_csv('master.csv')
    corr_matrix.to_csv('corrmatrix.csv')
    prelimdf.transpose().to_csv('points.csv')


print ""
print "_____Missing Batters_____"
for b in missing_batters:
    print b

print ""
print "_____Need to Get Hands_____"
for b in no_hand_list:
    print b

