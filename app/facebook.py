"""
  OAuthSignIn sub-class to support Facebook login
"""
from oauth import *

class FacebookSignIn(OAuthSignIn):
  public_name = "Facebook"
  provider_name = "facebook"
  
  def __init__(self):
    super(FacebookSignIn, self).__init__(self.provider_name)
    self.service = OAuth2Service(
        name='facebook',
        client_id=self.consumer_id,
        client_secret=self.consumer_secret,
        authorize_url='https://graph.facebook.com/oauth/authorize',
        access_token_url='https://graph.facebook.com/oauth/access_token',
        base_url='https://graph.facebook.com/'
    )
    self.oauth_session = None

  def authorize(self):
    print " * Facebook Authorize"
    print " * AUTHORIZE"
    return redirect(self.service.get_authorize_url(scope='email', response_type='code', redirect_uri=self.get_callback_url()))

  def callback(self):
    print " * Facebook Callback"
    print " * CALLBACK"
    if 'code' not in request.args: return None, None, None
    self.oauth_session = self.service.get_auth_session(data={'code': request.args['code'], 'grant_type': 'authorization_code', 'redirect_uri': self.get_callback_url()})
    session['access_token'] = self.oauth_session.access_token
    return self.getMe()

  @OAuthSignIn.auth_request
  def getMe(self):
    me = self.oauth_session.get('me?fields=email,picture.type(large),name,cover').json()
    social_id = me['id']
    name = me['name']
    username = me['email'].split('@')[0]
    email = me['email']
    profile_picture = me['picture']['data']['url']
    access_token = session['access_token']
    access_token_exp = None
    access_token_secret = None
    refresh_token = None
    # id, name, username, email, picture, access_token, access_token_exp, access_token_secret, refresh_token
    return social_id, name, username, email, profile_picture, access_token, access_token_exp, access_token_secret, refresh_token # Facebook does not expire access_tokens

  @OAuthSignIn.auth_request
  def getGeneralData(self):
    return self.oauth_session.get('me?fields=name,email,picture.type(large),cover').json()