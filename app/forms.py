from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import *
from flask_wtf.file import FileField
from app import app

class UploadForm(FlaskForm):
    file = FileField("File Upload")
    submit = SubmitField("Upload")

class PlotForm(FlaskForm):
    delete = SubmitField("Delete this File")
    calc_j_C = SubmitField("Plot and calculate j_C")
    show_norm = SubmitField("Show plotwindow for file")
    show_j_C = SubmitField("Show plotwindow of j_C")
    amplification = SelectField("Choose amplification", choices = [(1000,"1k"),(10000,"100"),(100000,"10")])
    submit_amplification = SubmitField("Save amplification")
    submit_I_C = SubmitField("Save I_C")
    set_border = StringField("Cut x for res-calculation [0.-1.]")
    submit_border = SubmitField("Submit border")

class PlotOptionsForm(FlaskForm):
    checkbox = SelectMultipleField("checkbox",
        choices=[("remove_offset","Remove Offset"),("remove_ohm","Remove ohmic resistance")])
    submit = SubmitField("Refresh with options")

class DeleteAllFiles(FlaskForm):
    submit = SubmitField("Delete all uploaded files")

class Editfile(FlaskForm):
    submit = SubmitField("Submit")

class PictureForm(FlaskForm):
    fourplot = SubmitField("Create Overview")
    threshold = StringField("threshold")
    brushsize = StringField("brushsize")
    set_threshold_brushsize = SubmitField("Save threshold and brushsize")
    show_fourplot = SubmitField("Show Plot of 4er")

class SubstrateEditForm(FlaskForm):
    YBCO_layer = StringField("Enter YBCO layer thickness")
    Au_layer = StringField("Enter Au layer thickness")
    submit_layer = SubmitField("Submit")
