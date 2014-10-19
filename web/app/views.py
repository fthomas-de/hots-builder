from flask import Flask, render_template, url_for, request, redirect, abort, jsonify, session
from app import app
from os import walk
from models import db
from dbupdate import get_heroes_by_role

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

assassins = get_heroes_by_role('assassin')
	warriors = get_heroes_by_role('warrior')
	supports = get_heroes_by_role('support')
	specialists = get_heroes_by_role('specialist')

with open('/home/fthomas/Dokumente/hots-builder/web/app/static/hero-data/weekly-heroes') as file:
	for row in file:
		filepath = row.strip()
		weekly_hero_lst.append(filepath)


#helper
def chunks(lst):
	for i in xrange(0, len(lst), 2):
		yield(lst[i:i+2])

def get_id():
	u_agent = request.headers.get('User-Agent')
	ip = request.remote_addr
	return u_agent, ip

#routing
@app.route('/')
@app.route('/hots')
@app.route('/hots/builder')
def index():
	from dbupdate import get_latest_builds, get_abilityname_by_id
	builds = get_latest_builds(2)
	abilities = []

	if len(builds) == 0:
		builds = None
	else:
		for build in builds:
			ability = []
			ability_ids = build.build.split('-')[1:]
			
			for id in ability_ids:
				ability.append(str(get_abilityname_by_id(int(id))))
			abilities.append(ability)

		builds = zip(builds, abilities)

	return render_template('index.html', 
				page='index', 
				builds=builds,
				assassins=assassins,
				warriors=warriors,
				supports=supports,
				specialists=specialists, 
				mode=0)

@app.route('/builds/<hero_name>')
def builds(hero_name):
	from dbupdate import get_builds_by_hero_name, get_abilityname_by_id
	
	builds = get_builds_by_hero_name(hero_name)
	abilities = []
	if len(builds) == 0:
		builds = None
	else:
		for build in builds:
			ability = []
			ability_ids = build.build.split('-')[1:]
			
			for id in ability_ids:
				ability.append(str(get_abilityname_by_id(int(id))))
			abilities.append(ability)

		builds = zip(builds, abilities)

	return render_template('index.html', 
							page='index',
							builds=builds,
							hero_name=hero_name,
							assassins=assassins,
							warriors=warriors,
							supports=supports,
							specialists=specialists,
							mode=2)

@app.route('/upvote_best/<name>')
def upvote_best(name):
	from dbupdate import upvote, insert_id

	u_agent, ip = get_id()
	check = insert_id(u-agent, ip, name)
	if check:
		upvote(name)

	return redirect('/best', code=302)

@app.route('/upvote_latest/<name>')
def upvote_latest(name):
	from dbupdate import upvote, insert_id

	u_agent, ip = get_id()
	check = insert_id(u_agent, ip, name)
	if check:
		upvote(name)

	return redirect('/', code=302)

@app.route('/upvote_build/<name>')
def upvote_build(name):
	from dbupdate import upvote, insert_id, get_build

	build = get_build(name)
	build_name = build.name
	build = build.build

	u_agent, ip = get_id()
	check = insert_id(u_agent, ip, name)
	if check:
		upvote(name)

	return redirect('/' + build + '_' + name) 

@app.route('/best')
def best():
	from dbupdate import get_best_builds
	builds = get_best_builds(3)
	if len(builds) == 0:
		builds = None
	return render_template('index.html', 
				page='index', 
				builds=builds, 
				mode=1)

@app.route('/create')
def create():
	return render_template('create.html', 
				page='create', 
				imgLst = hero_lst,
				assassins=assassins,
				warriors=warriors,
				supports=supports,
				specialists=specialists, 
				weekly_hero_lst = weekly_hero_lst)


@app.route('/submit/<var>', methods=['POST'])
def submit(var):
	from .forms import Build
	form = Build()
	name = form.build_name.data
	print var

	if name == "":
		return redirect('/' + var, code=302)
	
	from dbupdate import insert_build
	(hero, _, build) = var.split('_')
	text = ""
	if insert_build(name=name, text=text, hero=hero, build=var):
		return redirect('/', code=302)
	else: 
		return redirect('/' + var, code=302)

@app.route('/<name>')
def build(name):
	build = name
	build_name = ""

	from dbupdate import get_heroes_by_role
	assassins = get_heroes_by_role('assassin')
	warriors = get_heroes_by_role('warrior')
	supports = get_heroes_by_role('support')
	specialists = get_heroes_by_role('specialist')
	
	tuple = name.split('_')
	if len(tuple) == 3:
		name, lvl, hist =  tuple
		mode = 2
	elif len(tuple) == 4:
		name, lvl, hist, build_name = tuple
		mode = 3
	else:
		#case 0: first call
		print 'Exception: Resetting'
		hist = ''
		lvl = 1
		build_name = ""
		mode = 2
	lvl = int(lvl)

	
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
		from .forms import Build
		form = Build()
                return render_template('overview.html', 
					page='overview', 
					name=name, 
					lst=lst, 
					s=s, 
					build=build, 
					mode=mode, 
					form=form,
					assassins=assassins,
					warriors=warriors,
					supports=supports,
					specialists=specialists, 
					build_name=build_name)
	
 	#case 2: not rdy yet
	from dbupdate import get_hero_abilities
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
		next_lvl=str(next_lvl),
		assassins=assassins,
		warriors=warriors,
		supports=supports,
		specialists=specialists)
		

