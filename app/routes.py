from app import app
import os
from app.forms import *
from app.models import *
from app.j_C_intern import plot_file, filepath, plotpath, plot_j_C, close_plot, show_plot
from app.bridgewidth_intern import plot_picture, cut_image, get_size
from flask import render_template, url_for, flash, redirect, request
from werkzeug.utils import secure_filename
from app.filehandler import *


@app.route("/", methods=["POST","GET"])
@app.route("/index", methods=["POST","GET"])
def index():
    form=DeleteAllFiles()
    files = Document.query.all()
    if request.method =="POST":
        for file in files:
            deleteFile(file.filename)
        return redirect(url_for("index"))
    return render_template("index.html", title="home", files = files,form=form,substrates=Substrate.query.all(),pictures=Picture.query.all())

@app.route("/upload", methods = ["GET" ,"POST"])
def upload():
    form = UploadForm()
    if request.method == "POST":
        for f in request.files.getlist("file"):
            filename = secure_filename(f.filename)
            flash(filename)
            if filename.split(".")[1] == "txt":
                if Document.query.filter_by(filename=filename).first() is not None:
                    flash("File arleady uploaded")
                    return redirect(url_for("upload"))
                new_document = Document(filename=filename)
                new_document.remove_ohm=False
                new_document.remove_offset=False
                db.session.add(new_document)
                db.session.commit()
                detect_substrate_bridge(filename)
                f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            elif filename.split(".")[1] == "bmp":
                if Picture.query.filter_by(filename = filename).first() is not None:
                    flash("Picture already uploaded")
                    return redirect(url_for("upload"))
                new_picture = Picture(filename=filename)
                db.session.add(new_picture)
                db.session.commit()
                detect_picture_amp(filename)
                f.save(plotpath(filename))
                f.save(filepath(filename))
        return redirect(url_for("index"))
    return render_template("upload.html", form=form, files = Document.query.all())

@app.route("/edit/<filename>", methods = ["GET", "POST"])
def edit_file_information(filename):
    return render_template("editfile.html",filename = filename)


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
        elif form.submit_I_C.data:
            file.bridge.j_C = file.j_C
            db.session.add(file)
            db.session.commit()
        elif form.submit_border.data:
            file.res_border = float(form.set_border.data)
            db.session.add(file)
            db.session.commit()

        return redirect(url_for("file", filename = filename))
    if not os.path.isfile(plotpath(filename, "_plot.png")):
        #creating simple plots
        plot_file(filename)
        close_plot()
    form.process()
    return render_template("file.html",form = form, form2=form2, file = file, files = Document.query.all())

@app.route("/picture/<filename>", methods=["POST","GET"])
def picture(filename):
    picture = Picture.query.filter_by(filename=filename).first_or_404()
    form = PictureForm()
    form.brushsize.default = picture.brushsize
    form.threshold.default = picture.threshold
    if request.method == "POST":
        if form.fourplot.data:
            plot_picture(filename)
            close_plot()
        elif form.show_fourplot.data:
            plot_picture(filename)
            show_plot()
        elif form.set_threshold_brushsize:
            picture.brushsize = form.brushsize.data
            picture.threshold = form.threshold.data
            db.session.add(picture)
            db.session.commit()
        return redirect(url_for("picture",filename=filename))
    return render_template("picture.html", picture = picture, form = form)

@app.route("/substrate/<substratename>", methods=["POST","GET"])
def substrate(substratename):
    substrate = Substrate.query.filter_by(substratename=substratename).first_or_404()
    form = SubstrateEditForm()
    form.YCBO_layer.default = substrate.YCBO_layer
    form.Au_layer.default = substrate.Au_layer
    if request.method =="POST":
        if form.submit_layer.data:
            substrate.YBCO_layer = form.YBCO_layer.data
            substrate.Au_layer = form.Au_layer.data
            db.session.add(substrate)
            db.session.commit()

    return render_template("substrate.html", substrate = substrate, form = form)

@app.route("/bridge/<bridgename>")
def bridge(bridgename):
    bridge = Bridge.query.filter_by(bridgename=bridgename).first_or_404()

    return render_template("bridge.html",bridge=bridge)
