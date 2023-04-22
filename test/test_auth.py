import json

import pytest


def test_get_all_user(client):
  users = client.get("/crud/").data.decode("utf-8")
  assert json.loads(users) == []


@pytest.mark.parametrize(('username', 'password', 'status'), (
  ('', '', 405),
  ('a', '', 405),
  ('test', '1234', 200)))
@pytest.mark.dependency()
def test_create_user(client, username, password, status):
  request = client.post("/crud/create", data={"username": username, "password": password})
  assert request.status_code == status


@pytest.mark.parametrize(("userid", "status_code"), (("", 404), ("2323", 200)))
def test_delete_user(client, userid, status_code):
  request = client.delete("/crud/delete/" + userid)
  assert request.status_code == status_code


def test_read_user(client, user):
  request = client.get("/crud/read/"+user['id']).data.decode("utf-8")
  assert json.loads(request) == user


# @pytest.mark.dependency(depends=["test_create_user"])
def test_update_user(client, app, user):
  new_username = "tj-dibb"
  client.patch("/crud/update/"+user['id'], data={"username": new_username})
  updated_user = client.get("/crud/read/"+user['id']).data.decode("utf-8")

  assert json.loads(updated_user)["username"] == new_username
