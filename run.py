import os
import json
from flask import (
    Flask, render_template, request, flash, 
    redirect, session, url_for)
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


@app.route("/shepard")
def shepard():
    return render_template("shepard.html", page_title="Shepard")


@app.route("/login")
def login():
    return render_template("login.html", page_title="Log In")


@app.route("/register")
def register():
    return render_template("register.html", page_title="Register")


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