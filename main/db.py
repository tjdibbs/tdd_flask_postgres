import os

import click
import psycopg2
from flask import g, current_app


def get_db():
  if "db" not in g:
    conn = psycopg2.connect(
      host=os.getenv("DATABASE_HOST"),
      database=os.getenv("DATABASE"),
      user=os.getenv("DATABASE_USER"),
      password=os.getenv("DATABASE_PASSWORD"))

    g.db = conn

  return g.db


def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()


def init_db():
  db = get_db()
  with db.cursor() as cursor:
    cursor.execute(current_app.open_resource("schema.sql").read())

  db.commit()


@click.command('init-db', help="Initialize the database")
def init_db_command():
  """Clear the existing data and create new tables."""
  init_db()
  click.echo('Initialized the database.')


def init_app(app):
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)
