from flask import Flask
from flask import render_template
from flask import request
from flask import Response

import json
import time
import sys
import random
import math

import pyorient

from Queue import Queue

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/getData/")
def filter_database():

    client = pyorient.OrientDB("localhost", 2424)
    session_id = client.connect("root", "110891")

    db_name = "weibo"
    db_username = "admin"
    db_password = "admin"

    if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
		client.db_open( db_name, db_username, db_password )
		print db_name + " opened successfully"

    else:
		print "database [" + db_name + "] does not exist! session ending..."
		sys.exit()

	#get checkins
    query = 'SELECT FROM Checkin WHERE lat BETWEEN 22.929935 AND 22.961751 AND lng BETWEEN 113.639837 AND 113.693017 AND time BETWEEN "2014-09-03 03:00:00" and "2014-09-04 04:00:00"'
    records = client.command(query)

    numListings = len(records)
    print 'received ' + str(numListings) + ' Checkins'

    #uniqueUsers = []
    #originPlaces = []
    #connectedPlaces = []

    # for each checkin
    #for record in records:

    	#get user id
    #	user = str(record.out)

    	#skip repeating users
    #	if user in uniqueUsers:
    #		continue
    #	uniqueUsers.append(user)

    	#find connected places
     #   places = client.command("SELECT * FROM (TRAVERSE out(Checkin) FROM (SELECT * FROM {})) WHERE @class = 'Place'".format(record.out))
      #  print 'received ' + str(len(places)) + ' connected places from ' + str(record._in)

        #for each connected place, store information of origin and connected place in separate lists
       # for place in places:
        #	originPlaces.append(str(record._in))
        #	connectedPlaces.append(str(place._rid))

    #show connections between lists
   # for i in range(len(originPlaces)):
    #	print originPlaces[i] + " <--> " + connectedPlaces[i]

    client.db_close()

    output = {"type":"FeatureCollection","features":[]}

    for record in records:
	feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
	feature["id"] = record._rid
	feature["properties"]["text"] = record.text
	feature["properties"]["time"] = record.time
	feature["geometry"]["coordinates"] = [record.lat, record.lng]
	print 'features' + str(feature)

	output["features"].append(feature)
	print output
    return json.dumps(output)


#filter_database()
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)