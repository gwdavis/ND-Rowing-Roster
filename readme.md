# Rowing Roster v0.1 
###a Udacity Nano-Degree Project for Full Stack Foundations

March 2015 by Gary Davis

###Description:
Rowing Roster provides team rosters, rowing profiles, regatta schedules and a record of regatta attendance.  The program was developed as part of a Udacity Full-Stack Nano-Degree program to explore database object relational mapping ("ORM"), "CRUD" (create, read, update, delete), RESTful design, OAuth login and some light styling.  

###Requirements:
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

###Installation (on a Mac OS)
* Open Terminal on the Mac (it is found in the utilities folder or use Spotlight to search for it)
* Change the directory from home to the vagrant directory installed on the Mac.  This can be done with:
```ShellSession
> cd [path to get to:]vagrant/rowing 
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


###Running the program

* From the command line of the virtual machine, change directory to that of the program files:
```ShellSession
> cd [path to get to:]/vagrant/rowing
> python app.py
```

* Alternatively, you can set up the dummy database first:
```ShellSession
> cd [path to get to:]/vagrant/rowing
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

* Add favicon
* Add a login page to chose between Google, Facebook or Twitter authentication
* Add seasons, so that views can be for a current or prior season
* Enhance regatta profiles to include maps and directions


