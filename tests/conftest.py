import pytest

from app.models.doctor import Doctor, Specialization
from app.models.patient import Patient


@pytest.fixture
def doctor_1():
    return Doctor(
        doctor_id=1,
        employee_number="DOC001",
        first_name="Anna",
        last_name="Kowalska",
        specialization=Specialization.CARDIOLOGY,
        room="12A"
    )


@pytest.fixture
def doctor_2():
    return Doctor(
        doctor_id=2,
        employee_number="DOC002",
        first_name="Jan",
        last_name="Nowak",
        specialization=Specialization.NEUROLOGY,
        room="21"
    )


@pytest.fixture
def patient_1():
    return Patient(
        patient_id=1,
        first_name="Anna",
        last_name="Kowalska",
        pesel="67100702304",
        phone="500600700"
    )


@pytest.fixture
def patient_2():
    return Patient(
        patient_id=2,
        first_name="Jan",
        last_name="Nowak",
        pesel="92052412346",
        email="jan.nowak@example.com"
    )
