from flask import Flask, jsonify
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

hawaii_data = pd.read_csv('hawaii_df.csv')
#print(hawaii_data.head())

hawaii_data['Date'] = pd.to_datetime(hawaii_data['Date'])

keys = hawaii_data['Date'].to_list()
values = hawaii_data['Prcp'].to_list()


app = Flask(__name__)

my_dict = {key:value for key, value in zip(keys,values)}

station_dict = hawaii_data['Station'].to_dict()

#print(my_dict.keys())

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
#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
def jsonified():
    return jsonify(my_dict)


@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.
def station_json():
    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
def temps():
    last_date = hawaii_data['Date'].max()
    start_date = last_date - dt.timedelta(days=365)
    prev_year = hawaii_data[hawaii_data['Date'] > start_date]
    prev_year_dict = prev_year['Temp'].to_dict()
    return jsonify(prev_year_dict)

#@app.route("/api/v1.0/<start>") 
#@app.route("/api/v1.0/<start>/<end>")
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
if __name__ == "__main__":
    app.run(debug=True)