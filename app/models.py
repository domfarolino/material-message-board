from . import *

class Message(db.Model):
  __tablename__  = 'messages'

  id             = db.Column(db.Integer, primary_key=True, unique=True)
  author         = db.Column(db.Integer)    # What we're using in User model (foreign key)
  message        = db.Column(db.Text)
  time           = db.Column(db.Integer)

  def __init__(self, author, message, time):
    self.author  = author
    self.message = message
    self.time    = time


class User(UserMixin, db.Model):
    __tablename__         = 'users'
    id                    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    social_id             = db.Column(db.String(64), nullable=False, unique=True)
    name                  = db.Column(db.String(64), nullable=False)
    username              = db.Column(db.String(64), nullable=False)
    email                 = db.Column(db.String(64), nullable=True)
    profile_picture       = db.Column(db.String(256), nullable=False)
    provider              = db.Column(db.String(64), nullable=False)
    last_active           = db.Column(db.Integer)
    access_token          = db.Column(db.String(256), nullable=True)
    access_token_exp      = db.Column(db.Integer, nullable=True)
    access_token_secret   = db.Column(db.String(256), nullable=True)
    refresh_token         = db.Column(db.String(128), nullable=True)