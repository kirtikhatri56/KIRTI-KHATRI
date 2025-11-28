Assignment3
Kirti Khatri ,2501201005,(BCA-AI/DS), sem 1
Hospital Patient Management System

import json 
import uuid
from datetime import datetime
from typing import List, Optional, Dict

class Patient:

 def __init__(
        self,
        patient_id: Optional[str],
        name: str,
        age: int,
        gender: str,
        contact: str,
        address: str,
        medical_history: Optional[List[str]] = None,
    ):
        self.patient_id = patient_id or str(uuid.uuid4())
        self.name = name
        self.age = int(age)
        self.gender = gender
        self.contact = contact
        self.address = address
        self.medical_history = medical_history or []

    def add_medical_note(self, note: str):
        self.medical_history.append(f"{datetime.now().isoformat()} - {note}")

    def to_dict(self) -> Dict:
        return {
            "type": self.__class__.__name__,
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "contact": self.contact,
            "address": self.address,
            "medical_history": self.medical_history,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        # Factory: instantiate the correct subclass
        t = data.get("type", "Patient")
        if t == "InPatient":
            return InPatient.from_dict(data)
        elif t == "OutPatient":
            return OutPatient.from_dict(data)
        else:
            return Patient(
                patient_id=data.get("patient_id"),
                name=data["name"],
                age=data["age"],
                gender=data["gender"],
                contact=data["contact"],
                address=data["address"],
                medical_history=data.get("medical_history", []),
            )

    # Dunder methods
    def __str__(self):
        return f"{self.name} ({self.patient_id[:8]}) - {self.age}y"

    def __repr__(self):
        return f"<Patient {self.patient_id} {self.name!r}>"

    def __eq__(self, other):
        if not isinstance(other, Patient):
            return NotImplemented
        return self.patient_id == other.patient_id


class InPatient(Patient):
    def __init__(
        self,
        patient_id: Optional[str],
        name: str,
        age: int,
        gender: str,
        contact: str,
        address: str,
        room_no: str,
        admission_date: str,
        discharge_date: Optional[str] = None,
        medical_history: Optional[List[str]] = None,
    ):
        super().__init__(patient_id, name, age, gender, contact, address, medical_history)
        self.room_no = room_no
        # store dates as ISO strings
        self.admission_date = admission_date
        self.discharge_date = discharge_date

    def discharge(self, discharge_date: Optional[str] = None):
        self.discharge_date = discharge_date or datetime.now().strftime(DATE_FORMAT)

    def to_dict(self):
        d = super().to_dict()
        d.update(
            {
                "room_no": self.room_no,
                "admission_date": self.admission_date,
                "discharge_date": self.discharge_date,
            }
        )
        return d

    @classmethod
    def from_dict(cls, data):
        return InPatient(
            patient_id=data.get("patient_id"),
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            contact=data["contact"],
            address=data["address"],
            room_no=data.get("room_no", ""),
            admission_date=data.get("admission_date", ""),
            discharge_date=data.get("discharge_date"),
            medical_history=data.get("medical_history", []),
        )

    def __str__(self):
        discharge = self.discharge_date or "N/A"
        return f"InPatient {self.name} (Room {self.room_no}) admitted {self.admission_date}, discharge {discharge}"


class OutPatient(Patient):
    def __init__(
        self,
        patient_id: Optional[str],
        name: str,
        age: int,
        gender: str,
        contact: str,
        address: str,
        appointment_date: str,
        doctor: str,
        medical_history: Optional[List[str]] = None,
    ):
        super().__init__(patient_id, name, age, gender, contact, address, medical_history)
        self.appointment_date = appointment_date
        self.doctor = doctor

    def to_dict(self):
        d = super().to_dict()
        d.update({"appointment_date": self.appointment_date, "doctor": self.doctor})
        return d

    @classmethod
    def from_dict(cls, data):
        return OutPatient(
            patient_id=data.get("patient_id"),
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            contact=data["contact"],
            address=data["address"],
            appointment_date=data.get("appointment_date", ""),
            doctor=data.get("doctor", ""),
            medical_history=data.get("medical_history", []),
        )

    def __str__(self):
        return f"OutPatient {self.name} appointment {self.appointment_date} with Dr. {self.doctor}"


# -----------------------
# Manager
# -----------------------
class HospitalManager:
    """
    Manages patient records and persistence.
    Demonstrates dunder methods: __len__, __iter__
    """

    def __init__(self, db_file: str = DATA_FILE):
        self.db_file = db_file
        self._patients: Dict[str, Patient] = {}
        self.load()

    def add_patient(self, patient: Patient):
        if patient.patient_id in self._patients:
            raise InvalidInputError("Patient with this ID already exists.")
        self._patients[patient.patient_id] = patient
        self.save()

    def get_patient(self, patient_id: str) -> Patient:
        try:
            return self._patients[patient_id]
        except KeyError:
            raise PatientNotFoundError(f"No patient found with ID {patient_id}")

    def update_patient(self, patient_id: str, **kwargs):
        p = self.get_patient(patient_id)
        for k, v in kwargs.items():
            if hasattr(p, k):
                setattr(p, k, v)
        self.save()
        return p

    def remove_patient(self, patient_id: str):
        if patient_id not in self._patients:
            raise PatientNotFoundError(patient_id)
        del self._patients[patient_id]
        self.save()

    def list_patients(self) -> List[Patient]:
        return list(self._patients.values())

    def search_by_name(self, name_substr: str) -> List[Patient]:
        name_substr = name_substr.lower()
        return [p for p in self._patients.values() if name_substr in p.name.lower()]

    def save(self):
        data = [p.to_dict() for p in self._patients.values()]
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        # silent save

    def load(self):
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._patients = {d["patient_id"]: Patient.from_dict(d) for d in data}
        except FileNotFoundError:
            self._patients = {}
        except json.JSONDecodeError:
            print("Warning: data file corrupted; starting fresh.")
            self._patients = {}

    # dunder methods
    def __len__(self):
        return len(self._patients)

    def __iter__(self):
        return iter(self._patients.values())

    def export_to_file(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self._patients.values()], f, indent=2)

    def import_from_file(self, filepath: str, overwrite: bool = False):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if overwrite:
            self._patients.clear()
        for d in data:
            p = Patient.from_dict(d)
            self._patients[p.patient_id] = p
        self.save()


# -----------------------
# Helper functions
# -----------------------
def safe_input(prompt: str, required: bool = True) -> str:
    while True:
        v = input(prompt).strip()
        if not v and required:
            print("This field is required. Please enter a value.")
            continue
        return v


def parse_date(date_str: str) -> str:
    """Validate and return date in YYYY-MM-DD format."""
    try:
        dt = datetime.strptime(date_str, DATE_FORMAT)
        return dt.strftime(DATE_FORMAT)
    except ValueError:
        raise InvalidInputError(f"Date must be in {DATE_FORMAT} format.")


def print_patient_detail(p: Patient):
    print("-" * 40)
    print(f"ID       : {p.patient_id}")
    print(f"Name     : {p.name}")
    print(f"Age      : {p.age}")
    print(f"Gender   : {p.gender}")
    print(f"Contact  : {p.contact}")
    print(f"Address  : {p.address}")
    if isinstance(p, InPatient):
        print(f"Type     : InPatient")
        print(f"Room No. : {p.room_no}")
        print(f"Admitted : {p.admission_date}")
        print(f"Discharged: {p.discharge_date or 'N/A'}")
    elif isinstance(p, OutPatient):
        print(f"Type     : OutPatient")
        print(f"Appt.    : {p.appointment_date}")
        print(f"Doctor   : {p.doctor}")
    print("Medical History:")
    for note in p.medical_history:
        print("  -", note)
    print("-" * 40)


# -----------------------
# CLI
# -----------------------
def add_patient_cli(manager: HospitalManager):
    try:
        ptype = safe_input("Patient type (1-InPatient, 2-OutPatient): ")
        if ptype not in ("1", "2"):
            raise InvalidInputError("Invalid patient type selection.")
        name = safe_input("Name: ")
        age = int(safe_input("Age: "))
        gender = safe_input("Gender: ")
        contact = safe_input("Contact number: ")
        address = safe_input("Address: ")

        if ptype == "1":
            room = safe_input("Room No: ")
            adm = parse_date(safe_input(f"Admission date ({DATE_FORMAT}): "))
            patient = InPatient(
                patient_id=None,
                name=name,
                age=age,
                gender=gender,
                contact=contact,
                address=address,
                room_no=room,
                admission_date=adm,
            )
        else:
            appt = parse_date(safe_input(f"Appointment date ({DATE_FORMAT}): "))
            doc = safe_input("Doctor name: ")
            patient = OutPatient(
                patient_id=None,
                name=name,
                age=age,
                gender=gender,
                contact=contact,
                address=address,
                appointment_date=appt,
                doctor=doc,
            )

        manager.add_patient(patient)
        print("Patient added successfully. ID:", patient.patient_id)
    except (InvalidInputError, ValueError) as e:
        print("Error:", e)


def view_patient_cli(manager: HospitalManager):
    pid = safe_input("Enter patient ID: ")
    try:
        p = manager.get_patient(pid)
        print_patient_detail(p)
    except PatientNotFoundError as e:
        print("Error:", e)


def list_patients_cli(manager: HospitalManager):
    patients = manager.list_patients()
    if not patients:
        print("No patients found.")
        return
    print(f"Total patients: {len(patients)}")
    for p in patients:
        print(f"- {p.patient_id[:8]} | {p.name} | {p.age} | {p.__class__.__name__}")


def search_cli(manager: HospitalManager):
    q = safe_input("Enter name to search: ")
    res = manager.search_by_name(q)
    if not res:
        print("No matches.")
        return
    for p in res:
        print(f"- {p.patient_id[:8]} | {p.name} | {p.__class__.__name__}")


def update_patient_cli(manager: HospitalManager):
    pid = safe_input("Enter patient ID to update: ")
    try:
        p = manager.get_patient(pid)
        print("Leave blank to keep existing value.")
        name = safe_input(f"Name [{p.name}]: ", required=False) or p.name
        age_raw = safe_input(f"Age [{p.age}]: ", required=False)
        age = int(age_raw) if age_raw else p.age
        contact = safe_input(f"Contact [{p.contact}]: ", required=False) or p.contact
        address = safe_input(f"Address [{p.address}]: ", required=False) or p.address

        kwargs = {"name": name, "age": age, "contact": contact, "address": address}

        if isinstance(p, InPatient):
            room = safe_input(f"Room No [{p.room_no}]: ", required=False) or p.room_no
            kwargs["room_no"] = room
        elif isinstance(p, OutPatient):
            doc = safe_input(f"Doctor [{p.doctor}]: ", required=False) or p.doctor
            kwargs["doctor"] = doc

        updated = manager.update_patient(pid, **kwargs)
        print("Updated:", updated)
    except (PatientNotFoundError, InvalidInputError, ValueError) as e:
        print("Error:", e)


def discharge_cli(manager: HospitalManager):
    pid = safe_input("Enter InPatient ID to discharge: ")
    try:
        p = manager.get_patient(pid)
        if not isinstance(p, InPatient):
            print("Patient is not an InPatient.")
            return
        ddate = safe_input(f"Discharge date ({DATE_FORMAT}) or leave blank for today: ", required=False)
        if ddate:
            ddate = parse_date(ddate)
        p.discharge(discharge_date=ddate)
        manager.save()
        print(f"Patient {p.name} discharged on {p.discharge_date}")
    except (PatientNotFoundError, InvalidInputError) as e:
        print("Error:", e)


def delete_patient_cli(manager: HospitalManager):
    pid = safe_input("Enter patient ID to delete: ")
    conf = safe_input("Type 'YES' to confirm deletion: ")
    if conf != "YES":
        print("Deletion cancelled.")
        return
    try:
        manager.remove_patient(pid)
        print("Deleted.")
    except PatientNotFoundError as e:
        print("Error:", e)


def add_medical_note_cli(manager: HospitalManager):
    pid = safe_input("Enter patient ID: ")
    try:
        p = manager.get_patient(pid)
        note = safe_input("Enter medical note: ")
        p.add_medical_note(note)
        manager.save()
        print("Note added.")
    except PatientNotFoundError as e:
        print("Error:", e)


def import_export_cli(manager: HospitalManager):
    opt = safe_input("1-Export, 2-Import: ")
    if opt == "1":
        fname = safe_input("Export file name (e.g. export.json): ")
        manager.export_to_file(fname)
        print("Exported to", fname)
    elif opt == "2":
        fname = safe_input("Import file name (e.g. export.json): ")
        overwrite = safe_input("Overwrite existing DB? (y/N): ", required=False).lower() == "y"
        try:
            manager.import_from_file(fname, overwrite=overwrite)
            print("Imported.")
        except FileNotFoundError:
            print("File not found.")
    else:
        print("Invalid option.")


def main_menu():
    manager = HospitalManager()

    menu = """
Hospital Patient Management System
---------------------------------
1. Add Patient (InPatient/OutPatient)
2. View Patient by ID
3. List all patients
4. Search patients by name
5. Update patient
6. Discharge InPatient
7. Add medical note to patient
8. Delete patient
9. Import/Export JSON
0. Exit
"""

    actions = {
        "1": add_patient_cli,
        "2": view_patient_cli,
        "3": list_patients_cli,
        "4": search_cli,
        "5": update_patient_cli,
        "6": discharge_cli,
        "7": add_medical_note_cli,
        "8": delete_patient_cli,
        "9": import_export_cli,
    }

    while True:
        print(menu)
        choice = safe_input("Choose an option: ")
        if choice == "0":
            print("Goodbye — saving data...")
            manager.save()
            break
        action = actions.get(choice)
        if action:
            try:
                action(manager)
            except HospitalError as he:
                print("Operation failed:", he)
            except Exception as e:
                print("Unexpected error:", e)
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting due to keyboard interrupt. Data saved.")
