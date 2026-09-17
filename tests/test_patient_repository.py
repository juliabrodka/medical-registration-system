import pytest

from app.models.patient import Patient
from app.repositories.patient_repository import (PatientRepository,
                                                 InvalidPatientStatus,
                                                 PatientNotFound,
                                                 PatientDuplicateError,
                                                 InvalidPatientError,
                                                 InvalidSearchError)





@pytest.fixture
def patient_3():
    return Patient(
        patient_id=3,
        first_name="Maria",
        last_name="Nowakowska",
        pesel="85031512344",
        phone="600700800",
        email="maria.kowalska@example.com"
    )


@pytest.fixture
def patient_4():
    return Patient(
        patient_id=4,
        first_name="Piotr",
        last_name="Wiśniewski",
        pesel="99010112342",
        phone="700800900",
        active=False,
    )


@pytest.fixture
def duplicate_patient_pesel():
    return Patient(
        patient_id=5,
        first_name="Aleksandra",
        last_name="Nowicka",
        pesel="67100702304",
        email="aleksandra.nowicka@example.com"
    )


@pytest.fixture
def duplicate_patient_id():
    return Patient(
        patient_id=1,
        first_name="Aleksandra",
        last_name="Nowicka",
        pesel="03111512349",
        email="aleksandra.nowicka@example.com"
    )


@pytest.fixture
def repository():
    return PatientRepository()


@pytest.fixture
def populated_repository(repository, patient_1, patient_2, patient_3, patient_4):
    repository.add(patient_1)
    repository.add(patient_2)
    repository.add(patient_3)
    repository.add(patient_4)
    return repository


def test_add_valid_patient(repository, patient_1):
    repository.add(patient_1)
    assert repository.get_by_id(1) is patient_1


def test_add_invalid_type_patient(repository):
    with pytest.raises(InvalidPatientError):
        patient = "patient"
        repository.add(patient)


def test_add_duplicate_patient_pesel(populated_repository, duplicate_patient_pesel):
    with pytest.raises(PatientDuplicateError):
        populated_repository.add(duplicate_patient_pesel)


def test_add_duplicate_patient_id(populated_repository, duplicate_patient_id):
    with pytest.raises(PatientDuplicateError):
        populated_repository.add(duplicate_patient_id)


def test_found_get_by_id(populated_repository):
    patient = populated_repository.get_by_id(1)
    assert patient.patient_id == 1


def test_not_found_get_by_id(populated_repository):
    with pytest.raises(PatientNotFound):
        populated_repository.get_by_id(99)


def test_found_get_by_pesel(populated_repository):
    patient = populated_repository.get_by_pesel("67100702304")
    assert patient.pesel == "67100702304"


def test_not_found_get_by_pesel(populated_repository):
    with pytest.raises(PatientNotFound):
        populated_repository.get_by_pesel("03111512349")


def test_valid_activate_by_id(populated_repository):
    populated_repository.activate_by_id(4)
    patient = populated_repository.get_by_id(4)
    assert patient.active is True


def test_invalid_activate_by_id(populated_repository):
    with pytest.raises(InvalidPatientStatus):
        populated_repository.activate_by_id(1)


def test_valid_deactivate_by_id(populated_repository):
    populated_repository.deactivate_by_id(1)
    patient = populated_repository.get_by_id(1)
    assert patient.active is False


def test_invalid_deactivate_by_id(populated_repository):
    with pytest.raises(InvalidPatientStatus):
        populated_repository.deactivate_by_id(4)


def test_get_all(populated_repository):
    patients = populated_repository.get_all()
    assert len(patients) == 4


def test_get_all_copy(populated_repository, patient_1):
    patients_1 = populated_repository.get_all()
    patients_1.remove(patient_1)
    assert populated_repository.get_by_id(1) is patient_1


@pytest.mark.parametrize(
    "invalid_last_name",
    [
        123,
        "  ",
        "",
        "Now123ak",
        "123Now",
        "Nowak&",

    ]

)
def test_invalid_get_by_name(populated_repository, invalid_last_name):
    with pytest.raises(InvalidSearchError):
        populated_repository.get_by_last_name(invalid_last_name)


@pytest.mark.parametrize(
    "valid_last_name",
    [
        "Now",
        "Nowak",
        "nowak",
        "  Nowak   ",
    ]
)
def test_valid_get_by_name(populated_repository, valid_last_name):
    patients = populated_repository.get_by_last_name(valid_last_name)
    assert len(patients) == 2
    assert patients[0].get_full_name() == "Jan Nowak"
    assert patients[1].get_full_name() == "Maria Nowakowska"


def test_empty_get_by_name(populated_repository):
    patients = populated_repository.get_by_last_name("Smith")
    assert patients == []
