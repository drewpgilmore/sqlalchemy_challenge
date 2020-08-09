import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
       f'/api/v1.0/<start><br/>'
       f'/api/v1.0/<start>/<end><br/>'
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
    results = session.query()



    last_date = hawaii_data['Date'].max()
    start_date = last_date - dt.timedelta(days=365)
    prev_year = hawaii_data[hawaii_data['Date'] > start_date].reset_index()
    prev_year_dict = prev_year['Temp'].to_dict()
    return jsonify(prev_year_dict)

@app.route("/api/v1.0/<start>") 
def get_temps(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    timeframe = hawaii_data[hawaii_data['Date'] > start_date].reset_index()
    min_temp = timeframe['Temp'].min()
    max_temp = timeframe['Temp'].max()
    avg_temp = timeframe['Temp'].mean()
    return (
        f'{start}<br/>'
        f'Min Temp: {min_temp}<br/>'
        f'Max Temp: {max_temp}<br/>'
        f'Avg Temp: {avg_temp}<br/>'
    ) """

#@app.route("/api/v1.0/<start>/<end>")
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
if __name__ == "__main__":
    app.run(debug=True)