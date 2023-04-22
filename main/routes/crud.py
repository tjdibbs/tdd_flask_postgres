from flask import (
  Blueprint, request, session, Response, Flask, make_response
)

from werkzeug.security import check_password_hash, generate_password_hash

from main.db import get_db
from main.helpers.random import generate_id

bp = Blueprint("crud", __name__, url_prefix="/crud")


@bp.route("/")
def get_all_users():
  get_query = "SELECT id,username from users"

  with get_db() as db:
    with db.cursor() as cursor:
      cursor.execute(get_query)
      rows = cursor.fetchall()

      user_list = []
      for row in rows:
        user = {'id': row[0], 'username': row[1]}
        user_list.append(user)

      return user_list


@bp.route("/read/<userid>")
def get_user_by_id(userid):
  if not userid:
    return Response("not allowed", 405)

  print(userid)
  try:
    with get_db() as db:
      with db.cursor() as cursor:
        cursor.execute("SELECT id, username from users WHERE id=%s", (userid,))
        row = cursor.fetchone()

        user = {'id': row[0], 'username': row[1]} if row else "User Not Found"
        return make_response(user, 200 if row else 404)

  except Exception as e:
    print(e)
    return make_response({"success": False, "message": "Internal Server Error"})


@bp.route("/create", methods=["POST"])
def create():
  try:
    # application/json or x-www-urlencoded/form
    body = request.get_json(silent=True) or request.form

    password = body.get("password")
    username = body.get("username")

    if not password or not username:
      return Response("Not Allowed", status=405)

    with get_db() as db:
      with db.cursor() as cursor:
        query = 'INSERT INTO users (id, username, password) VALUES (%s, %s, %s)'
        cursor.execute(query, (generate_id(), username, generate_password_hash(password)))

    return {"success": True}
  except Exception as e:
    message = "Internal Server Error"
    e_msg = str(e)

    print(e)
    if "duplicate" in e_msg:
      message = "Account already exist"

    return make_response({"message": message, "success": False}, 500)


@bp.route("/update/<userid>", methods=["PATCH"])
def update(userid):
  # application/json or x-www-urlencoded/form
  fields = request.get_json(silent=True) or request.form

  if not userid or not bool(fields):
    return Response("Not allowed", 405)

  try:
    with get_db() as db:
      with db.cursor() as cursor:
        update_fields = ",".join([f"{key}='{value}'" for key, value in fields.items()])
        patch_query = f"UPDATE users SET {update_fields} WHERE id=%s"

        cursor.execute(patch_query, (userid,))
        return {"success": True}

  except Exception as e:
    print(e)
    return make_response({"success": False, "message": "Internal Server Error"}, 500)


@bp.route("/delete/<userid>", methods=["DELETE"])
def delete(userid):
  try:
    with get_db() as db:
      with db.cursor() as cursor:
        patch_query = "DELETE FROM users WHERE id=%s"
        cursor.execute(patch_query, (userid,))
        return {"success": True, "message": "Deleted Successfully"}

  except Exception as e:
    e_msg = e.args[0]
    return make_response({"success": False, "message": "Internal Server Error"})
