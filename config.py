import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "unguessable"
    UPLOAD_FOLDER = os.path.join(basedir, "upload_files")
    PLOT_FOLDER = os.path.join(basedir, "app", "static")
    SAVE_FOLDER = os.path.join(basedir, "save_files")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    THRESHOLD_START = 150
    BRUSHSIZE_START = 9
    SCALE_50 = 0.1544
    SCALE_100 = 0.07993
