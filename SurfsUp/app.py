# Import the dependencies.

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route('/')
def home():
    return (
        f"Welcome to the Homepage<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Perform the query to retrieve the precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_back).\
        filter(Measurement.date <= most_recent_date).all()
    
    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_dict = {}
    for date, prcp in results:
        precipitation_dict[date] = prcp
    
    # Return the JSON representation of the dictionary
    return jsonify(precipitation_dict)

@app.route('/api/v1.0/stations')
def stations():
   
    # Perform the query to retrieve the list of stations
    results = session.query(Station.station).all()
    
    # Convert the query results to a list
    station_list = [result[0] for result in results]
    
    # Return the JSON representation of the list
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():

    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def temperature_stats_start(start):
  
    
    return jsonify(stats_dict)

@app.route('/api/v1.0/<start>/<end>')
def temperature_stats_start_end(start, end):

    return jsonify(stats_dict)

if __name__ == '__main__':
    app.run()