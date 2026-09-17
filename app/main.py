from app.repositories.doctor_repository import DoctorRepository
from app.models.doctor import Doctor, Specialization
from app.models.patient import Patient

patient1 = Patient(
    patient_id=1,
    first_name="Anna",
    last_name="Nowak",
    pesel="95041212343",
    phone="500100200",
    email="anna.nowak@test.pl",
    address="Szczecin"
)

patient2 = Patient(
    patient_id=2,
    first_name="Jan",
    last_name="Nowak",
    pesel="88110356776",
    phone="501200300",
    email=None,
    address="Szczecin"
)

patient3 = Patient(
    patient_id=3,
    first_name="Maria",
    last_name="Kowalska",
    pesel="01221713580",
    phone=None,
    email="maria.kowalska@test.pl",
    address="Police"
)

patient4 = Patient(
    patient_id=4,
    first_name="Piotr",
    last_name="Kowalski",
    pesel="76072924676",
    phone="502300400",
    email=None,
    address=None
)

patient5 = Patient(
    patient_id=5,
    first_name="Ewa",
    last_name="Kowalińska",
    pesel="04320598764",
    phone="503400500",
    email="ewa.zielinska@test.pl",
    address="Goleniów"
)

patient6 = Patient(
    patient_id=6,
    first_name="Tomasz",
    last_name="Wiśniewski",
    pesel="92012131414",
    phone="504500600",
    email=None,
    address="Szczecin"
)

doctor1 = Doctor(
    doctor_id=1,
    employee_number="DOC001",
    first_name="Anna",
    last_name="Kowalska",
    specialization=Specialization.CARDIOLOGY,
    room="12A"
)

doctor2 = Doctor(
    doctor_id=2,
    employee_number="DOC002",
    first_name="Jan",
    last_name="Nowak",
    specialization=Specialization.NEUROLOGY,
    room="21"
)

doctor3 = Doctor(
    doctor_id=3,
    employee_number="DOC003",
    first_name="Maria",
    last_name="Nowicka",
    specialization=Specialization.CARDIOLOGY,
    room="14"
)

doctor4 = Doctor(
    doctor_id=4,
    employee_number="DOC004",
    first_name="Piotr",
    last_name="Wiśniewski",
    specialization=Specialization.DERMATOLOGY,
    room="B03"
)

doctor5 = Doctor(
    doctor_id=5,
    employee_number="DOC005",
    first_name="Katarzyna",
    last_name="Kowalska",
    specialization=Specialization.PEDIATRICS,
    room=None
)

doctor6 = Doctor(
    doctor_id=6,
    employee_number="DOC006",
    first_name="Tomasz",
    last_name="Zieliński",
    specialization=Specialization.INTERNAL_MEDICINE,
    room="8"
)

doctor7 = Doctor(
    doctor_id=7,
    employee_number="DOC007",
    first_name="Aleksandra",
    last_name="Maj",
    specialization=Specialization.GYNECOLOGY,
    room="17"
)





# repo=PatientRepository()
# repo.add(patient1)
# repo.add(patient2)
# repo.add(patient3)
# repo.add(patient4)
# repo.add(patient5)
# repo.add(patient6)
# print(repo.deactivate_by_id(1))
# print(repo)


repo_doctor = DoctorRepository()
repo_doctor.add(doctor1)
repo_doctor.add(doctor2)
repo_doctor.add(doctor3)
repo_doctor.add(doctor4)
repo_doctor.add(doctor5)
repo_doctor.add(doctor6)
repo_doctor.add(doctor7)

# print(repo_doctor)
print(repo_doctor.get_by_id(5))
