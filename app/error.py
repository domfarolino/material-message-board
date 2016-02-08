"""
  Simple APIException class to handle, a little more cleanly, routing
  exceptions especially with Rest API calls so we don't ouput a bunch
  of random or even sensitive information
  
  Based on the class found here:
  http://flask.pocoo.org/docs/0.10/patterns/apierrors/
"""

class APIException(Exception):
  def __init__(self, message, status_code=None, payload=None):
    Exception.__init__(self)
    self.message = message
    self.status_code = status_code or 400
    self.payload = payload

  def to_dict(self):
    re = dict(self.payload or ())
    re['message'] = self.message
    re['status_code'] = self.status_code
    return re