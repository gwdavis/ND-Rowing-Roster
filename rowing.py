from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, send_file

import os
import db_helper
import StringIO
import csv


app = Flask(__name__)

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
UPLOAD_FOLDER = dir_path + '/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route('/admin/')
def dashboard():
    """Handler for admin dashboard page"""
    season = db_helper.get_current_season()
    return render_template('dashboard.html', season=season)


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
        flash("You've successfully added a season")
        return redirect(url_for('showSeasons'))
    else:
        return render_template('addseason.html')


@app.route('/season/<season_id>/edit/', methods=['GET', 'POST'])
def editSeason(season_id):
    """Display html dashboard page to edit an already registered season
    Argument:   season id"""
    if request.method == 'POST':
        db_helper.update_season(season_id, request.form)
        flash("You've successfully edited a season")
        return redirect(url_for('showSeasons'))
    else:
        season = db_helper.get_season_from_season_id(season_id)
        return render_template('editseason.html', season=season)


@app.route('/season/<season_id>/delete/', methods=['GET', 'POST'])
def deleteSeasonConfirmation(season_id):
    """Display html dashboard sub-page confirming deletion an existing
    season. Care must be taken as that will orphan regattas and remove
    rowers from teams from that particular season.
    args:   season_id"""
    if request.method == 'POST':
        db_helper.remove_season(season_id)
        flash("You've successfully DELETED a season")
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
        flash("You've successfully added a regatta")
        return redirect(url_for('showRegattas'))
    else:
        return render_template('addregatta.html', seasons=seasons)


@app.route('/regatta/<regatta_id>/edit/', methods=['GET', 'POST'])
def editRegatta(regatta_id):
    """Display html dashboard page to edit an existing regatta.
    argument:   regatta id"""
    if request.method == 'POST':
        db_helper.update_regatta(regatta_id)
        flash("You've successfully edited a regatta")
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
        flash("You've successfully DELETED a regatta")
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
        flash("You've successfully edited a rower")
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
        flash("You've successfully added a rower")
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
        flash("You've successfully DELETED a rower")
        return redirect(url_for('showRoster', team_id=current_team.id,
                                season_id=current_season.id))
    else:
        rower = db_helper.get_rower_from_rower_id(rower_id)
        return render_template('deleterower.html', rower=rower,
                               currentseason=current_season,
                               currentteam=current_team)


# API Stuff
# see  http://flask.pocoo.org/docs/0.10/api/#useful-functions-and-classes

@app.route('/rowers/json')
def get_rowers_json():
    """Returns json of all rowers"""
    list_of_rowers = db_helper.get_all_rowers()
    rowers = []
    for r in list_of_rowers:
        rowers.append(r.serialize)
    return jsonify(Rowers=rowers)


@app.route('/rower/<rower_id>/regattas/json')
def get_regattas_for_rower_json(rower_id):
    """Returns json for all regettas for a given rower ID"""
    list_of_regattas = db_helper.get_all_regattas_for_rower(rower_id)
    regattas = []
    for r in list_of_regattas:
        regattas.append(r.serialize)
    return jsonify(Regattas_by_rower=regattas)


@app.route('/rower/<rower_id>/json')
def get_rower_json(rower_id):
    """Returns json for a given rower ID"""
    rower = db_helper.get_rower_from_rower_id(rower_id)
    return jsonify(Rower=rower.serialize)


@app.route('/rowers/download')
def download_rowers():
    "Export a CSV of all rowers"
    # Source: http://stackoverflow.com/questions/27238247/how
    # -to-stream-csv-from-flask-via-sqlalchemy-query
    rowers = db_helper.get_all_rowers()
    csvfile = StringIO.StringIO()
    headers = [
        "id",
        "fname",
        "lname",
        "graduation_year",
        "experience",
        "mother_fname",
        "father_fname",
    ]
    # Couldn't get a slice from serialize property so do it here
    rows = []
    for r in rowers:
        rows.append(
            {
                "id": r.id,
                "fname": r.fname,
                "lname": r.lname,
                "graduation_year": r.gyear,
                "experience": r.experience,
                "mother_fname": r.mother,
                "father_fname": r.father,
            }
        )
    writer = csv.DictWriter(csvfile, headers)
    writer.writeheader()
    for row in rows:
        writer.writerow(
            dict(
                (k, v.encode('utf-8') if type(v) is unicode else v) for k, v in row.iteritems()
            )
        )
    csvfile.seek(0)
    return send_file(csvfile, attachment_filename='rowers.csv', as_attachment=True)


@app.route('/regattas/download')
def download_regattas():
    "Export a CSV of all regattas"
    # Source: http://stackoverflow.com/questions/27238247/how
    # -to-stream-csv-from-flask-via-sqlalchemy-query
    regattas = db_helper.get_all_regattas()
    csvfile = StringIO.StringIO()
    headers = [
        "id",
        "name",
        "season_id",
        "date",
        "description",
        "weblink"
    ]
    # Couldn't get a slice from serialize property so do it here
    rows = []
    for r in regattas:
        rows.append(
            {
                "id": r.id,
                "name": r.name,
                "season_id": r.season_id,
                "date": r.date,
                "description": r.description,
                "weblink": r.weblink
            }
        )
    writer = csv.DictWriter(csvfile, headers)
    writer.writeheader()
    for row in rows:
        writer.writerow(
            dict(
                (k, v.encode('utf-8') if type(v) is unicode else v) for k, v in row.iteritems()
            )
        )
    csvfile.seek(0)
    return send_file(csvfile, attachment_filename='regattas.csv', as_attachment=True)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
