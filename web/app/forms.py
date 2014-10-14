from flask.ext.wtf import Form
from wtforms import StringField

class Build(Form):
    build_name = StringField('build')
