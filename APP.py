import io
from flask import Flask, render_template, request
import os
import numpy as np
import pandas as pd
from matplotlib.backends.backend_template import FigureCanvas

from CrimeAnalysis import CrimeAnalysis
from Predictions import Predictions

app = Flask(__name__)
# object of the crimeanalysis class
ca = CrimeAnalysis()
predict = Predictions()


@app.route('/',  methods=("POST", "GET"))
def overview():
    if request.method == 'POST':
        name = 'street'
        startyear = int(request.form.get('start_year'))
        startmonth = int(request.form.get('start_month'))
        finishyear = int(request.form.get('finish_year'))
        finishmonth = int(request.form.get('finish_month'))
        location = str(request.form.get('location')).lower()

        if startyear <= finishyear:
            uk_df = ca.load_data(name, startyear, startmonth, finishyear, finishmonth, location)
            ca.monthly_crime_frequency(uk_df)
            ca.crime_countplot(uk_df)
            ca.lsoa_countplot(uk_df)
            ca.locations_countplot(uk_df)
        else:
            print("The start needs to be smaller than finish")
    return render_template('overview.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/crime_advice')
def crime_advice():
    return render_template('crime_advice.html')

@app.route('/prediction',  methods=("POST", "GET"))
def prediction():



    return render_template('prediction.html')

@app.route('/statistics',  methods=("POST", "GET"))
def statistics():
    if request.method == 'POST':
        name = 'street'
        startyear = int(request.form.get('start_year'))
        startmonth = int(request.form.get('start_month'))
        finishyear = int(request.form.get('finish_year'))
        finishmonth = int(request.form.get('finish_month'))
        location = str(request.form.get('location')).lower()

        if startyear <= finishyear:
            #print(name, startyear, startmonth, finishyear, finishmonth, location)

            uk_df = ca.load_data(name, startyear, startmonth, finishyear, finishmonth, location)
            ca.crime_rate_heatmap(uk_df)
            ca.crime_pairplot(uk_df)
            #ca.geo_heatmap(uk_df)

    return render_template('statistics.html')

@app.route('/stop_and_search',  methods=("POST", "GET"))
def stop_and_search():
    if request.method == 'POST':
        name = 'stop-and-search'
        startyear = int(request.form.get('start_year'))
        startmonth = int(request.form.get('start_month'))
        finishyear = int(request.form.get('finish_year'))
        finishmonth = int(request.form.get('finish_month'))
        location = str(request.form.get('location')).lower()

        if startyear <= finishyear:
            #print(name, startyear, startmonth, finishyear, finishmonth, location)

            uk_df = ca.load_data(name, startyear, startmonth, finishyear, finishmonth, location)
            ca.monthly_stop_and_search_frequency(uk_df)
            ca.object_of_search_countplot(uk_df)
            ca.legislation_countplot(uk_df)
            ca.outcome_countplot(uk_df)


    return render_template('stop_and_search.html')


if __name__ == "__main__":
    app.run(debug=True)
