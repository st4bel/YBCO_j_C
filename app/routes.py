from app import app
import os
from app.forms import *
from app.models import *
from app.j_C_intern import plot_file, filepath, plotpath, plot_j_C, close_plot, show_plot
from flask import render_template, url_for, flash, redirect, request
from werkzeug.utils import secure_filename

@app.route("/")
@app.route("/index")
def index():
    files = Document.query.all()
    return render_template("index.html", title="home", files = files)

@app.route("/upload", methods = ["GET" ,"POST"])
def upload():
    form = UploadForm()
    if request.method == "POST":
        for f in request.files.getlist("file"):
            filename = secure_filename(f.filename)
            flash(filename)
            if Document.query.filter_by(filename=filename).first() is not None:
                flash("File arleady uploaded")
                return redirect(url_for("upload"))
            new_document = Document(filename=filename)
            new_document.remove_ohm=False
            new_document.remove_offset=False
            db.session.add(new_document)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            db.session.commit()
        return redirect(url_for("index"))
    return render_template("upload.html", form=form)

@app.route("/file/<filename>", methods=["GET", "POST"])
def file(filename):
    form = PlotForm()
    form2 = PlotOptionsForm()
    if request.method == "POST":
        if form.calc_j_C.data:
            plot_j_C(filename)
            close_plot()
        elif form.show_norm.data:
            plot_file(filename)
            show_plot()
        elif form.show_j_C.data:
            plot_j_C(filename)
            show_plot()
        elif form2.submit.data:
            flash(form2.checkbox.data)
            file = Document.query.filter_by(filename=filename).first()
            file.remove_offset = "remove_offset" in form2.checkbox.data
            file.remove_ohm = "remove_ohm" in form2.checkbox.data
            db.session.add(file)
            db.session.commit()

            plot_j_C(filename)
            close_plot()

        return redirect(url_for("file", filename = filename))
    if not os.path.isfile(plotpath(filename, "_plot.png")):
        #creating simple plots
        plot_file(filename)
        close_plot()
    return render_template("file.html",form = form, form2=form2, filename = filename, files = Document.query.all())
