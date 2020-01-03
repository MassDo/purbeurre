# Projet-8-Purbeurre

Search for a food product, and the application will find for you healther comparable products ! 

You can create an account, an save your favorite foods.

## Installation

The following steps are for bash:

**Clone this repository with:**
```sh
git clone https://github.com/MassDo/purbeurre.git
```
**Install dependencies with pipenv:**
```sh
cd purbeurre # default name of the project
pipenv install
```
**Create a postSQL database**
```sh
sudo -i -u postgres
createdb purbeurre 
```
if you have difficulty see the [postgresql documentation](https://www.postgresql.org/)
**Set environment variables**
You need to set 2 environment variables:
...SECRET_KEY: django key.
...PASSWORD: your database password.
**make the migrations**
Into the projet directory (purbeurre):
```sh
pipenv shell # activate the virtual env
./manage.py migrate 
```
Now the database schema are created but the database is empty we need to feed it with data from the OpenFoodFact project

## Database implementation
You can use the custom command data_feed to do it !
For example 
```sh
```

## Run the app

```sh
./manage.py runserver
```
The application is running on local http://127.0.0.1:8000/

## Deploying on heroku

Install heroku with this link:

https://devcenter.heroku.com/articles/heroku-cli#download-and-install

Deploy the app with this tutorial:

https://devcenter.heroku.com/articles/git

Wait you have two Last things to do ! You need first to go to the main.py module and do this changes:

![main.py_changes](images/prod.png)

And finally, create the following environment variable for containing your google map API keys for server use.

![main.py_changes](images/api_key.png)