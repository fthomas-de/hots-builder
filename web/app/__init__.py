from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

with open('/home/fthomas/Dokumente/hots-builder/web/app/sqluser') as file:
	login = file.readline().strip()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + login + '@localhost/hots'
db = SQLAlchemy(app)

from app import views, models

db.init_app(app)
db.create_all()

from dbupdate import update
#update()
