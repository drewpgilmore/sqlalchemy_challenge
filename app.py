import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################
#initiate flask and define routes
app = Flask(__name__)

@app.route("/")
def home():
    return (
       f'/api/v1.0/precipitation<br/>'
       f'/api/v1.0/stations<br/>'
       f'/api/v1.0/tobs<br/>'
       f'/api/v1.0/2012-05-01<br/>'
       f'/api/v1.0/2012-05-01/2012-06-01<br/>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a dictionary of dates and prcps
    # Query precipitation and date
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Convert list of tuples into dictionary
    prcp_dict = {result[0]:result[1] for result in results}
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a dictionary of dates and prcps
    # Query precipitation and date
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into regular list
    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
def temps():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()
    session.close()
    end_date = dt.datetime.strptime(results[-1][0], '%Y-%m-%d')
    start_date = end_date - dt.timedelta(days=365)
    last_year = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > start_date).all()
    dates = [date[0] for date in last_year]
    temps = [date[1] for date in last_year]
    last_year_dict = {date:temp for date,temp in zip(dates,temps)}
    return jsonify(last_year_dict)

@app.route("/api/v1.0/<start>") 
def get_temps(start):
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()
    session.close()
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()[0][0]
    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()[0][0]
    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()[0][0]
    
    return (
        f'Min Temp: {min_temp}<br/>'
        f'Max Temp: {max_temp}<br/>'
        f'Average Temp: {round(avg_temp, 2)}'
    )
    
@app.route("/api/v1.0/<start>/<end>") 
def trip_temps(start,end):
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()
    session.close()
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        all()[0][0]
    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        all()[0][0]
    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        all()[0][0]
    return (
        f'Min Temp: {min_temp}<br/>'
        f'Max Temp: {max_temp}<br/>'
        f'Average Temp: {round(avg_temp, 2)}'
    )

if __name__ == "__main__":
    app.run(debug=True)