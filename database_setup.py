import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()

# associative table for many to many
rowerseasons = Table('rowerseasons', Base.metadata,
                     Column('season_id', String, ForeignKey('seasons.id')),
                     Column('rower_id', String, ForeignKey('rowers.id'))
                     )


class Seasons(Base):
    __tablename__ = 'seasons'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    short = Column(String(15), unique=True)
    description = Column(String(15))
    


class Regattas(Base):
    __tablename__ = 'regattas'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    date = Column(DateTime)
    description = Column(String(250))
    weblink = Column(String(250))


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
    # Many-to-many relationship
    seasons = relationship('Seasons', secondary=rowerseasons)




class Teams(Base):
    __tablename__ = 'teams'

    id = Column(String(60), primary_key=True)
    name = Column(String(60), unique=True, nullable=False)


class RowerTeams(Base):
    __tablename__ = 'rowerteams'
# !!! I have linked to seasons.id but think I really want rowerseasons.season_id
    id = Column(Integer, primary_key=True)
    season_id = Column(String, ForeignKey('seasons.id'), nullable=False)
    rower_id = Column(String, ForeignKey('rowers.id'), nullable=False)
    team_id = Column(String, ForeignKey('teams.id'), nullable=False)
    season = relationship(Seasons)
    rower = relationship(Rowers)
    team = relationship(Teams)


class RowerRegattas(Base):
    __tablename__ = 'rowerregattas'

    id = Column(Integer, primary_key=True)
    regatta_id = Column(Integer, ForeignKey('regattas.id'), nullable=False)
    rower_id = Column(String, ForeignKey('rowers.id'), nullable=False)
    rower = relationship(Rowers)
    regatta = relationship(Regattas)


engine = create_engine('sqlite:///rowingteam.db')
Base.metadata.create_all(engine)
