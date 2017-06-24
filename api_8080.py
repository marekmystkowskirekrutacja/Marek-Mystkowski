from flask import Flask

from controllers.object import Controller as ObjectController
from container import Container

if __name__ == '__main__':
  app = Flask(__name__)
  ObjectController(app, '/api/objects', Container())
  app.run(port = 8080)