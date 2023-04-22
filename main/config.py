

import os  # new


class Config(object):
  TESTING = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False  # new
  SECRET_KEY = os.environ.get('SECRET_KEY')  # new


class DevelopmentConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # new


class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')  # new


class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # new
