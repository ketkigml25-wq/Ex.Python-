# Hospital Resource & Patient Management System
# Phase II - Python Programming Language Project

patients = {}
doctors = {}
appointments = []
rooms = {}
resources = {}
bills = {}
treatments = {}


# ---------------- PATIENT MANAGEMENT ----------------

def add_patient():
    patient_id = input("Enter Patient ID: ")

    if patient_id in patients:
        print("Patient already exists.")
        return

    name = input("Enter Patient Name: ")
    age = input("Enter Age: ")
    if not age.isdigit():
        print("Please enter a valid age.")
        return
    disease = input("Enter Disease/Problem: ")

    patients[patient_id] = {
        "name": name,
        "age": age,
        "disease": disease
    }

    print("Patient added successfully.")


def view_patients():
    if not patients:
        print("No patient records found.")
        return

    print("\n----- PATIENT RECORDS -----")

    for patient_id, data in patients.items():
        print("Patient ID:", patient_id)
        print("Name:", data["name"])
        print("Age:", data["age"])
        print("Disease:", data["disease"])
        print("--------------------------")


# ---------------- DOCTOR MANAGEMENT ----------------

def add_doctor():
    doctor_id = input("Enter Doctor ID: ")

    if doctor_id in doctors:
        print("Doctor already exists.")
        return

    name = input("Enter Doctor Name: ")
    department = input("Enter Department: ")

    doctors[doctor_id] = {
        "name": name,
        "department": department,
        "status": "Available"
    }

    print("Doctor added successfully.")


def view_doctors():
    if not doctors:
        print("No doctor records found.")
        return

    print("\n----- DOCTOR RECORDS -----")

    for doctor_id, data in doctors.items():
        print("Doctor ID:", doctor_id)
        print("Name:", data["name"])
        print("Department:", data["department"])
        print("Status:", data["status"])
        print("-------------------------")


# ---------------- APPOINTMENT MANAGEMENT ----------------

def book_appointment():
    patient_id = input("Enter Patient ID: ")
    doctor_id = input("Enter Doctor ID: ")

    if patient_id not in patients:
        print("Patient not found.")
        return

    if doctor_id not in doctors:
        print("Doctor not found.")
        return

    if doctors[doctor_id]["status"] != "Available":
        print("Doctor is currently unavailable.")
        return

    date = input("Enter Appointment Date: ")
    time = input("Enter Appointment Time: ")

    appointment = {
        "patient": patient_id,
        "doctor": doctor_id,
        "date": date,
        "time": time
    }

    appointments.append(appointment)

    doctors[doctor_id]["status"] = "Booked"

    print("Appointment booked successfully.")


def view_appointments():
    if not appointments:
        print("No appointments found.")
        return

    print("\n----- APPOINTMENTS -----")

    for appointment in appointments:
        print("Patient ID:", appointment["patient"])
        print("Doctor ID:", appointment["doctor"])
        print("Date:", appointment["date"])
        print("Time:", appointment["time"])
        print("-----------------------")


# ---------------- ROOM MANAGEMENT ----------------

def add_room():
    room_id = input("Enter Room ID: ")

    if room_id in rooms:
        print("Room already exists.")
        return

    room_type = input("Enter Room Type: ")

    rooms[room_id] = {
        "type": room_type,
        "status": "Free",
        "patient": None
    }

    print("Room added successfully.")


def allocate_room():
    patient_id = input("Enter Patient ID: ")
    room_id = input("Enter Room ID: ")

    if patient_id not in patients:
        print("Patient not found.")
        return

    if room_id not in rooms:
        print("Room not found.")
        return

    if rooms[room_id]["status"] != "Free":
        print("Room is already occupied.")
        return

    rooms[room_id]["status"] = "Occupied"
    rooms[room_id]["patient"] = patient_id

    print("Room allocated successfully.")


def release_room():
    room_id = input("Enter Room ID: ")

    if room_id not in rooms:
        print("Room not found.")
        return

    if rooms[room_id]["status"] == "Free":
        print("Room is already free.")
        return

    rooms[room_id]["status"] = "Free"
    rooms[room_id]["patient"] = None

    print("Room released successfully.")


def view_rooms():
    if not rooms:
        print("No rooms added.")
        return

    print("\n----- ROOM STATUS -----")

    for room_id, data in rooms.items():
        print("Room ID:", room_id)
        print("Type:", data["type"])
        print("Status:", data["status"])
        print("Patient:", data["patient"])
        print("----------------------")


# ---------------- MEDICAL RESOURCE MANAGEMENT ----------------

def add_resource():
    resource_id = input("Enter Resource ID: ")

    if resource_id in resources:
        print("Resource already exists.")
        return

    name = input("Enter Resource Name: ")
    quantity = int(input("Enter Quantity: "))

    resources[resource_id] = {
        "name": name,
        "quantity": quantity
    }

    print("Medical resource added successfully.")


def use_resource():
    resource_id = input("Enter Resource ID: ")
    quantity = int(input("Enter Quantity to Use: "))

    if resource_id not in resources:
        print("Resource not found.")
        return

    if quantity <= 0:
        print("Enter a valid quantity.")
        return

    if resources[resource_id]["quantity"] >= quantity:
        resources[resource_id]["quantity"] -= quantity
        print("Resource allocated successfully.")
    else:
        print("Insufficient resource available.")


def view_resources():
    if not resources:
        print("No medical resources found.")
        return

    print("\n----- MEDICAL RESOURCES -----")

    for resource_id, data in resources.items():
        print("Resource ID:", resource_id)
        print("Name:", data["name"])
        print("Available Quantity:", data["quantity"])
        print("----------------------------")


# ---------------- BILLING ----------------

def create_bill():
    patient_id = input("Enter Patient ID: ")

    if patient_id not in patients:
        print("Patient not found.")
        return

    consultation = float(input("Enter Consultation Charge: "))
    room_charge = float(input("Enter Room Charge: "))
    medicine = float(input("Enter Medicine Charge: "))

    total = consultation + room_charge + medicine

    bills[patient_id] = total

    print("Bill created successfully.")
    print("Total Bill: ₹", total)


def view_bill():
    patient_id = input("Enter Patient ID: ")

    if patient_id not in bills:
        print("Bill not found.")
        return

    print("Patient ID:", patient_id)
    print("Total Bill: ₹", bills[patient_id])


# ---------------- TREATMENT HISTORY ----------------

def add_treatment():
    patient_id = input("Enter Patient ID: ")

    if patient_id not in patients:
        print("Patient not found.")
        return

    treatment = input("Enter Treatment Details: ")

    if patient_id not in treatments:
        treatments[patient_id] = []

    treatments[patient_id].append(treatment)

    print("Treatment history added successfully.")


def view_treatment():
    patient_id = input("Enter Patient ID: ")

    if patient_id not in treatments:
        print("No treatment history found.")
        return

    print("\n----- TREATMENT HISTORY -----")

    for treatment in treatments[patient_id]:
        print("-", treatment)


# ---------------- RESOURCE REPORT ----------------

def resource_report():
    print("\n========== HOSPITAL STATUS REPORT ==========")

    print("\nRooms:")
    if rooms:
        for room_id, data in rooms.items():
            print(room_id, "-", data["type"], "-", data["status"])
    else:
        print("No rooms available.")

    print("\nDoctors:")
    if doctors:
        for doctor_id, data in doctors.items():
            print(doctor_id, "-", data["name"], "-", data["status"])
    else:
        print("No doctors available.")

    print("\nMedical Resources:")
    if resources:
        for resource_id, data in resources.items():
            print(
                resource_id,
                "-",
                data["name"],
                "- Quantity:",
                data["quantity"]
            )
    else:
        print("No medical resources available.")

    print("============================================")


# ---------------- MAIN MENU ----------------

def main():

    while True:

        print("\n")
        print("==============================================")
        print(" HOSPITAL RESOURCE & PATIENT MANAGEMENT SYSTEM")
        print("==============================================")

        print("1. Add Patient")
        print("2. View Patients")
        print("3. Add Doctor")
        print("4. View Doctors")
        print("5. Book Appointment")
        print("6. View Appointments")
        print("7. Add Room")
        print("8. Allocate Room")
        print("9. Release Room")
        print("10. View Rooms")
        print("11. Add Medical Resource")
        print("12. Use Medical Resource")
        print("13. View Medical Resources")
        print("14. Create Bill")
        print("15. View Bill")
        print("16. Add Treatment History")
        print("17. View Treatment History")
        print("18. Resource Status Report")
        print("19. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_patient()

        elif choice == "2":
            view_patients()

        elif choice == "3":
            add_doctor()

        elif choice == "4":
            view_doctors()

        elif choice == "5":
            book_appointment()

        elif choice == "6":
            view_appointments()

        elif choice == "7":
            add_room()

        elif choice == "8":
            allocate_room()

        elif choice == "9":
            release_room()

        elif choice == "10":
            view_rooms()

        elif choice == "11":
            add_resource()

        elif choice == "12":
            use_resource()

        elif choice == "13":
            view_resources()

        elif choice == "14":
            create_bill()

        elif choice == "15":
            view_bill()

        elif choice == "16":
            add_treatment()

        elif choice == "17":
            view_treatment()

        elif choice == "18":
            resource_report()

        elif choice == "19":
            print("Thank you for using the Hospital Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


# Start the program
main()
