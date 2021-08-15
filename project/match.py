from app import app, connection

import psycopg2

from flask import render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

@app.route("/match", methods=["GET", "POST"])
@login_required
def match():
    if request.method == "POST":

        # gets user's code
        user = request.form.get("code")

        # connect to database
        cursor = connection.cursor()

        # Select all movies both users have liked
        cursor.execute("SELECT * FROM top_250 WHERE id IN (SELECT movie_id FROM likes where preference = true AND user_id = %s) AND id IN (SELECT movie_id FROM likes where preference = true AND user_id = %s)", (session["user_id"], user))

        rows = cursor.fetchall()

        row_count = cursor.rowcount

        if row_count == 0:
            return apology("no matches", 400)

        # Copy those movies over into a dictionary for display purposes
        matches = []

        for i in range(row_count):
            match = {}

            match["title"] = rows[i][0]
            match["year"] = rows[i][1]
            match["image"] = rows[i][2]
            match["rating"] = rows[i][3]

            matches.append(match)

        return render_template("matched.html", matches = matches)
    
    else: 
        friend_code = session["user_id"]
        return render_template("match.html", friend_code = friend_code)