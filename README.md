The site should run properly immediately if you clone the repo. This assumes that the
database is turned on and that you have all the necessary modules installed.

There are some default user objects that are created by init.py, for the sake of the
database. However, do not use these users to log in as the site will throw an error.

We encourage you to log in using: mike (PW: mike) (role: student), andy
(PW: andy) (role: faculty), and jessica (PW: jessica) (role: employer).

If you intend to run the site, Maxwell will need to be informed in order to start the
database instance, as the site will not post until it can establish a connection to the 
SQL server.

Feel free to create any user you like; every piece of (role-specific) functionality in 
the site works with any and all users. Nothing in the project is hard coded.

Something I would have liked to implement was delete buttons for students who wish to
rescind their application to a listing, and for employers who have active listings that 
have since obsolesced.

One last thing I want to add: Cara, Brec, Steve, Maxi and I all put our best foot forward 
to make this site the best it could be given the timeframe and everyone's complex 
schedules. While you cannot realistically create a perfect product, we are still very
proud of what we were able to create, and we all learned a lot during the development
process. This project is a great preview of what goes on in the real computer science
world.
<hr>
Instructions to run the application

STEP 0: This assumes that you have a database named population already created.

STEP 1: Install the Flask login and security modules from the command line:

     ``sudo pip3 install flask_login werkzeug``

STEP 2: Go to the project home directory, and edit .flaskenv accordingly.
        Update the database variables to the appropriate values.
        Save your edits and quit micro.

STEP 3: Run the Flask application from the project home directory:
     
     ```flask run```

STEP 4: Login credentials for application:

     ```Admin user  : admin   password: csc330sp22```
     ```Regular user: user    password: csc330sp22```

Thank you.

Developed by Maxwell Hauser, Cara C., Maxi K., Steve M. and Brec A.
