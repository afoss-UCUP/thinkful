#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Write a script called "database.py" to print out the cities with the July being the warmest month. 
Your script must:

    Connect to the database
    
    Create the cities and weather tables 
    (HINT: first pass the statement DROP TABLE IF EXISTS <table_name>; to 
    	remove the table before you execute the CREATE TABLE ... statement)
    
    Insert data into the two tables
    
    Join the data together
    
    Load into a pandas DataFrame

    Print out the resulting city and state in a full sentence. 
      For example: "The cities that are warmest in July are: Las Vegas, NV, Atlanta, GA..."
'''

import sqlite3 as lite
import pandas as pd


# Data for tables

cities = (
	('New York City', 'NY'),
	('Boston', 'MA'),
	('Chicago', 'IL'),
	('Miami', 'FL'),
	('Dallas', 'TX'),
	('Seattle', 'WA'),
	('Portland', 'OR'),
	('San Francisco', 'CA'),
	('Los Angeles', 'CA')
	)

weather = (
	('New York City', 2013, 'July', 'January', 62),
	('Boston', 2013, 'July', 'January', 59),
	('Chicago', 2013, 'July', 'January', 59),
	('Miami', 2013, 'August', 'January', 84),
	('Dallas', 2013, 'July', 'January', 77),
	('Seattle', 2013, 'July', 'January', 61),
	('Portland', 2013, 'July', 'December', 63),
	('San Francisco', 2013, 'September', 'December', 64),
	('Los Angeles', 2013, 'September', 'December', 75)
	)	


con = lite.connect('getting_started.db')

with con:
    cur = con.cursor()

    # Drop any existing tables
    try: cur.execute('DROP TABLE cities')
    except: pass
    try: cur.execute('DROP TABLE weather') 
    except: pass
	try: cur.execute('DROP TABLE cities_copy')   
    except: pass

    # Create new tables
    cur.execute('CREATE TABLE cities (name text, state text)')
    cur.execute('CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)')  

    # Populate tables
    cur.executemany("INSERT INTO cities VALUES(?,?)", cities)
    cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)

    # Join tables
    cur.execute('''SELECT city, state, year, warm_month, cold_month, average_high 
    	           FROM cities INNER JOIN weather ON name=city;''')

    # Load data into Python
    rows = cur.fetchall()

    # Get header
    cols = [desc[0] for desc in cur.description]

    # Load data into Pandas
    df = pd.DataFrame(rows, columns=cols)

    # Grab the two cities that are warmest in July
    warmest_2 = sorted([(c, t) for c, m, t in 
                        zip(df['city'], df['warm_month'], df['average_high']) 
                        if m == 'July'], key=lambda x: x[1], reverse=True)[:2]
    
    print("The cities that are warmest in July are: {}.".format(' and '.join(x[0] for x in warmest_2)))

