from flask import Flask, render_template, url_for, request, redirect
from app import app

@app.route('/')
@app.route('/hots')
@app.route('/hots/builder')
def index():
	return render_template('index.html', page='index')

@app.route('/create')
def create():
	return render_template('create.html', page='create')
