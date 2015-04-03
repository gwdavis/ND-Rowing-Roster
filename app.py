from flask import Flask, render_template, request, redirect, url_for, jsonify,\
     flash, send_file
# For OAuth
from flask.ext.login import LoginManager, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn

import os
import db_helper
import StringIO
import csv


app = Flask(__name__)
lm = LoginManager(app)
lm.login_view = 'login'

app.secret_key = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '1421262574842214',
        'secret': '9183d54c95507f72c0eb93c80fcc5ef9'
    },
    'twitter': {
        'id': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        'secret': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    }
}

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
UPLOAD_FOLDER = dir_path + '/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@lm.user_loader
def load_user(id):
    return db_helper.get_user_id(id)


@app.route('/login/')
def login():
    return redirect(redirect_url())


@app.route('/logout')
def logout():
    logout_user()
    return redirect(redirect_url())


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('login'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('login'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('login'))
    user = db_helper.get_user_for_social_ID(social_id)
    if not user:
        db_helper.add_new_user(social_id, username, email)
    login_user(user, True)
    return redirect(url_for('login'))


# This will be another page so for the time being we will redirect
@app.route('/')
def mainPage():
    return redirect(url_for('seasonSummary',
                            season_id=db_helper.get_current_season().id))


# Source: http://stackoverflow.com/questions/14277067/redirect-back-in-flask
def redirect_url(default='index'):
    '''Helper function to return to referring URL
    Used mainly if there is a failed authentication.'''
    return request.args.get('next') or \
        request.referrer or \
        url_for('mainPage')


# Show current season regattas and links to rosters
@app.route('/<season_id>/')
def seasonSummary(season_id):
    """Handler for team summary page"""
    season = db_helper.get_season_from_season_id(season_id)
    regattas = db_helper.get_all_regattas_for_season(season_id)
    return render_template('seasonsummary.html', season=season,
                           regattas=regattas)


@app.route('/admin/')
def dashboard():
    """Handler for admin dashboard page."""
    if not current_user.is_authenticated():
        flash("Administration access is required to access the dashboard")
        return redirect(url_for('mainPage'))
    season = db_helper.get_current_season()
    return render_template('dashboard.html', season=season)


@app.route('/<season_id>/roster/<team_id>/')
def showRoster(season_id, team_id):
    """Handler for team roaster page for a given target team and season."""
    season = db_helper.get_season_from_season_id(season_id)
    team_roster = db_helper.get_team_roster_for_team_id(team_id)
    return render_template('roster.html', team_id=team_id, season=season,
                           teamroster=team_roster)


@app.route('/seasons/')
def showSeasons():
    """Handler showing a list of registered seasons."""
    seasons = db_helper.get_all_seasons()
    return render_template('seasons.html', seasons=seasons)


@app.route('/season/new/', methods=['GET', 'POST'])
def addSeason():
    """Handler to register a new season."""
    if not current_user.is_authenticated():
        flash("Login is required to access this page")
        return redirect(redirect_url())
    if request.method == 'POST':
        db_helper.add_new_season(request.form)
        flash("You've successfully added a season")
        return redirect(url_for('showSeasons'))
    else:
        return render_template('addseason.html')


@app.route('/season/<season_id>/edit/', methods=['GET', 'POST'])
def editSeason(season_id):
    """Handler to edit an already registered season"""
    if not current_user.is_authenticated():
        flash("Login is required to access this page")
        return redirect(redirect_url())
    if request.method == 'POST':
        db_helper.update_season(season_id, request.form)
        flash("You've successfully edited a season")
        return redirect(url_for('showSeasons'))
    else:
        season = db_helper.get_season_from_season_id(season_id)
        return render_template('editseason.html', season=season)


@app.route('/season/<season_id>/delete/', methods=['GET', 'POST'])
def deleteSeasonConfirmation(season_id):
    """Handler to confirming deletion an existing
    season."""
    if not current_user.is_authenticated():
        flash("Login is required to access this page")
        return redirect(redirect_url())
    if request.method == 'POST':
        db_helper.remove_season(season_id)
        flash("You've successfully DELETED a season")
        return redirect(url_for('showSeasons'))
    else:
        season = db_helper.get_season_from_season_id(season_id)
        return render_template('deleteseason.html', season=season)


@app.route('/regattas/')
def showRegattas():
    """Handler to display all regattas for all registered seasons"""
    seasons = db_helper.get_all_seasons()
    regattas = db_helper.get_all_regattas()
    return render_template('regattas.html', seasons=seasons, regattas=regattas)


@app.route('/regatta/<regatta_id>/')
def showRegatta(regatta_id):
    """Handler for page showing regatta profile."""
    regatta = db_helper.get_regatta_from_regatta_id(regatta_id)
    return render_template('regatta.html', regatta=regatta)


@app.route('/regatta/new/', methods=['GET', 'POST'])
def addRegatta():
    """Hander for page to add a new regatta."""
    if not current_user.is_authenticated():
        flash("Login is required to access this page")
        return redirect(redirect_url())
    seasons = db_helper.get_all_seasons()
    if request.method == 'POST':
        db_helper.add_new_regatta(request.form)
        flash("You've successfully added a regatta")
        return redirect(url_for('showRegattas'))
    else:
        return render_template('addregatta.html', seasons=seasons)


@app.route('/regatta/<regatta_id>/edit/', methods=['GET', 'POST'])
def editRegatta(regatta_id):
    """Handler for page to edit an existing regatta."""
    if not current_user.is_authenticated():
        flash("Login is required to access this page")
        return redirect(redirect_url())
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
    """Handler to confirm deletion an existing regatta."""
    if not current_user.is_authenticated():
        flash("Login is required to delete a regatta")
        return redirect(redirect_url())
    if request.method == 'POST':
        db_helper.remove_regatta(regatta_id)
        flash("You've successfully DELETED a regatta")
        return redirect(url_for('showRegattas'))
    else:
        regatta = db_helper.get_regatta_from_regatta_id(regatta_id)
        return render_template('deleteregatta.html', regatta=regatta)


@app.route('/rower/<rower_id>/')
def showRower(rower_id):
    """Handler to display rower profile"""
    rower = db_helper.get_rower_from_rower_id(rower_id)
    current_season = db_helper.get_current_season()
    current_team = db_helper.get_current_season_teams_for_rower_id(rower_id)
    return render_template('rowerprofile.html', rower=rower,
                           currentseason=current_season,
                           currentteam=current_team)


@app.route('/rower/<rower_id>/edit/', methods=['GET', 'POST'])
def editRower(rower_id):
    """Handler to edit existing rower profile"""
    if not current_user.is_authenticated():
        flash("Login is required to access this page")
        return redirect(redirect_url())
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
        current_team = db_helper.get_current_season_teams_for_rower_id(
                                                            rower_id=rower_id)
        return render_template('editrower.html', rower=rower,
                               rowedregattas=rowed_regattas,
                               seasons=seasons,
                               regattas=regattas,
                               currentseason=current_season,
                               currentteam=current_team)


@app.route('/rower/new/', methods=['GET', 'POST'])
def addRower():
    """Handler to add a new rower to DB"""
    if not current_user.is_authenticated():
        flash("Login required to access this page")
        return redirect(redirect_url())
    current_season = db_helper.get_current_season()
    if request.method == 'POST':
        # a bit of a kluge...  adds new rower to db and returns
        # the rower team ID... I could not get it to return the
        # rower with an id which would have been more general
        rower_team_id = db_helper.add_new_rower(request.form,
                                                request.files,
                                                UPLOAD_FOLDER)
        flash("You've successfully added a rower")
        return redirect(url_for('showRoster',
                                season_id=current_season.id,
                                team_id=rower_team_id))
    else:
        seasons = db_helper.get_all_seasons()
        regattas = db_helper.get_all_regattas()
        return render_template('addrower.html',
                               seasons=seasons,
                               currentseason=current_season,
                               regattas=regattas)


@app.route('/rower/<rower_id>/delete/', methods=['GET', 'POST'])
def deleteRowerConfirmation(rower_id):
    """Handler to confirm deletion of a rower."""
    if not current_user.is_authenticated():
        flash("Login required to delete rower")
        return redirect(redirect_url())
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
                (k, v.encode('utf-8') if type(v) is unicode
                    else v) for k, v in row.iteritems()
            )
        )
    csvfile.seek(0)
    return send_file(csvfile,
                     attachment_filename='rowers.csv',
                     as_attachment=True)


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
                (k, v.encode('utf-8') if type(v) is unicode
                    else v) for k, v in row.iteritems()
            )
        )
    csvfile.seek(0)
    return send_file(csvfile,
                     attachment_filename='regattas.csv',
                     as_attachment=True)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
