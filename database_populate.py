# Rowing Roster v0.1- a Udacity Nano-Degree Project for Full Stack Foundations
# v0.1 adds:   1)Routing
#                2)Templates and Forms
#                3)CRUD Functionality
# March 2015 by Gary Davis


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Regattas, Seasons, Rowers, Teams, Base
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
regatta5 = Regattas(season_id=3, name="Great Regatta",
                    date=datetime.date(2015, 4, 25), weblink='google.com/lsalkd')
regatta6 = Regattas(season_id=3, name="Greenwich Regatta",
                    date=datetime.date(2015, 4, 25), weblink='google.com/lsalkd')
regatta7 = Regattas(season_id=3, name="Some Invitational",
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
rower1 = Rowers(fname='Bob', lname='Etherington', photo='avatar_missing_lg.png',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower2 = Rowers(fname='John', lname='Bacon', photo='avatar_missing_lg.png',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower3 = Rowers(fname='David', lname='Christian', photo='avatar_missing_lg.png',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower4 = Rowers(fname='Bill', lname='Davis', photo='avatar_missing_lg.png',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower5 = Rowers(fname='Susan', lname='Anderson', photo='avatar_missing_lg.png',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower6 = Rowers(fname='Jane', lname='Farnsworth', photo='avatar_missing_lg.png',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower7 = Rowers(fname='Sally', lname='Gallagher', photo='avatar_missing_lg.png',
                gyear='2017', experience='4', mother='Jane', father='Bob')
rower8 = Rowers(fname='Holly', lname='Holiday', photo='avatar_missing_lg.png',
                gyear='2017', experience='4', mother='Jane', father='Bob')

# Used http://www.pythoncentral.io/overview-sqlalchemys-expression-language-orm-queries/
# to figure out how to populate associative table entries
# and http://stackoverflow.com/questions/252703/python-append-vs-extend to understand
# how to add multiple elements
rower1.season.extend([season1, season2, season3])
rower2.season.extend([season1, season2, season3])
rower3.season.extend([season1, season2, season3])
rower4.season.extend([season1, season3])
rower5.season.extend([season1, season2, season3])
rower6.season.extend([season1, season2, season3])
rower7.season.extend([season1, season2, season3])
rower8.season.extend([season2, season3])
rower1.regatta.extend([regatta1, regatta2, regatta3, regatta4,
                       regatta5, regatta6, regatta7, regatta8])
rower2.regatta.extend([regatta1, regatta2, regatta3, regatta4,
                       regatta5, regatta6, regatta7, regatta8])
rower3.regatta.extend([regatta1, regatta2, regatta3, regatta4,
                       regatta5, regatta6, regatta7, regatta8])
rower4.regatta.extend([regatta1, regatta2, regatta3, regatta4,
                       regatta5, regatta6, regatta7, regatta8])
rower5.regatta.extend([regatta1, regatta2, regatta3, regatta4,
                       regatta5, regatta6, regatta7, regatta8])
rower6.regatta.extend([regatta1, regatta2, regatta3, regatta4,
                       regatta5, regatta6, regatta7, regatta8])
rower7.regatta.extend([regatta1, regatta2, regatta3, regatta4,
                       regatta5, regatta6, regatta7, regatta8])
rower8.regatta.extend([regatta5, regatta6, regatta7, regatta8])
rower1.team.append(team1)
rower2.team.append(team1)
rower3.team.append(team1)
rower4.team.append(team1)
rower5.team.append(team2)
rower6.team.append(team2)
rower7.team.append(team2)
rower8.team.append(team2)


session.add(rower1)
session.add(rower2)
session.add(rower3)
session.add(rower4)
session.add(rower5)
session.add(rower6)
session.add(rower7)
session.add(rower8)
session.commit()


print "added a bunch of rowers, seasons and regattas!"
