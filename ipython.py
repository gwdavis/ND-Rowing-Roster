from sqlalchemy import create_engine  # , desc
from sqlalchemy.orm import sessionmaker
from database_setup import Regattas, Seasons, Rowers, Teams, RowerSeasons,\
                           RowerRegattas, RowerTeams, Base

import os
import sys
import db_helper


# Below used to format date fileds in forms
import datetime
# Below used to verify no code is injected in uploaded filenames
from werkzeug import secure_filename

engine = create_engine('sqlite:///rowingteam.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

