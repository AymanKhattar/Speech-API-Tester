from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField , SelectField , TextAreaField , IntegerField , SelectMultipleField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database4.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
Bootstrap(app)
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotifyId = db.Column(db.String(80))
    spotifySecret = db.Column(db.String(80))
    # spotifyPlaylist =  Column('article_text', sqlalchemy.UnicodeText())
    spotifyPlaylist =  db.Column(db.Text)
    sttapiCheckbox = db.Column(db.String(15)) 
    stthintCheckbox = db.Column(db.Boolean)
    sttaltCheckbox = db.Column(db.Boolean)
    artistAlbumTracks = db.Column(db.String(15)) 
    nbPlaylist = db.Column(db.Integer)
    nbSamples = db.Column(db.Integer)
