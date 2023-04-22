import click
from flask.cli import FlaskGroup

from main import create_app  # new
from main.db import init_db


app = create_app()
cli = FlaskGroup(app)


@cli.command("trigger_db")
def trigger_db():
  """Clear the existing data and create new tables."""
  init_db()


if __name__ == '__main__':
  cli()
