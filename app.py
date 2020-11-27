from flask import Flask, jsonify, render_template

import datetime as dt
import calendar as cal
import re

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Column, Integer, String, Float, Table

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind=engine)


                

app = Flask(__name__)
#Creating dictionary for 

@app.route("/")
def home():
        return render_template('root.html')

@app.route("/api/v1.0/precipitation")
def precipitation():
        print('entro')
        #Answer dictionary definition
        answer = []

        # Design a query to retrieve the last 12 months of precipitation data and plot the results
        measurement_q = session.query(Measurement.date, Measurement.prcp)

        #Getting the last 12 months registered by getting results from measurement in a date descending order
        measure_recs = measurement_q.order_by(Measurement.date.desc())

        # Calculate the date 1 year ago from the last data point in the database
        end_date = dt.datetime.strptime(measure_recs.first().date, '%Y-%m-%d')
        start_date = (end_date - dt.timedelta(364))
        measurement_filter = measurement_q.filter(Measurement.date<=end_date).filter(Measurement.date>=start_date)

        for row in measurement_filter:
                answer.append({'date': row.date, 'prcp': row.prcp})

        return jsonify(answer)

#Getting list of stations
@app.route("/api/v1.0/stations")
def stations():
        station_results = []

        #Getting list of Stations
        station_results_q = session.query(Station)

        for station_row in station_results_q:
                station_results.append({'station': station_row.station, 'name': station_row.name, 'latitude': station_row.latitude, 'longitude': station_row.longitude, 'elevation': station_row.elevation})

        return jsonify(station_results)

#Getting tobs of the most active station
@app.route("/api/v1.0/tobs")
def tobs():

        query= (session.query(Measurement.station, func.count(Measurement.station))
       .group_by(Measurement.station)
       .order_by(func.count(Measurement.station).desc())
      )

      #The most active station:
        station_id = query.first()
     
        #To associate dates and tobs to the station
        dates_tobs_dic = []
        #Adding station id as first element of array
        max_temp_station = {}
        #max_temp_station = [{ 'dates_tobs': dates_tobs_dic, 'station': station_id[0]}]
        max_temp_station['station']= station_id[0]

        max_temp_station_q = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station==station_id[0])
        
        #Adding all dates and temperatures
        for max_temp_station_row in max_temp_station_q:
                dates_tobs_dic.append({'date': max_temp_station_row.date, 'tobs': max_temp_station_row.tobs})

        #Adding the list of dates and tem`peratures at the same level as station 
        max_temp_station['dates_tobs']=dates_tobs_dic
        return jsonify(max_temp_station)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
def temperature(start):
        
        #Validating start date format
        try:
                dt.datetime.strptime(start, '%Y-%m-%d')
        except ValueError:     
                return jsonify({"Error":"Incorrect start date format, should be YYYY-MM-DD"})


        query= (session.query(Measurement.station, func.count(Measurement.station))
                .group_by(Measurement.station)
                .order_by(func.count(Measurement.station).desc())
                )

      #The most active station:
        station_id = query.first()
             
        
        #Getting max, min, average temperatures given a start date and end date
        station_temp_q = (
                session.query(Measurement.station, func.min(Measurement.tobs).label('min_temp'), 
                func.max(Measurement.tobs).label('max_temp'), 
                func.avg(Measurement.tobs).label('avg_temp'),
                Measurement.date)
                .filter(Measurement.station==station_id[0])
                .filter(Measurement.date>=start)
                .first()
                )

        #To print results
        station_temp = {}
        station_temp['station'] = station_temp_q.station
        station_temp['min_temp'] = station_temp_q.min_temp
        station_temp['max_temp'] = station_temp_q.max_temp
        station_temp['avg_temp'] = station_temp_q.avg_temp

        return jsonify(station_temp)

        
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>/<end>")
def temperature_2(start, end):
        
        #Validating start date format
        try:
                dt.datetime.strptime(start, '%Y-%m-%d')
        except ValueError:     
                return jsonify({"Error":"Incorrect start date format, should be YYYY-MM-DD"})

       
        #Validating end date format
        try:
                dt.datetime.strptime(end, '%Y-%m-%d')
                       
        except ValueError:
                return jsonify({"Error":"Incorrect end date format, should be YYYY-MM-DD"})
        

        query= (session.query(Measurement.station, func.count(Measurement.station))
                .group_by(Measurement.station)
                .order_by(func.count(Measurement.station).desc())
                )

      #The most active station:
        station_id = query.first()
             
        
        #Getting max, min, average temperatures given a start date and end date
        station_temp_q = (
                session.query(Measurement.station, func.min(Measurement.tobs).label('min_temp'), 
                func.max(Measurement.tobs).label('max_temp'), 
                func.avg(Measurement.tobs).label('avg_temp'),
                Measurement.date)
                .filter(Measurement.station==station_id[0])
                .filter(Measurement.date>=start)
                .filter(Measurement.date<=end)
                .first()
                )

        #To print results
        station_temp = {}
        station_temp['station'] = station_temp_q.station
        station_temp['min_temp'] = station_temp_q.min_temp
        station_temp['max_temp'] = station_temp_q.max_temp
        station_temp['avg_temp'] = station_temp_q.avg_temp

        return jsonify(station_temp)


if __name__ == "__main__":
    # @TODO: Create your app.run statement here
    app.run(debug=True)