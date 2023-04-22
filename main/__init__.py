import os

from flask import Flask
from . import db


def create_app(test_config=None):
  testing = test_config.get("TESTING") if test_config else False

  app = Flask(__name__)

  # set config
  app_settings = os.getenv("TESTING" if testing else 'DEVELOPMENT')
  app.config.from_object(app_settings)

  db.init_app(app)

  from .routes.crud import bp as crud_bp
  app.register_blueprint(crud_bp)

  return app
