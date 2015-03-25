# Rowing Roster v0.1- a Udacity Nano-Degree Project for Full Stack Foundations
# v0.1 adds:   1)Routing
#                2)Templates and Forms
#                3)CRUD Functionality
# March 2015 by Gary Davis

from flask import Flask, render_template, request, redirect, url_for
# , , , flash
app = Flask(__name__)

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Regattas, Seasons, Rowers, Teams, RowerSeasons,\
                           RowerRegattas, RowerTeams, Base
import datetime, time
# Below used to verify no code is injected in uploaded filenames
from werkzeug import secure_filename





engine = create_engine('sqlite:///rowingteam.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Start fake data
# season = {'id': 1, 'name': 'Spring 2015', 'description': 'Spring of 2015',
#           'short': 's15'}

# regattas = [{'id': 1, 'season_id': 1, 'name': "Saratoga Invitational",
#             'date': '2015/4/21', 'weblink': 'google.com/lsdkfsdf'},
#             {'id': 2, 'season_id': 1, 'name': "Greenwich Invitational",
#              'date': '2015/4/21', 'weblink': 'google.com/lsdkwer'},
#             {'id': 3, 'season_id': 1, 'name': "Housatonic Invitational",
#              'date': '2014/4/21', 'weblink': 'google.com/lsdvbn'},
#             {'id': 4, 'season_id': 1, 'name': "Scholastic Nationals",
#              'date': '2014/4/21', 'weblink': 'google.com/lsalkd'}]

# regatta = {'id': 1, 'season_id': 1, 'season_name': 'Spring 2015',
#            'name': "Saratoga Invitational",
#            'date': '2015/4/21', 'description': 'A great regatta',
#            'weblink': 'google.com/lsdkfsdf'}

# teamroster = [{'id': '1', 'photo': '1.jpg', 'team': 'women', 'fname': 'Susan',
#                'lname': 'Latham', 'gyear': '2017', 'experience': '4',
#                'mother': 'Jane', 'father': 'Bob'},
#               {'id': '1', 'photo': '1.jpg', 'team': 'women', 'fname': 'Susan',
#                'lname': 'Latham', 'gyear': '2017', 'experience': '4',
#                'mother': 'Jane', 'father': 'Bob'},
#               {'id': '1', 'photo': '1.jpg', 'team': 'women', 'fname': 'Susan',
#                'lname': 'Latham', 'gyear': '2017', 'experience': '4',
#                'mother': 'Jane', 'father': 'Bob'},
#               {'id': '1', 'photo': '1.jpg', 'team': 'women', 'fname': 'Susan',
#                'lname': 'Latham', 'gyear': '2017', 'experience': '4',
#                'mother': 'Jane', 'father': 'Bob'},
#               {'id': '1', 'photo': '1.jpg', 'team': 'women', 'fname': 'Susan',
#                'lname': 'Latham', 'gyear': '2017', 'experience': '4',
#                'mother': 'Jane', 'father': 'Bob'}]

# rower = {'id': '1', 'photo': '1.jpg', 'team': 'womens', 'fname': 'Susan',
#          'lname': 'Latham', 'gyear': '2017', 'experience': '4',
#          'mother': 'Jane', 'father': 'Bob'}

# rowerhistoryseasons = [{'id': '1', 'name': 'Spring 2015', 'description': 'Spring of 2015',
#             'short': 's15', 'rowed': True},
#            {'id': '2', 'name': 'Spring 2014', 'description': 'Spring of 2014',
#             'short': 's14', 'rowed': True},
#            {'id': '3', 'name': 'Spring 2013', 'description': 'Spring of 2013',
#             'short': 's13', 'rowed': False},
#            {'id': '4', 'name': 'Spring 2012', 'description': 'Spring of 2012',
#             'short': 's12', 'rowed': False}]

# seasons = [{'id': '1', 'name': 'Spring 2015', 'description': 'Spring of 2015',
#             'short': 's15'},
#            {'id': '2', 'name': 'Spring 2014', 'description': 'Spring of 2014',
#             'short': 's14'},
#            {'id': '3', 'name': 'Spring 2013', 'description': 'Spring of 2013',
#             'short': 's13'},
#            {'id': '4', 'name': 'Spring 2012', 'description': 'Spring of 2012',
#             'short': 's12'}]

# rowerhistoryregattas = [{'id': '1', 'season_id': '1',
#             'name': "Saratoga Invitational",
#             'date': '2015/4/21', 'weblink': 'google.com/lsdkfsdf', 'rowed': True},
#             {'id': '2', 'season_id': '1', 'name': "Greenwich Invitational",
#              'date': '2015/4/21', 'weblink': 'google.com/lsdkwer', 'rowed': False},
#             {'id': '3', 'season_id': '2', 'name': "Housatonic Invitational",
#              'date': '2014/4/21', 'weblink': 'google.com/lsdvbn', 'rowed': True},
#             {'id': '4', 'season_id': '2', 'name': "Scholastic Nationals",
#              'date': '2014/4/21', 'weblink': 'google.com/lsalkd', 'rowed': False}]

currentseason = {'season_id': 1}

# end fake data

# Set up for Flask receipt of files from HTML form
# see http://flask.pocoo.org/docs/0.10/patterns/fileuploads/#uploading-files
# !!! generalize the UPLOAD_FOLDER http://www.karoltomala.com/blog/?p=622
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
UPLOAD_FOLDER = dir_path + '/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# checks if uploaded photo files have an acceptable extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Temporary manual plug to select the applicable season
currentseason = {'season_id': 1}

# This will be another page so for the time being we will redirect
@app.route('/')
def mainPage():
    return redirect(url_for('seasonSummary',
                            season_id=currentseason['season_id']))


# Show current season regattas and links to rosters
@app.route('/<season_id>/')
def seasonSummary(season_id):
    season = session.query(Seasons).filter_by(id=season_id).one()
    regattas = session.query(Regattas).filter_by(season_id=season_id)
    return render_template('seasonsummary.html', season=season,
                           regattas=regattas)


@app.route('/<season_id>/roster/<team_id>/')
def showRoster(season_id, team_id):
    season = session.query(Seasons).filter_by(id=season_id).one()
    teamroster = session.query(Teams).filter_by(id=team_id).one()
    return render_template('roster.html', team_id=team_id, season=season,
                           teamroster=teamroster)


@app.route('/seasons/')
def showSeasons():
    seasons = session.query(Seasons)
    return render_template('seasons.html', seasons=seasons)


@app.route('/season/new/', methods=['GET', 'POST'])
def addSeason():
    if request.method == 'POST':
        newSeason = Seasons(name=request.form['name'],
                            short=request.form['short'],
                            description=request.form['description'])
        session.add(newSeason)
        session.commit()
        return redirect(url_for('showSeasons'))
    else:
        return render_template('addseason.html')


@app.route('/season/<season_id>/edit/', methods=['GET', 'POST'])
def editSeason(season_id):
    eSeason = session.query(Seasons).filter_by(id=season_id).one()
    if request.method == 'POST':
        eSeason.name = request.form['name']
        eSeason.short = request.form['short']
        eSeason.description = request.form['description']
        session.add(eSeason)
        session.commit()
        return redirect(url_for('showSeasons'))
    else:
        return render_template('editseason.html', season=editSeason)


@app.route('/season/<season_id>/delete/', methods=['GET', 'POST'])
def deleteSeasonConfirmation(season_id):
    deleteSeason = session.query(Seasons).filter_by(id=season_id).one()
    if request.method == 'POST':
        session.delete(deleteSeason)
        session.commit()
        return redirect(url_for('showSeasons'))
    else:
        return render_template('deleteseason.html', season=deleteSeason)


@app.route('/regattas/')
def showRegattas():
    seasons = session.query(Seasons)
    regattas = session.query(Regattas)
    return render_template('regattas.html', seasons=seasons, regattas=regattas)


@app.route('/regatta/<regatta_id>/')
def showRegatta(regatta_id):
    regatta = session.query(Regattas).filter_by(id=regatta_id).one()
    return render_template('regatta.html', regatta=regatta)


@app.route('/regatta/new/', methods=['GET', 'POST'])
def addRegatta():
    seasons = session.query(Seasons)
    if request.method == 'POST':
        newRegatta = Regattas(name=request.form['name'],
                              date=datetime.datetime.strptime(
                             request.form['date'], '%Y-%m-%d'),
                              season_id=request.form['season_id'],
                              weblink=request.form['weblink'],
                              description=request.form['description'])
        session.add(newRegatta)
        session.commit()
        return redirect(url_for('showRegattas'))
    else:
        return render_template('addregatta.html', seasons=seasons)


@app.route('/regatta/<regatta_id>/edit/', methods=['GET', 'POST'])
def editRegatta(regatta_id):
    #seasons = session.query(Seasons)
    eRegatta = session.query(Regattas).filter_by(id=regatta_id).one()
   
    if request.method == 'POST':
        if request.form['name']:
            eRegatta.name = request.form['name']
        if request.form['date']:
            # Sqlite apparently outputs strings for date fields
            # so need to convert to Python datetime for datebase type
            eRegatta.date = datetime.datetime.strptime(
                             request.form['date'], '%Y-%m-%d')         
        if request.form['season_id']:
            eRegatta.season_id = request.form['season_id']
        if request.form['weblink']:
            eRegatta.weblink = request.form['weblink']
        if request.form['description']:
            eRegatta.description = request.form['description']
      
        session.add(eRegatta)
        session.commit()
        return redirect(url_for('showRegattas'))
    else:
        return render_template('editregatta.html', regatta=eRegatta,
                               seasons=seasons)


@app.route('/regatta/<regatta_id>/delete/', methods=['GET', 'POST'])
def deleteRegattaConfirmation(regatta_id):
    deleteRegatta = session.query(Regattas).filter_by(id=regatta_id).one()
    if request.method == 'POST':
        session.delete(deleteRegatta)
        session.commit()
        return redirect(url_for('showRegattas'))
    else:
        return render_template('deleteregatta.html', regatta=deleteRegatta)


@app.route('/rower/<rower_id>/')
def showRower(rower_id):
    rower = session.query(Rowers).get(rower_id)
    cseason = session.query(Seasons).get(currentseason['season_id'])
    # While we will be using only one team below accomodates a rower belonging
    # to more than one team
    currentteam = ['None']
    for s in rower.season:
        if s.id == currentseason['season_id']:
            # !!! got error rower.team was not iterable when I tried
            # [dict(row) for row in rower.team]
            currentteam = []
            for t in rower.team:
                currentteam.append({'id': t.id, 'name': t.name})
                print t.name, t.id
    return render_template('rowerprofile.html', rower=rower,
                           currentseason=cseason, currentteam=currentteam)

# !!! need to pass the current team and season of the rower for cancel button
@app.route('/rower/<rower_id>/edit/', methods=['GET', 'POST'])
def editRower(rower_id):
    seasons = session.query(Seasons)
    regattas = session.query(Regattas)
    rower = session.query(Rowers).filter_by(id=rower_id).one()
    cseason = session.query(Seasons).filter_by(id=currentseason['season_id']).one()
    # Identify current team or teams 
    currentteam = ['None']
    for s in rower.season:
        if s.id == currentseason['season_id']:
            currentteam = []
            for t in rower.team:
                currentteam.append(t.id)
    # Identify what regattas have been rowed
    rowedregattas = []
    for rr in rower.regatta:
        rowedregattas.append(rr.id)

    # !!! NEED TO CLEAN UP THIS IF STATEMENT
    # !!! 1) fix current season register and regattas
    # !!! 2) do we need the commented if statements below
    # !!! 3) We we really need to get all the data from the form every time?
    if request.method == 'POST':

            photofile = request.files['photo']
            if photofile and allowed_file(photofile.filename):
                filename = secure_filename(photofile.filename)
                photofile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                rower.photo = filename
                print 'current photo is %s' % rower.photo
            else:
                print 'no file I guess'    
        #        rower.photo = request.form['photo']
        # if request.form['fname']:
            rower.fname = request.form['fname']
#         if request.form['lname']:
            rower.lname = request.form['lname']
#         if request.form['gyear']:
            rower.gyear = request.form['gyear']

            # Update Team - because the db model allows more than one team
            # that will be implemented at a later date, we remove all the
            # current teams (there should only be one) and append the new team
            # !!! Do we need an if request.form to avoid doing this on all submits
            t = session.query(Teams).filter_by(id=request.form['team']).one()
            for ct in rower.team:
                rower.team.remove(ct)
            rower.team.append(t)

            # Update current season status
            # !!! Houston!!!   we cannot get a '1' returned here.
            if request.form['rower_seasons'][0] == 0:
                print request.form['rower_seasons'][0]
                print 'not this season'
                pass
            else:
                print request.form['rower_seasons'][0]
                print 'we have a season'
                # ss = session.query(Seasons).get(request.form['rower_seasons'])
                # rower.season.append(ss)

#         if request.form['experience']:
            rower.experience = request.form['experience']
#         if request.form['mother']:
            rower.mother = request.form['mother']
#         if request.form['father']:
            rower.father = request.form['father']

            # Update regattas rowed
            # great reference for 'getlist' http://stackoverflow.com/questions/
            #       7996075/iterate-through-checkboxes-in-flask
            # !!! with square brackets I get an error:
            # TypeError: 'instancemethod' object has no attribute '__getitem__'
            # !!! for rr in rower.regatta, we are only picking up every other
            # regatta yet same for loop works on line 265
            new_rowed_regattas = request.form.getlist('rower_regattas')
            for rr in rower.regatta:
                print 'remove %s' % rr.name
                rower.regatta.remove(rr)
            for nr in new_rowed_regattas:
                new = session.query(Regattas).get(nr)
                rower.regatta.append(new)
            print new_rowed_regattas

            session.add(rower)
            session.commit()
            return redirect(url_for('showRower', rower_id=rower.id))
    else:
        return render_template('editrower.html', rower=rower,
                           rowedregattas=rowedregattas,
                           seasons=seasons, 
                           regattas=regattas,
                           currentseason=cseason,
                           currentteam=currentteam)


@app.route('/rower/new/')
def addRower():
    seasons = session.query(Seasons)
    regattas = session.query(Regattas)
    return render_template('addrower.html', seasons=seasons, regattas=regattas)


@app.route('/rower/<rower_id>/delete/')
def deleteRowerConfirmation(rower_id):
    return render_template('deleterower.html', rower=rower,
                           rowerhistoryseasons=rowerhistoryseasons,
                           rowerhistoryregattas=rowerhistoryregattas,
                           currentseason=currentseason)


if __name__ == '__main__':
    # app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
