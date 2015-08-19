For gasoline! 

## Install

No need to install

## Run

1. Run `sql.sql` in your own mysql database. It will create a database `pytrace` and tables needed. 
2. Update app.config, give it the real source code location(should be svn repo), and mysql connection configurations.
3. update server ip and port number in server.py, keep it remembered.
4. `$ nohub python server.py &`
5. See the result after you setup bus_station project.