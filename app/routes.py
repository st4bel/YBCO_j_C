from app import app
import os
from app.forms import *
from app.models import *
from app.j_C_intern import plot_file, filepath, plotpath, plot_j_C, close_plot, show_plot
from flask import render_template, url_for, flash, redirect, request
from werkzeug.utils import secure_filename

def deleteFile(filename):
    file=Document.query.filter_by(filename = filename).first()
    db.session.delete(file)
    db.session.commit()
    os.remove(filepath(filename))
    if os.path.isfile(plotpath(filename,"_plot.png")):
        os.remove(plotpath(filename,"_plot.png"))
    if os.path.isfile(plotpath(filename,"_j_C.png")):
        os.remove(plotpath(filename,"_j_C.png"))
    flash("removed all Files of: "+filename)

@app.route("/", methods=["POST","GET"])
@app.route("/index", methods=["POST","GET"])
def index():
    form=DeleteAllFiles()
    files = Document.query.all()
    if request.method =="POST":
        for file in files:
            deleteFile(file.filename)
        return redirect(url_for("index"))
    return render_template("index.html", title="home", files = files,form=form)

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
    return render_template("upload.html", form=form, files = Document.query.all())

@app.route("/file/<filename>", methods=["GET", "POST"])
def file(filename):
    file = Document.query.filter_by(filename=filename).first_or_404()
    form = PlotForm()
    form.amplification.default = file.amplification

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
            file.remove_offset = "remove_offset" in form2.checkbox.data
            file.remove_ohm = "remove_ohm" in form2.checkbox.data
            db.session.add(file)
            db.session.commit()

            plot_j_C(filename)
            close_plot()
        elif form.delete.data:
            deleteFile(filename)
            return redirect(url_for("index"))
        elif form.submit_amplification.data:
            flash(form.amplification.data)
            file.amplification = form.amplification.data
            db.session.add(file)
            db.session.commit()

        return redirect(url_for("file", filename = filename))
    if not os.path.isfile(plotpath(filename, "_plot.png")):
        #creating simple plots
        plot_file(filename)
        close_plot()
    form.process()
    return render_template("file.html",form = form, form2=form2, filename = filename, files = Document.query.all())
