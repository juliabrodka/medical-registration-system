import datetime

import pytest

from app.models.appointment import Appointment, AppointmentStatus
from app.models.doctor import Doctor, Specialization
from app.models.patient import Patient
from app.repositories.appointment_repository import AppointmentRepository, InactiveDoctorError, InvalidAppointmentError, \
    AppointmentDuplicateError, AppointmentConflictError, AppointmentNotFound


@pytest.fixture
def inactive_doctor():
    return Doctor(
        doctor_id=3,
        employee_number="DOC003",
        first_name="Maria",
        last_name="Nowicka",
        specialization=Specialization.DERMATOLOGY,
        room="14",
        active=False
    )


@pytest.fixture
def patient_1():
    return Patient(
        patient_id=1,
        first_name="Piotr",
        last_name="Wiśniewski",
        pesel="67100702304",
        phone="500600700"
    )


@pytest.fixture
def patient_2():
    return Patient(
        patient_id=2,
        first_name="Aleksandra",
        last_name="Zielińska",
        pesel="92052412346",
        email="aleksandra@example.com"
    )


@pytest.fixture
def appointment_1(doctor_1):
    return Appointment(
        appointment_id=1,
        date=datetime.date(2026, 9, 20),
        time=datetime.time(10, 0),
        doctor=doctor_1
    )


@pytest.fixture
def appointment_2(doctor_1, patient_1):
    appointment = Appointment(
        appointment_id=2,
        date=datetime.date(2026, 9, 20),
        time=datetime.time(11, 0),
        doctor=doctor_1
    )

    appointment.book_appointment(patient_1)

    return appointment


@pytest.fixture
def appointment_3(doctor_2):
    appointment = Appointment(
        appointment_id=3,
        date=datetime.date(2026, 9, 20),
        time=datetime.time(12, 0),
        doctor=doctor_2
    )

    appointment.cancel_appointment()

    return appointment


@pytest.fixture
def appointment_4(doctor_2, patient_2):
    appointment = Appointment(
        appointment_id=4,
        date=datetime.date(2026, 9, 21),
        time=datetime.time(10, 0),
        doctor=doctor_2
    )

    appointment.book_appointment(patient_2)

    return appointment


@pytest.fixture
def conflicting_appointment(doctor_1):
    return Appointment(
        appointment_id=5,
        date=datetime.date(2026, 9, 20),
        time=datetime.time(10, 0),
        doctor=doctor_1
    )


@pytest.fixture
def duplicate_appointment_id(doctor_2):
    return Appointment(
        appointment_id=1,
        date=datetime.date(2026, 9, 22),
        time=datetime.time(15, 0),
        doctor=doctor_2
    )


@pytest.fixture
def inactive_doctor_appointment(inactive_doctor):
    return Appointment(
        appointment_id=6,
        date=datetime.date(2026, 9, 22),
        time=datetime.time(9, 0),
        doctor=inactive_doctor
    )


@pytest.fixture
def repository():
    return AppointmentRepository()


@pytest.fixture
def populated_repository(
        repository,
        appointment_1,
        appointment_2,
        appointment_3,
        appointment_4
):
    repository.add(appointment_1)
    repository.add(appointment_2)
    repository.add(appointment_3)
    repository.add(appointment_4)

    return repository


def test_valid_add(repository, appointment_1):
    repository.add(appointment_1)
    assert repository.get_by_id(1) is appointment_1


def test_invalid_add(repository):
    appointment = "appointment"
    with pytest.raises(InvalidAppointmentError):
        repository.add(appointment)


def test_inactive_doctor_add(repository, inactive_doctor_appointment):
    with pytest.raises(InactiveDoctorError):
        repository.add(inactive_doctor_appointment)


def test_duplicate_id_add(populated_repository, duplicate_appointment_id):
    with pytest.raises(AppointmentDuplicateError):
        populated_repository.add(duplicate_appointment_id)


def test_conflict_appointment_add(populated_repository, conflicting_appointment):
    with pytest.raises(AppointmentConflictError):
        populated_repository.add(conflicting_appointment)


def test_get_all(populated_repository):
    appointments = populated_repository.get_all()
    assert len(appointments) == 4


def test_get_all_copy(populated_repository, appointment_1):
    appointments_copy = populated_repository.get_all()
    appointments_copy.remove(appointment_1)
    assert populated_repository.get_by_id(1) is appointment_1


def test_valid_get_by_id(populated_repository, appointment_1):
    appointment = populated_repository.get_by_id(1)
    assert appointment is appointment_1


def test_invalid_get_by_id(populated_repository):
    with pytest.raises(AppointmentNotFound):
        populated_repository.get_by_id(99)


def test_non_empty_get_by_date(populated_repository):
    date = datetime.date(2026, 9, 20)
    appointments = populated_repository.get_by_date(date)
    assert len(appointments) == 3


def test_empty_get_by_date(populated_repository):
    date = datetime.date(2026, 10, 20)
    appointments = populated_repository.get_by_date(date)
    assert appointments == []


def test_non_empty_get_by_doctor_id(populated_repository):
    appointments = populated_repository.get_by_doctor_id(1)
    assert len(appointments) == 2


def test_empty_get_by_doctor_id(populated_repository):
    appointments = populated_repository.get_by_doctor_id(99)
    assert appointments == []


def test_non_empty_get_by_patient_id(populated_repository):
    appointments = populated_repository.get_by_patient_id(1)
    assert len(appointments) == 1


def test_empty_get_by_patient_id(populated_repository):
    appointments = populated_repository.get_by_patient_id(99)
    assert appointments == []


def test_booked_get_by_status(populated_repository):
    appointments = populated_repository.get_by_status(AppointmentStatus.BOOKED)
    assert len(appointments) == 2


def test_free_get_by_status(populated_repository):
    appointments = populated_repository.get_by_status(AppointmentStatus.FREE)
    assert len(appointments) == 1


def test_cancelled_get_by_status(populated_repository):
    appointments = populated_repository.get_by_status(AppointmentStatus.CANCELLED)
    assert len(appointments) == 1


def test_empty_get_by_status(repository):
    appointments = repository.get_by_status(AppointmentStatus.FREE)
    assert appointments == []
