import json

import js
import pyodide_http as ph
import requests

# Patch the Requests library so it works with Pyscript
ph.patch_all()

HOST_URL = "http://localhost:8000/"

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "X-CSRFTOKEN": "IEDa0idwFDVCKUwTKp3IAcIIsfEQaNokWbrchZ4D1FQoiXBNnBkA7CsHxsusHNR0",
}


def login():
    url = f"{HOST_URL}api/auth/login"
    email = js.document.getElementById("email")
    password = js.document.getElementById("password")
    data = {
        "email": email.value,
        "password": password.value,
    }
    response = requests.post(url, json.dumps(data), headers=HEADERS)
    if response.status_code == 200:
        content = json.dumps(response.json()["data"])
        js.localStorage.setItem("auth_data", content)
        js.window.location.reload()


def reset():
    url = f"{HOST_URL}api/auth/password/forgot"
    email = js.document.getElementById("email")
    data = {
        "email": email.value,
    }
    response = requests.post(url, json.dumps(data), headers=HEADERS)
    js.alert(response.json()["message"])


def set_password():
    queries = js.window.location.search.split("?")[-1].split("&")
    js.console.log(queries)
    query_dict = {name.split("=")[0]: name.split("=")[1] for name in queries}
    uid = query_dict.get("uuid")
    token = query_dict.get("token")
    url = f"{HOST_URL}api/auth/password/{uid}/{token}/reset"
    data = {
        "password": js.document.getElementById("new_pass").value,
        "pass_again": js.document.getElementById("pass_again").value,
    }
    response = requests.post(url, json.dumps(data), headers=HEADERS)
    js.console.log(response.json()["success"])
    js.window.location.href = "http://localhost:8000/auth/login"


def change_password():
    url = f"{HOST_URL}api/auth/password/change"
    data = {
        "old_password": js.document.getElementById("old_pass").value,
        "new_password": js.document.getElementById("new_pass").value,
    }
    auth_data = js.localStorage.getItem("auth_data")
    auth_data = json.loads(auth_data)
    headers = {"Authorization": f'Token {auth_data["token"]}'}
    headers.update(HEADERS)
    response = requests.post(url, json.dumps(data), headers=headers)
    print(response.json())


def logout():
    url = f"{HOST_URL}api/auth/logout"
    auth_data = js.localStorage.getItem("auth_data")
    auth_data = json.loads(auth_data)
    headers = {"Authorization": f'Token {auth_data["token"]}'}
    headers.update(HEADERS)
    data = {"token": auth_data["token"]}
    response = requests.post(url, json.dumps(data), headers=headers)
    if response.status_code == 200:
        js.localStorage.removeItem("auth_data")
        js.window.location.replace(f"{HOST_URL}auth/login")
