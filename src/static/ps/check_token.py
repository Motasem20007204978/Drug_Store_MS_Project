import json

import js

auth_data = js.localStorage.getItem("auth_data")
if auth_data is not None:
    auth_data = json.loads(auth_data)
    if auth_data.get("token") and js.window.location.href.__contains__(
        "auth"
    ):
        js.window.location.replace("http://localhost:8000/profile")
    else:
        js.localStorage.removeItem("auth_data")
