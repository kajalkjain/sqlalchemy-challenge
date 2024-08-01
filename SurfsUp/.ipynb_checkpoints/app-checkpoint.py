# Import the dependencies.

from flask import Flask, json, jsonify
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
import pandas as pd

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#connect_args={'check_same_thread': False})

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
#Base.prepare(engine, reflect=True)
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__) 

#################################################
# Flask Routes
#################################################
# List all routes that are available.
@app.route("/")
def home():
        return (
        f"Welcome to Home page of Hawaii Climate API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-01-01/<br/>"
        f"/api/v1.0/2016-01-01/2016-12-31/"
    )

# Return the JSON representation of your dictionary
@app.route('/api/v1.0/precipitation/')
def precipitation():
    print("In Precipitation section.")
    
    last_12months = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_1year = dt.datetime.strptime(last_12months, '%Y-%m-%d') - dt.timedelta(days=365)

    prec_scores = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_1year).\
    order_by(Measurement.date).all()

    prec_scores_dict = dict(prec_scores)
    print(f"Results for Precipitation - {prec_scores_dict}")
    print("Out of Precipitation section.")
    return jsonify(prec_scores_dict) 

# Return a JSON-list of stations from the dataset.
@app.route("/api/v1.0/stations/")
def stations():
    
    # Query for stations.
    stations = session.query(Station.station).all()
    
    # Convert the query results to a dictionary.
    list_sta = [station for station, in  stations]
    
    # Return the JSON representation of dictionary.
    return jsonify(list_sta)

@app.route('/api/v1.0/tobs/')
def tobs():
    # Determine the date one year ago from the last data point in the database
    last_12months = session.query(func.max(Measurement.date)).scalar()
    last_1year = (pd.to_datetime(last_12months) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')

    # Query the dates and temperature observations of the most-active station for the previous year of data.
    #mostactive_stn = session.query(Measurement.station, Measurement.tobs).filter(Measurement.station =='USC00519281')
    mostactive_stn = session.query(
        Measurement.station,
        func.count(Measurement.station)
    ).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]
    
    mostactive_stn1=session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.station == mostactive_stn,
        Measurement.date >= last_1year).all()
        
    #Return a JSON list of temperature observations for the previous year.
    tobs_list = [{'date': date, 'tobs': tobs} for date, tobs in  mostactive_stn1]
    return jsonify(tobs_list)


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
@app.route('/api/v1.0/<start_date>/')

def temp_start(start_date):
    startdt = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start_date).all()
    
    temp_start1 = {
        'MIN_TEMP': startdt[0][0],
        'AVG_TEMP': startdt[0][1],
        'MAX_TEMP': startdt[0][2]
    }
    return jsonify(temp_start1)  
    
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
@app.route('/api/v1.0/<start>/<end>/')
def temp_startEnd(start,end):
   
    start_end_dt = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temp_st_end = {
        'MIN_TEMP': start_end_dt[0][0],
        'AVG_TEMP': start_end_dt[0][1],
        'MAX_TEMP': start_end_dt[0][2]
    }
    return jsonify(temp_st_end)    

if __name__ == "__main__":
    app.run(debug=True)
