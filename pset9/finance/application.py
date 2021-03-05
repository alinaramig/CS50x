import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# API code pk_b6bc2c9b8b3e48f294b5e951f582dde7


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # create dictionary where I can store everything needed for the table
    rows = db.execute("SELECT * FROM stocks WHERE user = ?", session["user_id"])

    stocks = []

    outflow = 0

    # Create a dictionary for each stock
    for row in rows:
        stock = {}
        stock["symbol"] = row["Symbol"]
        stock["name"] = row["name"]
        stock["shares"] = row["shares"]
        stock["price"] = (lookup(row["Symbol"]))["price"]
        stock["total"] = round(float(stock["shares"]) * float(stock["price"]), 2)

        outflow += stock["total"]

        stocks.append(stock)

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    current_cash = 10000 - outflow

    total = current_cash + outflow

    return render_template("index.html", stocks=stocks, current_cash=current_cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        key = session["user_id"]

        symbol = request.form.get("symbol")

        shares = request.form.get("shares")

        # Checks to make sure key is correct
        if not lookup(symbol):
            return apology("Stock not found", 400)

        # Checks to make sure shares is an int
        try:
            # Checks to make sure shares is non negative
            if int(shares) < 1:
                raise ValueError("Enter Valid Shares")

        except ValueError:
            return apology("Enter valid shares", 400)

        # checks current price of stock
        price = (lookup(symbol))["price"]

        total_price = float(price) * float(shares)

        # Checks users current cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", key)[0]["cash"]

        # makes sure the user can afford the stock
        if total_price > int(cash):
            return apology("Not enouph cash", 400)

        # Checks if user already owns this stock
        matching_stock = db.execute("SELECT * FROM stocks WHERE user =? AND Symbol =?", key, symbol)

        # if they own it update the # of shares
        if len(matching_stock) == 1:

            owned_shares = matching_stock[0]["shares"]

            new_shares = int(owned_shares) + int(shares)

            db.execute("UPDATE stocks SET shares =? WHERE user =? AND Symbol =?", new_shares, key, symbol)

        # if they don't already own it, add it to the database
        else:
            db.execute("INSERT into stocks (symbol, name, user, shares, price) VALUES(?, ?, ?, ?, ?)",
                       (lookup(symbol))["symbol"], (lookup(symbol))["name"], key, shares, price)

        # updates users cash
        db.execute("UPDATE users SET cash =? WHERE id =?", (cash - total_price), key)

        ct = datetime.datetime.now()

        # Add data to history table
        db.execute("INSERT into history (user, symbol, shares, price, transacted, type) VALUES(?, ?, ?, ?, ?, ?)", 
                   key, symbol, shares, lookup(symbol)["price"], ct, "Bought")

        return redirect("/")

    else:

        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT * FROM history WHERE user =?", session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Checks to make sure key is correct
        if not lookup(request.form.get("symbol")):
            return apology("Stock not found", 400)

        # Gets current value of stock
        info = lookup(request.form.get("symbol"))

        return render_template("quoted.html", info=info)

    else:
        return render_template("quote.html")


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
        
        # Ensure password is 8 charachters or more
        if len(password) < 8:
            return apology("Password must be at least 8 charachters", 400)
        
        number = False
        
        # Ensure password includes a number
        for letter in password:
            if letter.isnumeric():
                number = True
                
        if number == False:
            return apology("Password must include a number", 400)

        # Ensures User does not already have an account
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 0:
            return apology("Username already exists", 400)

        # Ensures passwords match
        if password != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Insert user into database
        phash = generate_password_hash(password)

        db.execute("INSERT into users (username, hash) VALUES(?, ?)", username, phash)

        # Redirect user to login - not completely done might need to log them in
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        key = session["user_id"]

        symbol = request.form.get("symbol")

        shares = request.form.get("shares")

        # Checks to make sure the seller owns the stock
        owned = db.execute("SELECT * FROM stocks WHERE user = ? and Symbol =?", key, symbol)
        if len(owned) < 1:
            return apology("You do not own this stock", 400)

        # Checks to make shares is positive
        if int(shares) < 1:
            return apology("Enter valid shares", 400)

        # Checks to make sure there's enouph shares to sell
        if owned[0]["shares"] < int(shares):
            return apology("You don't own enouph shares", 400)

        # Checks users current cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", key)[0]["cash"]

        # checks current price of stock
        price = (lookup(symbol))["price"]

        total_price = float(price) * float(shares)

        # updates users cash
        db.execute("UPDATE users SET cash =? WHERE id =?", (cash + total_price), key)

        # if the user isn't selling all of their shares update their shares
        if int(owned[0]["shares"]) > int(shares):

            new_shares = int(owned[0]["shares"] - int(shares))

            db.execute("UPDATE stocks SET shares =? WHERE user =? AND Symbol =?", new_shares, key, symbol)

        # if the user is selling all of their shares delete their stock from the database
        else:
            db.execute("DELETE FROM stocks WHERE user =? AND Symbol =?", key, symbol)

        ct = datetime.datetime.now()

        # Add data to history table
        db.execute("INSERT into history (user, symbol, shares, price, transacted, type) VALUES(?, ?, ?, ?, ?, ?)", 
                   key, symbol, shares, lookup(symbol)["price"], ct, "Sold")

        return redirect("/")

    else:
        
        # finds what stocks the user owns
        stocks = db.execute("SELECT * FROM stocks WHERE user = ?", session["user_id"],)
        
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
