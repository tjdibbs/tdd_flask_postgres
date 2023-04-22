import pytest
from werkzeug.security import generate_password_hash

from main import create_app
from main.db import init_db, get_db
from dotenv import load_dotenv

from main.helpers.random import generate_id

load_dotenv()


@pytest.fixture
def app():

  app = create_app({
    "TESTING": True
  })

  with app.app_context():
    init_db()

  return app


@pytest.fixture
def client(app):
  return app.test_client()


@pytest.fixture
def runner(app):
  return app.test_cli_runner()


@pytest.fixture
def user(app):
  user = {"id": generate_id(), "username": "test", "password": generate_password_hash("12344")}
  with app.app_context():
    with get_db() as db:
      with db.cursor() as cursor:
        query = 'INSERT INTO users (id, username, password) VALUES (%s, %s, %s)'
        cursor.execute(query, (user["id"], user['username'], user['password']))

  del user['password']
  return user
