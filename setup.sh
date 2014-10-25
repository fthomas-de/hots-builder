apt-get update
apt-get upgrade
apt-get install git git-core
apt-get install python2.7
apt-get install python-pip python-dev build-essential libmysqlclient-dev
apt-get install python-mysqldb
pip install pip --upgrade
pip install virtualenv
virtualenv ./web/flask
./web/flask/bin/pip install Flask
./web/flask/bin/pip install Flask-SQLAlchemy
./web/flask/bin/pip install Flask-wtf
./web/flask/bin/pip install mysql-python
echo "hots-admin:hitchcock" > ./web/app/sqluser
echo "hitchcock" > ./web/app/secret_key
apt-get install mysql-server mysql-client
apt-get install php5-mysql
#mysql -u root -p
#CREATE DATABASE hots;
#CREATE USER 'hots-admin'@'localhost' IDENTIFIED BY 'hitchcock';
#GRANT ALL PRIVILEGES ON * . * TO 'hots-admin'@'localhost';
#FLUSH PRIVILEGES;

