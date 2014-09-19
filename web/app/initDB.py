from sqlalchemy import create_engine

with open('/home/fthomas/Dokumente/hots-builder/web/app/sqluser') as file:
        login = file.readline().strip()

engine = create_engine('mysql://' + login + '@localhost/hots', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask('test')
db = SQLAlchemy(app)

class Heroes(Base):
        __tablename__ = 'heroes'
        id = Column(Integer, primary_key = True)
        name = Column(String(15), unique = True)
        abilities = db.relationship('Abilities', backref = 'hero', lazy = 'dynamic')

        def __repr__(self):
                return '<User %r>' % (self.name)

class Abilities(Base):
        __tablename__ = 'abilities'
        id = Column(Integer, primary_key = True)
        name = Column(String(15), unique = True)
        text = Column(String(200))
        hero_id = Column(Integer, db.ForeignKey('heroes.id'))

        def __repr__(self):
                return '<Post %r>' % (self.name)

Base.metadata.create_all(engine) 

hero = Heroes(name='abathur')

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

session = Session()

session.add(hero)

our_hero = session.query(Heroes).filter_by(name='abathur').first() 
print our_hero

session.commit()
