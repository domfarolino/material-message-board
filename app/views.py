"""
  Application Routing
"""

from . import *
from app.models import *

from flask import render_template, request, redirect, url_for, jsonify, make_response, session, flash, g
from functools import wraps, update_wrapper
from datetime import datetime
from oauth import OAuthSignIn
from error import APIException
import time

"""
  Standard Dependencies
"""
css_list = ['https://fonts.googleapis.com/css?family=RobotoDraft:400,500,700,400italic',
            'https://ajax.googleapis.com/ajax/libs/angular_material/1.0.0/angular-material.min.css',
            '/static/styles/global.css']

js_list =  ['https://ajax.googleapis.com/ajax/libs/angularjs/1.4.8/angular.min.js',
            'https://code.angularjs.org/1.4.8/angular-animate.js',
            'https://ajax.googleapis.com/ajax/libs/angular_material/1.0.0/angular-material.min.js',
            'https://code.angularjs.org/1.5.0-beta.2/angular-resource.min.js',
            'https://ajax.googleapis.com/ajax/libs/angularjs/1.4.8/angular-aria.min.js',
            'http://www.datejs.com/build/date.js',
            '/static/js/app.js',
            '/static/js/controllers/MessageController.js',
            '/static/js/controllers/MenuController.js',
            '/static/js/controllers/LoginController.js',
            '/static/js/controllers/UserMenuController.js',
            ]


"""
  Wrapper and helper functions for application routes
"""
#http://arusahni.net/blog/2014/03/flask-nocache.html
def nocache(view):
  @wraps(view)
  def no_cache(*args, **kwargs):
    response = make_response(view(*args, **kwargs))
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
  return update_wrapper(no_cache, view)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      if current_user.is_anonymous:
        return redirect(url_for('login'))
      return f(*args, **kwargs)
    return decorated_function

def update_user_last_active(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    updateUserLastActive()
    return f(*args, **kwargs)
  return decorated_function

def not_logged_in(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not current_user.is_anonymous:
      return redirect(url_for('home'))
    return f(*args, **kwargs)
  return decorated_function

def valid_session(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    oauth = OAuthSignIn.get_provider(current_user.provider)
    if oauth.oauth_session is None:
      print " * Session is None, redirecting to authorize"
      return redirect(url_for('oauth_authorize', provider=current_user.provider))
    if current_user.provider.lower() == "google":
      print " * Provider is google"
      if current_user.access_token_exp <= time.time():
        print " * Refreshing Google session with refresh token"
        refreshAccessToken(current_user.refresh_token)
    print " * Valid Session - Moving on with request"
    return f(*args, **kwargs)
  return decorated_function

def refreshAccessToken(refresh_token):
  oauth = OAuthSignIn.get_provider(current_user.provider)
  oauth.refreshAccessToken(current_user.refresh_token)
  access_token, access_token_exp = oauth.getAccessTokenAndExpire()
  current_user.access_token, current_user.access_token_exp = access_token, access_token_exp
  db.session.commit()

"""
  Flask-Restful API Resource Classes
"""
from api import MessageAPI, MessageListAPI

api.add_resource(MessageAPI, '/api/message/<id>')
api.add_resource(MessageListAPI, '/api/messages')

"""
  Application view routes to render pages
"""
@app.route('/')
@login_required
#@nocache
@update_user_last_active
def home():
  return render_template('home.html', cssdep=css_list, jsdep=js_list)

@app.route('/login')
@not_logged_in
@nocache
def login():
  return render_template('login.html', cssdep=css_list, jsdep=js_list)

@app.route('/addMessage', methods=['POST', 'OPTIONS'])
@login_required
def addMessage():
  a = request.get_json()
  resp = make_response();
  err = []
  ins = Message(current_user.id, a['message'], int(time.time()))
  try:
    db.session.add(ins)
    db.session.commit()
  except Exception as e:
    err.append(str(e))
    print(err)
    return resp, 500
  return resp, 201

@app.route('/deleteMessage', methods=['POST'])
@login_required
def deleteMessages():
  a = request.get_json();
  err = []
  resp = make_response()
  for x in a['id']:
    try:
      Message.query.filter(Message.id == x).delete()
      db.session.commit()
    except Exception as e:
      err.append(str(e))
      print(e)
      return resp, 500
  return resp, 200

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
@nocache
def logout():
  logout_user()
  return redirect(url_for('home'))

@app.route('/isLoggedIn')
@nocache
def logged_in():
  try:
    data = {'logged_in': not current_user.is_anonymous}
    resp = make_response()
    resp = jsonify(data)
  except Exception as e:
    resp = str(e)
  finally:
    return resp

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
  oauth = OAuthSignIn.get_provider(provider)
  if not current_user.is_anonymous:
      print "***logout_user()***"
      logout_user()
  return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
  oauth = OAuthSignIn.get_provider(provider)
  try:
      social_id, name, username, email, profile_picture, access_token, access_token_exp, access_token_secret, refresh_token = oauth.callback()
  except ValueError as v:
      print "Callback failed to return all user values"
      print str(v)
      return redirect(url_for('home'))
  except Exception as e:
      print "Callback failed for some reason"
      print str(e)
      return redirect(url_for('home'))
  if social_id is None: return redirect(url_for('home'))
  # Query database for existing users with social_id
  user = User.query.filter_by(social_id=social_id).first()
  if not user:
      print " * User does not exist in database"
      # If provider is google but no refresh token is provided then that means they had
      # already authorized our application but we're in this logic branch because they
      # do not exist in our users table.
      # This can help if our database goes down and users try to log in, we cannot let
      # Google users continue because we cannot refresh their access tokens
      if provider == 'google' and refresh_token is None: return redirect(url_for('home'))
      
      # Try and use their name, but if not set, use first part of email
      if name is None or name == "": name = username
      user = User(social_id=social_id,
                  name=name,
                  username=username,
                  email=email,
                  profile_picture=profile_picture,
                  provider=provider,
                  last_active=int(time.time()),
                  access_token=access_token,
                  access_token_exp=access_token_exp,
                  access_token_secret=access_token_secret,
                  refresh_token=refresh_token)
      db.session.add(user)
      db.session.commit()
  
  print " * Updating user values (AT, ATE, ATS, RT)"
  # Update the current access_token and access_token_exp
  # in the db with values just returned by oauth.callback()
  user.access_token = access_token
  user.access_token_exp = access_token_exp
  user.access_token_secret = access_token_secret
  
  # This is for if a google user revokes access and tries to log in re-granting access
  # our current refresh token on file has been revoked so we need to update, if given
  user.refresh_token = refresh_token or user.refresh_token
  db.session.commit()
  login_user(user, remember=True)
  return redirect(url_for('home'))

@app.route('/time')
def getTime():
  data = {'time': int(time.time())}
  resp = make_response()
  resp = jsonify(data)
  return resp

@app.route('/getUserDataFromId/<id>')
@login_required
def getUserDataFromId(id):
  try:
    u = User.query.get(id)
    data = {'id': u.id, 'name': u.name, 'username': u.username, 'profile_picture': u.profile_picture}
    resp = make_response()
    resp = jsonify(data)
  except Exception as e:
    resp = str(e)
  finally:
    return resp

@app.route('/getGeneralData')
@login_required
@valid_session
def generalData():
  oauth = OAuthSignIn.get_provider(current_user.provider)
  resp = oauth.getGeneralData()
  return jsonify(resp)

@login_required
def updateUserLastActive():
  print " * Update User Activity"
  current_user.last_active = int(time.time())
  db.session.commit()


"""
  The functions below should be applicable to all Flask apps.
"""
@app.before_request
def preRequest():
  pass

@app.after_request
def postRequest(response):
  # Add headers to both force latest IE rendering engine or Chrome Frame
  response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  # response.headers['Cache-Control'] = 'public, max-age=600' # overriding this with @nocache
  return response

@app.errorhandler(APIException)
def handle_invalid_usage(error):
  this_js = js_list[:]
  this_js.append('/static/js/404.js')
  return render_template('404.html', cssdep=css_list, jsdep=this_js), APIException.status_code

@app.errorhandler(404)
def page_not_found(error):
  this_js = js_list[:]
  this_js.append('/static/js/404.js')
  return render_template('404.html', cssdep=css_list, jsdep=this_js), 404


if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)