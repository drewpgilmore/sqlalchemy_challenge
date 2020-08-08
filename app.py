from flask import Flask
import pandas as pd

hawaii_data = pd.read_csv('hawaii_df.csv')
#print(hawaii_data.head())


#app = Flask(__name__)

my_dict = {
    'Date': hawaii_data['Date'],
    'Prcp': hawaii_data['Prcp']
}

print(my_dict.keys())

""" @app.route("/")
def home():
    return 'Welcome to my home page!'
    #return all routes available

@app.route("/api/v1.0/precipitation")
#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
def jsonified():
    return jsonify(my_dict)


@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/tobs")
#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/<start>") 
@app.route("/api/v1.0/<start>/<end>")
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive. """