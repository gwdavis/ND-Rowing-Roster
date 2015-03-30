from sqlalchemy import create_engine  # , desc
from sqlalchemy.orm import sessionmaker
from database_setup import Regattas, Seasons, Rowers, Teams,\
                           RowerRegattas, RowerTeams, Base

import os
import sys


# Below used to format date fileds in forms
import datetime
# Below used to verify no code is injected in uploaded filenames
from werkzeug import secure_filename

engine = create_engine('sqlite:///rowingteam.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Set up for Flask receipt of files from HTML form
# see http://flask.pocoo.org/docs/0.10/patterns/fileuploads/#uploading-files
# see generalized path (i.e. dir_path) using module __file__ directory at:
# http://www.karoltomala.com/blog/?p=622
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# Temporary manual plug to select the applicable season.
# A later version will allow the selection of the season to display
# teams, regattas and possibly results.
currentseason = {'season_id': 1}


# checks if uploaded photo files have an acceptable extension
def allowed_file(filename):
    """Check if uploaded file has allowed extensions
    args:   filename"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_season_from_season_id(season_id):
    """Get season object for given season ID."""
    return session.query(Seasons).get(season_id)


def get_current_season():
    """Get season object for current season"""
    return session.query(Seasons).get(currentseason['season_id'])


def get_all_seasons():
    """Get season object for all seasons"""
    return session.query(Seasons).all()


def get_all_regattas_for_season(season_id):
    """Get regatta object for all the regattas for given season ID."""
    return session.query(Regattas).filter_by(season_id=season_id).all()


def get_all_regattas():
    """Get regatta object for all regattas."""
    return session.query(Regattas).all()


def get_regatta_from_regatta_id(regatta_id):
    """Get regatta object for a given regatta ID."""
    return session.query(Regattas).get(regatta_id)


def get_rower_from_rower_id(rower_id):
    """Get rower object for a given rower ID."""
    return session.query(Rowers).get(rower_id)


def get_list_rowed_regattas(rower_id):
    """Get list of regattas rowed for a given rower ID."""
    rower = session.query(Rowers).get(rower_id)
    rowedregattas = []
    for rr in rower.regatta:
        rowedregattas.append(rr.id)
    return rowedregattas


def get_team_from_team_id(team_id):
    """Get team object for a given team ID."""
    return session.query(Teams).get(team_id)


def get_first(iterable, default=None):
    """Get first item in a list from:
    http://stackoverflow.com/questions/363944/
    python-idiom-to-return-first-item-or-none"""
    if iterable:
        for item in iterable:
            return item
    return default


def get_teams_for_rower_id_and_season_id(rower_id, season_id):
    """Get team object for a given rower ID and season ID.
    If there are more than one team, it only picks the first"""
    rower = get_rower_from_rower_id(rower_id)
    current_team = get_first(rower.team)
    return current_team


def get_current_season_teams_for_rower_id(rower_id):
    """Get team object for a given rower ID and the current season.
    If there are more than one team, it only picks the first"""
    season_id = get_current_season().id
    return get_teams_for_rower_id_and_season_id(rower_id, season_id)


def get_team_roster_for_team_id(team_id):
    """Get rower object of all rowers for a given team ID."""
    return session.query(Teams).get(team_id)


def add_new_season(form):
    """Add new season into DB"""
    new_season = Seasons(name=form['name'],
                         short=form['short'],
                         description=form['description'])
    session.add(new_season)
    session.commit()
    return


def update_season(season_id, form):
    """Update an existing season in the DB."""
    season = get_season_from_season_id(season_id)
    # Update each field in season
    season.name = form['name']
    season.short = form['short']
    season.description = form['description']
    session.add(season)
    session.commit()
    return


def remove_season(season_id):
    """Remove a season from the DB."""
    season = get_season_from_season_id(season_id)
    session.delete(season)
    session.commit()
    return


def add_new_regatta(form):
    """Add new regatta into DB"""
    new_regatta = Regattas(name=form['name'],
                           date=datetime.datetime.strptime(
                                form['date'], '%Y-%m-%d'),
                           season_id=form['season_id'],
                           weblink=form['weblink'],
                           description=form['description'])
    session.add(new_regatta)
    session.commit()
    return


def update_regatta(regatta_id, form):
    """Update an existing regatta in the DB."""
    regatta = get_regatta_from_regatta_id(regatta_id)
    # Udpate each field in regatta:
    regatta.name = form['name']
    # Sqlite apparently outputs strings for date fields
    # so need to convert to Python datetime for datebase type
    regatta.date = datetime.datetime.strptime(
                   form['date'], '%Y-%m-%d')
    regatta.season_id = form['season_id']
    regatta.weblink = form['weblink']
    regatta.description = form['description']
    session.add(regatta)
    session.commit()
    return


def remove_regatta(regatta_id):
    """Remove a regatta from the DB."""
    regatta = get_regatta_from_regatta_id(regatta_id)
    session.delete(regatta)
    session.commit()
    return


def add_new_rower(form, files, image_folder):
    """Add new rower in DB"""
    print image_folder
    new_rower = Rowers(fname=form['fname'],
                       lname=form['lname'],
                       photo=get_avatar(rower=None,
                                        files=files,
                                        image_folder=image_folder),
                       gyear=form['gyear'],
                       experience=form['experience'],
                       mother=form['mother'],
                       father=form['father']
                       )
    new_rower.team.append(get_team_from_team_id(form['team']))
    if '1' in form.getlist('rower_seasons'):
        add_season_to_rower(new_rower, get_current_season().id)
    new_rowed_regattas = form.getlist('rower_regattas')
    for nr in new_rowed_regattas:
        add_regatta_to_rower(new_rower, nr)
    session.add(new_rower)
    session.commit


def update_rower(rower_id, form, files, image_folder):
    """Update fields for a rower already in the DB."""
    rower = get_rower_from_rower_id(rower_id)
    rower.photo = get_avatar(rower, files, image_folder)
    rower.fname = form['fname']
    rower.lname = form['lname']
    rower.gyear = form['gyear']
    rower.experience = form['experience']
    rower.mother = form['mother']
    rower.father = form['father']
    update_team_for_rower(rower, form['team'])
    update_regattas_for_rower(rower, form.getlist('rower_regattas'))
    # Update current season status
    if '1' in form.getlist('rower_seasons'):
        add_season_to_rower(rower, get_current_season().id)
    else:
        remove_season_from_rower(rower, get_current_season().id)
    session.add(rower)
    session.commit()
    return


def remove_rower(rower_id):
    """Remove a rower from the DB."""
    rower = get_rower_from_rower_id(rower_id)
    session.delete(rower)
    session.commit()
    return


# Methods of updating rower


def get_avatar(rower, files, image_folder):
    """get image file for rower avatar
    args:   request.files from form
            image_folder path
    returns:filename"""
    image = files['photo']
    if rower:
        filename = rower.photo
    else:
        filename = 'avatar_missing_lg.png'
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(image_folder + filename)
    return filename


def update_team_for_rower(rower, team_id):
    """Update team object in rower object"""
    team = get_team_from_team_id(team_id)
    for current_team in rower.team:
        rower.team.remove(current_team)
    rower.team.append(team)
    return


def add_regatta_to_rower(rower, regatta_id):
    """Adds a regatta reference object to a rower object
    and if the regatta season is in the rower.season, adds the
    season to the rower
    args:   rower oject
            regatta_id"""
    new_regatta = session.query(Regattas).get(regatta_id)
    rower.regatta.append(new_regatta)
    for s in rower.season:
        if s.id == new_regatta.season_id:
            return
    else:
        add_season_to_rower(rower, new_regatta.season_id)
    return


def update_regattas_for_rower(rower, new_rowed_regattas):
    """Updates rower object by adding new regatta objects and removing
    deleted regatta objects
    args:   rower objects
            new list of rowed regattas"""
    # great reference for 'getlist' http://stackoverflow.com/questions/
    # 7996075/iterate-through-checkboxes-in-flask
    # also http://stackoverflow.com/questions/9335773/python-list-difference
    existing_rowed_regattas = []
    for rr in rower.regatta:
        existing_rowed_regattas.append(rr.id)
        if rr.id not in new_rowed_regattas:
            print 'remove %s' % rr.name
            rower.regatta.remove(rr)
    for nr in set(new_rowed_regattas).difference(existing_rowed_regattas):
        add_regatta_to_rower(rower, nr)
    print new_rowed_regattas
    return


def add_season_to_rower(rower, season_id):
    """Adds a season reference object to a rower object
    args:   rower object
            season ID"""
    for season in rower.season:
        if season.id == season_id:
            return
    rower.season.append(get_season_from_season_id(season_id))
    return


def remove_season_from_rower(rower, season_id):
    """Removes a season reference object from a rower object
    args:   rower object
            season ID"""
    for season in rower.season:
        if season.id == season_id:
            rower.season.remove(season)
    return
