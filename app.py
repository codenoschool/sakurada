from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new", methods=["GET", "POST"])
def new():

    if request.method == "POST":
        new_post = Posts(title=request.form["title"], content=request.form["content"])
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("sakurada"))
    return render_template("post.html")

@app.route("/sakurada")
def sakurada():
    posts = Posts.query.all()

    return render_template("sakurada.html", posts=posts)

@app.route("/<int:cap>")
def cap(cap):
    post = Posts.query.get(cap)

    return render_template("sak.html", post=post)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
