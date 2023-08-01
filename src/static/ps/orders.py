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
    "X-CSRFTOKEN": "IEDa0idwFDVCKUwTKp3IAcIIsfEQaNokWbrchZ4D1FQoiXBNnBkA7CsHxsusHNR0",
    "Authorization": f'Token {AUTH_DATA["token"]}',
}

import datetime


def check_expired(date: str):
    """Gets the current date in the format 2023-07-15."""
    current_date = datetime.datetime.now()
    current_date_str = current_date.strftime("%Y-%m-%d")
    if current_date_str > date:
        return "expired".capitalize()
    return "available".capitalize()


def check_user_to_add_modifying_buttons(oid):
    if js.window.location.href.__contains__("orders/current"):
        if AUTH_DATA["is_staff"]:
            return f"""
                <label for="approve-checkbox{oid}">
                    <input type="checkbox" id="approve-checkbox{oid}" py-click="approve_order({oid})">
                    Approve
                </label>
            """
        return f"""
            <button class="delete-button" py-click="delete_order({oid})">
                <i class="fas fa-trash"></i>
            </button>
        """
    return ""


def get_orders():
    url = f"{HOST_URL}api/orders/"
    if (
        js.window.location.href.__contains__("orders/current")
        and AUTH_DATA["is_staff"]
    ):
        response = requests.get(
            url, params={"status": "pending"}, headers=HEADERS
        )
    elif js.window.location.href.__contains__("orders/current"):
        response = requests.get(
            url,
            params={"status": "pending", "username": AUTH_DATA["username"]},
            headers=HEADERS,
        )

    if (
        js.window.location.href.__contains__("orders/archived")
        and AUTH_DATA["is_staff"]
    ):
        response = requests.get(
            url, params={"status": "completed"}, headers=HEADERS
        )
    elif js.window.location.href.__contains__("orders/archived"):
        response = requests.get(
            url,
            params={"status": "completed", "username": AUTH_DATA["username"]},
            headers=HEADERS,
        )

    ele = js.document.getElementById("get-orders")
    for o in response.json():
        ele.innerHTML += f"""
            <tr id="tr-{o["id"]}">
                <td colspan="4" style="text-align: left;">
                    <label>Order {o["id"]}</label>
                </td>
                <td colspan="4" style="text-align: right;">
                    Total Price
                    <label style="margin-right: 10px;">{o["total_price"]} NIS</label>
                    {check_user_to_add_modifying_buttons(o["id"])}
                </td>
            </tr>
        """
        for od in o.get("ordered_drugs"):
            ele.innerHTML += f"""
            <tr name="order{o["id"]}">
                <td>{od["drug"]["id"]}</td>
                <td>{od["drug"]["name"]}</td>
                <td>{od["quantity"]}</td>
                <td>{od["drug"]["exp_date"]}</td>
                <td>{check_expired(od["drug"]["exp_date"])}</td>
                <td>{od["drug"]["drug_price"]}</td>
                <td>{od["total_drug_price"]}</td>
                <td>{o["status"]}</td>
            </tr>
            """


def remove_rows(oid):
    js.document.getElementById(f"tr-{oid}").remove()
    rows = js.document.getElementsByName(f"order{oid}")
    for row in rows:
        row.remove()


def delete_order(oid):
    url = f"{HOST_URL}api/orders/{oid}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        remove_rows(oid)


def approve_order(oid):
    chkbox = js.document.getElementById(f"approve-checkbox{oid}")
    if chkbox.checked:
        url = f"{HOST_URL}api/orders/{oid}/status"
        data = {"status": "completed"}
        response = requests.patch(url, json.dumps(data), headers=HEADERS)
        if response.status_code == 200:
            remove_rows(oid)


if __name__ == "__main__":
    get_orders()
