# material-message-board

## [Demo Me!](https://material-message-board.herokuapp.com)
By the way: if you get internal server errors trying to login its godaddy's fault

This is a basic flask application that utilizes the features listed below to make an OAuth public message board.

Check out the [issue log](https://docs.google.com/document/d/1gPy4qg61OyH7I3pLaGjP3E-DxEnF_jPBbQ2PReFaYN0/edit?usp=sharing) I've kept to document some problems and solutions I've encounted along the life span of this app.

Project Features:
  - OAuth support for login with Google, Twitter, and Facebook
  - [Material Design](https://material.angularjs.org)
  - [AngularJS](https://angularjs.org/)
  - [Python Flask](http://flask.pocoo.org/)
  - [REST API](http://flask-restful-cn.readthedocs.org/zh/latest/)
  - [Heroku](https://www.heroku.com/) deployable out of the box

### Get up and running

 - Create a localhost database called `material-message-board`
 - Find the `database-structure.sql` dump file in the root of the app directory
 - Run the contents on your database to create the `messages` and `users` tables

Run the following commands in a terminal
```sh
$ git clone git@github.com:domfarolino/material-message-board.git
$ cd material-message-board
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python run.py
```
