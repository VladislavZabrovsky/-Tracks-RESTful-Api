# -Tracks-RESTful-Api
Labwork №3 from course Computer Networks
This is my implementation of RESTful Api fo retrieving tracks from database.
User can use GET,POST,PUT,PATCH,DELETE HTTP methods to glean specific info about
a track or make some changes.

Api is located in main.py,can be launched in terminal via "python main.py"

You can test the requests in test.py file, launching it in terminal via "python test.py"

Every time we launch Api,it initializes database with default 5 tracks and during
restart of Api or implemented changes will droped and database with default 5 tracks
will be created again.
