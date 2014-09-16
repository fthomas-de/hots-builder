from flask import Flask, render_template, url_for, request, redirect
from app import app
from os import walk

path = '/home/fthomas/Dokumente/hots-builder/web/app/static/img/heroes'
(_, _, hero_images_tmp) = walk(path).next()

hero_images = []
hero_images.append(hero_images_tmp[:10])
hero_images.append(hero_images_tmp[10:19])
hero_images.append(hero_images_tmp[19:])

@app.route('/')
@app.route('/hots')
@app.route('/hots/builder')
def index():
	return render_template('index.html', page='index')

@app.route('/create')
def create():
	return render_template('create.html', page='create', img=hero_images)

@app.route('/<name>')
def build(name):
	return render_template('build.html', page='build', name=name)
