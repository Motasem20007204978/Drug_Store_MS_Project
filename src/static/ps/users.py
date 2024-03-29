import json

import js
import pyodide_http as ph
import requests

ph.patch_all()

HOST_URL = "http://localhost:8000/"
AUTH_DATA = js.localStorage.getItem("auth_data")
AUTH_DATA = json.loads(AUTH_DATA)
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f'Token {AUTH_DATA["token"]}',
}


def all_users():
    tbody = js.document.getElementById("users-body")
    tbody.innerHTML = ""

    url = f"{HOST_URL}api/users/"
    HEADERS["Authorization"] = f"Token {AUTH_DATA['token']}"
    response = requests.get(url, headers=HEADERS)
    for u in response.json():
        if u["username"] == AUTH_DATA["username"]:
            continue
        # https://bootdey.com/img/Content/avatar/avatar1.png
        tbody.innerHTML += f"""
            <tr id="user{u["username"]}">
                <th scope="row" class="ps-4"> 
                </th>
                <td>
                <img src="{u["profile_pic"]}" alt="" class="avatar-sm rounded-circle me-2" />
            {u["username"]}
          </td>
          <td>{u["email"]}
          </td>
          <td>
            {u["first_name"]}
          </td>
          <td>{u["last_name"]}</td>
            <td>{u["location"]}</td>
                <td>
                    <ul class="list-inline mb-0">
                    <li class="list-inline-item">
                        <a
                        href="javascript:void(0);"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        py-click="delete_user('{u["username"]}')"
                        title="Delete"
                        class="px-2 text-danger"
                        ><i class="bx bx-trash-alt font-size-18"></i
                        ></a>
                    </li>
                    </ul>
                </td>
            </tr>
        """
    js.document.getElementById("users-count").innerHTML = (
        len(response.json()) - 1
    )


def delete_user(username):
    url = f"{HOST_URL}api/users/{username}"
    HEADERS["Authorization"] = f"Token {AUTH_DATA['token']}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        js.document.getElementById(f"user{username}").remove()
        uchtml = js.document.getElementById("users-count")
        users_count = int(uchtml.innerHTML)
        users_count -= 1
        uchtml.innerHTML = users_count


def get_data():
    url = f"{HOST_URL}api/users/{AUTH_DATA['username']}"
    HEADERS["Authorization"] = f"Token {AUTH_DATA['token']}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        response = response.json()
        js.document.getElementById("profile_pic").src = response[
            "profile_pic"
        ]
        js.document.getElementById("inputUsername").value = response[
            "username"
        ]
        js.document.getElementById("inputFirstName").value = response[
            "first_name"
        ]
        js.document.getElementById("inputLastName").value = response[
            "last_name"
        ]
        js.document.getElementById("inputLocation").value = response[
            "location"
        ]
        js.document.getElementById("inputEmailAddress").value = response[
            "email"
        ]


def patch_data():
    url = f"{HOST_URL}api/users/{AUTH_DATA['username']}"
    data = {
        "username": js.document.getElementById("inputUsername").value,
        "first_name": js.document.getElementById("inputFirstName").value,
        "last_name": js.document.getElementById("inputLastName").value,
        "location": js.document.getElementById("inputLocation").value,
        "email": js.document.getElementById("inputEmailAddress").value,
    }
    HEADERS["Authorization"] = f"Token {AUTH_DATA['token']}"
    response = requests.patch(url, json.dumps(data), headers=HEADERS)
    if response.status_code == 200:
        AUTH_DATA["username"] = data["username"]
        js.localStorage.setItem("auth_data", json.dumps(AUTH_DATA))


def popup():
    js.document.getElementById("popup").style.display = "block"
    body_style = js.document.getElementsByTagName("body")[0].style
    body_style.background = "black"
    body_style.opacity = 0.7


def upload(base64_text):
    data = {"profile_pic": base64_text}
    url = f"{HOST_URL}api/users/{AUTH_DATA['username']}"
    HEADERS["Authorization"] = f"Token {AUTH_DATA['token']}"
    response = requests.patch(url, json.dumps(data), headers=HEADERS)
    if response.status_code == 200:
        image_url = response.json()["profile_pic"]
        js.document.getElementById("profile_pic").src = image_url
        js.document.getElementById("profilepicture").src = image_url
        AUTH_DATA["profile_pic"] = image_url
        js.localStorage.setItem("auth_data", json.dumps(AUTH_DATA))


def change_pass():
    old_pass = js.document.getElementById("old_pass")
    new_pass = js.document.getElementById("new_pass")
    url = f"{HOST_URL}api/auth/password/change"
    data = {
        "old_password": old_pass,
        "new_password": new_pass,
    }
    HEADERS["Authorization"] = f"Token {AUTH_DATA['token']}"
    response = requests.post(url, json.dumps(data), headers=HEADERS)
    if response.status_code == 201:
        js.alert("password changed successfully")


if __name__ == "__main__":
    if js.location.href.__contains__("/users"):
        all_users()
    else:
        get_data()
