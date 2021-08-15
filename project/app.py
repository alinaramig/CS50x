import os
import requests
import urllib.parse
import psycopg2

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS
from functools import wraps

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to the movie_match postgres DB
connection = psycopg2.connect("dbname=movie_match user=postgres password=postgres")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# export API_KEY=pk_b6bc2c9b8b3e48f294b5e951f582dde7

# Import endpoints in other files
import auth
import match

@app.route("/")
@login_required
def index():
    """Show homepage, including users liked movies"""
    # connect to database
    cursor = connection.cursor()

    # Get movies a user likes from database
    cursor.execute("SELECT * FROM top_250 WHERE id IN (SELECT movie_id FROM likes WHERE user_id =%s AND preference ='t') ", [session["user_id"]])
    rows = cursor.fetchall()

    row_count = cursor.rowcount

    # Fill dictionary with movies
    likes = []

    for i in range(row_count):
        like = {}

        like["title"] = rows[i][0]
        like["year"] = rows[i][1]
        like["image"] = rows[i][2]
        like["rating"] = rows[i][3]

        likes.append(like)

    return render_template("index.html", likes = likes)

@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate():

    if request.method == "POST":

        # Retrieve Movie ID
        movie_id = request.form.get("movie")

        # Tell if user liked or Disliked movie
        preference = False

        if request.form.get("like") is not None:
            preference = True
        

        #connect to database
        cursor = connection.cursor()

        #Reccord movie_id and Preference in the users database
        cursor.execute("INSERT into likes ( user_id, movie_id, preference ) VALUES (%s, %s, %s)", (session["user_id"], movie_id, preference))

         # save changes to database
        connection.commit()

        # close cursor
        cursor.close()

        #redirect to rate the next movie
        return redirect("/rate")


    else:

        #connect to top_250 database
        cursor = connection.cursor()

        # Selects one movie that the user hasn't rated
        cursor.execute("SELECT * FROM top_250 WHERE id NOT IN (SELECT movie_id FROM likes WHERE user_id =%s) ORDER BY rating DESC LIMIT 1", [session["user_id"]])
        rows = cursor.fetchall()
        row_count = cursor.rowcount

        # Fill dictionary with movies
        movies = []

        for i in range(row_count):
            movie = {}

            movie["title"] = rows[i][0]
            movie["year"] = rows[i][1]
            movie["image"] = rows[i][2]
            movie["rating"] = rows[i][3]
            movie["id"] = rows[i][4]

            movies.append(movie)

        return render_template("rate.html", movies=movies)