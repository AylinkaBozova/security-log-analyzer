from flask import Blueprint, render_template

web = Blueprint("web", __name__)


@web.get("/")
def home():
    return render_template("index.html")
