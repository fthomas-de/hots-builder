from flask.ext.sqlalchemy import SQLAlchemy
from app import db 

class Hero(db.Model):
	__tablename__ = 'heroes'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(15), unique = True)
	abilities = db.relationship('Ability', backref = 'hero', lazy = 'dynamic')
	role = db.Column(db.String(15))	

	def __repr__(self):
		return '<Hero %s>' % (self.name)	
	
class Ability(db.Model):
	__tablename__ = 'abilities'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	text = db.Column(db.String(200))
	lvl = db.Column(db.Integer)
	hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
	
	def __repr__(self):
		return '<Skill %s>' % (self.name)

class Build(db.Model):
	__tablename__ = 'builds'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(15), unique = True)
	text = db.Column(db.String(200))
	hero = db.Column(db.String(50))
	votes = db.Column(db.Integer)
	pos_votes = db.Column(db.Integer)
	build = db.Column(db.String(75))
	date = db.Column(db.String(21))

	def __repr__(self):
		return '<Build %s>' % (self.name)

class Id(db.Model):
	__tablename__ = 'id'
	id = db.Column(db.Integer, primary_key = True)
	hash = db.Column(db.String(56), unique = True)
	build = db.Column(db.String(56), unique = True)
	
	def __repr__(self):
		return '<ID>'
