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

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# def home():
#     return (
#         f"Welcome to the Homepage<br/><br/>"
#         f"Available Routes:<br/>"
#         f"/api/v1.0/precipitation<br/>"
#         f"/api/v1.0/stations<br/>"
#         f"/api/v1.0/tobs<br/>"
#         f"/api/v1.0/&lt;start&gt;<br/>"
#         f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
#     )

@app.route('/')
def home():
    return '''
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: left;
                    background-color: #f2f2f2;
                }

                h1 {
                    font-family: 'Hanalei Fill', cursive;
                    font-size: 40px;
                    color: #d4af37;
                    margin-top: 50px;
                    text-align: center;
                    text-shadow: 2px 2px #8B4513;
                }

                p {
                    color: #777;
                    font-size: 18px;
                    margin-top: 0; 
                }

                a {
                    color: #337ab7;
                    text-decoration: underline;
                }

                .directions {
                    color: #777;
                    font-size: 12px;
                    margin-top: 10px;
                }
            </style>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Hanalei+Fill&display=swap" rel="stylesheet">
        </head>
        <body>
            <h1>Welcome to the Hawaiian Climate API</h1>
            <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br>
            <p class="directions">Returns precipitation data for 12 months (2016-08-23 to 2017-08-23).</p>
            <a href="/api/v1.0/stations">/api/v1.0/stations</a><br>
            <p class="directions">Returns a list of stations.</p>
            <a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br>
            <p class="directions">Returns temperature observations for the most active station in the last 12 months.</p>
            <a href="/api/v1.0/start">/api/v1.0/start</a><br>
            <p class="directions">Returns the minimum, average, and maximum temperatures after a start date entered in the YYYY-MM-DD format.</p>
            <a href="/api/v1.0/start-end">/api/v1.0/start-end</a><br>
            <p class="directions">Returns the minimum, average, and maximum temperatures between start and end dates entered in the YYYY-MM-DD format</p>
        </body>
        </html>
    '''

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in the data set.
    
    session = Session(engine)

    most_recent_date = session.query(Measurement.date).order_by(desc(Measurement.date)).first()[0]
    one_year_back = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query the precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_back).all()

    session.close()

    # Convert the query results to a dictionary
    precipitation_data = []
    for date, prcp in results:
        precipitation_data.append({
            "date": date,
            "prcp": prcp
        })

    return jsonify(precipitation_data)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
   
    """Return a JSON list of stations from the dataset."""
    
    session = Session(engine)
    
    # Query all the stations
    results = session.query(Station.station).all()
    
    session.close()
    
    # Convert the query results to a list
    station_list = [station for station, in results]
    return jsonify(station_list)

# Define the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most-active station for the previous year of data."""
    # Calculate the date one year from the last date in the data set.
    session = Session(engine)

    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = most_recent_date[0]
    one_year_back = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    most_active_station = 'USC00519281'
    # Query the temperature observations for the most-active station for the previous year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_back).all()
    
    session.close()
    # Convert the query results to a dictionary
    temperature_data = {date: tobs for date, tobs in results}
    
    return jsonify(temperature_data)

# Define the start route
@app.route("/api/v1.0/<start>")
def start(start):
    # Convert the start date string to a datetime object
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date).first()
    
    session.close()
    
    min_temp, avg_temp, max_temp = results

    temp_summary = {
        "TMIN": min_temp,
        "TAVG": avg_temp,
        "TMAX": max_temp
    }

    return jsonify(temp_summary)

# Define the start-end route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Convert the start and end date strings to datetime objects
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).first()

    session.close()

    min_temp, avg_temp, max_temp = results

    temp_summary = {
        "TMIN": min_temp,
        "TAVG": avg_temp,
        "TMAX": max_temp
    }
    return jsonify(temp_summary)

# Run the application
if __name__ == "__main__":
    app.run(debug=True)