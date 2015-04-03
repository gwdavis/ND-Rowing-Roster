# Rowing Roster v0.1 
###a Udacity Nano-Degree Project for Full Stack Foundations

April 2015 by Gary Davis

###Description:
Rowing Roster provides team rosters, rowing profiles, regatta schedules and a record of regatta attendance.  The program was developed as part of a Udacity Full-Stack Nano-Degree program to explore database object relational mapping ("ORM"), "CRUD" (create, read, update, delete), RESTful design, OAuth login and some light styling.

###Live Demo Site:
A live demo site can be seen on Heroku [here](http://cryptic-woodland-5962.herokuapp.com/admin/)
You may notice an intermittent bug when you try to authorize through Facebook.  If so a refresh will allow you to keep going.  Also the Heroku install included the Gunicorn web server (pip install gunicorn) and a file named Procfile containing::
```
web: gunicorn app:app --log-file -
```

###Requirements:
* virtualenv or a virtual machine
* See in file requirements.txt

For the Udacity Nano-Degree class, we installed a virtual machine using VirtualBox and Vagrant and pulled the necessary setup from GIT (see: https://www.udacity.com/wiki/ud197/install-vagrant)

###Files:
|File|Purpose|
|------------------------|------------------------------|
|app.py					|The main application program|
|db_helper.py 			|Database access functions
|oauth.py 				|OAuth login functions
|database_setup.py		|Database model
|database_populate.py 	|Sets up dummy database content

###Installation (on a Mac OS with Vagrant installed)
* Open Terminal on the Mac (it is found in the utilities folder or use Spotlight to search for it)
* Change the directory from home to the vagrant directory installed on the Mac and install Rowing Roster from Github.  This can be done with:
```ShellSession
> cd [path to get to:]vagrant
> git clone https://github.com/gwdavis/ND-Rowing-Roster.git
```
* Fire up the virtual machine: 
```ShellSession 
> vagrant up
```  
* SSH into the virtual machine, again form the Mac Terminal program: 
```ShellSession 
> vagrant SSH  
```
  You should now see the command line of the virtual machine
 * Change directories to ND-Rowing_Roster and install requirements:

 ```ShellSession
 > pip intall -r requirements.txt
 ```

###Installation (on a Mac OS with Vitrualenv)
* Open Terminal on the Mac (it is found in the utilities folder or use Spotlight to search for it)
* Change the directory from home to the vagrant directory installed on the Mac and install Rowing Roster from Github.  This can be done with:
```ShellSession
> cd [path to get to where you wish to install the rowing roster directory:]
> git clone https://github.com/gwdavis/ND-Rowing-Roster.git
> cd ND-Rowing-Roster
```
Note - If you want to change the name of the directory, now is the time to do it before you set up your virutal environment
* Install virtualenv if not already installed: 
```ShellSession 
> pip install virtualenv
```  

* Set up virtualenv in the rowing roster directory (make sure you are in the ND-Rowing_Roster or the renamed directory).  You can use any name for the virtualenv directory but venv will do:
```ShellSession
> virtualenv venv
```
* Activate the enviroment with the following command. It can be deactived with "deactivate""
```ShellSession
> source: venv/bin/activate
```
* Install requirements:
```ShellSession
> pip install -r requirements.txt
```
* One more thing...  the last line of app.py is set up for Vagrant.
```python
app.run(host='0.0.0.0', port=5000)
```
You can edit it to remove host='0.0.0.0', or be aware that other computers on your network can access the website by using your machines IP address/5000.  Alternatively, on a Mac, if you firewall is up, your machine should ask if you ant python to accept incoming connections, simply "Deny".

###Setting up Facebook Credentials for OAuth
* Check out Miguel Grinberg's detailed description [here](http://blog.miguelgrinberg.com/post/oauth-authentication-with-flask)
> To create a Facebook app you can visit https://developer.facebook.com. Select "Add a New App" from the Apps dropdown, and make the type "WWW/Website". Then enter a name and category for your app. Once the application is created, go to the "App Configuration" section and set the URL of the application, which in the case of you running it on your own computer will be http://localhost:5000.

* in app.py in the variable app.config['OAUTH_CREDENTIALS'], add the id and secret key you obtained from Facebook.

###Running the program

* From the command line of the virtual machine, change directory to that of the program files:
```ShellSession
> cd [path to get to:]/ND-Rowing-Roster
> python app.py
```

* Alternatively, you can set up the dummy database first:
```ShellSession
> cd [path to get to:]/ND-Rowing-Roster
> python database_setup.py
> python database_populate.py
> python app.py
```

* Next go to your browser and connect to localhost:5000/


###Resources and Sources Used in Developing Rowing Roster

In addition to Udacity materials, I found the following information helpful:

* http://www.sqlalchemy.org
* http://flask.pocoo.org
* Udacity Student FSND P3 Submission - http://nd-sharables.herokuapp.com
* Udacity Student FSND P3 Submission - https://github.com/DawoonC/nd-sharables
* Udacity Student FSND P3 Submission - https://github.com/allanbreyes/mooc-catalog
* http://stackoverflow.com/questions/14277067/redirect-back-in-flask
* API - http://flask.pocoo.org/docs/0.10/api/#useful-functions-and-classes
* API - http://stackoverflow.com/questions/27238247/how-to-stream-csv-from-flask-via-sqlalchemy-query
* Upload - http://flask.pocoo.org/docs/0.10/patterns/fileuploads/#uploading-files
* module path - http://www.karoltomala.com/blog/?p=622
* getlist - http://stackoverflow.com/questions/7996075/iterate-through-checkboxes-in-flask
* list difference - http://stackoverflow.com/questions/9335773/python-list-difference
* Oauth - https://github.com/miguelgrinberg/flask-oauth-example
* Styling - http://getbootstrap.com/getting-started/



###Possible Future Enhancements

* Fix OAuth bug on Heroku deployment
* Add favicon
* Add a login page to chose between Google, Facebook or Twitter authentication
* Add seasons, so that views can be for a current or prior season
* Enhance regatta profiles to include maps and directions


