Database Application
=======================

## Tools to install 
1. lxml
    ``` 
    sudo pip install lxml

    ```
2. flask
    ```
    sudo pip install virtualenv
    mkdir myproject
    cd myproject
    virtualenv venv
    . venv/bin/activate
    venv\scripts/activate

    ```

  now install flask

    ```
    pip install Flask

    ```

3. sqlalchemy

    ```
    pip install SQLAlchemy

    ```
## how to run

    start the mysqld demon process in the backend

    ```
    mysqld

    ```
    start the backend sql program

    ```
    ./sql.py

    ```
    execute the sehll script which includes generating the new xml files 

    ```
    ./run.sh

    ```
    after running through all those steps, the new_test.xml
    is the final output generated from database


## functions
#   init_db()

create a db session

#   class Node

table Node definition

#   class Database
table Database definition

#   class Datacenter
table Datacenter definition

#   class OS
table OS definition

#   class PatchRelease
table PatchRelease definition

#   class App
table App definition

#   function main
call the index.html page showing

#   function generate()
function to get request from the web page on the front end and insert the values into the tables

#   function create()
function to create xml file from database



