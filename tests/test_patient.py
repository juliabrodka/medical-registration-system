import datetime

import pytest

from app.models.patient import Patient, MissingContactError
from app.validators.pesel import InvalidPeselError, Gender


def test_valid_patient(patient_1):
    assert patient_1.active is True
    assert patient_1.birth_date == datetime.date(1967, 10, 7)
    assert patient_1.gender == Gender.FEMALE
    assert patient_1.get_full_name() == "Anna Kowalska"


def test_deactivate_patient(patient_1):
    patient_1.deactivate()
    assert patient_1.active is False


def test_activate_deactivated_patient(patient_1):
    patient_1.deactivate()
    patient_1.activate()
    assert patient_1.active is True


@pytest.mark.parametrize(
    "invalid_pesel",
    [
        "1234567890",
        "123456789012",
        "abcdefghijk"
    ]
)
def test_invalid_pesel(invalid_pesel):
    with pytest.raises(InvalidPeselError):
        Patient(
            patient_id=1,
            first_name="Anna",
            last_name="Kowalska",
            pesel=invalid_pesel,
            phone="123456789",

        )


def test_missing_contact():
    with pytest.raises(MissingContactError):
        Patient(
            patient_id=1,
            first_name="Anna",
            last_name="Kowalska",
            pesel="67100702304",
        )


def test_empty_contact():
    with pytest.raises(MissingContactError):
        Patient(
            patient_id=1,
            first_name="Jane",
            last_name="Doe",
            pesel="67100702304",
            phone="",
            email="",
        )


def test_strip_empty_contact():
    with pytest.raises(MissingContactError):
        Patient(
            patient_id=1,
            first_name="Jane",
            last_name="Doe",
            pesel="67100702304",
            phone="   ",
            email="   ",
        )


def test_one_contact_phone():
    patient = Patient(
        patient_id=1,
        first_name="Jane",
        last_name="Doe",
        pesel="67100702304",
        phone="100200300",

    )
    assert patient.phone == "100200300"
    assert patient.email is None


def test_one_contact_email():
    patient = Patient(
        patient_id=1,
        first_name="Jane",
        last_name="Doe",
        pesel="67100702304",
        email="jane@doe.com",
    )
    assert patient.phone is None
    assert patient.email == "jane@doe.com"
