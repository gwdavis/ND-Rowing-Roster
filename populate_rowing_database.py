# Rowing Roster v0.1- a Udacity Nano-Degree Project for Full Stack Foundations
# v0.1 adds:   1)Routing
#                2)Templates and Forms
#                3)CRUD Functionality
# March 2015 by Gary Davis


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Regattas, Seasons, Rowers, Teams, RowerSeasons,\
                           RowerRegattas, RowerTeams, Base
import datetime

engine = create_engine('sqlite:///rowingteam.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Add Seasons
season1 = Seasons(name='Fall 2014', short='F14', description='Fall 2014')
season2 = Seasons(name='Winter 2014', short='W14', description='Winter 2014-2015')
season3 = Seasons(name='Spring 2015', short='S15', description='Spring 2015')

session.add(season1)
session.add(season2)
session.add(season3)
session.commit()

# Add Teams
team1 = Teams(id='mens', name="Men's")
team2 = Teams(id='womens', name="Women's")

session.add(team1)
session.add(team2)
session.commit()

# Add Regattas
regatta1 = Regattas(season_id=1, name="Saratoga Invitational",
                    date=datetime.date(2014, 4, 25), weblink='google.com/lsdkfsdf')
regatta2 = Regattas(season_id=1, name="Greenwich Invitational",
                    date=datetime.date(2014, 4, 25), weblink='google.com/lsdkwer')
regatta3 = Regattas(season_id=1, name="Housatonic Invitational",
                    date=datetime.date(2014, 4, 25), weblink='google.com/lsdvbn')
regatta4 = Regattas(season_id=1, name="Scholastic Nationals",
                    date=datetime.date(2014, 4, 25), weblink='google.com/lsalkd')
regatta5 = Regattas(season_id=3, name="Scholastic Nationals",
                    date=datetime.date(2015, 4, 25), weblink='google.com/lsalkd')
regatta6 = Regattas(season_id=3, name="Scholastic Nationals",
                    date=datetime.date(2015, 4, 25), weblink='google.com/lsalkd')
regatta7 = Regattas(season_id=3, name="Scholastic Nationals",
                    date=datetime.date(2015, 4, 25), weblink='google.com/lsalkd')
regatta8 = Regattas(season_id=3, name="Scholastic Nationals",
                    date=datetime.date(2015, 4, 25), weblink='google.com/lsalkd')

session.add(regatta1)
session.add(regatta2)
session.add(regatta3)
session.add(regatta4)
session.add(regatta5)
session.add(regatta6)
session.add(regatta7)
session.add(regatta8)
session.commit()

# Add Rowers
rower1 = Rowers(fname='Bob', lname='Latham', photo='1.jpg',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower2 = Rowers(fname='John', lname='Latham', photo='1.jpg',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower3 = Rowers(fname='David', lname='Latham', photo='1.jpg',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower4 = Rowers(fname='Bill', lname='Latham', photo='1.jpg',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower5 = Rowers(fname='Susan', lname='Latham', photo='1.jpg',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower6 = Rowers(fname='Jane', lname='Latham', photo='1.jpg',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower7 = Rowers(fname='Sally', lname='Latham', photo='1.jpg',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower8 = Rowers(fname='Holly', lname='Latham', photo='1.jpg',
                gyear='2017', experience='4', mother='Jane', father='Bob')

session.add(rower1)
session.add(rower2)
session.add(rower3)
session.add(rower4)
session.add(rower5)
session.add(rower6)
session.add(rower7)
session.add(rower8)
session.commit()

# Add Seasons the rower rowed
#rower1.seasons.append(season1)
#rowerseason1 = RowerSeasons(season=season1, rower=rower1)
#rowerseason2 = RowerSeasons(season=season1, rower=rower2)
#rowerseason3 = RowerSeasons(season=season1, rower=rower3)
#rowerseason4 = RowerSeasons(season=season1, rower=rower4)
#rowerseason5 = RowerSeasons(season=season1, rower=rower5)
#rowerseason6 = RowerSeasons(season=season1, rower=rower6)
#rowerseason7 = RowerSeasons(season=season1, rower=rower7)
#rowerseason8 = RowerSeasons(season=season1, rower=rower8)
#rowerseason9 = RowerSeasons(season=season1, rower=rower1)
#rowerseason10 = RowerSeasons(season=season2, rower=rower2)
#rowerseason11 = RowerSeasons(season=season2, rower=rower3)
#rowerseason12 = RowerSeasons(season=season2, rower=rower4)
#rowerseason13 = RowerSeasons(season=season3, rower=rower5)
#rowerseason14 = RowerSeasons(season=season3, rower=rower6)
#rowerseason15 = RowerSeasons(season=season3, rower=rower7)
#rowerseason16 = RowerSeasons(season=season3, rower=rower8)

#session.add(rowerseason1)
#session.add(rowerseason2)
#session.add(rowerseason3)
#session.add(rowerseason4)
#session.add(rowerseason5)
#session.add(rowerseason6)
#session.add(rowerseason7)
#session.add(rowerseason8)
#session.add(rowerseason9)
#session.add(rowerseason10)
#session.add(rowerseason11)
#session.add(rowerseason12)
#session.add(rowerseason13)
#session.add(rowerseason14)
#session.add(rowerseason15)
#session.add(rowerseason16)
#session.commit()

# Add Regattas the rower rowed
rowerregattas1 = RowerRegattas(rower=rower1, regatta=regatta1)
rowerregattas2 = RowerRegattas(rower=rower2, regatta=regatta1)
rowerregattas3 = RowerRegattas(rower=rower3, regatta=regatta1)
rowerregattas4 = RowerRegattas(rower=rower4, regatta=regatta1)
rowerregattas5 = RowerRegattas(rower=rower5, regatta=regatta1)
rowerregattas6 = RowerRegattas(rower=rower6, regatta=regatta1)
rowerregattas7 = RowerRegattas(rower=rower7, regatta=regatta1)
rowerregattas8 = RowerRegattas(rower=rower8, regatta=regatta1)
rowerregattas9 = RowerRegattas(rower=rower1, regatta=regatta2)
rowerregattas10 = RowerRegattas(rower=rower2, regatta=regatta2)
rowerregattas11 = RowerRegattas(rower=rower3, regatta=regatta2)
rowerregattas12 = RowerRegattas(rower=rower4, regatta=regatta2)
rowerregattas13 = RowerRegattas(rower=rower5, regatta=regatta2)
rowerregattas14 = RowerRegattas(rower=rower6, regatta=regatta2)
rowerregattas15 = RowerRegattas(rower=rower7, regatta=regatta2)
rowerregattas16 = RowerRegattas(rower=rower8, regatta=regatta2)
rowerregattas17 = RowerRegattas(rower=rower1, regatta=regatta3)
rowerregattas18 = RowerRegattas(rower=rower2, regatta=regatta3)
rowerregattas19 = RowerRegattas(rower=rower3, regatta=regatta3)
rowerregattas20 = RowerRegattas(rower=rower4, regatta=regatta3)
rowerregattas21 = RowerRegattas(rower=rower5, regatta=regatta3)
rowerregattas22 = RowerRegattas(rower=rower6, regatta=regatta3)
rowerregattas23 = RowerRegattas(rower=rower7, regatta=regatta3)
rowerregattas24 = RowerRegattas(rower=rower8, regatta=regatta3)
rowerregattas25 = RowerRegattas(rower=rower1, regatta=regatta4)
rowerregattas26 = RowerRegattas(rower=rower2, regatta=regatta4)

session.add(rowerregattas1)
session.add(rowerregattas2)
session.add(rowerregattas3)
session.add(rowerregattas4)
session.add(rowerregattas5)
session.add(rowerregattas6)
session.add(rowerregattas7)
session.add(rowerregattas8)
session.add(rowerregattas9)
session.add(rowerregattas10)
session.add(rowerregattas11)
session.add(rowerregattas12)
session.add(rowerregattas13)
session.add(rowerregattas14)
session.add(rowerregattas15)
session.add(rowerregattas16)
session.add(rowerregattas17)
session.add(rowerregattas18)
session.add(rowerregattas19)
session.add(rowerregattas20)
session.add(rowerregattas21)
session.add(rowerregattas22)
session.add(rowerregattas23)
session.add(rowerregattas24)
session.add(rowerregattas25)
session.add(rowerregattas26)
session.commit()

# Add Team Rosters
rowerteams1 = RowerTeams(rower=rower1, team=team1, season=season1)
rowerteams2 = RowerTeams(rower=rower2, team=team1, season=season1)
rowerteams3 = RowerTeams(rower=rower3, team=team1, season=season1)
rowerteams4 = RowerTeams(rower=rower4, team=team1, season=season1)
rowerteams5 = RowerTeams(rower=rower5, team=team2, season=season1)
rowerteams6 = RowerTeams(rower=rower6, team=team2, season=season1)
rowerteams7 = RowerTeams(rower=rower7, team=team2, season=season1)
rowerteams8 = RowerTeams(rower=rower8, team=team2, season=season1)
rowerteams9 = RowerTeams(rower=rower1, team=team1, season=season2)
rowerteams10 = RowerTeams(rower=rower2, team=team1, season=season2)
rowerteams11 = RowerTeams(rower=rower3, team=team1, season=season2)
rowerteams12 = RowerTeams(rower=rower4, team=team2, season=season2)
rowerteams13 = RowerTeams(rower=rower5, team=team2, season=season2)
rowerteams14 = RowerTeams(rower=rower6, team=team2, season=season2)
rowerteams15 = RowerTeams(rower=rower7, team=team2, season=season2)
rowerteams16 = RowerTeams(rower=rower8, team=team2, season=season2)

session.add(rowerteams1)
session.add(rowerteams2)
session.add(rowerteams3)
session.add(rowerteams4)
session.add(rowerteams5)
session.add(rowerteams6)
session.add(rowerteams7)
session.add(rowerteams8)
session.add(rowerteams9)
session.add(rowerteams10)
session.add(rowerteams11)
session.add(rowerteams12)
session.add(rowerteams13)
session.add(rowerteams14)
session.add(rowerteams15)
session.add(rowerteams16)
session.commit()


print "added menu items!"
