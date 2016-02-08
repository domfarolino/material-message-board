"""
  API Resource sub-classes
"""
from flask_restful import Resource, Api
from models import Message
from error import APIException
from views import nocache, login_required, update_user_last_active, not_logged_in, valid_session

"""
  MessageAPI to GET and POST a single message
"""
class MessageAPI(Resource):

  @login_required
  def get(self, id):
    try:
      m = Message.query.get(id)
      resp = {'id': m.id, 'author': m.author, 'message': m.message}
    except Exception as e:
      print e
      raise APIException(str(e), status_code=500)
    finally:
      return resp

"""
  MessageListAPI to GET the last 10 messages in the database
  This is subject to change soon
"""
class MessageListAPI(Resource):

  @login_required
  def get(self):
    try:
      #messageList = Message.query.order_by(Message.time.desc(), Message.id.desc()).limit(10).offset(10)
      length = len(Message.query.all())
      offset = min(length, 10)
      messageList = Message.query.order_by(Message.time, Message.id).limit(10).offset(length-offset)
      resp = []
      for message in messageList:
        resp.append({'id': message.id, 'author': message.author, 'message': message.message, 'time': message.time})
    except Exception as e:
      print e
      raise APIException(str(e), status_code=500)
    return {'messages': resp}