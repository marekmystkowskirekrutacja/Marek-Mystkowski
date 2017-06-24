from flask import request, jsonify, Response
import re

def valid_key(key):
  return re.search('^[a-zA-Z0-9]{1,100}$', key) != None

class Controller:
  def __init__(self, app, url, con):
    
    @app.route(url + '/<id>', methods = ['PUT'])
    def api_update(id):
      if not valid_key(id):
        return '', 400
      content = request.stream.read()
      if len(content) > 1024*1024:
        return '', 413
      if not 'Content-Type' in request.headers:
        return '', 400
      con.add(id, content.decode("utf-8") , request.headers['Content-Type'])
      return '', 201
    
    @app.route(url + '/<id>', methods = ['GET'])
    def api_get(id):
      if not valid_key(id):
        return '', 400
      try:
        obj = con.get(id)
        return Response(obj['content'], mimetype = obj['type'])
      except KeyError:
        return '', 404;
    
    @app.route(url + '/<id>', methods = ['DELETE'])
    def api_delete(id):
      if not valid_key(id):
        return '', 400
      try:
        con.delete(id)
      except KeyError:
        return '', 404;
      return '', 200;
    
    @app.route(url, methods = ['GET'])
    @app.route(url + '/', methods = ['GET'])
    def api_get_all():
      return jsonify(con.get_all()), 200
