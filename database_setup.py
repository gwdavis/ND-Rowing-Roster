# Rowing Roster v0.1- a Udacity Nano-Degree Project for Full Stack Foundations
# v0.1 adds:   1)Routing
#                2)Templates and Forms
#                3)CRUD Functionality
# March 2015 by Gary Davis

# changes on march 20 11am are to refactor associative table appropriately

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


# Create Database Model
# - Where rowers can belong to a team, a season and attend regattas
#   in many-to-many relationships as a female coxain could be on both
#   the men's and the women's team.
# - Teams have a unique name for the time being
# - Regattas are unique events i.e. Greenwich Invitational in 2014 is
#   distingt from Greenwich Invitational in 2015
#
# Future Enhancement:
# - A team is unique for each season (i.e. women's varsity spring 2014)
#   but we may wish to search for all women's varsity rowers from all
#   teams over the past several seasons.
# - Similarily for regattas, i.e. the Greenwich Invitational 2014 is a
#   unique event but we may wish to see all the Greenwich Invitational rowers
#   from past events.


class Seasons(Base):
    __tablename__ = 'seasons'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    short = Column(String(15), unique=True)
    description = Column(String(120))
    rower = relationship('Rowers', secondary='rowerseasons')


class Regattas(Base):
    __tablename__ = 'regattas'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    date = Column(DateTime)
    description = Column(String(250))
    weblink = Column(String(250))
    rower = relationship('Rowers', secondary='rowerregattas')
    season = relationship('Seasons')


class Rowers(Base):
    __tablename__ = 'rowers'

    id = Column(Integer, primary_key=True)
    fname = Column(String(60), nullable=False)
    lname = Column(String(60), nullable=False)
    photo = Column(String(60))
    gyear = Column(String(4))
    experience = Column(String(15))
    mother = Column(String(60))
    father = Column(String(60))
    # Add Many-to-many relationship for new associative table
    season = relationship('Seasons', secondary='rowerseasons')
    regatta = relationship('Regattas', secondary='rowerregattas')
    team = relationship('Teams', secondary='rowerteams')


class Teams(Base):
    __tablename__ = 'teams'

    id = Column(String(60), primary_key=True)
    name = Column(String(60), unique=True, nullable=False)
    rower = relationship('Rowers', secondary='rowerteams')


# associative table for many-to-many relationships
# Considered refactoring with SQLAlchemy expressions but chose instead
# to move the relationships to the base tables as per:
# http://www.pythoncentral.io/overview-sqlalchemys-expression-language-orm-queries/
class RowerSeasons(Base):
    __tablename__ = 'rowerseasons'

    id = Column(Integer, primary_key=True)
    season_id = Column(String, ForeignKey('seasons.id'), nullable=False)
    rower_id = Column(String, ForeignKey('rowers.id'), nullable=False)


# !!! Refactor:  RowerTeam-link and a SeasonTeam-link with references in rower,
# team and season.  This is be more logical but will require changing the html
class RowerTeams(Base):
    __tablename__ = 'rowerteams'
    id = Column(Integer, primary_key=True)
    rower_id = Column(String, ForeignKey('rowers.id'), nullable=False)
    team_id = Column(String, ForeignKey('teams.id'), nullable=False)


# Associative table for many-to-many relationships
class RowerRegattas(Base):
    __tablename__ = 'rowerregattas'

    id = Column(Integer, primary_key=True)
    regatta_id = Column(Integer, ForeignKey('regattas.id'), nullable=False)
    rower_id = Column(String, ForeignKey('rowers.id'), nullable=False)


engine = create_engine('sqlite:///rowingteam.db')
Base.metadata.create_all(engine)
