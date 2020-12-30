import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
    stockData = db.execute("SELECT stock, quantity FROM bought WHERE id= :activeUser", activeUser=session["user_id"])
    activeUser = session["user_id"]
    activeUserCash = round(db.execute("SELECT cash FROM users WHERE id= :activeUser", activeUser = activeUser)[0]["cash"], 2)

    if stockData == []:
        return redirect("/buy")


    portfolioValue = []
    for item in stockData:
        stocksOwned = item["stock"]
        stockQuantity = item["quantity"]
        item["stockPrices"] = lookup(stocksOwned)["price"]
        item["stockPriceTotals"] = item["stockPrices"] * stockQuantity
        portfolioValue.append(item["stockPriceTotals"])

        print(item["stockPriceTotals"])

    portfolioValue = round((sum(portfolioValue) + activeUserCash), 2)

    return render_template("index.html", activeUserCash=activeUserCash, portfolioValue=portfolioValue, stockData=stockData, stocksOwned=stocksOwned, stockQuantity=stockQuantity)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        stockCheck = lookup(request.form.get("stockSymbol"))
        stockQuantity = request.form.get("stockQuantity")
        activeUser = session["user_id"]
        activeUserCash = db.execute("SELECT cash FROM users WHERE id= :activeUser", activeUser = activeUser)[0]["cash"]

        # check stock exists
        if stockCheck == None:
            return apology("Stock not found")
        # check a quantity is entered
        if stockQuantity == '':
            return apology("Please enter a number above 0")
        # check quantity > 0
        if int(stockQuantity) <= 0:
            return apology("Please enter a number above 0")
        # check user can afford purchase
        if activeUserCash < stockCheck["price"] * int(stockQuantity):
            return apology("Not enough money")

        # purchase stocks and update bought table
        # check if id already owns stock if so update quantity in bought
        checkExist = db.execute("SELECT * FROM bought WHERE stock= :stock AND id= :activeUser", stock=stockCheck["symbol"], activeUser=activeUser)
        # if stock not owned add it
        if checkExist == []:
            db.execute("INSERT INTO bought (id, stock, quantity) VALUES (:id, :stock, :quantity)", id=activeUser, stock=stockCheck["symbol"], quantity=int(stockQuantity))
        else:
            # update stock quantity
            newQuantity = checkExist[0]["quantity"] + int(stockQuantity)
            db.execute("UPDATE bought SET quantity = :newQuantity WHERE id= :activeUser AND stock=:stock", newQuantity=newQuantity, activeUser=activeUser, stock=stockCheck["symbol"])
        # update cash in users account
        newCashAmount = activeUserCash - (stockCheck["price"] * int(stockQuantity))
        db.execute("UPDATE users SET cash = :newCashAmount WHERE id= :activeUser", newCashAmount=newCashAmount, activeUser=activeUser)

        # update history table
        datetime = db.execute("SELECT datetime('now'), datetime('now', 'localtime')")
        db.execute("INSERT INTO history (id, stock, boughtsold, price, quantity, datetime) VALUES (:id, :stock, :boughtsold, :price, :quantity, :datetime)", id=activeUser, stock=stockCheck["symbol"], boughtsold="bought", price=(stockCheck["price"] * int(stockQuantity)), quantity=int(stockQuantity), datetime=datetime[0]["datetime('now', 'localtime')"])

        return redirect("/")


@app.route("/history")
@login_required
def history():

    userHistory = db.execute("SELECT stock, boughtsold, price, quantity, datetime FROM history WHERE id= :activeUser ORDER BY datetime DESC", activeUser=session["user_id"])

    if userHistory == []:
        return redirect("/buy")

    for item in userHistory:
        historyStock = item["stock"]
        historyBoughtsold = item["boughtsold"]
        historyPrice = item["price"]
        historyQuantity = item["quantity"]
        historyDatetime = item["datetime"]
        print(item["datetime"])

    """Show history of transactions"""
    return render_template("history.html", userHistory=userHistory, historyStock=historyStock, historyBoughtsold=historyBoughtsold, historyPrice=historyPrice, historyQuantity=historyQuantity, historyDatetime=historyDatetime)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    if request.method == "GET":
        return render_template("quote.html")
    else:
        stockCheck = lookup(request.form.get("stockSymbol"))
        """if stock not found"""
        if stockCheck == None:
            return apology("Stock not found")

    stockQuote = stockCheck["name"] + " (" + stockCheck["symbol"] + ") stock is currently priced at " + str(stockCheck["price"])
    return render_template("quote.html", stockQuote=stockQuote)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        """check value in input"""
        if not request.form.get("username"):
            return apology("Please enter a username", 403)
        """check passwords match"""
        if request.form.get("password") != request.form.get("confirmPassword"):
            return apology("Passwords must match", 403)
        """check username doesn't already exist in users"""
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return apology("Username already in use")
        else:
            """add (insert) username & hashed pasword into users"""
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=password)

        return redirect("/login")
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        return render_template("sell.html")
    else:
        stockCheck = lookup(request.form.get("stockSymbol"))
        stockSelected = request.form.get("stockSymbol")
        stockQuantity = request.form.get("stockQuantity")
        activeUser = session["user_id"]
        activeUserCash = db.execute("SELECT cash FROM users WHERE id= :activeUser", activeUser = activeUser)[0]["cash"]


        stockSold = db.execute("SELECT * FROM bought WHERE id =:activeUser AND stock =:stockSelected", activeUser = activeUser, stockSelected = stockSelected)
        # check user owns stock at all
        if stockSold == []:
            return apology("You don't own this stock")
        # check user owns >= what they want to sell
        if stockSold[0]["quantity"] < int(stockQuantity):
            return apology("You don't own enough of this stock")
        # update the bought table with the new values
        newQuantity = stockSold[0]["quantity"] - int(stockQuantity)
        db.execute("UPDATE bought SET quantity = :newQuantity WHERE id= :activeUser AND stock= :stock", newQuantity = newQuantity, activeUser = activeUser, stock=stockSelected)
        # update uers cash with new amount
        newCash = activeUserCash + (lookup(stockSold[0]["stock"])["price"] * float(stockQuantity))
        db.execute("UPDATE users SET cash = :newCash WHERE id= :activeUser", newCash = newCash, activeUser = activeUser)

        #if new quantity of stock is now zero delete it from bought
        db.execute("DELETE FROM bought WHERE quantity = 0")

                # update history table
        datetime = db.execute("SELECT datetime('now'), datetime('now', 'localtime')")
        db.execute("INSERT INTO history (id, stock, boughtsold, price, quantity, datetime) VALUES (:id, :stock, :boughtsold, :price, :quantity, :datetime)", id=activeUser, stock=stockCheck["symbol"], boughtsold="sold", price=(stockCheck["price"] * int(stockQuantity)), quantity=int(stockQuantity), datetime=datetime[0]["datetime('now', 'localtime')"])

    return redirect("/")


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    if request.method == "GET":
        return render_template("cash.html")
    else:
        if request.form.get("cash") == '':
            return apology("Please enter a number above 0")
        # check quantity > 0
        if int(request.form.get("cash")) <= 0:
            return apology("Please enter a number above 0")

        activeUser = session["user_id"]
        newCash =  float(request.form.get("cash")) + db.execute("SELECT cash FROM users WHERE id= :activeUser", activeUser = activeUser)[0]["cash"]
        db.execute("UPDATE users SET cash = :newCash WHERE id= :activeUser", newCash = newCash, activeUser = activeUser)
        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
