import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, searchCity, searchHike

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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/myhikes", methods =["GET", "POST"])
@login_required
def myHikes():

    if request.method == "GET":

        hikeData = db.execute("SELECT * FROM hikes WHERE activeuser= :activeuser", activeuser=session["user_id"])

        if hikeData == []:
            return redirect("/add")

        for item in hikeData:
            name = item["name"]
            description = item["description"]
            difficulty = item["difficulty"]

        return render_template("myhikes.html", hikeData=hikeData, name=name, description=description, difficulty=difficulty)

    else:
        hikeName = request.form.get("deleteBtn")
        db.execute("DELETE FROM hikes WHERE activeuser= :activeuser AND name= :hikeName", activeuser=session["user_id"], hikeName=hikeName)
        return redirect("/myhikes")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return ("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return ("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return ("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/myhikes")

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



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        """check value in input"""
        if not request.form.get("username"):
            return ("Please enter a username")
        if not request.form.get("password"):
            return ("Please enter a password")
        """check passwords match"""
        if request.form.get("password") != request.form.get("confirmPassword"):
            return("passwords must match")

        """check username doesn't already exist in users"""
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return ("Username already in use")
        else:
            """add (insert) username & hashed pasword into users"""
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=password)

        return redirect("/login")


@app.route("/add", methods = ["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        activeuser = session["user_id"]
        name = request.form.get("name")
        description = request.form.get("description")
        difficulty = request.form.get("difficulty")
        if name == "" or description == "" or difficulty == "":
            return "please complete all fields"
        db.execute("INSERT INTO hikes (activeuser, name, description, difficulty) VALUES (:activeuser, :name, :description, :difficulty)", activeuser=activeuser, name=name, description=description, difficulty=difficulty)
    return redirect("/myhikes")

@app.route("/find", methods = ["GET", "POST"])
@login_required
def find():
    if request.method == "GET":
        return render_template("find.html")
    else:
        searched = request.form.get("searched")
        #call to geocoding api, enter city print long/lat of city
        info = searchCity(searched)
        lat = info["lat"]
        lng = info["lng"]
        hikes = searchHike(lat, lng)
        # shows list of trail dicts with info
        hikeList = (hikes["trails"])

        if hikeList == []:
            return "no hikes found"

        for hike in hikeList:
            hikeName = hike["name"]
            hikeDescription = hike["summary"]
            hikeDifficulty = hike["difficulty"]
        return render_template("find.html", hikeList=hikeList, hikeName=hikeName, hikeDescription=hikeDescription, hikeDifficulty=hikeDifficulty)

@app.route("/addToMyHike", methods=["POST"])
@login_required
def addToMyHike():
    if request.method == "POST":
        activeuser = session["user_id"]
        name = request.form.get("hikeName")
        nameList = name.split("@")
        hikeName = nameList[0]
        hikeDescription = nameList[1]
        hikeDifficulty = nameList[2]
        db.execute("INSERT INTO hikes (activeuser, name, description, difficulty) VALUES (:activeuser, :name, :description, :difficulty)", activeuser=activeuser, name=hikeName, description=hikeDescription, difficulty=hikeDifficulty)
        return redirect("/myhikes")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return (e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
