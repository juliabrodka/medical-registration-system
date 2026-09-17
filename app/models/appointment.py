from dataclasses import dataclass, field
from enum import Enum
from datetime import date, time
from app.exceptions.appointment import InactiveDoctorError, AppointmentAlreadyBookedError, InactivePatientError, \
    InvalidStatusError
from .doctor import Doctor
from .patient import Patient


class AppointmentStatus(Enum):
    FREE = "Free"
    BOOKED = "Booked"
    CANCELLED = "Cancelled"


@dataclass
class Appointment:
    appointment_id: int
    date: date
    time: time
    doctor: Doctor

    patient: Patient | None = field(
        default=None,
        init=False
    )

    status: AppointmentStatus = field(
        default=AppointmentStatus.FREE,
        init=False
    )

    def book_appointment(self, patient: Patient) -> None:
        if self.status == AppointmentStatus.BOOKED:
            raise AppointmentAlreadyBookedError(
                "Appointment already booked"
            )
        if self.status == AppointmentStatus.CANCELLED:
            raise InvalidStatusError(
                "Cannot book cancelled appointment"
            )
        if not patient.active:
            raise InactivePatientError(
                "Cannot book appointment for inactive patient"
            )

        if not self.doctor.active:
            raise InactiveDoctorError(
                "Cannot book appointment for inactive doctor"
            )

        self.patient = patient
        self.status = AppointmentStatus.BOOKED

    def cancel_booking(self) -> None:
        if self.status == AppointmentStatus.CANCELLED:
            raise InvalidStatusError(
                "Cannot cancel cancelled appointment"
            )
        if self.status == AppointmentStatus.FREE:
            raise InvalidStatusError(
                "Cannot cancel booking for a free appointment"
            )
        self.status = AppointmentStatus.FREE
        self.patient = None

    def cancel_appointment(self) -> None:
        if self.status == AppointmentStatus.CANCELLED:
            raise InvalidStatusError(
                "Appointment already cancelled"
            )
        self.status = AppointmentStatus.CANCELLED

    def __str__(self) -> str:
        return (
            "--- APPOINTMENT INFO ---\n"
            f"Date: {self.date}\n"
            f"Time: {self.time}\n"
            f"Doctor: {self.doctor.get_full_name()}\n"
            f"Patient: "
            f"{self.patient.get_full_name() if self.patient else 'None'}\n"
            f"Status: {self.status.value}\n"
        )
