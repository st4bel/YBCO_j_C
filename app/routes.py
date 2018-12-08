from app import app
import os
from app.forms import *
from app.models import *
from app.j_C_intern import plot_file, filepath, plotpath#, plot_j_C
from flask import render_template, url_for, flash, redirect, request
from werkzeug.utils import secure_filename

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="home")

@app.route("/upload", methods = ["GET" ,"POST"])
def upload():
    form = UploadForm()
    if request.method == "POST":
        for f in request.files.getlist("file"):
            filename = secure_filename(f.filename)
            if Document.query.filter_by(filename=filename).first() is not None:
                flash("File arleady uploaded")
                return redirect(url_for("upload"))
            new_document = Document(filename=filename)
            db.session.add(new_document)
            db.session.commit()
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return redirect(url_for("index"))
    return render_template("upload.html", form=form)

@app.route("/file/<filename>", methods=["GET", "POST"])
def file(filename):
    if plotpath(filename, "_plot.png") in None:
        #creating simple plots
        plot_file(filename)

    return render_template("file.html", filename = filename)
