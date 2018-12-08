from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField
from wtforms.validators import *
from flask_wtf.file import FileField
from app import app

class UploadForm(FlaskForm):
    file = FileField("File Upload")
    submit = SubmitField("Upload")
