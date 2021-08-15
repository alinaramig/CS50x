import os
import requests
import urllib.parse
import psycopg2
import json

from flask import redirect, render_template, request, session
from functools import wraps

# Connect to the movie_match postgres DB
connection = psycopg2.connect("dbname=movie_match user=postgres password=postgres")

api_key = os.environ.get("API_KEY")
url = f"https://imdb-api.com/en/API/Top250Movies/{api_key}"
response = requests.get(url)

items = response.json()['items']

for i in items:
    # Get values from database
   idenification = i["id"]
   title = i["title"]
   year = i["year"]
   image = i["image"]
   rating = i["imDbRating"]

   # insert values into table top_250
   cur = connection.cursor()
   cur.execute("INSERT into top_250 (id, title, year, image, rating) VALUES(%s, %s, %s, %s, %s)",(idenification, title, year, image, rating))

# save changes to database
connection.commit()

# close connection to database
cur.close()
connection.close()