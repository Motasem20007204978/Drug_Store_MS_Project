import datetime
import json

import js
import pyodide_http as ph
import requests

ph.patch_all()

HOST_URL = "http://localhost:8000/"
AUTH_DATA = js.localStorage.getItem("auth_data")
AUTH_DATA = json.loads(AUTH_DATA)
HEADERS = {
    "accept": "*/*",
    "Content-Type": "*/*",
    "Authorization": f'Token {AUTH_DATA["token"]}',
}


def upload_file_drugs_data(form_data):
    url = f"{HOST_URL}api/drugs/upload"
    response = requests.post(url, headers=HEADERS, files=form_data["file"])


def check_expired(date: str):
    """Gets the current date in the format 2023-07-15."""
    current_date = datetime.datetime.now()
    current_date_str = current_date.strftime("%Y-%m-%d")
    if current_date_str > date:
        return "expired"
    return "available"


def get_drugs():
    url = f"{HOST_URL}api/drugs/"
    response = requests.get(
        url, params={"fields": "id,name"}, headers=HEADERS
    )
    ele = js.document.getElementById("get-drugs")
    for o in response.json():
        ele.innerHTML += f"<option value='{o['id']}'>{o['name']}</option>"


ORDERED_DRUGS = {"ordered_drugs": []}


def calc_total_price():
    eles = js.document.getElementsByName("price")
    tp = sum([float(e.innerText) for e in eles])
    return tp


def add_drug():
    did = js.document.getElementById("get-drugs").value
    quantity = js.document.getElementsByName("quantity")[0].value
    if int(did) > 0 and int(quantity) > 0:
        url = f"{HOST_URL}api/drugs/{int(did)}"
        response = requests.get(
            url,
            params={"fields": "id,name,drug_price,exp_date"},
            headers=HEADERS,
        ).json()
        od = {"drug": int(did), "quantity": int(quantity)}
        ORDERED_DRUGS["ordered_drugs"].append(od)
        tr_tp = js.document.getElementsByName("tr-total-price")
        if tr_tp:
            tr_tp[0].remove()
        tbody = js.document.getElementsByTagName("tbody")[0]
        tbody.innerHTML += f"""
        <tr id="tr-{response["id"]}">
            <td>{response["id"]}</td>
            <td>{response["name"]}</td>
            <td>{quantity}</td>
            <td>{check_expired(response["exp_date"])}</td>
            <td>{response["exp_date"]}</td>
            <td>{response["drug_price"]}</td>
            <td name="price">{int(quantity)*float(response["drug_price"])}</td>
            <td><button type="button" class="btn" id="remove" py-click="remove({response["id"]})">remove</button></td>
        </tr>
        """
        tbody.innerHTML += f"""
            <tr name="tr-total-price">
                <td colspan="8">Total Price <label name="total-price">{calc_total_price()} NIS</label></td>
            </tr>
        """


def remove(id):
    js.document.getElementById(f"tr-{id}").remove()
    ORDERED_DRUGS["ordered_drugs"] = list(
        filter(
            lambda item: item["drug"] != id, ORDERED_DRUGS["ordered_drugs"]
        )
    )
    tr_tp = js.document.getElementsByName("tr-total-price")
    if tr_tp:
        tr_tp[0].remove()
    if calc_total_price():
        tbody = js.document.getElementsByTagName("tbody")[0]
        tbody.innerHTML += f"""
            <tr name="tr-total-price">
                <td colspan="8">Total Price <label name="total-price">{calc_total_price()} NIS</label></td>
            </tr>
        """


def save():
    url = f"{HOST_URL}api/orders/"
    response = requests.post(
        url, data=json.dumps(ORDERED_DRUGS), headers=HEADERS
    )
    if response.status_code == 201:
        js.alert("Order saved successfully")


get_drugs()
