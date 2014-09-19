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
