from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session
from functools import wraps
import urllib2, json, time

# OAuth classes inspired by Miguel Grinberg's flask oauth blog post and code
# can be found here http://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
# and here          https://github.com/miguelgrinberg/flask-oauth-example
#
# Check the issue log in the README.md to see how I fixed an issue with making OAuth provider
# requests with multiple users logged on the site
#
# OAuthSignInObject is an object that uses a list
# structure to store a list of all of the OAuth subclasses
# The OAuth signin classes are objects specific to each OAuth
# provider. The get_provider method will get the appropriate
# subclass object for OAuth API Endpoint usage. The user specific
# access key will then be injected to the object.self.oauth_session.access_key
# variable so we can make an endpoint call on their behalf.
class OAuthSignIn(object):
  providers = None
  
  def __init__(self, provider_name):
    print " * Creating", provider_name.upper(), "OAuth Service"
    credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
    self.consumer_id = credentials['id']
    self.consumer_secret = credentials['secret']

  def authorize(self):
    pass

  def callback(self):
    pass

  def get_callback_url(self):
    return url_for('oauth_callback', provider=self.provider_name, _external=True)

  @classmethod
  def auth_request(self, f):
    @wraps(f)
    def wrapper(self):
        try:
            self.oauth_session.access_token = session['access_token']
            self.oauth_session.access_token_secret = session['access_token_secret'] # Twitter only
        except Exception as e:
            pass
        return f(self)
    return wrapper

  @classmethod
  def get_provider_names(self):
    provider_names = []
    for provider_class in self.__subclasses__():
        provider_names.append(provider_class.public_name)
    return provider_names

  @classmethod
  def get_provider(self, provider_name):
    print " * OAuthSignIn get_provider(", provider_name, ")"
    provider_name = provider_name.lower()
    if self.providers is None:
        self.providers = {}
        for provider_class in self.__subclasses__():
            provider = provider_class()
            self.providers[provider.provider_name] = provider
    print " * OAuth get_provider returning object"
    return self.providers[provider_name]

from facebook import FacebookSignIn
from twitter import TwitterSignIn
from google import GoogleSignIn