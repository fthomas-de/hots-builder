from flask import Flask, render_template, url_for, request, redirect, abort
from app import app
from os import walk
from models import db

#set up available heroes for create page
path = '/home/fthomas/Dokumente/hots-builder/web/app/static/img/heroes'
(_, _, hero_img_names) = walk(path).next()
hero_img_names.sort()

hero_lst = []
hero_lst.append(hero_img_names[:7])
hero_lst.append(hero_img_names[7:13])
hero_lst.append(hero_img_names[13:20])
hero_lst.append(hero_img_names[20:26])
hero_lst.append(hero_img_names[26:34])

weekly_hero_lst = []

with open('/home/fthomas/Dokumente/hots-builder/web/app/static/hero-data/weekly-heroes') as file:
	for row in file:
		filepath = row.strip()
		weekly_hero_lst.append(filepath)


#helper
def get_hero_abilities(name, lvl=1):
        from app import db, models

        hero_id = models.Hero.query.filter_by(name=name).first().id
        abilities = models.Ability.query.filter_by(hero_id=hero_id, lvl=lvl).all()

	return abilities

def chunks(lst):
	for i in xrange(0, len(lst), 2):
		yield(lst[i:i+2])

@app.route('/')
@app.route('/hots')
@app.route('/hots/builder')
def index():
	return render_template('index.html', page='index')

@app.route('/create')
def create():
	return render_template('create.html', page='create', imgLst = hero_lst, weekly_hero_lst = weekly_hero_lst)


@app.route('/submit/<var>')
def submit(var):
	#from dbupdate import insert_build
	#insert_build(var)
	print var
	return redirect('/', code=302)

@app.route('/<name>')
def build(name):
	try:
		name, lvl, hist = name.split('_')
		lvl = int(lvl)
	except ValueError:
		#case 0: first call
		print 'Exception: Resetting'
		hist = ''
		lvl = 1
	
	if not name + '_frame.png' in hero_img_names: abort(401)
	
	#case 1: rdy now
        if lvl == 0:
		from app import db, models
		#get all skilled abilities
		hist = hist.split('-')[1:]
		lst = []
		s = ''
		for id in hist:
			ability = models.Ability.query.filter_by(id=id).first()
			lst.append(ability)
			s += str(ability.id) + '_'	
		lst = chunks(lst)
                return render_template('overview.html', page='overview', name=name, lst=lst, s=s)
	
 	#case 2: not rdy yet
	abilities = get_hero_abilities(name, lvl)
        lst = chunks(abilities)

	#calculate next_lvl for the website
	if lvl <= 13:
		next_lvl = lvl + 3
	elif lvl == 16:
		next_lvl = 20
	elif lvl == 20:
		next_lvl = 0

	return render_template('build.html', 
		page='build', 
		name=name, 
		lst=lst, 
		lvl=lvl, 
		hist=hist,
		next_lvl=str(next_lvl))
		

