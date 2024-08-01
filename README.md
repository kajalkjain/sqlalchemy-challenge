# sqlalchemy-challenge
Module 10 Challenge is about exploring Hawaii Climate database provided using Python and SQLAlchemy.

Python and SQLAlchemy is used to do a basic climate analysis and data exploration of climate database. 
SQLAlchemy ORM queries, Pandas, and Matplotlib are included in exploring.

Part 1:  climate_starter.ipynb 

This code contains:

Create_engine() functions is used to connect to SQLite database.
Linked Python to the database by creating a SQLAlchemy session.
Explored and Analysed Climate Data:
  calculate the total number of stations in the dataset
  List the stations and observation counts in descending order.
  Using the most-active station id, calculate the lowest, highest, and average temperatures.

Precipitation and Station Analysis
  Pandas is used to print the summary statistics for the precipitation data
  Histogram is plotted for previous 12 months of TOBS data for the station

Part 2: app.py (Climate App)

Designed a Flask API based on various queries
Convert the query results to a dictionary by using date as the key and prcp as the value.
Return the JSON representation of your dictionary.
Return a JSON list of stations from the dataset.
Query the dates and temperature observations of the most-active station for the previous year of data.
Return a JSON list of temperature observations for the previous year.
Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
