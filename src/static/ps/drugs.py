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


def new_drug(drug_data):
    url = f"{HOST_URL}api/drugs"
    response = requests.post(url, json.dumps(drug_data), headers=HEADERS)
    if response.status_code == 201:
        response.json()


def all_drugs(page=1):
    tbody = js.document.getElementById("drugs-body")
    tbody.innerHTML = ""

    url = f"{HOST_URL}api/drugs/"
    HEADERS["Authorization"] = f"Token {AUTH_DATA['token']}"
    response = requests.get(url, headers=HEADERS)
    for d in response.json():
        tbody.innerHTML += f"""
            <tr id="drug{d["id"]}">
                <th scope="row" class="ps-4"> 
                </th>
                <td contenteditable="false">
                    {d["name"]}
                </td>
                <td contenteditable="false">{d["quantity"]}
                </td>
                <td contenteditable="false">
                    {d["exp_date"]}
                </td>
                <td contenteditable="false">{d["drug_price"]}</td>
                <td>
                    <ul class="list-inline mb-0">
                    <li class="list-inline-item" id="editable{d["id"]}">
                        <a
                        href="javascript:void(0);"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        py-click="make_cells_editable({d["id"]})"
                        title="Edit"
                        class="px-2 text-primary"
                        ><i class="bx bx-pencil font-size-18"></i
                        ></a>
                    </li>
                    <li class="list-inline-item" id="edit{d["id"]}" style="display:none;">
                        <button class="btn btn-sm btn-primary" py-click="update_drug({d["id"]})">
                            Edit <i class="fas fa-edit"></i>
                        </button>
                    </li>  
                    <li class="list-inline-item">
                        <a
                        href="javascript:void(0);"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        py-click="delete_drug({d["id"]})"
                        title="Delete"
                        class="px-2 text-danger"
                        ><i class="bx bx-trash-alt font-size-18"></i
                        ></a>
                    </li>
                    </ul>
                </td>
            </tr>
        """
    js.document.getElementById("drugs-count").innerHTML = len(response.json())


def delete_drug(did):
    url = f"{HOST_URL}api/drugs/{did}"
    HEADERS["Authorization"] = f"Token {AUTH_DATA['token']}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        js.document.getElementById(f"drug{did}").remove()
        dchtml = js.document.getElementById("drugs-count")
        drugs_count = int(dchtml.innerHTML)
        drugs_count -= 1
        dchtml.innerHTML = drugs_count


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


def make_cells_editable(did):
    tr = js.document.getElementById(f"drug{did}")
    tds = tr.getElementsByTagName("td")
    js.console.log(len(tds))
    # // Loop through all cells in a row and replace the content with editable one
    for i in range(0, len(tds) - 1):
        tds[i].setAttribute("contenteditable", "true")
    js.document.getElementById(f"editable{did}").style.display = "none"
    js.document.getElementById(f"edit{did}").style.display = "inline"


def update_drug(did):
    url = f"{HOST_URL}api/drugs/{did}"
    tr = js.document.getElementById(f"drug{did}")
    tds = tr.getElementsByTagName("td")
    data = {
        "name": tds[0].innerHTML.strip(),
        "quantity": tds[1].innerHTML.strip(),
        "exp_date": tds[2].innerHTML.strip(),
        "drug_price": tds[3].innerHTML.strip(),
    }
    response = requests.patch(url, json.dumps(data), headers=HEADERS)
    js.console.log(response.json())
    if response.status_code == 200:
        for i in range(0, len(tds) - 1):
            tds[i].setAttribute("contenteditable", "false")
        js.document.getElementById(f"edit{did}").style.display = "none"
        js.document.getElementById(f"editable{did}").style.display = "inline"


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

    if ORDERED_DRUGS["ordered_drugs"].__len__() != 0:
        response = requests.post(
            url, data=json.dumps(ORDERED_DRUGS), headers=HEADERS
        )
        if response.status_code == 201:
            js.alert("Order saved successfully")
    else:
        js.alert("must add drugs")


if js.location.href.__contains__("/drugs"):
    all_drugs()
else:
    get_drugs()
