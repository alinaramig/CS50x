import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS

from helpers import login_required

# Configure application
app = Flask(__name__)
CORS(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("postgres://postgres:postgres@localhost:5432/movie_match")


@app.route("/hello")
# @login_required
def hello():
    """Show portfolio of stocks"""

    # create dictionary where I can store everything needed for the table
    rows = db.execute("SELECT * FROM test_table")

    return rows[0]


# @app.route("/login", methods=["POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     # Ensure username was submitted
#     if not request.form.get("username"):
#         return apology("must provide username", 403)

#     # Ensure password was submitted
#     elif not request.form.get("password"):
#         return apology("must provide password", 403)

#     # Query database for username
#     rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

#     # Ensure username exists and password is correct
#     if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#         return apology("invalid username and/or password", 403)

#     # Remember which user has logged in
#     session["user_id"] = rows[0]["id"]

#     # Redirect user to home page
#     return redirect("/")


# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")


# @app.route("/register", methods=["POST"])
# def register():
#     """Register user"""
        
#     password = request.form.get("password")
    
#     username = request.form.get("username")

#     # Ensure username was submitted
#     if not username:
#         return apology("must provide username", 400)

#     # Ensure password was submitted
#     elif not password:
#         return apology("must provide password", 400)

#     # Ensure confirm password was submitted
#     elif not request.form.get("confirmation"):
#         return apology("must confirm password", 400)
    
#     # Ensure password is 8 charachters or more
#     if len(password) < 8:
#         return apology("Password must be at least 8 charachters", 400)
    
#     number = False
    
#     # Ensure password includes a number
#     for letter in password:
#         if letter.isnumeric():
#             number = True
            
#     if number == False:
#         return apology("Password must include a number", 400)

#     # Ensures User does not already have an account
#     rows = db.execute("SELECT * FROM users WHERE username = ?", username)

#     if len(rows) != 0:
#         return apology("Username already exists", 400)

#     # Ensures passwords match
#     if password != request.form.get("confirmation"):
#         return apology("passwords do not match", 400)

#     # Insert user into database
#     phash = generate_password_hash(password)

#     db.execute("INSERT into users (username, hash) VALUES(?, ?)", username, phash)

#     # Redirect user to login - not completely done might need to log them in
#     return redirect("/login")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return "Error"


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
