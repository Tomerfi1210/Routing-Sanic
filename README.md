# TCM-TEST
Dependencies and Installations:

* Clone this repository

* Must have postgresql installed on a local machine or a remote to connect to. 
  The default host is localhost and port is 5432. 
  To use postgres on localhost, please install postgresql and run the service on your local machine. 
  For information on installing and running postgresql refer to: https://www.postgresqltutorial.com/install-postgresql/

* In order to start/stop the server you must find the location of your PostgreSQL database directory it can be like: C:\Program Files\PostgreSQL\data
  - To start the server you need to open the command line and execute: **pg_ctl -D "C:\Program Files\PostgreSQL\data" start**
  - To stop the server you need to open the command line and execute: **pg_ctl -D "C:\Program Files\PostgreSQL\data" stop**
* have python installed
* open the command line and run "python -m venv [your_project/venv]"
* run **your_project/venv/Scripts/activate.bat** in order to activate the venv
* run "pip install -r requirements.txt" to install python dependencies
* To run the script run "python main.py"
* now you can send requests to the api. if you are running on localhost then an example is:
  http://localhost:8000/Tel_Aviv 

* in order to see results you can view the DB through program like pgAdmin
