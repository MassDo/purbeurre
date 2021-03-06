# Projet-8-Purbeurre

Search for a food product, and the application will find for you healther comparable products ! 

You can create an account, an save your favorite foods.

## Installation

Follow the steps:

**Clone this repository with:**
```sh
git clone https://github.com/MassDo/purbeurre.git
```
**Install dependencies with [pipenv](https://github.com/pypa/pipenv):**<br><br>
Make sure you’ve got Python & pip, [here](https://pipenv.kennethreitz.org/en/latest/install/) some help !
```sh
cd purbeurre # default name of the project
pipenv install
```
**Create a postSQL database**
```sh
sudo -i -u postgres
createdb purbeurre 
```
If you have any difficulties see the postgresql [documentation](https://www.postgresql.org/).<br><br>
**Set environment variables**<br>
You need to set 2 environment variables:
* SECRET_KEY: django key.
* PASSWORD: your database password.<br><br>

**Make the migrations**<br>
Into the project directory (purbeurre):
```sh
pipenv shell # activate the virtual env
./manage.py migrate 
```
Now the database schema are created, but the database is empty, we need to feed it with data from the OpenFoodFacts project !

## Database implementation
You can use the custom command data_feed to do it !
For example: 
```sh
./manage.py data_feed olives tapas badacategory 'pâtes à tartiner' --prod=25
```
You will have a report of the database implementation:
![data_feed](static/img/data_feed.png)

## Create admin account
```sh
./manage.py createsuperuser
```
## Run the app

```sh
./manage.py runserver
```
The application is running on local http://127.0.0.1:8000/ <br>
You can acces to the back office here http://127.0.0.1:8000/admin using your admin credentials.

## Deploying on heroku

Install heroku with this link:

https://devcenter.heroku.com/articles/heroku-cli#download-and-install

Deploy the app with this tutorial:

https://devcenter.heroku.com/articles/git
