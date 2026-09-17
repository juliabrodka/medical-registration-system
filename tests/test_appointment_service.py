import datetime

import pytest

from app.models.appointment import Appointment, AppointmentStatus, AppointmentAlreadyBookedError
from app.models.doctor import Doctor, Specialization
from app.models.patient import Patient
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.doctor_repository import DoctorRepository, DoctorNotFoundError
from app.repositories.patient_repository import PatientRepository
from app.services.appointment_service import AppointmentService, CollidingAppointmentsError, InvalidDateRangeError


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
    return Appointment(
        appointment_id=3,
        date=datetime.date(2026, 9, 20),
        time=datetime.time(11, 0),
        doctor=doctor_2
    )


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
def appointment_5(doctor_1):
    return Appointment(
        appointment_id=5,
        date=datetime.date(2026, 9, 21),
        time=datetime.time(9, 0),
        doctor=doctor_1
    )


@pytest.fixture
def appointment_6(doctor_1):
    appointment = Appointment(
        appointment_id=6,
        date=datetime.date(2026, 9, 22),
        time=datetime.time(12, 0),
        doctor=doctor_1
    )

    appointment.cancel_appointment()

    return appointment


@pytest.fixture
def patient_repository(patient_1, patient_2):
    repository = PatientRepository()

    repository.add(patient_1)
    repository.add(patient_2)

    return repository


@pytest.fixture
def doctor_repository(doctor_1, doctor_2):
    repository = DoctorRepository()

    repository.add(doctor_1)
    repository.add(doctor_2)

    return repository


@pytest.fixture
def appointment_repository(
        appointment_1,
        appointment_2,
        appointment_3,
        appointment_4,
        appointment_5,
        appointment_6
):
    repository = AppointmentRepository()

    repository.add(appointment_1)
    repository.add(appointment_2)
    repository.add(appointment_3)
    repository.add(appointment_4)
    repository.add(appointment_5)
    repository.add(appointment_6)

    return repository


@pytest.fixture
def service(
        appointment_repository,
        patient_repository,
        doctor_repository
):
    return AppointmentService(
        appointments=appointment_repository,
        patients=patient_repository,
        doctors=doctor_repository
    )


def test_valid_book_appointment(service, appointment_5, patient_1):
    service.book_appointment(5, 1)
    assert appointment_5.patient is patient_1
    assert appointment_5.status == AppointmentStatus.BOOKED


def test_colliding_book_appointment(service):
    with pytest.raises(CollidingAppointmentsError):
        service.book_appointment(3, 1)


def test_book_booked_appointment(service):
    with pytest.raises(AppointmentAlreadyBookedError):
        service.book_appointment(2, 1)


def test_valid_cancel_booking(service, appointment_2):
    service.cancel_booking(2)
    assert appointment_2.status == AppointmentStatus.FREE


def test_valid_cancel_appointment(service, appointment_2):
    service.cancel_appointment(2)
    assert appointment_2.status == AppointmentStatus.CANCELLED


def test_valid_get_doctor_schedule(service):
    appointments = service.get_doctor_schedule(1)
    assert len(appointments) == 4


def test_invalid_get_doctor_schedule(service):
    with pytest.raises(DoctorNotFoundError):
        service.get_doctor_schedule(99)


def test_valid_handle_doctor_absence(
        service,
        appointment_1,
        appointment_2,
        appointment_5,
        appointment_6
):
    start = datetime.date(2026, 9, 20)
    end = datetime.date(2026, 9, 22)

    assert appointment_1.status == AppointmentStatus.FREE
    assert appointment_2.status == AppointmentStatus.BOOKED
    assert appointment_5.status == AppointmentStatus.FREE
    assert appointment_6.status == AppointmentStatus.CANCELLED

    service.handle_doctor_absence(1, start, end)

    assert appointment_1.status == AppointmentStatus.CANCELLED
    assert appointment_2.status == AppointmentStatus.CANCELLED
    assert appointment_5.status == AppointmentStatus.CANCELLED
    assert appointment_6.status == AppointmentStatus.CANCELLED


def test_valid_handle_doctor_absence_one_day(
        service,
        appointment_1,
        appointment_2,
        appointment_5,
        appointment_6
):
    start = datetime.date(2026, 9, 20)
    end = datetime.date(2026, 9, 20)

    assert appointment_1.status == AppointmentStatus.FREE
    assert appointment_2.status == AppointmentStatus.BOOKED
    assert appointment_5.status == AppointmentStatus.FREE
    assert appointment_6.status == AppointmentStatus.CANCELLED

    service.handle_doctor_absence(1, start, end)

    assert appointment_1.status == AppointmentStatus.CANCELLED
    assert appointment_2.status == AppointmentStatus.CANCELLED

    assert appointment_5.status == AppointmentStatus.FREE
    assert appointment_6.status == AppointmentStatus.CANCELLED


def test_invalid_handle_doctor_absence(service):
    start = datetime.date(2026, 9, 22)
    end = datetime.date(2026, 9, 20)
    with pytest.raises(InvalidDateRangeError):
        service.handle_doctor_absence(1, start, end)
