# TCM-TEST
Dependencies and Installations:

* Clone this repository

* Must have a postgresdb to connect to. 
  enter user, password, port and host in the database.ini file.
  The defualt host is localhost and port is 5432. 
  To use postgresdb on localhost, please install postgresql and run the service on your local machine. 
  For information on installing and running postgresql refer to: https://www.postgresqltutorial.com/install-postgresql/

* Must have python and pip installed on device
  
* In order to install all the python dependencies run: "pip install -r requirements.txt"

* In order to start/stop the server you must find the location of your PostgreSQL database directory it can be like: C:\Program Files\PostgreSQL\data
  - To start the server you need to open the command line and execute: **pg_ctl -D "C:\Program Files\PostgreSQL\data" start**
  - To stop the server you need to open the command line and execute: **pg_ctl -D "C:\Program Files\PostgreSQL\data" stop**

* To run the script run "python main.py"
* now you can send requests to the api. if you are running on localhost then an example is:
  http://localhost:8000/Tel_Aviv 

* in order to see resuls you can view the DB 
