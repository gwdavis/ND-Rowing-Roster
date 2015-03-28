from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

import os
import db_helper

app = Flask(__name__)

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
UPLOAD_FOLDER = dir_path + '/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# API :

# Return a json object for a list of

# all rowers
#    /rowers/json
# all regattas by a rower:
#    /rower/rower_id/regattas/json
# Specific rower:
#   /rower/rower_id/json

# import jsonify and a serializable property to your database
# setup file where needed


# This will be another page so for the time being we will redirect
@app.route('/')
def mainPage():
    return redirect(url_for('seasonSummary',
                            season_id=db_helper.get_current_season().id))


# Show current season regattas and links to rosters
@app.route('/<season_id>/')
def seasonSummary(season_id):
    """Handler for team summary page
    args:   season id"""
    season = db_helper.get_season_from_season_id(season_id)
    regattas = db_helper.get_all_regattas_for_season(season_id)
    return render_template('seasonsummary.html', season=season,
                           regattas=regattas)


@app.route('/<season_id>/roster/<team_id>/')
def showRoster(season_id, team_id):
    """Display html page showing roster for a target team and season.
    args:   season id and team id"""
    season = db_helper.get_season_from_season_id(season_id)
    team_roster = db_helper.get_team_roster_for_team_id(team_id)
    return render_template('roster.html', team_id=team_id, season=season,
                           teamroster=team_roster)


@app.route('/seasons/')
def showSeasons():
    """Display html dashboard page showing a list of registered seasons."""
    seasons = db_helper.get_all_seasons()
    return render_template('seasons.html', seasons=seasons)


@app.route('/season/new/', methods=['GET', 'POST'])
def addSeason():
    """Display html dashboard page to register a new season."""
    if request.method == 'POST':
        db_helper.add_new_season(request.form)
        flash("A new season has been successfully added!")
        return redirect(url_for('showSeasons'))
    else:
        return render_template('addseason.html')


@app.route('/season/<season_id>/edit/', methods=['GET', 'POST'])
def editSeason(season_id):
    """Display html dashboard page to edit an already registered season
    Argument:   season id"""
    if request.method == 'POST':
        db_helper.update_season(season_id, request.form)
        flash("You have successfully updated a season!")
        return redirect(url_for('showSeasons'))
    else:
        return render_template('editseason.html', season=editSeason)


@app.route('/season/<season_id>/delete/', methods=['GET', 'POST'])
def deleteSeasonConfirmation(season_id):
    """Display html dashboard sub-page confirming deletion an existing
    season. Care must be taken as that will orphan regattas and remove
    rowers from teams from that particular season.
    args:   season_id"""
    if request.method == 'POST':
        db_helper.remove_season(season_id)
        flash("You have succesfully removed the season")
        return redirect(url_for('showSeasons'))
    else:
        season = db_helper.get_season_from_season_id(season_id)
        return render_template('deleteseason.html', season=season)


@app.route('/regattas/')
def showRegattas():
    """Display html page showing regattas for all registered seasons"""
    seasons = db_helper.get_all_seasons()
    regattas = db_helper.get_all_regattas()
    return render_template('regattas.html', seasons=seasons, regattas=regattas)


@app.route('/regatta/<regatta_id>/')
def showRegatta(regatta_id):
    """Display html page showing detailed regatta information.
    args: regatta id"""
    regatta = db_helper.get_regatta_from_regatta_id(regatta_id)
    return render_template('regatta.html', regatta=regatta)


@app.route('/regatta/new/', methods=['GET', 'POST'])
def addRegatta():
    """Display html dashboard page to add a new regatta."""
    seasons = db_helper.get_all_seasons()
    if request.method == 'POST':
        db_helper.add_new_regatta(request.form)
        flash("You have successfully added a new regatta!")
        return redirect(url_for('showRegattas'))
    else:
        return render_template('addregatta.html', seasons=seasons)


@app.route('/regatta/<regatta_id>/edit/', methods=['GET', 'POST'])
def editRegatta(regatta_id):
    """Display html dashboard page to edit an existing regatta.
    argument:   regatta id"""
    if request.method == 'POST':
        db_helper.update_regatta(regatta_id)
        flash("You have successfully updated your regatta.")
        return redirect(url_for('showRegattas'))
    else:
        seasons = db_helper.get_all_seasons()
        eRegatta = db_helper.get_regatta_from_regatta_id(regatta_id)
        return render_template('editregatta.html', regatta=eRegatta,
                               seasons=seasons)


@app.route('/regatta/<regatta_id>/delete/', methods=['GET', 'POST'])
def deleteRegattaConfirmation(regatta_id):
    """Display html dashboard sub-page to confirm deletion an existing
    regatta.  Use care as deleting a regatta will remove that regatta
    form list of regatta's rowed for each rower.
    argument regatta id"""
    if request.method == 'POST':
        db_helper.remove_regatta(regatta_id)
        flash("You have successfully removed your regatta.")
        return redirect(url_for('showRegattas'))
    else:
        regatta = db_helper.get_regatta_from_regatta_id(regatta_id)
        return render_template('deleteregatta.html', regatta=regatta)


@app.route('/rower/<rower_id>/')
def showRower(rower_id):
    """Display detailed rower information for given rower ID."""
    rower = db_helper.get_rower_from_rower_id(rower_id)
    current_season = db_helper.get_current_season()
    current_team = db_helper.get_current_season_teams_for_rower_id(rower_id)
    return render_template('rowerprofile.html', rower=rower,
                           currentseason=current_season,
                           currentteam=current_team)


@app.route('/rower/<rower_id>/edit/', methods=['GET', 'POST'])
def editRower(rower_id):
    """Display html dashboard page to edit an existing rower."""
    if request.method == 'POST':
        db_helper.update_rower(rower_id, request.form,
                               request.files, UPLOAD_FOLDER)
        flash("You have successfully updated your rower!")
        return redirect(url_for('showRower', rower_id=rower_id))
    else:
        rower = db_helper.get_rower_from_rower_id(rower_id)
        rowed_regattas = db_helper.get_list_rowed_regattas(rower_id=rower_id)
        seasons = db_helper.get_all_seasons()
        regattas = db_helper.get_all_regattas()
        current_season = db_helper.get_current_season()
        current_team = db_helper.get_current_season_teams_for_rower_id(rower_id=rower_id)
        return render_template('editrower.html', rower=rower,
                               rowedregattas=rowed_regattas,
                               seasons=seasons,
                               regattas=regattas,
                               currentseason=current_season,
                               currentteam=current_team)


@app.route('/rower/new/', methods=['GET', 'POST'])
def addRower():
    """Display html dashboard page to add a new rower"""
    # !!! need to fill out once done with edit....
    current_season = db_helper.get_current_season()
    print current_season.name
    if request.method == 'POST':
        rower = db_helper.add_new_rower(request.form, request.files, UPLOAD_FOLDER)
        flash("You have successfully added a new rower!")
        return redirect(url_for('showRoster',
                                season_id=current_season.id,
                                team_id='womens'))
    else:
        seasons = db_helper.get_all_seasons()
        regattas = db_helper.get_all_regattas()
    return render_template('addrower.html',
                           seasons=seasons,
                           currentseason=current_season,
                           regattas=regattas)


@app.route('/rower/<rower_id>/delete/', methods=['GET', 'POST'])
def deleteRowerConfirmation(rower_id):
    """Display html dashboard sub-page confirming deletion of a rower."""
    current_season = db_helper.get_current_season()
    current_team = db_helper.get_teams_for_rower_id_and_season_id(
                   rower_id=rower_id, season_id=current_season.id)
    if request.method == 'POST':
        db_helper.remove_rower(rower_id)
        flash("You have successfully updated your rower!")
        return redirect(url_for('showRoster', team_id=current_team.id,
                                season_id=current_season.id))
    else:
        rower = db_helper.get_rower_from_rower_id(rower_id)
        return render_template('deleterower.html', rower=rower,
                               currentseason=current_season,
                               currentteam=current_team)


# API Stuff
# see  http://flask.pocoo.org/docs/0.10/api/#useful-functions-and-classes

# @app.route('/rowers/json')
# def get_rowers():
#    list_of_rowers = session.query(Rowers).order_by(desc(Rowers.lname).all()
#    return jsonify(Rowers=[e.serialize for e in ])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
