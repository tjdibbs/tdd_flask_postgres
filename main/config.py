

import os  # new


class Config(object):
  TESTING = False
  SECRET_KEY = os.environ.get('SECRET_KEY')  # new


class DevelopmentConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # new


class TestingConfig(Config):
  TESTING = True


class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # new
