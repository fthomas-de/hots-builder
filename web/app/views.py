from flask import Flask, render_template, url_for, request, redirect
from app import app
from os import walk

path = '/home/fthomas/Dokumente/hots-builder/web/app/static/img/heroes'
(_, _, hero_img_names) = walk(path).next()

hero_lst = []

hero_lst.append(hero_img_names[:7])
hero_lst.append(hero_img_names[7:13])
hero_lst.append(hero_img_names[13:20])
hero_lst.append(hero_img_names[20:26])
hero_lst.append(hero_img_names[26:34])

@app.route('/')
@app.route('/hots')
@app.route('/hots/builder')
def index():
	return render_template('index.html', page='index')

@app.route('/create')
def create():
	return render_template('create.html', page='create', imgLst = hero_lst)

@app.route('/<name>')
def build(name):
	return render_template('build.html', page='build', name=name)
