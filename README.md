# DefinitelyNotTwitter

A social media application, that will definitely not be anything like Twitter.

## Getting Started

WIP


## Prerequisites

Python3 und pip3 müssen installiert sein

```
sudo apt-get install python3
sudo apt-get install python3-pip
```

Außerdem wird git benötigt

```
sudo apt-get install git
```

und virtualenv

```
sudo pip3 install virtualenv
```

### Installing

Repository klonen

```
git clone <linkToRepo>
```

Virtual Environment erstellen und aktivieren

```
cd DefinitelyNotTwitter
virtualenv venv
. venv/bin/activate
```

Flask und Flask Bootstrap installieren

```
pip3 install Flask
pip3 install Flask-Bootstrap
```

Außerdem wird SQLite3 benötigt

```
sudo apt-get install sqlite3
```

Nun muss die Datenbank initialisiert und gefüllt werden

```
flask init-db
flask fill-db
```

Die letzten Schritte

```
export FLASK_APP=DefinitelyNotTwitter
flask run
```

Jetzt kann die Anwendung über localhost:5000 erreicht werden.

## Built With

* [Flask](http://flask.pocoo.org/) - Web framework
* [Bootstrap](https://getbootstrap.com/) - CSS framework
* [SQLite3](https://www.sqlite.org/index.html) - Database engine

## Authors

* **Jakob Kohlhas**
* **Nick Hafkemeyer**
