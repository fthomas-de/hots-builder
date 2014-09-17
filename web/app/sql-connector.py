from sqlalchemy import *

with open('sqluser') as file:
	login = file.readline().strip().split(':')
	username = login[0]
	passw = login[1]
	
