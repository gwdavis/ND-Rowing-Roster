from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Regattas, Seasons, Rowers, Teams, RowerSeasons,\
                           RowerRegattas, RowerTeams, Base

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
                    date='2015/4/21', weblink='google.com/lsdkfsdf')
regatta2 = Regattas(season_id=1, name="Greenwich Invitational",
                    date='2015/4/21', weblink='google.com/lsdkwer')
regatta3 = Regattas(season_id=1, name="Housatonic Invitational",
                    date='2014/4/21', weblink='google.com/lsdvbn')
regatta4 = Regattas(season_id=1, name="Scholastic Nationals",
                    date='2014/4/21', weblink='google.com/lsalkd')
regatta5 = Regattas(season_id=3, name="Scholastic Nationals",
                    date='2015/4/21', weblink='google.com/lsalkd')
regatta6 = Regattas(season_id=3, name="Scholastic Nationals",
                    date='2015/4/21', weblink='google.com/lsalkd')
regatta7 = Regattas(season_id=3, name="Scholastic Nationals",
                    date='2015/3/21', weblink='google.com/lsalkd')
regatta8 = Regattas(season_id=3, name="Scholastic Nationals",
                    date='2015/4/21', weblink='google.com/lsalkd')

session.add(regatta1)
session.add(regatta2)
session.add(regatta3)
session.add(regatta4)
session.add(regatta5)
session.add(regatta6)
session.add(regatta7)
session.add(regatta8)
session.commit()



print "added menu items!"
