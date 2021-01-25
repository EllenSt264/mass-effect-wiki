import os
import json
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html", page_title="About")


@app.route("/squad")
def squad():
    data = []
    with open("data/squad.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("squad.html", page_title="Squad", squad=data)


@app.route("/gameone")
def gameone():
    data = []
    with open("data/squad.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("gameone.html", page_title="Squad", squad=data)


@app.route("/gametwo")
def gametwo():
    data = []
    with open("data/squad.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("gametwo.html", page_title="Squad", squad=data)


@app.route("/gamethree")
def gamethree():
    data = []
    with open("data/squad.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("gamethree.html", page_title="Squad", squad=data)


@app.route("/about/<member_name>")
def about_member(member_name):
    member = {}
    with open("data/squad.json", "r") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["url"] == member_name:
                member = obj
    return render_template("member.html", member=member)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if user already exisits in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")

        if password == confirm_password:
            register = {
                "username": request.form.get("username").lower(),
                "email": request.form.get("email").lower(),
                "password": generate_password_hash(password)
            }
            mongo.db.users.insert_one(register)

            # Put new user into session cookie
            session["user"] = request.form.get("username").lower()
            flash("Registration Successful")
            return redirect(url_for("shepard", username=session["user"]))

    return render_template("register.html", page_title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if user exists within the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Check if hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome {}".format(request.form.get("username").capitalize()))
                    return redirect(
                        url_for("shepard", username=session["user"]))
            else:
                # Invalid password
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            # Username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    
    return render_template("login.html", page_title="Log In")


@app.route("/shepard/<username>", methods=["GET", "POST"])
def shepard(username):
    # Grab session user's username from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"].capitalize()
    
    user_shepard = list(mongo.db.user_shepard.find())

    if session["user"]:
        return render_template("shepard.html", username=username, user_shepard=user_shepard)

    return redirect(url_for("login"))


@app.route("/shepard/<username>/build_shepard")
def build_shepard(username):
    return render_template("build_shepard.html", username=session["user"])


@app.route("/shepard/<username>/build_shepard/mass_effect_1", methods=["GET", "POST"])
def mass_effect_1(username):

    if request.method == "POST":
        shepard = {
            "created_by": session["user"],
            "gender": request.form.getlist("gender"),
            "service_history": request.form.getlist("service-history"),
            "psychological_profile": request.form.getlist("psychological-profile"),
            "class": request.form.getlist("class")
        }

        if session["user"]:

            # Grab session user's username from the database
            existing_data = mongo.db.mass_effect_1.find_one(
                {"created_by": session["user"]})["created_by"]

            if existing_data == shepard["created_by"]:
                flash("You've Already Created Your Profile. ")
                flash("Please Update Your Existing Data Instead")
                return redirect(url_for("shepard", username=session["user"]))
            
            mongo.db.mass_effect_1.insert_one(shepard)
            flash("Profile Sucessfully Constructed")
            return redirect(url_for("shepard", username=session["user"]))

    return render_template("mass_effect_1.html", username=session["user"])


@app.route("/logout")
def logout():
    # Remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we have received your message!".format(
            request.form.get("name")))
    return render_template("contact.html", page_title="Join Our Team!")


if __name__ == "__main__":
    app.run(
        host = os.environ.get("IP"),
        port = int(os.environ.get("PORT")),
        debug = True)