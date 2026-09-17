import pytest

from app.models.doctor import Doctor, Specialization
from app.repositories.doctor_repository import DoctorRepository, InvalidDoctorStatusError, InvalidSearchError, \
    DoctorNotFoundError, InvalidDoctorError, DoctorDuplicateError


@pytest.fixture
def doctor_3():
    return Doctor(
        doctor_id=3,
        employee_number="DOC003",
        first_name="Maria",
        last_name="Nowakowska",
        specialization=Specialization.CARDIOLOGY,
        room="14"
    )


@pytest.fixture
def doctor_4():
    return Doctor(
        doctor_id=4,
        employee_number="DOC004",
        first_name="Piotr",
        last_name="Wiśniewski",
        specialization=Specialization.DERMATOLOGY,
        room="B03",
        active=False
    )


@pytest.fixture
def duplicate_doctor_employee_number():
    return Doctor(
        doctor_id=5,
        employee_number="DOC003",
        first_name="Robert",
        last_name="Kamiński",
        specialization=Specialization.NEUROLOGY,
        room="25"
    )


@pytest.fixture
def duplicate_doctor_id():
    return Doctor(
        doctor_id=1,
        employee_number="DOC005",
        first_name="Katarzyna",
        last_name="Zielińska",
        specialization=Specialization.PEDIATRICS,
        room="08"
    )


@pytest.fixture
def repository():
    return DoctorRepository()


@pytest.fixture
def populated_repository(
        repository,
        doctor_1,
        doctor_2,
        doctor_3,
        doctor_4
):
    repository.add(doctor_1)
    repository.add(doctor_2)
    repository.add(doctor_3)
    repository.add(doctor_4)

    return repository


def test_valid_deactivate_by_id(populated_repository):
    populated_repository.deactivate_by_id(1)
    assert populated_repository.get_by_id(1).active is False


def test_invalid_deactivate_by_ide(populated_repository):
    with pytest.raises(InvalidDoctorStatusError):
        populated_repository.deactivate_by_id(4)


def test_valid_activate_by_id(populated_repository):
    populated_repository.activate_by_id(4)
    assert populated_repository.get_by_id(4).active is True


def test_invalid_activate_by_id(populated_repository):
    with pytest.raises(InvalidDoctorStatusError):
        populated_repository.activate_by_id(1)


def test_invalid_get_by_specialization(populated_repository):
    specialization = "Cardiology"
    with pytest.raises(InvalidSearchError):
        populated_repository.get_by_specialization(specialization)


def test_valid_get_by_specialization(populated_repository):
    doctors = populated_repository.get_by_specialization(Specialization.CARDIOLOGY)
    assert len(doctors) == 2
    for doctor in doctors:
        assert doctor.specialization is Specialization.CARDIOLOGY


def test_valid_empty_get_by_specialization(populated_repository):
    doctors = populated_repository.get_by_specialization(Specialization.INTERNAL_MEDICINE)
    assert doctors == []


def test_valid_get_by_employee_number(populated_repository):
    doctor = populated_repository.get_by_employee_number("DOC001")
    assert doctor.employee_number == "DOC001"


def test_not_found_get_by_employee_number(populated_repository):
    with pytest.raises(DoctorNotFoundError):
        populated_repository.get_by_employee_number("DOC010")


@pytest.mark.parametrize(
    "invalid_employee_number",
    [
        123,
        "   ",
        "",
        None,

    ]
)
def test_invalid_get_by_employee_number(populated_repository, invalid_employee_number):
    with pytest.raises(InvalidSearchError):
        populated_repository.get_by_employee_number(invalid_employee_number)


def test_get_all(populated_repository):
    doctors = populated_repository.get_all()
    assert len(doctors) == 4


def test_get_all_copy(populated_repository, doctor_1):
    doctors = populated_repository.get_all()
    doctors.remove(doctor_1)
    assert populated_repository.get_by_id(1) is doctor_1


def test_add_valid_doctor(repository, doctor_1):
    repository.add(doctor_1)
    assert repository.get_by_id(1) is doctor_1


def test_add_invalid_type_doctor(repository):
    with pytest.raises(InvalidDoctorError):
        doctor = "doctor"
        repository.add(doctor)


def test_add_duplicate_doctor_employee_number(populated_repository, duplicate_doctor_employee_number):
    with pytest.raises(DoctorDuplicateError):
        populated_repository.add(duplicate_doctor_employee_number)


def test_add_duplicate_patient_id(populated_repository, duplicate_doctor_id):
    with pytest.raises(DoctorDuplicateError):
        populated_repository.add(duplicate_doctor_id)


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
def test_invalid_get_by_last_name(populated_repository, invalid_last_name):
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
def test_valid_get_by_last_name(populated_repository, valid_last_name):
    doctors = populated_repository.get_by_last_name(valid_last_name)
    assert len(doctors) == 2
    assert doctors[0].get_full_name() == "Jan Nowak"
    assert doctors[1].get_full_name() == "Maria Nowakowska"


def test_valid_empty_get_by_last_name(populated_repository):
    doctors = populated_repository.get_by_last_name("Smith")
    assert doctors == []


def test_valid_get_by_id(populated_repository, doctor_1):
    doctor = populated_repository.get_by_id(1)
    assert doctor is doctor_1


def test_invalid_get_by_id(populated_repository):
    with pytest.raises(DoctorNotFoundError):
        populated_repository.get_by_id(99)
