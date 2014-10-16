from flask import Flask, render_template, url_for, request, redirect, abort, jsonify
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

def id():
	u_agent = request.headers.get('User-Agent')
	ip = jsonify({'ip': request.remote_addr}), 200
	ip2 = request.environ['REMOTE_ADDR']	
	ip3 = request.remote_addr
	print 'agent', u_agent
	print 'IP', ip3

#routing
@app.route('/')
@app.route('/hots')
@app.route('/hots/builder')
def index():
	from dbupdate import get_latest_builds
	builds = get_latest_builds(3)
	#print builds
	if len(builds) == 0:
		builds = None
	for build in builds:
		import datetime
		build.date = str(datetime.timedelta(seconds=build.date)).split(',')[1].strip()
		
	return render_template('index.html', page='index', builds=builds, mode=0)

@app.route('/upvote_best/<name>')
def upvote_best(name):
	from dbupdate import upvote
	upvote(name)
	id()
	return redirect('/best', code=302)

@app.route('/upvote_latest/<name>')
def upvote_latest(name):
	from dbupdate import upvote
	upvote(name)
	id()
	return redirect('/', code=302)

@app.route('/best')
def best():
	from dbupdate import get_best_builds
	builds = get_best_builds(3)
	if len(builds) == 0:
		builds = None
	return render_template('index.html', page='index', builds=builds, mode=1)

@app.route('/create')
def create():
	return render_template('create.html', page='create', imgLst = hero_lst, weekly_hero_lst = weekly_hero_lst)


@app.route('/submit/<var>', methods=['POST'])
def submit(var):
	from .forms import Build
	form = Build()
	name = form.build_name.data
	print var

	if name == "":
		return redirect('/' + var, code=302)
	
	#from dbupdate import insert_build
	(hero, _, build) = var.split('_')
	text = ""
	insert_build(name=name, text=text, hero=hero, build=var)
	#print name, text, hero, build

	return redirect('/', code=302)

@app.route('/<name>')
def build(name):
	build = name
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
	mode = 2
        if lvl == 0:
		from app import db, models
		if hist[-1] == 'a':
			hist == hist[:-1]
			mode = 3
	
		#get all skilled abilities
		hist = hist.split('-')[1:]
		lst = []
		s = ''
		for id in hist:
			ability = models.Ability.query.filter_by(id=id).first()
			lst.append(ability)
			s += str(ability.id) + '_'	
		lst = chunks(lst)
		from .forms import Build
		form = Build()
                return render_template('overview.html', page='overview', name=name, lst=lst, s=s, build=build, mode=mode, form=form)
	
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
		

