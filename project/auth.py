from app import app, connection

import psycopg2

from flask import render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        # Ensure username was submitted

        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", [request.form.get("username")])


        # Ensure username exists and password is correct
        try:
            row = cursor.fetchone()

            if not check_password_hash(row[2], request.form.get("password")):
                return apology("invalid password", 403)
        
        except:
            return apology("invalid username", 403)
        
        # Stop acessing database
        cursor.close()

        # Remember which user has logged in
        session["user_id"] = row[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        
        password = request.form.get("password")
        
        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure confirm password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        
        # Ensures passwords match
        if password != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        
        # Ensure password is 8 charachters or more
        #if len(password) < 8:
            #return apology("Password must be at least 8 charachters", 400)
        
        #number = False
        
        # Ensure password includes a number
        #for letter in password:
            #if letter.isnumeric():
                #number = True
                
        #if number == False:
            #return apology("Password must include a number", 400)

        # Ensures User does not already have an account
        # Query the databse
        cur = connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
    

        # Check if an existing password exists
        if cur.fetchone():
            return apology("Username already exists", 400)

        # Insert user into database
        phash = generate_password_hash(password)

        cur.execute("INSERT into users (username, password) VALUES(%s, %s)",(username, phash))

        # save changes to database
        connection.commit()

        # close cursor
        cur.close()

        # Opens login cursor
        # Gets user's ID
        login_cursor = connection.cursor()
        login_cursor.execute("SELECT id FROM users WHERE username = %s", [username])
        user_id = login_cursor.fetchone()

        # Remember which user has logged in, and log them in
        session["user_id"] = user_id[0]
        
        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")