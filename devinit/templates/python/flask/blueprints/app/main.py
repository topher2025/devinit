from flask import Blueprint, render_template

demo = Blueprint("main", __name__)


@demo.route("/")
def index():
    return render_template("index.html")