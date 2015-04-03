# NAME OF APP v0.1- a Udacity Nano-Degree Project for Full Stack Foundations
March 2015 by Gary Davis

DESCRIPTION OF THE APP


For the Udacity Nano-Degree class, we installed a virtual machine using VirtualBox and Vagrant and pulled the necessary setup from GIT (see: https://www.udacity.com/wiki/ud197/install-vagrant)

###Files:
* app.py
* dp_helper.py
* Oauth.py
* database_setup.py
* database_populate.py

###Installation (on a Mac OS)
* Open Terminal on the Mac (it is found in the utilities folder or use Spotlight to search for it)
* Change the directory from home to the vagrant directory installed on the Mac.  This can be done with:
```ShellSession
> cd [path to get to:]fullstack/vagrant  
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

* From the command line of the virtual machine, change directory to that of the rowing program files:
```ShellSession
> cd /vagrant/rowing
```

* The database can be set up and populated in sqlite:
```>python database_setup.py
> pytyon database_populate.py
```

* And then run the program and open a browser window to localhost:5000
```> python app.py
```








