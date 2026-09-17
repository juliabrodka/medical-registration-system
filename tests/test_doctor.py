import pytest

from app.models.doctor import Doctor, Specialization, InvalidSpecializationError


def test_valid_doctor():
    doctor = Doctor(
        doctor_id=1,
        employee_number="DOC001",
        first_name="Anna",
        last_name="Kowalska",
        specialization=Specialization.CARDIOLOGY,
        room="12A"
    )
    assert doctor.get_full_name() == "Anna Kowalska"
    assert doctor.specialization == Specialization.CARDIOLOGY
    assert doctor.active is True
    assert doctor.room == "12A"


def test_invalid_specialization_doctor():
    with pytest.raises(InvalidSpecializationError):
        Doctor(
            doctor_id=1,
            employee_number="DOC001",
            first_name="Anna",
            last_name="Kowalska",
            specialization="Cardiology",
            room="12A"
        )


@pytest.fixture
def doctor():
    return Doctor(
        doctor_id=1,
        employee_number="DOC001",
        first_name="Anna",
        last_name="Kowalska",
        specialization=Specialization.CARDIOLOGY,
        room="12A"
    )


def test_deactivate_doctor(doctor):
    doctor.deactivate()
    assert doctor.active is False


def test_activate_deactivated_doctor(doctor):
    doctor.deactivate()
    doctor.activate()
    assert doctor.active is True


def test_change_room(doctor):
    doctor.change_room("00A")
    assert doctor.room == "00A"


def test_change_specialization(doctor):
    doctor.change_specialization(Specialization.INTERNAL_MEDICINE)
    assert doctor.specialization == Specialization.INTERNAL_MEDICINE


def test_invalid_specialization(doctor):
    with pytest.raises(InvalidSpecializationError):
        doctor.change_specialization("Internal Medicine")
