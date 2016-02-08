"""
  OAuthSignIn sub-class to support Google login
"""
from oauth import *

class GoogleSignIn(OAuthSignIn):
  public_name = "Google"
  provider_name = "google"
  
  def __init__(self):
    import ast
    print "GoogleSignIn Object __init__()"
    super(GoogleSignIn, self).__init__(self.provider_name)
    print " * Creating googleinfo variable to store latest api information"
    googleinfo = urllib2.urlopen('https://accounts.google.com/.well-known/openid-configuration')
    print " * Creating json from googleinfo"
    google_params = json.load(googleinfo)
    self.service = OAuth2Service(name='google', client_id=self.consumer_id, client_secret=self.consumer_secret, authorize_url=google_params.get('authorization_endpoint'), base_url=google_params.get('userinfo_endpoint'), access_token_url=google_params.get('token_endpoint'))
    self.oauth_session = None
    print " * GoogleSignIn Object __init__() complete"

  def authorize(self):
    print " * Google Authorize"
    print " * AUTHORIZE"
    return redirect(self.service.get_authorize_url(scope='email', response_type='code', redirect_uri=self.get_callback_url(), access_type='offline'))

  def callback(self):
    print " * Google Callback"
    print " * CALLBACK"
    if 'code' not in request.args: return None
    print " * Google creating self.oauth_session"
    self.oauth_session = self.service.get_auth_session(data={'code': request.args['code'], 'grant_type': 'authorization_code', 'redirect_uri': self.get_callback_url() }, decoder=json.loads)
    print vars(self.oauth_session)
    session['access_token'] = self.oauth_session.access_token
    return self.getMe()

  @OAuthSignIn.auth_request
  def getMe(self):
    print " * Google getMe()"
    me = self.oauth_session.get('').json()
    social_id = me['sub']
    name = me['name']
    username = me['email'].split('@')[0]
    email = me['email']
    profile_picture = me['picture']
    access_token = session['access_token']
    
    access_token_info = urllib2.urlopen('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=' + access_token)
    access_token_info = json.load(access_token_info)
    
    access_token_exp = access_token_info['expires_in']+time.time()
    access_token_secret = None # Google does not use access_token_secret
    refresh_token = None
    #print self.oauth_session.access_token_response._content.json()
    try:
        refresh_token = str(ast.literal_eval(self.oauth_session.access_token_response._content)['refresh_token'])
        print " * This is user's first time giving access to this site"
    except:
        print " * User must've already granted access to this site"
    # id, name, username, email, picture, access_token, access_token_exp, access_token,_secret refresh_token
    return social_id, name, username, email, profile_picture, access_token, access_token_exp, access_token_secret, refresh_token

  def refreshAccessToken(self, refresh_token):
    data = {'client_id':self.consumer_id,
            'client_secret': self.consumer_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
            }
    self.oauth_session = self.service.get_auth_session(data=data, decoder=ast.literal_eval)
    session['access_token'] = self.oauth_session.access_token

  
  def getAccessTokenAndExpire(self):
    access_token_info = urllib2.urlopen('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=' + access_token)
    access_token_info = json.load(access_token_info)
    return access_token_info['access_token'], access_token_info['expires_in']+time.time()

  @OAuthSignIn.auth_request
  def getGeneralData(self):
    return self.oauth_session.get('').json()