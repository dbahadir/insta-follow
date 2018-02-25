from flask import Flask
from flask_admin import Admin
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore
from database import db_session, init_db
from models import User, Role
from InstagramAPI import InstagramAPI

app = Flask(__name__)
app.config.from_object('config')

admin = Admin(app, name='insta-follow', template_mode='bootstrap3')

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

@app.route("/")
def hello():
    return "Hello Everybody"

@app.route("/test")
def test():
    api = InstagramAPI(app.config['INSTA_USER'], app.config['INSTA_PASS'])
    api.login() # login
    #api.getProfileData()
    #api.getSelfUsernameInfo()
    #api.getUserFollowers("459980542")
    api.searchUsername('hede')
    return "%s" % (api.LastJson)
