
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

patients = {}
doctors = {}
appointments = []
rooms = {}
resources = {}
bills = []
treatments = []

STYLE = """
*{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif;background:#f4f7fb;color:#1e293b}
.layout{display:flex;min-height:100vh}
.sidebar{width:225px;background:#10243a;color:white;padding:25px 15px}
.brand{font-size:21px;font-weight:bold;margin:0 8px 8px}
.sub{font-size:12px;color:#b9c9da;margin:0 8px 28px}
.sidebar a{display:block;padding:12px 13px;color:#dce6f1;text-decoration:none;border-radius:8px;margin:4px 0}
.sidebar a:hover{background:#24415e;color:white}
main{padding:30px;width:100%;max-width:1300px;margin:auto}
h1{margin-top:0;font-size:28px}
.muted{color:#64748b}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:15px;margin:24px 0}
.card,.panel{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:20px}
.number{font-size:29px;font-weight:bold;margin-top:12px}
.panel{margin:18px 0}
form{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
input,select,textarea{padding:12px;border:1px solid #cbd5e1;border-radius:7px;width:100%;font-size:14px}
button{background:#176b87;color:white;border:0;padding:12px 18px;border-radius:7px;cursor:pointer;font-weight:bold}
button:hover{background:#12556d}
table{width:100%;border-collapse:collapse;margin-top:15px;background:white}
th,td{text-align:left;padding:12px;border-bottom:1px solid #e2e8f0;font-size:14px}
th{background:#edf3f8}
.table-wrap{overflow-x:auto}
.notice{background:#e7f5ee;padding:12px;border-radius:8px;margin:15px 0}
@media(max-width:650px){.layout{display:block}.sidebar{width:100%;padding:15px}.sidebar nav{display:flex;flex-wrap:wrap}.sidebar a{padding:9px;font-size:13px}main{padding:18px}}
"""

NAV = [
    ("Dashboard", "/"),
    ("Patients", "/patients"),
    ("Doctors", "/doctors"),
    ("Appointments", "/appointments"),
    ("Rooms", "/rooms"),
    ("Medical Resources", "/resources"),
    ("Billing", "/billing"),
    ("Treatment History", "/treatments"),
    ("Resource Report", "/report"),
]

PAGE = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CarePoint | Hospital Management</title>
<style>""" + STYLE + """</style></head><body>
<div class="layout">
<aside class="sidebar">
<div class="brand">CarePoint</div><div class="sub">Hospital Management System</div>
<nav>{% for label, link in nav %}<a href="{{link}}">{{label}}</a>{% endfor %}</nav>
</aside>
<main>
<h1>{{title}}</h1><p class="muted">{{subtitle}}</p>
{% if message %}<div class="notice">{{message}}</div>{% endif %}
{{content|safe}}
<p class="muted" style="font-size:12px;margin-top:35px">Academic project prototype · Do not enter real patient information</p>
</main></div></body></html>
"""


def page(title, subtitle, content, message=""):
    return render_template_string(
        PAGE, title=title, subtitle=subtitle, content=content,
        nav=NAV, message=message
    )


def table(headers, rows):
    result = "<div class='table-wrap'><table><tr>"
    for h in headers:
        result += f"<th>{h}</th>"
    result += "</tr>"
    if not rows:
        result += f"<tr><td colspan='{len(headers)}'>No records yet.</td></tr>"
    for row in rows:
        result += "<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>"
    return result + "</table></div>"


def form(fields, button="Save Record"):
    result = "<div class='panel'><form method='post'>"
    for name, label, kind in fields:
        if kind == "textarea":
            result += f"<textarea name='{name}' placeholder='{label}' required></textarea>"
        else:
            result += f"<input name='{name}' type='{kind}' placeholder='{label}' required>"
    result += f"<div><button type='submit'>{button}</button></div></form></div>"
    return result


@app.route("/")
def dashboard():
    content = "<div class='cards'>"
    stats = [
        ("Total Patients", len(patients)),
        ("Doctors", len(doctors)),
        ("Appointments", len(appointments)),
        ("Rooms", len(rooms)),
        ("Medical Resources", len(resources)),
        ("Bills Generated", len(bills)),
    ]
    for label, value in stats:
        content += f"<div class='card'><div class='muted'>{label}</div><div class='number'>{value}</div></div>"
    content += "</div><div class='panel'><h3>Hospital Overview</h3>"
    content += "<p>Manage patient records, appointments, room allocation, resources and billing from one place.</p></div>"
    return page("Dashboard", "Hospital operations at a glance", content)


@app.route("/patients", methods=["GET", "POST"])
def patient_page():
    msg = ""
    if request.method == "POST":
        pid = request.form["id"].strip()
        if pid in patients:
            msg = "Patient ID already exists."
        else:
            patients[pid] = {
                "name": request.form["name"].strip(),
                "age": request.form["age"],
                "gender": request.form["gender"],
                "contact": request.form["contact"].strip(),
                "disease": request.form["disease"].strip(),
            }
            msg = "Patient registered successfully."
    content = form([
        ("id", "Patient ID", "text"), ("name", "Full Name", "text"),
        ("age", "Age", "number"), ("gender", "Gender", "text"),
        ("contact", "Contact", "text"), ("disease", "Condition / Diagnosis", "text")
    ], "Register Patient")
    rows = [[k, v["name"], v["age"], v["gender"], v["contact"], v["disease"]]
            for k, v in patients.items()]
    content += "<div class='panel'><h3>Patient Directory</h3>"
    content += table(["Patient ID", "Name", "Age", "Gender", "Contact", "Condition"], rows) + "</div>"
    return page("Patients", "Register and manage patient records", content, msg)


@app.route("/doctors", methods=["GET", "POST"])
def doctor_page():
    msg = ""
    if request.method == "POST":
        did = request.form["id"].strip()
        if did in doctors:
            msg = "Doctor ID already exists."
        else:
            doctors[did] = {
                "name": request.form["name"].strip(),
                "specialty": request.form["specialty"].strip(),
                "contact": request.form["contact"].strip()
            }
            msg = "Doctor added successfully."
    content = form([
        ("id", "Doctor ID", "text"), ("name", "Doctor Name", "text"),
        ("specialty", "Specialization", "text"), ("contact", "Contact", "text")
    ], "Add Doctor")
    rows = [[k, v["name"], v["specialty"], v["contact"]] for k, v in doctors.items()]
    content += "<div class='panel'><h3>Doctor Directory</h3>"
    content += table(["Doctor ID", "Name", "Specialization", "Contact"], rows) + "</div>"
    return page("Doctors", "Manage doctors and specializations", content, msg)


@app.route("/appointments", methods=["GET", "POST"])
def appointment_page():
    msg = ""
    if request.method == "POST":
        pid, did = request.form["patient_id"].strip(), request.form["doctor_id"].strip()
        if pid not in patients:
            msg = "Please register the patient first."
        elif did not in doctors:
            msg = "Please add the doctor first."
        else:
            appointments.append({
                "patient": patients[pid]["name"], "doctor": doctors[did]["name"],
                "date": request.form["date"], "time": request.form["time"],
                "status": "Scheduled"
            })
            msg = "Appointment booked successfully."
    content = form([
        ("patient_id", "Patient ID", "text"), ("doctor_id", "Doctor ID", "text"),
        ("date", "Appointment Date", "date"), ("time", "Appointment Time", "time")
    ], "Book Appointment")
    rows = [[a["patient"], a["doctor"], a["date"], a["time"], a["status"]]
            for a in appointments]
    content += "<div class='panel'><h3>Appointments</h3>"
    content += table(["Patient", "Doctor", "Date", "Time", "Status"], rows) + "</div>"
    return page("Appointments", "Schedule patient visits", content, msg)


@app.route("/rooms", methods=["GET", "POST"])
def room_page():
    msg = ""
    if request.method == "POST":
        rid = request.form["id"].strip()
        action = request.form["action"]
        if action == "Add Room":
            if rid in rooms:
                msg = "Room ID already exists."
            else:
                rooms[rid] = {"type": request.form["type"], "patient": "", "status": "Available"}
                msg = "Room added successfully."
        elif rid not in rooms:
            msg = "Room not found."
        elif action == "Allocate Room":
            pid = request.form.get("patient_id", "").strip()
            if pid not in patients:
                msg = "Register the patient first."
            elif rooms[rid]["status"] == "Occupied":
                msg = "Room is already occupied."
            else:
                rooms[rid].update({"patient": patients[pid]["name"], "status": "Occupied"})
                msg = "Room allocated successfully."
        else:
            rooms[rid].update({"patient": "", "status": "Available"})
            msg = "Room released successfully."
    content = form([
        ("id", "Room ID", "text"), ("type", "Room Type", "text"),
        ("patient_id", "Patient ID (for allocation)", "text"),
        ("action", "Action: Add Room / Allocate Room / Release Room", "text")
    ], "Submit Room Action")
    rows = [[k, v["type"], v["patient"] or "—", v["status"]] for k, v in rooms.items()]
    content += "<div class='panel'><h3>Room Directory</h3>"
    content += table(["Room ID", "Type", "Patient", "Status"], rows) + "</div>"
    return page("Rooms", "Add rooms, allocate and release beds", content, msg)


@app.route("/resources", methods=["GET", "POST"])
def resource_page():
    msg = ""
    if request.method == "POST":
        rid = request.form["id"].strip()
        action = request.form["action"].strip().lower()
        try:
            qty = int(request.form["quantity"])
            if qty < 0:
                raise ValueError
        except ValueError:
            msg = "Enter a valid non-negative quantity."
        else:
            if action == "add":
                if rid in resources:
                    resources[rid]["quantity"] += qty
                else:
                    resources[rid] = {"name": request.form["name"].strip(), "quantity": qty}
                msg = "Resource stock updated."
            elif rid not in resources:
                msg = "Resource ID not found."
            elif qty <= 0:
                msg = "Quantity to use must be greater than zero."
            elif resources[rid]["quantity"] < qty:
                msg = "Insufficient stock available."
            else:
                resources[rid]["quantity"] -= qty
                msg = "Resource usage recorded."
    content = form([
        ("id", "Resource ID", "text"), ("name", "Resource Name (when adding)", "text"),
        ("quantity", "Quantity", "number"), ("action", "Action: add or use", "text")
    ], "Update Resources")
    rows = [[k, v["name"], v["quantity"]] for k, v in resources.items()]
    content += "<div class='panel'><h3>Resource Inventory</h3>"
    content += table(["Resource ID", "Name", "Quantity Available"], rows) + "</div>"
    return page("Medical Resources", "Track hospital supplies and usage", content, msg)


@app.route("/billing", methods=["GET", "POST"])
def billing_page():
    msg = ""
    if request.method == "POST":
        pid = request.form["patient_id"].strip()
        try:
            amount = float(request.form["amount"])
            if amount < 0:
                raise ValueError
        except ValueError:
            msg = "Enter a valid non-negative bill amount."
        else:
            if pid not in patients:
                msg = "Patient ID not found."
            else:
                bills.append({
                    "patient": patients[pid]["name"],
                    "amount": f"{amount:.2f}",
                    "description": request.form["description"].strip()
                })
                msg = "Bill created successfully."
    content = form([
        ("patient_id", "Patient ID", "text"), ("amount", "Amount (INR)", "number"),
        ("description", "Bill Description", "text")
    ], "Create Bill")
    rows = [[b["patient"], "₹" + b["amount"], b["description"]] for b in bills]
    content += "<div class='panel'><h3>Billing Records</h3>"
    content += table(["Patient", "Amount", "Description"], rows) + "</div>"
    return page("Billing", "Create and view billing records", content, msg)


@app.route("/treatments", methods=["GET", "POST"])
def treatment_page():
    msg = ""
    if request.method == "POST":
        pid = request.form["patient_id"].strip()
        if pid not in patients:
            msg = "Patient ID not found."
        else:
            treatments.append({
                "patient": patients[pid]["name"],
                "date": request.form["date"],
                "details": request.form["details"].strip()
            })
            msg = "Treatment history added."
    content = form([
        ("patient_id", "Patient ID", "text"), ("date", "Treatment Date", "date"),
        ("details", "Treatment Details", "textarea")
    ], "Add Treatment")
    rows = [[t["patient"], t["date"], t["details"]] for t in treatments]
    content += "<div class='panel'><h3>Treatment History</h3>"
    content += table(["Patient", "Date", "Details"], rows) + "</div>"
    return page("Treatment History", "Maintain treatment records", content, msg)


@app.route("/report")
def report_page():
    content = "<div class='cards'>"
    content += f"<div class='card'>Available Rooms<div class='number'>{sum(r['status'] == 'Available' for r in rooms.values())}</div></div>"
    content += f"<div class='card'>Occupied Rooms<div class='number'>{sum(r['status'] == 'Occupied' for r in rooms.values())}</div></div>"
    content += f"<div class='card'>Low Stock Items<div class='number'>{sum(r['quantity'] <= 5 for r in resources.values())}</div></div>"
    content += "</div><div class='panel'><h3>Medical Resource Status</h3>"
    content += table(["Resource ID", "Name", "Quantity", "Status"], [
        [k, v["name"], v["quantity"], "Low stock" if v["quantity"] <= 5 else "Available"]
        for k, v in resources.items()
    ]) + "</div>"
    return page("Resource Report", "Room occupancy and inventory overview", content)


if __name__ == "__main__":
    app.run(debug=True)
