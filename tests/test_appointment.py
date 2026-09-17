import datetime

import pytest

from app.models.appointment import (
    Appointment,
    AppointmentStatus,
    InvalidStatusError,
    AppointmentAlreadyBookedError,
    InactivePatientError,
    InactiveDoctorError,
)
from app.models.doctor import Doctor, Specialization
from app.models.patient import Patient


@pytest.fixture
def appointment(doctor_1):
    return Appointment(
        appointment_id=1,
        date=datetime.date(2026, 9, 20),
        time=datetime.time(10, 0),
        doctor=doctor_1
    )


def test_new_appointment_is_free(appointment):
    assert appointment.status == AppointmentStatus.FREE
    assert appointment.patient is None


def test_book_appointment(appointment, patient_1):
    appointment.book_appointment(patient_1)
    assert appointment.status == AppointmentStatus.BOOKED
    assert appointment.patient == patient_1


def test_cancel_booking(appointment, patient_1):
    appointment.book_appointment(patient_1)
    appointment.cancel_booking()
    assert appointment.status == AppointmentStatus.FREE
    assert appointment.patient is None


def test_cancel_appointment(appointment):
    appointment.cancel_appointment()
    assert appointment.status == AppointmentStatus.CANCELLED


def test_book_cancelled_appointment(appointment, patient_1):
    appointment.cancel_appointment()
    with pytest.raises(
            InvalidStatusError,
            match="Cannot book cancelled appointment"
    ):
        appointment.book_appointment(patient_1)


def test_cancel_booking_free(appointment):
    with pytest.raises(
            InvalidStatusError,
            match="Cannot cancel booking for a free appointment"
    ):
        appointment.cancel_booking()


def test_book_booked_appointment(appointment, patient_1):
    appointment.book_appointment(patient_1)
    with pytest.raises(
            AppointmentAlreadyBookedError,
            match="Appointment already booked"
    ):
        appointment.book_appointment(patient_1)


def test_inactive_patient_booking(appointment, patient_1):
    patient_1.deactivate()
    with pytest.raises(
            InactivePatientError,
            match="Cannot book appointment for inactive patient"
    ):
        appointment.book_appointment(patient_1)


def test_inactive_doctor_booking(appointment, patient_1, doctor_1):
    doctor_1.deactivate()
    with pytest.raises(
            InactiveDoctorError,
            match="Cannot book appointment for inactive doctor"
    ):
        appointment.book_appointment(patient_1)


def test_patient_in_cancelled_appointment(appointment, patient_1):
    appointment.book_appointment(patient_1)
    appointment.cancel_appointment()
    assert appointment.status == AppointmentStatus.CANCELLED
    assert appointment.patient is patient_1


def test_cancel_cancelled_appointment(appointment):
    appointment.cancel_appointment()
    with pytest.raises(
            InvalidStatusError,
            match="Appointment already cancelled"
    ):
        appointment.cancel_appointment()


def test_cancel_booking_cancelled_appointment(appointment):
    appointment.cancel_appointment()
    with pytest.raises(
            InvalidStatusError,
            match="Cannot cancel cancelled appointment"
    ):
        appointment.cancel_booking()
