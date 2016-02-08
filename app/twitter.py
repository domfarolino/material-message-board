"""
  OAuthSignIn sub-class to support Twitter login
"""
from oauth import *

class TwitterSignIn(OAuthSignIn):
  public_name = "Twitter"
  provider_name = "twitter"
  
  def __init__(self):
    super(TwitterSignIn, self).__init__(self.provider_name)
    self.service = OAuth1Service(
        name='twitter',
        consumer_key=self.consumer_id,
        consumer_secret=self.consumer_secret,
        request_token_url='https://api.twitter.com/oauth/request_token',
        authorize_url='https://api.twitter.com/oauth/authorize',
        access_token_url='https://api.twitter.com/oauth/access_token',
        base_url='https://api.twitter.com/1.1/'
    )
    self.oauth_session = None

  def authorize(self):
    print " * Twitter Authorize"
    print " * AUTHORIZE"
    request_token = self.service.get_request_token(params={'oauth_callback': self.get_callback_url()})
    session['request_token'] = request_token
    return redirect(self.service.get_authorize_url(request_token[0]))

  def callback(self):
    print " * Twitter Callback"
    print " * CALLBACK"
    request_token = session.pop('request_token')
    if 'oauth_verifier' not in request.args: return None
    self.oauth_session = self.service.get_auth_session(request_token[0], request_token[1], data={'oauth_verifier': request.args['oauth_verifier']})
    print vars(self.oauth_session)
    session['access_token'] = self.oauth_session.access_token
    session['access_token_secret'] = self.oauth_session.access_token_secret
    return self.getMe()

  @OAuthSignIn.auth_request
  def getMe(self):
    me = self.oauth_session.get('account/verify_credentials.json').json()
    social_id = me['id_str']
    name = me['name']
    username = me['screen_name']
    email = None # Twitter does not provide email
    profile_picture = me['profile_image_url_https']
    access_token = session['access_token']
    access_token_exp = None # Twitter doesn't expires ACs
    access_token_secret = session['access_token_secret']
    refresh_token = None # Twitter doesn't use refresh tokens
    # id, name, username, email, picture, access_token, access_token_exp, access_token_secret, refresh_token
    return social_id, name, username, email, profile_picture, access_token, access_token_exp, access_token_secret, refresh_token # Twitter does not expire access_tokens
  
  @OAuthSignIn.auth_request
  def getGeneralData(self):
    return self.oauth_session.get('account/verify_credentials.json').json()