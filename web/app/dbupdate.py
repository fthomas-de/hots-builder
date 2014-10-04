from app import app
from os import walk 
from models import db
from app import models, db

def update():
	path = '/home/fthomas/Dokumente/hots-builder/web/app/static/hero-data/'
	(_, _, available_heroes) = walk(path).next()
	available_heroes.remove('weekly-heroes')
	available_heroes.sort()
	
	print 'Found heroes:', available_heroes		

	for hero in available_heroes:
		print '\nCurrent hero:', hero
		with open('/home/fthomas/Dokumente/hots-builder/web/app/static/hero-data/' + hero) as file:
			role = file.readline().strip()
			print 'Role:', role
			abilities = []
			for row in file:
				try:
					(ability, text) = row.split(';;')
					(lvl, text) = text.split(';')
				except ValueError:
					print 'Format Error:', row
				abilities.append((ability, lvl, text.strip()))
			
			exist = models.Hero.query.filter_by(name=hero).first()
			if not exist == None:
				print hero, 'exists'
				hero_id = models.Hero.query.filter_by(name=hero).first().id
                                print 'Hero id:', hero_id
				for (ability, lvl, text) in abilities: 
					update_ability(ability, text, lvl, hero_id)
			else: 
				print hero, 'doesnt exist'
				insert_hero(hero, role)
				
				hero_id = models.Hero.query.filter_by(name=hero).first().id
				print 'New id:', hero_id
				
				for (ability, lvl, text) in abilities:
					insert_ability(ability, text, lvl, hero_id)


def insert_hero(name, role):
	hero = models.Hero(name=name, role=role)
	db.session.add(hero)
	db.session.commit()

def insert_ability(name, text, lvl, hero_id):
	ability = models.Ability(name=name, text=text, lvl=lvl, hero_id=hero_id)
	db.session.add(ability)
	db.session.commit()

def update_ability(name, text, lvl, hero_id):
	ability = models.Ability.query.filter_by(name=name, lvl=lvl, hero_id=hero_id).first()

	if ability == None:
		print 'Inserting:', name, lvl, hero_id
		insert_ability(name, text, lvl, hero_id)
	else:
		print 'Updating:', name, lvl, hero_id
		ability.text = text
		db.session.commit()
def insert_build(build):
	print "wtf"
	pass
