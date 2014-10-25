apt-get update
apt-get upgrade
apt-get install git git-core
git clone https://github.com/trudikampfschaf/hots-builder
apt-get install python2.7
apt-get install python-pip python-dev build-essential libmysqlclient-dev
apt-get install python-mysqldb
pip install pip --upgrade
pip install virtualenv
virtualenv ./hots-builder/web/flask
./hots-builder/web/flask/bin/pip install Flask
./hots-builder/web/flask/bin/pip install Flask-SQLAlchemy
./hots-builder/web/flask/bin/pip install Flask-wtf
./hots-builder/web/flask/bin/pip install mysql-python
echo "hots-admin:hitchcock" > ./hots-builder/web/app/sqluser
apt-get install mysql-server mysql-client
apt-get install php5-mysql
#mysql -u root -p
#CREATE DATABASE hots;
#CREATE USER 'hots-admin'@'localhost' IDENTIFIED BY 'hitchcock';
#GRANT ALL PRIVILEGES ON * . * TO 'hots-admin'@'localhost';
#FLUSH PRIVILEGES;

