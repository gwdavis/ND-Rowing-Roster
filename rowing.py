from flask import Flask, render_template, request, redirect, url_for
# , , , flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Regattas, Seasons, Rowers, Teams, RowerSeasons,\
                           RowerRegattas, RowerTeams, Base
import datetime, time

engine = create_engine('sqlite:///rowingteam.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Start fake data
season = {'id': 1, 'name': 'Spring 2015', 'description': 'Spring of 2015',
          'short': 's15'}

regattas = [{'id': 1, 'season_id': 1, 'name': "Saratoga Invitational",
            'date': '2015/4/21', 'weblink': 'google.com/lsdkfsdf'},
            {'id': 2, 'season_id': 1, 'name': "Greenwich Invitational",
             'date': '2015/4/21', 'weblink': 'google.com/lsdkwer'},
            {'id': 3, 'season_id': 1, 'name': "Housatonic Invitational",
             'date': '2014/4/21', 'weblink': 'google.com/lsdvbn'},
            {'id': 4, 'season_id': 1, 'name': "Scholastic Nationals",
             'date': '2014/4/21', 'weblink': 'google.com/lsalkd'}]

regatta = {'id': 1, 'season_id': 1, 'season_name': 'Spring 2015',
           'name': "Saratoga Invitational",
           'date': '2015/4/21', 'description': 'A great regatta',
           'weblink': 'google.com/lsdkfsdf'}

teamroster = [{'id': '1', 'photo': '1.jpg', 'team': 'women', 'fname': 'Susan',
               'lname': 'Latham', 'gyear': '2017', 'experience': '4',
               'mother': 'Jane', 'father': 'Bob'},
              {'id': '1', 'photo': '1.jpg', 'team': 'women', 'fname': 'Susan',
               'lname': 'Latham', 'gyear': '2017', 'experience': '4',
               'mother': 'Jane', 'father': 'Bob'},
              {'id': '1', 'photo': '1.jpg', 'team': 'women', 'fname': 'Susan',
               'lname': 'Latham', 'gyear': '2017', 'experience': '4',
               'mother': 'Jane', 'father': 'Bob'},
              {'id': '1', 'photo': '1.jpg', 'team': 'women', 'fname': 'Susan',
               'lname': 'Latham', 'gyear': '2017', 'experience': '4',
               'mother': 'Jane', 'father': 'Bob'},
              {'id': '1', 'photo': '1.jpg', 'team': 'women', 'fname': 'Susan',
               'lname': 'Latham', 'gyear': '2017', 'experience': '4',
               'mother': 'Jane', 'father': 'Bob'}]

rower = {'id': '1', 'photo': '1.jpg', 'team': 'womens', 'fname': 'Susan',
         'lname': 'Latham', 'gyear': '2017', 'experience': '4',
         'mother': 'Jane', 'father': 'Bob'}

rowerhistoryseasons = [{'id': '1', 'name': 'Spring 2015', 'description': 'Spring of 2015',
            'short': 's15', 'rowed': True},
           {'id': '2', 'name': 'Spring 2014', 'description': 'Spring of 2014',
            'short': 's14', 'rowed': True},
           {'id': '3', 'name': 'Spring 2013', 'description': 'Spring of 2013',
            'short': 's13', 'rowed': False},
           {'id': '4', 'name': 'Spring 2012', 'description': 'Spring of 2012',
            'short': 's12', 'rowed': False}]

seasons = [{'id': '1', 'name': 'Spring 2015', 'description': 'Spring of 2015',
            'short': 's15'},
           {'id': '2', 'name': 'Spring 2014', 'description': 'Spring of 2014',
            'short': 's14'},
           {'id': '3', 'name': 'Spring 2013', 'description': 'Spring of 2013',
            'short': 's13'},
           {'id': '4', 'name': 'Spring 2012', 'description': 'Spring of 2012',
            'short': 's12'}]

rowerhistoryregattas = [{'id': '1', 'season_id': '1',
            'name': "Saratoga Invitational",
            'date': '2015/4/21', 'weblink': 'google.com/lsdkfsdf', 'rowed': True},
            {'id': '2', 'season_id': '1', 'name': "Greenwich Invitational",
             'date': '2015/4/21', 'weblink': 'google.com/lsdkwer', 'rowed': False},
            {'id': '3', 'season_id': '2', 'name': "Housatonic Invitational",
             'date': '2014/4/21', 'weblink': 'google.com/lsdvbn', 'rowed': True},
            {'id': '4', 'season_id': '2', 'name': "Scholastic Nationals",
             'date': '2014/4/21', 'weblink': 'google.com/lsalkd', 'rowed': False}]

currentseason = {'season_id': '1', 'name': 'Spring 2015'}

# end fake data


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
    teamroster = session.query(RowerTeams).filter_by(team_id=team_id, season_id=season_id)
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
    rower = session.query(Rowers).filter_by(id=rower_id).one()
    rowerhistoryseasons = session.query(RowerSeasons).filter_by(rower_id=rower_id)
    rowerhistoryregattas = session.query(RowerRegattas).filter_by(rower_id=rower_id)
    return render_template('rowerprofile.html', rower=rower,
                           rowerhistoryseasons=rowerhistoryseasons,
                           rowerhistoryregattas=rowerhistoryregattas,
                           currentseason=currentseason)

# !!! need to pass the current team and season of the rower for cancel button
@app.route('/rower/<rower_id>/edit/')
def editRower(rower_id):
    seasons = session.query(Seasons)
    regattas = session.query(Regattas)
    rower = session.query(Rowers).filter_by(id=rower_id).one()
    rowerhistoryseasons = session.query(RowerSeasons).filter_by(rower_id=rower_id)
    rowerhistoryregattas = session.query(RowerRegattas)
    if False:
        pass
    else:
        return render_template('editrower.html', rower=rower,
                           rowerhistoryseasons=rowerhistoryseasons,
                           rowerhistoryregattas=rowerhistoryregattas,
                           seasons=seasons, 
                           regattas=regattas,
                           currentseason=currentseason)


@app.route('/rower/new/')
def addRower():
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
