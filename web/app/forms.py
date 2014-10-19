from flask.ext.wtf import Form
from wtforms import StringField, validators, TextField

class Build(Form):
    build_name = TextField('build')
