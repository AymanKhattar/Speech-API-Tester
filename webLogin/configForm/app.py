from flask import Flask, render_template, redirect, url_for , request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField , SelectField , TextAreaField , IntegerField , SelectMultipleField , validators
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sys
from flask_socketio import SocketIO
from wtforms.validators import Optional
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database4.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
Bootstrap(app)
socketio = SocketIO(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
emptyDB = sys.argv[1]


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    spotifyId = db.Column(db.String(80))
    spotifySecret = db.Column(db.String(80))
    spotifyPlaylist =  db.Column(db.Text)
    sttapiCheckbox = db.Column(db.String(15)) 
    stthintCheckbox = db.Column(db.Boolean)
    sttaltCheckbox = db.Column(db.Boolean)
    artistAlbumTracks = db.Column(db.String(15)) 
    nbPlaylist = db.Column(db.Integer)
    nbSamples = db.Column(db.Integer)

@login_manager.user_loader # interesting, see what happens when user click on 'Lunch speech API Tester'
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):

    spotifyId = StringField('Spotify ID', validators=[InputRequired(), Length(min=4, max=80)])
    spotifySecret = PasswordField('Spotify Secret', validators=[InputRequired(), Length(min=8, max=80)])
    spotifyPlaylist = TextAreaField('Spotify Playlists URI',validators=[InputRequired(), Length(min=4, max=10000)])
    sttapiCheckbox = SelectField('Select the API you need to text',choices=[('googleapi','Google Discovery API'), ('googlecloud','Google Cloud Speech API')], coerce=unicode, option_widget=None)
    stthintCheckbox = BooleanField('Check if you want to contextualise STT with hints')    
    sttaltCheckbox = BooleanField('Check if you want to include alternative STT guesses in the process')    
    artistAlbumTracks = SelectField('Select the type sample you need to test STT API with', choices=[('albums', 'Albums'), ('artists', 'Artists'), ('tracks', 'Tracks')])
    nbPlaylist = IntegerField('Input the maximum number of playlists you want to STT API with')
    nbSamples = IntegerField('Input the maximum number of musics per playlists you want to STT API with')

class UpdateForm(FlaskForm):

    spotifyId = StringField('Spotify ID')
    spotifySecret = PasswordField('Spotify Secret')
    spotifyPlaylist = TextAreaField('Spotify Playlists URI')
    sttapiCheckbox = SelectField('Select the API you need to text',choices=[('googleapi','Google Discovery API'), ('googlecloud','Google Cloud Speech API')], coerce=unicode, option_widget=None)
    stthintCheckbox = BooleanField('Check if you want to contextualise STT with hints',[validators.optional()])    
    sttaltCheckbox = BooleanField('Check if you want to include alternative STT guesses in the process')    
    artistAlbumTracks = SelectField('Select the type sample you need to test STT API with', choices=[('albums', 'Albums'), ('artists', 'Artists'), ('tracks', 'Tracks')])
    nbPlaylist = IntegerField('Input the maximum number of playlists you want to STT API with',[validators.optional()])
    nbSamples = IntegerField('Input the maximum number of musics per playlists you want to STT API with',[validators.optional()])


def make_optional(field):
    field.validators.insert(0, Optional())

def handleNoneField(field):
    if field == None or field == '':
        return ''
    else : return field

if emptyDB == 'empty': 
    @app.route('/', methods=['GET', 'POST'])
    def login():
        '''
            is called if fieldProcessing find out 'Spotify ID' case in sqlite is empty 
        '''

        form = RegisterForm()
        # make_optional(form)
        if request.method == 'POST' : #if form.validate_on_submit():
            new_user = User(spotifyId=form.spotifyId.data, spotifyPlaylist=form.spotifyPlaylist.data, spotifySecret=form.spotifySecret.data, sttapiCheckbox=form.sttapiCheckbox.data, stthintCheckbox=form.stthintCheckbox.data, artistAlbumTracks=form.artistAlbumTracks.data, nbPlaylist=form.nbPlaylist.data, nbSamples=form.nbSamples.data)
            db.session.add(new_user) 
            db.session.commit()
            return '<h1>You are awesome ! You successfully configured Speech API Tester parameters ;) Now go back to your consol and hit Ctrl+C </h1>'
        return render_template('login.html', form=form)
        # return '<h1> The parameters you intered are not valide please try again </h1>'  


    # new_user = User(spotifyId=make_optional(form.spotifyId.data), spotifyPlaylist=make_optional(form.spotifyPlaylist.data), \
    #                 spotifySecret=form.make_optional(spotifySecret.data), sttapiCheckbox=make_optional(form.sttapiCheckbox.data), \
    #                 stthintCheckbox=make_optional(form.stthintCheckbox.data), artistAlbumTracks=make_optional(form.artistAlbumTracks.data),\
    #                 nbPlaylist=make_optional(form.nbPlaylist.data), nbSamples=make_optional(form.nbSamples.data))

else :
    @socketio.on('disconnect', '/')
    def test_disconnect():
        print('Client disconnected')

    @app.route('/', methods=['GET', 'POST'])
    def signup():
        '''
            is called if fieldProcessing find out 'Spotify ID' case in sqlite is not empty 
        '''
        form = UpdateForm(request.form)

        '''
        Warning ! probleme with validate(), keep returning FALSE
            Problem unsolved yet : 
                Tries : (i thaught it was due to None fields but it seems like returning False even with clean values)
                    - https://stackoverflow.com/questions/14304308/whats-the-right-way-to-optionally-require-a-field-using-flask-wtforms
                    - https://stackoverflow.com/questions/20905188/flask-wtforms-validation-always-false
                    - https://stackoverflow.com/questions/14304308/whats-the-right-way-to-optionally-require-a-field-using-flask-wtforms
        '''
        if request.method == 'POST' :
            new_user = User(spotifyId=form.spotifyId.data, spotifyPlaylist=form.spotifyPlaylist.data, spotifySecret=form.spotifySecret.data, sttapiCheckbox=form.sttapiCheckbox.data, stthintCheckbox=form.stthintCheckbox.data, artistAlbumTracks=form.artistAlbumTracks.data, nbPlaylist=form.nbPlaylist.data, nbSamples=form.nbSamples.data,sttaltCheckbox=form.sttaltCheckbox.data)
            db.session.add(new_user) 
            db.session.commit()
            return '<h1>You are the best ! You successfully configured Speech API Tester parameter ;) Now go back to your consol and hit Ctrl+C </h1>'        
        return render_template('signup.html', form=form)

if __name__ == '__main__':
    socketio.run(app, debug=True)


